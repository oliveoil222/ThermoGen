import serial
import threading
from time import sleep

class TemperatureSim:
    def __init__(self, simPort = "COM4", baudrate = 115200):
        self.ser = serial.Serial(simPort, baudrate)
        self.voltage = 0.0
        self.temperature = 25.00
        self.targetTemperature = 25.00
        self._run_event = threading.Event()
        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def _loop(self):
        while True:
            if self._run_event.is_set():
                try:
                    self.ser.write(self.getTemperatureString().encode())
                    self.getTemperatureFromString(self.ser.readline())
                except Exception:
                    pass
            else:
                sleep(0.1)

    # Backwards-compatible API
    def startSim(self):
        self._run_event.set()

    def pauseSim(self):
        self._run_event.clear()

    def voltageFromTemperature(self):
        self.voltage = ((80.0 * self.targetTemperature) / 800.0) - 2.0

    def getTemperatureString(self):
        self.voltageFromTemperature()
        return f"SOUR:VOLT {self.voltage}\n"

    def getTemperatureFromString(self, line):
        self.temperature = float(line.decode().strip())

if __name__ == "__main__":
    sim = TemperatureSim()
    sim.startSim()