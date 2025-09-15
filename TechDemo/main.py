import asyncio
import sys

from PySide6 import QtAsyncio
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QCoreApplication
from mainWindow import Ui_TechDemoMainWindow

class MainWindow(QMainWindow, Ui_TechDemoMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_TechDemoMainWindow()
        self.ui.setupUi(self)

def stop_event_loops():
    loop = asyncio.get_event_loop()
    loop.stop()  # Stop the asyncio loop
    app.quit()  # Quit the Qt application

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    QtAsyncio.run()

    if app:
        app.lastWindowClosed.connect(stop_event_loops)