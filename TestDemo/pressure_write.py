import time
import re
import serial
import serial.tools.list_ports


def find_ports():
    return list(serial.tools.list_ports.comports())


class PressureWriter:
    def __init__(self, port_hint=None, gauge_baud=9600, pico_baud=115200, valve_baud=9600, timeout=1.0):
        self.gauge_conn = None
        self.valve_conn = None
        self.pico_conn = None

        self.mode = "none"
        self.sim_pressure = 760.0
        self.timeout = timeout

        ports = find_ports()
        print(f"[PressureWriter] Scanning ports: {[p.device for p in ports]}")

        # 1) try explicit pico hint first
        if port_hint:
            print(f"[PressureWriter] Trying explicit port hint: {port_hint}")
            self._try_open_as_pico(port_hint, pico_baud)

        # 2) probe ports for Pico first (ping/pong)
        if not self.pico_conn:
            for p in ports:
                dev = p.device
                try:
                    if self._probe_pico(dev, pico_baud):
                        break
                except Exception:
                    pass

        # 3) if no Pico found probe for gauge (READ? -> numeric)
        if not self.pico_conn:
            for p in ports:
                dev = p.device
                # try gauge probe at gauge_baud
                try:
                    if self._probe_gauge(dev, gauge_baud):
                        break
                except Exception:
                    pass

        # 4) heuristic valve detection (try to open any remaining devices at valve_baud)
        for p in ports:
            if not self.valve_conn:
                dev = p.device
                # skip if already assigned as pico or gauge_conn
                if self.pico_conn and dev == self.pico_conn.port:
                    continue
                if self.gauge_conn and dev == self.gauge_conn.port:
                    continue
                # try open and check for any response to simple query (non-destructive)
                try:
                    conn = serial.Serial(dev, valve_baud, timeout=self.timeout)
                    time.sleep(0.05)
                    conn.reset_input_buffer()
                    conn.reset_output_buffer()
                    # try an id or noop that wont break device
                    try:
                        conn.write(b"*IDN?\n")
                        time.sleep(0.05)
                        r = conn.readline().decode(errors="ignore").strip()
                        if r:
                            print(f"[PressureWriter] Valve candidate {dev} replied to *IDN?: {r}")
                            self.valve_conn = conn
                            break
                    except Exception:
                        conn.close()
                except Exception:
                    pass

        # finalize mode
        if self.gauge_conn and self.valve_conn:
            self.mode = "hardware"
        elif self.pico_conn and not (self.gauge_conn and self.valve_conn):
            self.mode = "pico_sim"
        else:
            self.mode = "sim_only"

        print(f"[PressureWriter] Mode = {self.mode}")


    # ---------------- probe helpers ----------------
    def _open_serial(self, device, baud):
        try:
            conn = serial.Serial(device, baudrate=baud, timeout=self.timeout)
            time.sleep(0.05)
            conn.reset_input_buffer()
            conn.reset_output_buffer()
            print(f"[PressureWriter] Opened {device} @ {baud}")
            return conn
        except Exception as e:
            # debug
            # print(f"[PressureWriter] Could not open {device} @ {baud}: {e}")
            return None

    def _probe_pico(self, device, baud):
        # open device at pico baud send ping expect pong keep connection open on success
        conn = self._open_serial(device, baud)
        if not conn:
            return False
        try:
            conn.write(b"PING\n")
            time.sleep(0.1)
            reply = conn.readline().decode(errors="ignore").strip()
            if reply.upper() == "PONG":
                print(f"[PressureWriter] Pico detected on {device} (PONG).")
                self.pico_conn = conn
                return True
            else:
                # not pico close transient connection
                conn.close()
                return False
        except Exception:
            try:
                conn.close()
            except Exception:
                pass
            return False

    def _try_open_as_pico(self, device, baud):
        # try to open the explicit port hint as pico
        conn = self._open_serial(device, baud)
        if not conn:
            return False
        try:
            conn.write(b"PING\n")
            time.sleep(0.1)
            reply = conn.readline().decode(errors="ignore").strip()
            if reply.upper() == "PONG":
                print(f"[PressureWriter] Pico handshake on {device}: {reply}")
                self.pico_conn = conn
                return True
            else:
                conn.close()
                return False
        except Exception:
            conn.close()
            return False

    def _probe_gauge(self, device, baud):
        #probe a port for gauge by opening and sending read and parsing a numeric reply
        conn = self._open_serial(device, baud)
        if not conn:
            return False
        try:
            # send read
            conn.write(b"READ?\n")
            time.sleep(0.1)
            reply = conn.readline().decode(errors="ignore").strip()
            if reply:
                # parse numeric
                m = re.search(r"-?\d+(\.\d+)?", reply)
                if m:
                    try:
                        val = float(m.group(0))
                        print(f"[PressureWriter] Gauge detected on {device}, sample: {val}")
                        self.gauge_conn = conn
                        return True
                    except Exception:
                        pass
            # not a gauge close probe
            conn.close()
            return False
        except Exception:
            try:
                conn.close()
            except Exception:
                pass
            return False


    # ----------------- low level actions -----------------
    def _read_gauge_line(self):
        if not self.gauge_conn or not self.gauge_conn.is_open:
            return None
        try:
            line = self.gauge_conn.readline().decode(errors="ignore").strip()
            if line:
                return line
            # try read request fallback
            self.gauge_conn.write(b"READ?\n")
            time.sleep(0.05)
            line = self.gauge_conn.readline().decode(errors="ignore").strip()
            return line if line else None
        except Exception as e:
            print(f"[PressureWriter] Gauge read error: {e}")
            return None

    def _parse_pressure_from_string(self, s):
        if not s:
            return None
        m = re.search(r"-?\d+(\.\d+)?", s)
        return float(m.group(0)) if m else None

    def _send_valve_command(self, cmd):
        if not self.valve_conn or not self.valve_conn.is_open:
            print("[PressureWriter] Valve serial not available.")
            return False
        try:
            self.valve_conn.write((cmd + "\n").encode())
            time.sleep(0.05)
            # optional ack
            try:
                ack = self.valve_conn.readline().decode(errors="ignore").strip()
                if ack:
                    print(f"[PressureWriter] Valve ack: {ack}")
            except Exception:
                pass
            print(f"[PressureWriter] Sent valve command: {cmd}")
            return True
        except Exception as e:
            print(f"[PressureWriter] Valve command error: {e}")
            return False

    def _send_pico_led(self, on: bool):
        if not self.pico_conn or not self.pico_conn.is_open:
            return
        try:
            cmd = b"LED ON\n" if on else b"LED OFF\n"
            # flush small input and write
            try:
                self.pico_conn.reset_input_buffer()
            except Exception:
                pass
            self.pico_conn.write(cmd)
            # read optional ack
            time.sleep(0.05)
            try:
                ack = self.pico_conn.readline().decode(errors="ignore").strip()
                if ack:
                    print(f"[PressureWriter] Pico ack: '{ack}'")
            except Exception:
                pass
            print(f"[PressureWriter] Sent to Pico: {cmd.strip().decode()}")
        except Exception as e:
            print(f"[PressureWriter] Error sending LED: {e}")


    # ----------------- public method -----------------
    def adjust_pressure(self, current_pressure, target_pressure):

        # single step toward the target returns the updated pressure (actual or simulated)

        if self.mode == "hardware":
            # prefer gauge reading
            line = self._read_gauge_line()
            measured = self._parse_pressure_from_string(line) if line else None
            if measured is None:
                measured = current_pressure
                print(f"[PressureWriter] Gauge read empty; using supplied {measured:.2f} Torr")
            else:
                print(f"[PressureWriter] Gauge reading: {measured:.2f} Torr")

            diff = target_pressure - measured
            tol = max(0.1, 0.001 * target_pressure)
            if abs(diff) <= tol:
                print("[PressureWriter] Within tolerance; no action.")
                return measured

            if diff < 0:
                self._send_valve_command("CLOSE 5")
            else:
                self._send_valve_command("OPEN 5")
            return measured

        elif self.mode == "pico_sim":
            diff = target_pressure - self.sim_pressure
            tol = 0.01
            if abs(diff) <= tol:
                # stabilized
                self._send_pico_led(False)
                print(f"[PressureWriter] Simulated Pressure stabilized at {self.sim_pressure:.2f} Torr (Simulated)")
                return self.sim_pressure

            step = max(0.05, abs(diff) * 0.05)  # 5% of diff
            if diff < 0:
                # need to decrease = led on
                self._send_pico_led(True)
                self.sim_pressure = max(target_pressure, self.sim_pressure - step)
                print(f"[PressureWriter] Simulating DECREASE -> LED ON | {self.sim_pressure:.2f} Torr (Simulated)")
            else:
                # need to increase = led off
                self._send_pico_led(False)
                self.sim_pressure = min(target_pressure, self.sim_pressure + step)
                print(f"[PressureWriter] Simulating INCREASE -> LED OFF | {self.sim_pressure:.2f} Torr (Simulated)")
            return self.sim_pressure

        else:
            # sim only
            diff = target_pressure - self.sim_pressure
            tol = 0.01
            if abs(diff) <= tol:
                print(f"[PressureWriter] Simulated Pressure stabilized at {self.sim_pressure:.2f} Torr (Simulated)")
                return self.sim_pressure
            step = max(0.05, abs(diff) * 0.05)
            if diff < 0:
                self.sim_pressure = max(target_pressure, self.sim_pressure - step)
            else:
                self.sim_pressure = min(target_pressure, self.sim_pressure + step)
            print(f"[PressureWriter] Simulated Pressure: {self.sim_pressure:.2f} Torr (Simulated)")
            return self.sim_pressure


    # ---------------- Cleanup ----------------
    def _shutdown(self):
        # ensure led is off and serial ports are closed at program exit
        try:
            if self.pico_conn and self.pico_conn.is_open:
                self.pico_conn.write(b"LED OFF\n")
                time.sleep(0.05)
                print("[PressureWriter] LED OFF sent during shutdown.")
        except Exception:
            pass
        self.close()
        
    def close(self):
        for conn, name in ((self.gauge_conn, "gauge"), (self.valve_conn, "valve"), (self.pico_conn, "pico")):
            try:
                if conn and conn.is_open:
                    conn.close()
                    print(f"[PressureWriter] Closed {name} connection.")
            except Exception:
                pass
