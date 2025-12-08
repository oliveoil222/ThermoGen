import serial
import threading
from time import sleep

class PressureSim:
    def __init__(self, simPort = "COM4", baudrate = 115200):
        self.ser = serial.Serial(simPort, baudrate)
        self.voltage = 0.0
        self.pressure = 760.00
        self.targetPressure = 760.00
        self._run_event = threading.Event()
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def _loop(self):
        while True:
            if self._run_event.is_set():
                try:
                    self.ser.write(self.getPressureString().encode())
                    self.getPressureFromString(self.ser.readline())
                except Exception:
                    pass
            else:
                sleep(0.1)

    # Backwards-compatible API
    def startSim(self):
        self._run_event.set()

    def pauseSim(self):
        self._run_event.clear()

    def voltageFromPressure(self):
        self.voltage = 80.0 - ( (80.0 * self.targetPressure) / 760.0)

    def getPressureString(self):
        self.voltageFromPressure()
        return f"SOUR:VOLT {self.voltage}\n"

    def getPressureFromString(self, line):
        self.pressure = float(line.decode().strip())

if __name__ == "__main__":
    sim = PressureSim()
    sim.startSim()