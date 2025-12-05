import serial
import threading
from time import sleep

class TemperatureSim:
    def __init__(self, simPort = "COM4", baudrate = 115200):
        self.ser = serial.Serial(simPort, baudrate)
        self.voltage = 0.0
        self.temperature = 25.00
        self.targetTemperature = 25.00
        self.thread = threading.Thread(target=self.startSim)
        self.thread.daemon = True

    def startSim(self):
        while True:
            print("writing")
            self.ser.write(self.getTemperatureString().encode())
            print("written")
            print("reading")
            self.getTemperatureFromString(self.ser.readline())
            print(self.temperature)
            print("read")

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