import sys
import threading
from time import sleep
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

import pressureSim
from DemoUI import Ui_TechDemoMainWindow
from notifications import NotificationManager
from pressureSim import PressureSim
from temperature_read import TemperatureReader
from temperature_write import TemperatureWriter
from pressure_read import PressureReader
from pressure_write import PressureWriter
from temperatureSim import TemperatureSim
from pressureSim import PressureSim
import configparser


class TechDemoMainWindow(QMainWindow):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        super(TechDemoMainWindow, self).__init__()
        self.ui = Ui_TechDemoMainWindow()
        self.ui.setupUi(self)

        # Core modules
        self.notifier = NotificationManager()
        self.notification_sent = False
        if config.getboolean('SIMULATION', 'TEMP_SIMULATION'):
            self.tempSim = TemperatureSim(config.get('SIMULATION', 'TEMP_SIM_DEVICE'))
            self.tempSim.temperature = 25.0
            # self.tempSim.startSim()
            self.ui.tempSubmitButton.clicked.connect(self.updateTempValueSim)
        else:
            self.tempReader = TemperatureReader(config.get('TEMPERATURE', 'TEMP_INPUT_DEVICE'))
            self.tempWriter = TemperatureWriter(config.get('TEMPERATURE', 'TEMP_OUTPUT_DEVICE'))
            self.ui.tempSubmitButton.clicked.connect(self.updateTempValue)



        if config.getboolean('SIMULATION', 'PRESSURE_SIMULATION'):
            # self.pressureSim = PressureSim(config.get('SIMULATION', 'PRESSURE_SIM_DEVICE'))
            # self.pressureSim.voltage = 0.0
            # self.pressureSim.startSim()
            self.ui.pressureSubmitButton.clicked.connect(self.updatePressureValueSim)

        else:
            self.pressureWriter = PressureWriter()
            self.pressureReader = PressureReader()
            self.ui.pressureSubmitButton.clicked.connect(self.updatePressureValue)


        # Threads and state
        self.displayThread = None
        self.updateGPIBThread = None

        # Dont need, just check state of radio button.
        # Buttons 1 & 2 are for temperature control.
        # buttons 3 & 4 are for pressure control.
        # 1 & 3 are automatic, 2 & 4 are manual.
        # self.isTempAutoOn = False
        # self.isPressureAutoOn = False

        self.autoTemp = 25.0
        self.autoPressure = 760.0

        # Setup the UI
        self.setupUI()

        # Start background threads
        self.startThreads(config.getboolean('SIMULATION', 'TEMP_SIMULATION'))

    # -----------------------------
    # --- UI Setup ---
    # -----------------------------
    def setupUI(self):
        # Add pressure units
        self.ui.pressureUnitSelector.addItems(["Torr", "kPa", "atm"])
        self.adjustPressureLimits("Torr")

        # Add temperature units
        self.ui.tempUnitSelector.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.adjustTempLimits("Celsius")

        # Connect UI signals
        # self.ui.autoToggleBox.stateChanged.connect(self.on_autoToggleBox_stateChanged)
        # self.ui.manualToggleBox.stateChanged.connect(self.on_manualToggleBox_stateChanged)
        self.ui.radioButton.toggled.connect(self.on_radioButton_1_stateChanged)
        self.ui.radioButton_3.toggled.connect(self.on_radioButton_3_stateChanged)
        self.ui.pressureUnitSelector.currentTextChanged.connect(self.adjustPressureLimits)
        self.ui.tempUnitSelector.currentTextChanged.connect(self.adjustTempLimits)
        # self.ui.manualToggleBox.setCheckState(Qt.CheckState.Checked)

    def startThreads(self, isSimulated):

        if not isSimulated:
            self.displayThread = threading.Thread(target=self.updateDisplay, daemon=True)
            self.displayThread.start()

            self.updateGPIBThread = threading.Thread(target=self.updateGPIB, daemon=True)
            self.updateGPIBThread.start()
        else:
            self.displayThread = threading.Thread(target=self.updateDisplaySimulation, daemon=True)
            self.displayThread.start()

    # # -----------------------------
    # # --- TOGGLE BOX HANDLERS ---
    # # -----------------------------
    # def on_autoToggleBox_stateChanged(self, state):
    #     if state == 0:
    #         self.ui.manualToggleBox.setCheckState(Qt.CheckState.Checked)
    #         self.isAutoOn = False
    #     else:
    #         self.ui.manualToggleBox.setCheckState(Qt.CheckState.Unchecked)
    #         self.isAutoOn = True
    #
    # def on_manualToggleBox_stateChanged(self, state):
    #     if state == 0:
    #         self.ui.autoToggleBox.setCheckState(Qt.CheckState.Checked)
    #         self.isAutoOn = True
    #     else:
    #         self.ui.autoToggleBox.setCheckState(Qt.CheckState.Unchecked)
    #         self.isAutoOn = False

    def on_radioButton_1_stateChanged(self, state):
        if state == 1:
            print("START")
            self.tempSim.thread.start()

    def on_radioButton_3_stateChanged(self, state):
        if state == 1:
            self.pressureSim.thread.start()




    # -----------------------------
    # --- LIMITS AND UNIT CONTROL ---
    # -----------------------------
    def adjustPressureLimits(self, unit):
        if unit == "Torr":
            self.ui.pressureValueSelector.setRange(0.0, 760.0)
            self.ui.pressureValueSelector.setValue(760.0)
        elif unit == "kPa":
            self.ui.pressureValueSelector.setRange(0.0, 101.325)
            self.ui.pressureValueSelector.setValue(101.325)
        elif unit == "atm":
            self.ui.pressureValueSelector.setRange(0.0, 1.0)
            self.ui.pressureValueSelector.setValue(1.0)

    def adjustTempLimits(self, unit):
        if unit == "Celsius":
            self.ui.tempValueSelector.setRange(0.0, 1250.0)
            self.ui.tempValueSelector.setValue(25.0)
        elif unit == "Fahrenheit":
            self.ui.tempValueSelector.setRange(32.0, 2282.0)
            self.ui.tempValueSelector.setValue(77.0)
        elif unit == "Kelvin":
            self.ui.tempValueSelector.setRange(273.15, 1523.15)
            self.ui.tempValueSelector.setValue(298.15)

    # -----------------------------
    # --- UI VALUE UPDATES ---
    # -----------------------------
    def updateTempValue(self):
        self.autoTemp = self.ui.tempValueSelector.value()
        unit = self.ui.tempUnitSelector.currentText()
        self.notifier.set_message("Temperature Set", f"Set Temperature: {self.autoTemp:.2f} {unit}")
        self.notifier.send_notification()

    def updatePressureValue(self):
        self.autoPressure = self.ui.pressureValueSelector.value()
        unit = self.ui.pressureUnitSelector.currentText()
        self.notifier.set_message("Pressure Set", f"Set Pressure: {self.autoPressure:.2f} {unit}")
        self.notifier.send_notification()

    def updateTempValueSim(self):
        self.autoTemp = self.ui.tempValueSelector.value()
        self.tempSim.targetTemperature = self.autoTemp
        unit = self.ui.tempUnitSelector.currentText()
        self.notifier.set_message("Temperature Set", f"Set Temperature: {self.autoTemp:.2f} {unit}")
        self.notifier.send_notification()

    def updatePressureValueSim(self):
        self.autoPressure = self.ui.pressureValueSelector.value()
        # print(self.autoPressure)
        self.pressureSim.targetPressure = self.autoPressure
        # print(self.pressureSim.targetPressure)
        unit = self.ui.pressureUnitSelector.currentText()
        self.notifier.set_message("Pressure Set", f"Set Pressure: {self.autoPressure:.2f} {unit}")
        self.notifier.send_notification()

    def sendCompletePressureNotification(self):
        self.notifier.set_message("Pressure Target Reached", f"Pressure has reach target value of {self.autoPressure:.2f} {self.ui.pressureUnitSelector.currentText()}")
        self.notifier.send_notification()

    def sendCompleteTempNotification(self):
        self.notifier.set_message("Temperature Target Reached", f"Temperature has reach target value of {self.autoTemp:.2f} {self.ui.tempUnitSelector.currentText()}")
        self.notifier.send_notification()
    # -----------------------------
    # --- THREADS ---
    # -----------------------------
    def updateDisplay(self):
        """Continuously updates live readings on the UI."""
        while True:
            try:
                # Temperature display
                if self.tempReader.data is not None:
                    self.ui.top_thermo.setText(f"{self.tempReader.data[0]:.2f}°C")
                    self.ui.middle_thermo.setText(f"{self.tempReader.data[1]:.2f}°C")
                    self.ui.bottom_thermo.setText(f"{self.tempReader.data[2]:.2f}°C")

                # Pressure display
                pressure_value = self.pressureReader.read_pressure()
                if pressure_value is not None:
                    self.ui.pressureValueDisplayLabel.setText(f"{pressure_value:.2f} Torr")

            except Exception as e:
                print(f"[DisplayThread] Error updating display: {e}")
            sleep(1)

    def updateDisplaySimulation(self):

        while True:
            try:
                if self.tempSim.temperature is not None:
                    self.ui.top_thermo.setText(f"{self.tempSim.temperature:.2f}°C")
                    self.ui.middle_thermo.setText(f"{self.tempSim.temperature:.2f}°C")
                    self.ui.bottom_thermo.setText(f"{self.tempSim.temperature:.2f}°C")

                # if self.pressureSim.pressure is not None:
                #     self.ui.pressureValueDisplayLabel.setText(f"{self.pressureSim.pressure:.2f} Torr")

                if self.tempSim.temperature == self.tempSim.targetTemperature:
                    self.sendCompleteTempNotification()


                # if round(self.pressureSim.targetPressure,2) == round(self.pressureSim.pressure,2) and self.notification_sent == False:
                #     print("SENDING NOTIFICATION")
                #     self.sendCompletePressureNotification()
                #     self.notification_sent = True


            except Exception as e:
                print(f"[DisplayThread] Error updating display: {e}")
            sleep(1)

    def updateGPIB(self):
        """Automatic control for temperature and pressure."""
        while True:
            try:
                if self.ui.radioButton.isChecked():
                    # --- Temperature control ---
                    targetVolt = self.tempWriter.temp_to_volt(self.autoTemp)
                    currentVolt = self.tempWriter.read_volt()
                    if abs(currentVolt - targetVolt) > 0.01:
                        self.tempWriter.write_volt(targetVolt)
                        print(f"[TEMP] Target={targetVolt:.2f}V, Current={currentVolt:.2f}V")
                if self.ui.radioButton_3.isChecked():
                    # --- Pressure control ---
                    current_pressure = self.pressureReader.read_pressure()
                    if current_pressure is not None:
                        adjusted = self.pressureWriter.adjust_pressure(current_pressure, self.autoPressure)
                        self.pressureReader.base_pressure = adjusted
                        print(f"[PRESSURE] Current={current_pressure:.2f} Torr → Adjusted={adjusted:.2f} Torr")
            except Exception as e:
                print(f"[GPIBThread] Error updating devices: {e}")
            sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechDemoMainWindow()
    window.show()
    sys.exit(app.exec())
