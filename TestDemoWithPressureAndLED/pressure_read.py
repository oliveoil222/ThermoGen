import serial
import time
import math
import random

class PressureReader:

    # reads live pressure data from a gauge via rs232 if unavailable simulates a pressure curve in torr

    def __init__(self, port: str = "COM6", baudrate: int = 9600, timeout: float = 1.0,
                 base_pressure: float = 760.0, amplitude: float = 5.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.start_time = time.time()
        self.base_pressure = base_pressure
        self.amplitude = amplitude

        try:
            self.serial_conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            time.sleep(1)
            self.simulation = False
            print(f"[PressureReader] Connected to Pirani gauge on {self.port}")
        except serial.SerialException:
            print("[PressureReader] Could not open serial port. Running in SIMULATION mode.")
            self.simulation = True
            self.serial_conn = None

    def read_pressure(self) -> float:
        if self.simulation:
            elapsed = time.time() - self.start_time
            pressure = self.base_pressure + self.amplitude * math.sin(2 * math.pi * (elapsed / 90))
            noise = random.uniform(-0.5, 0.5)
            simulated_pressure = pressure + noise
            print(f"[PressureReader] Simulated Pressure: {simulated_pressure:.2f} Torr")
            return simulated_pressure
        else:
            try:
                raw_data = self.serial_conn.readline().decode(errors='ignore').strip()
                if not raw_data:
                    return None
                pressure_value = float(raw_data)
                print(f"[PressureReader] Actual Pressure: {pressure_value:.3f} Torr")
                return pressure_value
            except Exception as e:
                print(f"[PressureReader] Error reading pressure: {e}")
                return None

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("[PressureReader] Connection closed.")
