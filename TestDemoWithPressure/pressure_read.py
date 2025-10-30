import serial
import time

class PressureReader:
    """
    reads live pressure data from the pressure gauge over rs232
    the gauge is expected to report readings in torr
    """

    def __init__(self, port: str = "COM5", baudrate: int = 9600, timeout: float = 1.0):
        """
        initialize serial connection to the gauge
        :param port: serial port the gauge is connected to
        :param baudrate: serial baud rate, default 9600
        :param timeout: serial read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        try:
            self.serial_conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            time.sleep(1)
            print(f"[PressureReader] Connected to the gauge on {self.port}")
        except serial.SerialException as e:
            print(f"[PressureReader] ERROR: Could not open serial port {self.port}: {e}")
            self.serial_conn = None

    def read_pressure(self) -> float:
        """
        reads the current pressure from the gauge
        returns the pressure in torr as a float
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            print("[PressureReader] Serial connection not open.")
            return -1.0

        try:
            # self.serial_conn.write(b"READ?\r")
            raw_data = self.serial_conn.readline().decode(errors='ignore').strip()

            if not raw_data:
                return -1.0

            # try to parse numeric value
            pressure_value = float(raw_data)
            print(f"[PressureReader] Pressure reading: {pressure_value:.3f} Torr")
            return pressure_value
        except Exception as e:
            print(f"[PressureReader] Error reading pressure: {e}")
            return -1.0

    def close(self):
        #closes the serial connection.
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("[PressureReader] Connection closed.")
