import sys
import asyncio
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QThread, Signal

from DemoUI import Ui_TechDemoMainWindow
from temperature_read import TemperatureReader
from temperature_write import TemperatureWriter
from pressure_read import PressureReader
from pressure_write import PressureWriter
from notifications import Notifier


class WorkerThread(QThread):
    progress = Signal(str)

    def __init__(self, temp_reader, temp_writer, pres_reader, pres_writer, target_temp, target_pres):
        super().__init__()
        self.temp_reader = temp_reader
        self.temp_writer = temp_writer
        self.pres_reader = pres_reader
        self.pres_writer = pres_writer
        self.target_temp = target_temp
        self.target_pres = target_pres
        self.running = True

    def run(self):
        print("[WorkerThread] Starting control loop...")
        while self.running:
            temp = self.temp_reader.read_temperature()
            pres = self.pres_reader.read_pressure()

            if temp is not None:
                print(f"[WorkerThread] Current Temp: {temp:.2f} °C")
            if pres is not None:
                print(f"[WorkerThread] Current Pressure: {pres:.2f} Torr")

            # control logic placeholder
            if temp is not None and temp < self.target_temp:
                print("[WorkerThread] Increasing PSU voltage (simulation).")

            if pres is not None:
                self.pres_writer.adjust_pressure(pres, self.target_pres)

            self.sleep(2)

    def stop(self):
        print("[WorkerThread] Stopping control loop...")
        self.running = False
        self.quit()
        self.wait()


class TechDemoMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TechDemoMainWindow()
        self.ui.setupUi(self)

        # hardware modules
        self.temp_reader = TemperatureReader()
        self.temp_writer = TemperatureWriter()
        self.pres_reader = PressureReader()
        self.pres_writer = PressureWriter()
        self.notifier = Notifier()

        # connect ui buttons
        self.ui.tempSubmitButton.clicked.connect(self.submit_temperature)
        self.ui.pressureSubmitButton.clicked.connect(self.submit_pressure)

        self.worker_thread = None
        print("[MainWindow] UI initialized.")

    def submit_temperature(self):
        # handle temperature submit button click
        target_temp = self.ui.tempValueSelector.value()
        print(f"[UI] Target Temperature submitted: {target_temp} °C")
        QMessageBox.information(self, "Temperature Submitted", f"Target temperature set to {target_temp} °C")
        self.start_control_loop(temp=target_temp)

    def submit_pressure(self):
        # handle pressure submit button click
        target_pres = self.ui.pressureValueSelector.value()
        print(f"[UI] Target Pressure submitted: {target_pres} Torr")
        QMessageBox.information(self, "Pressure Submitted", f"Target pressure set to {target_pres} Torr")
        self.start_control_loop(pressure=target_pres)

    def start_control_loop(self, temp=None, pressure=None):
        #starts or updates the background control loop
        target_temp = temp or self.ui.tempValueSelector.value()
        target_pres = pressure or self.ui.pressureValueSelector.value()

        if self.worker_thread:
            self.worker_thread.stop()

        self.worker_thread = WorkerThread(
            self.temp_reader, self.temp_writer,
            self.pres_reader, self.pres_writer,
            target_temp, target_pres
        )
        self.worker_thread.start()
        print("[MainWindow] Control loop started with targets:",
              f"Temperature = {target_temp} °C, Pressure = {target_pres} Torr")

    def closeEvent(self, event):
        #clean up on window close
        if self.worker_thread:
            self.worker_thread.stop()
        self.temp_reader.close()
        self.pres_reader.close()
        self.pres_writer.close()
        print("[MainWindow] Closed safely.")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechDemoMainWindow()
    window.show()
    sys.exit(app.exec())
