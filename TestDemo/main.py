import sys
import threading
from time import sleep
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from DemoUI_OLD2 import Ui_TechDemoMainWindow
from notifications import NotificationManager
from temperature_read import TemperatureReader
from temperature_write import TemperatureWriter
from pressure_read import PressureReader
from pressure_write import PressureWriter


class TechDemoMainWindow(QMainWindow):
    def __init__(self):
        super(TechDemoMainWindow, self).__init__()
        self.ui = Ui_TechDemoMainWindow()
        self.ui.setupUi(self)

        # Core modules
        self.notifier = NotificationManager()
        self.tempReader = TemperatureReader()
        self.tempWriter = TemperatureWriter()
        self.pressureReader = PressureReader()
        self.pressureWriter = PressureWriter()

        # Threads and state
        self.displayThread = None
        self.updateGPIBThread = None
        self.isAutoOn = False

        self.autoTemp = 25.0
        self.autoPressure = 760.0

        # Setup the UI
        self.setupUI()

        # Start background threads
        self.startThreads()

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
        self.ui.pressureUnitSelector.currentTextChanged.connect(self.adjustPressureLimits)
        self.ui.tempUnitSelector.currentTextChanged.connect(self.adjustTempLimits)
        self.ui.tempSubmitButton.clicked.connect(self.updateTempValue)
        self.ui.pressureSubmitButton.clicked.connect(self.updatePressureValue)
        # self.ui.manualToggleBox.setCheckState(Qt.CheckState.Checked)

    def startThreads(self):
        self.displayThread = threading.Thread(target=self.updateDisplay, daemon=True)
        self.displayThread.start()

        self.updateGPIBThread = threading.Thread(target=self.updateGPIB, daemon=True)
        self.updateGPIBThread.start()

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
    # -----------------------------
    # --- THREADS ---
    # -----------------------------
    def updateDisplay(self):
        """Continuously updates live readings on the UI."""
        while True:
            try:
                # Temperature display
                if self.tempReader.data is not None:
                    self.ui.tempValueDisplayLabel.setText(f"{self.tempReader.data[2]:.2f}°C")

                # Pressure display
                pressure_value = self.pressureReader.read_pressure()
                if pressure_value is not None:
                    self.ui.pressureValueDisplayLabel.setText(f"{pressure_value:.2f} Torr")

            except Exception as e:
                print(f"[DisplayThread] Error updating display: {e}")
            sleep(1)

    def updateGPIB(self):
        """Automatic control for temperature and pressure."""
        while True:
            try:
                if self.isAutoOn:
                    # --- Temperature control ---
                    targetVolt = self.tempWriter.temp_to_volt(self.autoTemp)
                    currentVolt = self.tempWriter.read_volt()
                    if abs(currentVolt - targetVolt) > 0.01:
                        self.tempWriter.write_volt(targetVolt)
                        print(f"[TEMP] Target={targetVolt:.2f}V, Current={currentVolt:.2f}V")

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
