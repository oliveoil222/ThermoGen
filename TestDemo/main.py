import sys
import threading
from time import sleep
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, Signal, QObject

import configparser
from DemoUI import Ui_TechDemoMainWindow
from notifications import NotificationManager
from pressureSim import PressureSim
from temperatureSim import TemperatureSim
from temperature_read import TemperatureReader
from temperature_write import TemperatureWriter
from pressure_read import PressureReader
from pressure_write import PressureWriter


# ----------------------------------------------------
# Thread-safe notification dispatcher
# ----------------------------------------------------
class NotificationDispatcher(QObject):
    notify = Signal(str, str)


class TechDemoMainWindow(QMainWindow):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")

        super(TechDemoMainWindow, self).__init__()
        self.ui = Ui_TechDemoMainWindow()
        self.ui.setupUi(self)

        # Notification system
        self.notifier = NotificationManager()
        self.dispatcher = NotificationDispatcher()
        self.dispatcher.notify.connect(self._send_notification_safe)

        # State flags
        self.temp_notification_sent = True
        self.pressure_notification_sent = True

        # ----------------------------------------------------
        # Temperature Setup
        # ----------------------------------------------------
        if config.getboolean('SIMULATION', 'TEMP_SIMULATION'):
            self.tempSim = TemperatureSim(config.get('SIMULATION', 'TEMP_SIM_DEVICE'))
            self.tempSim.temperature = 25.0
            self.tempSim.targetTemperature = 25.0
            self.ui.tempSubmitButton.clicked.connect(self.updateTempValueSim)
        else:
            self.tempReader = TemperatureReader(config.get('TEMPERATURE', 'TEMP_INPUT_DEVICE'))
            self.tempWriter = TemperatureWriter(config.get('TEMPERATURE', 'TEMP_OUTPUT_DEVICE'))
            self.ui.tempSubmitButton.clicked.connect(self.updateTempValue)

        # ----------------------------------------------------
        # Pressure Setup
        # ----------------------------------------------------
        if config.getboolean('SIMULATION', 'PRESSURE_SIMULATION'):
            self.pressureSim = PressureSim(config.get('SIMULATION', 'PRESSURE_SIM_DEVICE'))
            self.pressureSim.pressure = 760.0
            self.pressureSim.targetPressure = 760.0
            self.ui.pressureSubmitButton.clicked.connect(self.updatePressureValueSim)
        else:
            self.pressureReader = PressureReader()
            self.pressureWriter = PressureWriter()
            self.ui.pressureSubmitButton.clicked.connect(self.updatePressureValue)

        self.autoTemp = 25.0
        self.autoPressure = 760.0

        # UI setup
        self.setupUI()

        # Threads
        self.displayThread = None
        self.updateGPIBThread = None
        self.startThreads(config.getboolean('SIMULATION', 'TEMP_SIMULATION'),
                          config.getboolean('SIMULATION', 'PRESSURE_SIMULATION'))

    # ----------------------------------------------------
    # Notification Safe Method
    # ----------------------------------------------------
    def _send_notification_safe(self, title, message):
        self.notifier.set_message(title, message)
        self.notifier.send_notification()

    # ----------------------------------------------------
    # UI Setup
    # ----------------------------------------------------
    def setupUI(self):
        self.ui.pressureUnitSelector.addItems(["Torr", "kPa", "atm"])
        self.adjustPressureLimits("Torr")

        self.ui.tempUnitSelector.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.adjustTempLimits("Celsius")

        self.ui.radioButton.toggled.connect(self.on_radioButton_1_stateChanged)
        self.ui.radioButton_2.toggled.connect(self.on_radioButton_2_stateChanged)
        self.ui.radioButton_3.toggled.connect(self.on_radioButton_3_stateChanged)
        self.ui.radioButton_4.toggled.connect(self.on_radioButton_4_stateChanged)
        self.ui.pressureUnitSelector.currentTextChanged.connect(self.adjustPressureLimits)
        self.ui.tempUnitSelector.currentTextChanged.connect(self.adjustTempLimits)

    # ----------------------------------------------------
    # Thread Startup
    # ----------------------------------------------------
    def startThreads(self, tempSimulated, pressureSimulated):
        if tempSimulated or pressureSimulated:
            self.displayThread = threading.Thread(target=self.updateDisplaySimulation, daemon=True)
            self.displayThread.start()
        else:
            self.displayThread = threading.Thread(target=self.updateDisplay, daemon=True)
            self.displayThread.start()
            self.updateGPIBThread = threading.Thread(target=self.updateGPIB, daemon=True)
            self.updateGPIBThread.start()

    # ----------------------------------------------------
    # Radio Button Handlers
    # ----------------------------------------------------
    def on_radioButton_1_stateChanged(self, state):
        if state == 1 and hasattr(self, 'tempSim'):
            self.tempSim.startSim()

    def on_radioButton_2_stateChanged(self, state):
        if state == 1 and hasattr(self, 'tempSim'):
            self.tempSim.pauseSim()

    def on_radioButton_3_stateChanged(self, state):
        if state == 1 and hasattr(self, 'pressureSim'):
            self.pressureSim.startSim()

    def on_radioButton_4_stateChanged(self, state):
        if state == 1 and hasattr(self, 'pressureSim'):
            self.pressureSim.pauseSim()

    # ----------------------------------------------------
    # Limit Adjustments
    # ----------------------------------------------------
    def adjustPressureLimits(self, unit):
        if unit == "Torr":
            self.ui.pressureValueSelector.setRange(0, 760)
            self.ui.pressureValueSelector.setValue(760)
        elif unit == "kPa":
            self.ui.pressureValueSelector.setRange(0, 101.325)
            self.ui.pressureValueSelector.setValue(101.325)
        else:  # atm
            self.ui.pressureValueSelector.setRange(0, 1)
            self.ui.pressureValueSelector.setValue(1)

    def adjustTempLimits(self, unit):
        if unit == "Celsius":
            self.ui.tempValueSelector.setRange(0, 1250)
            self.ui.tempValueSelector.setValue(25)
        elif unit == "Fahrenheit":
            self.ui.tempValueSelector.setRange(32, 2282)
            self.ui.tempValueSelector.setValue(77)
        else:
            self.ui.tempValueSelector.setRange(273.15, 1523.15)
            self.ui.tempValueSelector.setValue(298.15)

    # ----------------------------------------------------
    # Temperature & Pressure Setters
    # ----------------------------------------------------
    def updateTempValue(self):
        self.autoTemp = self.ui.tempValueSelector.value()
        unit = self.ui.tempUnitSelector.currentText()
        self.dispatcher.notify.emit("Temperature Set",
                                    f"Set Temperature: {self.autoTemp:.2f} {unit}")
        self.temp_notification_sent = False

    def updateTempValueSim(self):
        self.autoTemp = self.ui.tempValueSelector.value()
        self.tempSim.targetTemperature = self.autoTemp
        unit = self.ui.tempUnitSelector.currentText()
        self.dispatcher.notify.emit("Temperature Set",
                                    f"Set Temperature: {self.autoTemp:.2f} {unit}")
        self.temp_notification_sent = False

    def updatePressureValue(self):
        self.autoPressure = self.ui.pressureValueSelector.value()
        unit = self.ui.pressureUnitSelector.currentText()
        self.dispatcher.notify.emit("Pressure Set",
                                    f"Set Pressure: {self.autoPressure:.2f} {unit}")
        self.pressure_notification_sent = False

    def updatePressureValueSim(self):
        self.autoPressure = self.ui.pressureValueSelector.value()
        self.pressureSim.targetPressure = self.autoPressure
        unit = self.ui.pressureUnitSelector.currentText()
        self.dispatcher.notify.emit("Pressure Set",
                                    f"Set Pressure: {self.autoPressure:.2f} {unit}")
        self.pressure_notification_sent = False

    # ----------------------------------------------------
    # Display Threads (Hardware vs Simulation)
    # ----------------------------------------------------
    def updateDisplaySimulation(self):
        while True:
            try:
                # TEMPERATURE
                t = getattr(self.tempSim, 'temperature', None)
                if t is not None:
                    self.ui.top_thermo.setText(f"{t:.2f}°C")
                    self.ui.middle_thermo.setText(f"{t:.2f}°C")
                    self.ui.bottom_thermo.setText(f"{t:.2f}°C")

                # PRESSURE
                p = getattr(self.pressureSim, 'pressure', None)
                if p is not None:
                    self.ui.pressureValueDisplayLabel.setText(f"{p:.2f} Torr")

                # Temperature notification
                if t is not None and abs(t - self.autoTemp) < 0.1 and not self.temp_notification_sent and self.ui.radioButton.isChecked():
                    self.dispatcher.notify.emit(
                        "Temperature Target Reached",
                        f"Temperature has reached {self.autoTemp:.2f} {self.ui.tempUnitSelector.currentText()}"
                    )
                    self.temp_notification_sent = True

                # Pressure notification
                if p is not None and abs(p - self.autoPressure) < 0.1 and not self.pressure_notification_sent:
                    self.dispatcher.notify.emit(
                        "Pressure Target Reached",
                        f"Pressure has reached {self.autoPressure:.2f} {self.ui.pressureUnitSelector.currentText()}"
                    )
                    self.pressure_notification_sent = True

            except Exception as e:
                print(f"[DisplayThread] Error: {e}")

            sleep(0.5)

    def updateDisplay(self):
        while True:
            try:
                # Hardware temperature values
                if self.tempReader.data is not None:
                    self.ui.top_thermo.setText(f"{self.tempReader.data[0]:.2f}°C")
                    self.ui.middle_thermo.setText(f"{self.tempReader.data[1]:.2f}°C")
                    self.ui.bottom_thermo.setText(f"{self.tempReader.data[2]:.2f}°C")

                # Hardware pressure
                pressure_value = self.pressureReader.read_pressure()
                if pressure_value is not None:
                    self.ui.pressureValueDisplayLabel.setText(f"{pressure_value:.2f} Torr")

                # Completion notifications
                if abs(self.tempReader.data[0] - self.autoTemp) < 0.1 and not self.temp_notification_sent:
                    self.dispatcher.notify.emit(
                        "Temperature Target Reached",
                        f"Temperature has reached {self.autoTemp:.2f}°C"
                    )
                    self.temp_notification_sent = True

                if abs(pressure_value - self.autoPressure) < 0.1 and not self.pressure_notification_sent:
                    self.dispatcher.notify.emit(
                        "Pressure Target Reached",
                        f"Pressure has reached {self.autoPressure:.2f} Torr"
                    )
                    self.pressure_notification_sent = True

            except Exception as e:
                print(f"[DisplayThread] Error updating display: {e}")

            sleep(1)

    # ----------------------------------------------------
    # Hardware GPIB Thread
    # ----------------------------------------------------
    def updateGPIB(self):
        while True:
            try:
                # AUTOMATIC TEMPERATURE
                if self.ui.radioButton.isChecked():
                    targetVolt = self.tempWriter.temp_to_volt(self.autoTemp)
                    currentVolt = self.tempWriter.read_volt()
                    if abs(currentVolt - targetVolt) > 0.01:
                        self.tempWriter.write_volt(targetVolt)

                # AUTOMATIC PRESSURE
                if self.ui.radioButton_3.isChecked():
                    current_pressure = self.pressureReader.read_pressure()
                    if current_pressure is not None:
                        adjusted = self.pressureWriter.adjust_pressure(current_pressure, self.autoPressure)
                        self.pressureReader.base_pressure = adjusted

            except Exception as e:
                print(f"[GPIBThread] Error: {e}")

            sleep(1)


# ----------------------------------------------------
# Run Application
# ----------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechDemoMainWindow()
    window.show()
    sys.exit(app.exec())
