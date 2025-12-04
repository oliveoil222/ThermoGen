import sys
from time import sleep

dataIn = ""

voltage = 0.0
max_voltage = 80.0
min_voltage = 0.0

amps = 0.0
max_amps = 13.0
min_amps = 0.0

temperature = 760.0
min_temperature = 0.0
max_temperature = 760.0
targetTemperature = 50.0


def sendData():
    global temperature

    dataOut = f"{temperature:.2f}\n"

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
    voltageToTemperature()


def voltageToTemperature():
    global voltage
    global targetTemperature
    targetTemperature = 10.0 * voltage + 20


def within1percent(a, b, threshold=0.01):
    return abs(a - b) / b < threshold


def adjustTemperature():
    global temperature
    global targetTemperature

    if not within1percent(temperature, targetTemperature):
        temperature -= (temperature - targetTemperature) / 100
    else:
        temperature = targetTemperature


def main():
    while True:
        # print("1")
        sendData()
        # print("2")
        adjustTemperature()
        # print("3")
        getData()
        # print("4")
        sleep(0.1)


if __name__ == "__main__":
    main()