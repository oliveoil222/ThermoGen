import serial
import time

class PressureWriter:
    """
    sends control commands to a pi pico that adjusts
    a bürkert type 3280 c valve to reach a target pressure
    """

    def __init__(self, port: str = "COM6", baudrate: int = 115200, timeout: float = 1.0):
        """
        initialize serial connection to the pi pico
        :param port: com port or device path connected to the pico
        :param baudrate: serial communication speed
        :param timeout: serial timeout
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.serial_conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            time.sleep(2)
            print(f"[PressureWriter] Connected to pi pico on {self.port}")
        except serial.SerialException as e:
            print(f"[PressureWriter] ERROR: could not open serial port {self.port}: {e}")
            self.serial_conn = None

    def adjust_pressure(self, current_pressure: float, target_pressure: float) -> None:
        # compares the current and target pressure then sends commands to adjust the valve
        if not self.serial_conn or not self.serial_conn.is_open:
            print("[PressureWriter] Serial connection not open.")
            return

        # determine adjustment direction and size
        diff = target_pressure - current_pressure
        step = abs(diff) / target_pressure

        if abs(diff) < 0.01 * target_pressure:
            command = "HOLD"
        elif diff > 0:
            # need to increase pressure: close valve slightly
            command = "CLOSE 5" if step < 0.1 else "CLOSE 10"
        else:
            # need to decrease pressure: open valve slightly
            command = "OPEN 5" if step < 0.1 else "OPEN 10"

        try:
            self.serial_conn.write(f"{command}\n".encode())
            print(f"[PressureWriter] Sent command: {command}")
        except Exception as e:
            print(f"[PressureWriter] Error sending command: {e}")

    def close(self):
        # closes the serial connection.
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("[PressureWriter] Connection closed.")
