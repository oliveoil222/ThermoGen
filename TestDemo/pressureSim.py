import serial
import threading
from time import sleep

class PressureSim:
    def __init__(self, simPort = "COM4", baudrate = 115200):
        self.ser = serial.Serial("COM4", baudrate)
        self.voltage = 0.0
        self.pressure = 760.00
        self.targetPressure = 150.00
        self.thread = threading.Thread(target=self.startSim)
        self.thread.daemon = True

    def startSim(self):
        while True:
            print("writing")
            self.ser.write(self.getPressureString().encode())
            print("written")
            print("reading")
            self.getPressureFromString(self.ser.readline())
            print(self.pressure)
            print("read")

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