import sys
from time import sleep

dataIn = ""

voltage = 0.0
max_voltage = 80.0
min_voltage = 0.0

amps = 0.0
max_amps = 13.0
min_amps = 0.0

pressure = 760.0
min_pressure = 0.0
max_pressure = 760.0
targetPressure = 50.0


def sendData():
    global pressure

    dataOut = f"{pressure:.2f}\n"

    sys.stdout.write(dataOut.encode())


def getData():
    global dataIn
    global voltage
    global amps
    dataIn = sys.stdin.readline()
    # dataIn needs to be [10:-1] not [10:-2]. \n counted as one character
    if dataIn[0:9] == "SOUR:VOLT":
        voltage = float(dataIn[10:-1])
    elif dataIn[0:8] == "SOUR:AMP":
        amps = float(dataIn[9:-1])
    voltageToPressure()


def voltageToPressure():
    global voltage
    global targetPressure
    targetPressure = (-760.0 / 80.0) * (voltage - 80.0)


def within1percent(a, b, threshold=0.01):
    return abs(a - b) / b < threshold


def adjustPressure():
    global pressure
    global targetPressure

    if not within1percent(pressure, targetPressure):
        pressure -= (pressure - targetPressure) / 100
    else:
        pressure = targetPressure


def main():
    while True:
        # print("1")
        sendData()
        # print("2")
        adjustPressure()
        # print("3")
        getData()
        # print("4")
        sleep(0.1)


if __name__ == "__main__":
    main()