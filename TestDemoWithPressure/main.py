import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, Slot, Qt
from DemoUI import Ui_TechDemoMainWindow
from notifications import NotificationManager
from temperature_read import TemperatureReader
from temperature_write import TemperatureWriter

class TechDemoMainWindow(QMainWindow):
    def __init__(self):
        super(TechDemoMainWindow, self).__init__()
        self.ui = Ui_TechDemoMainWindow()
        self.ui.setupUi(self)
        self.notifier = NotificationManager()
        self.tempReader = TemperatureReader()
        self.tempWriter = TemperatureWriter()

        # Add Units to pressure selector
        self.ui.pressureUnitSelector.addItem("Torr")
        self.ui.pressureUnitSelector.addItem("kPa")
        self.ui.pressureUnitSelector.addItem("atm")

        # Set default limits for pressure selector
        self.ui.pressureValueSelector.setMinimum(0.0)
        self.ui.pressureValueSelector.setMaximum(760.0)
        self.ui.pressureValueSelector.setValue(760.0)

        # Add Units to temperature selector
        self.ui.tempUnitSelector.addItem("Celsius")
        self.ui.tempUnitSelector.addItem("Fahrenheit")
        self.ui.tempUnitSelector.addItem("Kelvin")

        # Set default limits for temperature selector
        self.ui.tempValueSelector.setMinimum(0.0)
        self.ui.tempValueSelector.setMaximum(1250.0)

        # Connect signals and slots
        self.ui.autoToggleBox.stateChanged.connect(self.on_autoToggleBox_stateChanged)
        self.ui.manualToggleBox.stateChanged.connect(self.on_manualToggleBox_stateChanged)
        self.ui.pressureUnitSelector.currentTextChanged.connect(self.adjustPressureLimits)

    def print_temp_data(self):
        print(self.tempReader.data)

    def on_autoToggleBox_stateChanged(self, state):
        if state == 0: # Unchecked
            self.ui.manualToggleBox.setCheckState(Qt.CheckState.Checked)
        else: # Checked
            self.ui.manualToggleBox.setCheckState(Qt.CheckState.Unchecked)

    def on_manualToggleBox_stateChanged(self, state):
        if state == 0: # Unchecked
            self.ui.autoToggleBox.setCheckState(Qt.CheckState.Checked)
        else: # Checked
            self.ui.autoToggleBox.setCheckState(Qt.CheckState.Unchecked)

    def adjustPressureLimits(self, unit):
        if unit == "Torr":
            self.ui.pressureValueSelector.setMinimum(0.0)
            self.ui.pressureValueSelector.setMaximum(760.0)
            self.ui.pressureValueSelector.setValue(760.0)
        elif unit == "kPa":
            self.ui.pressureValueSelector.setMinimum(0.0)
            self.ui.pressureValueSelector.setMaximum(101.325)
            self.ui.pressureValueSelector.setValue(101.325)
        elif unit == "atm":
            self.ui.pressureValueSelector.setMinimum(0.0)
            self.ui.pressureValueSelector.setMaximum(1.0)
            self.ui.pressureValueSelector.setValue(1.0)

    def adjustTempLimits(self, unit):
        if unit == "Celsius":
            self.ui.tempValueSelector.setMinimum(0.0)
            self.ui.tempValueSelector.setMaximum(1250.0)
            self.ui.tempValueSelector.setValue(25.0)
        elif unit == "Fahrenheit":
            self.ui.tempValueSelector.setMinimum(32.0)
            self.ui.tempValueSelector.setMaximum(2282.0)
            self.ui.tempValueSelector.setValue(77.0)
        elif unit == "Kelvin":
            self.ui.tempValueSelector.setMinimum(273.15)
            self.ui.tempValueSelector.setMaximum(1523.15)
            self.ui.tempValueSelector.setValue(298.15)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechDemoMainWindow()
    window.show()
    sys.exit(app.exec())


