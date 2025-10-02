# main.py
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
    try:
        # stop the asyncio loop
        loop.stop()  
    except Exception:
        pass
    # quit the Qt application
    QCoreApplication.quit()  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # ensure event loop shutdown when windows closed
    if app:
        app.lastWindowClosed.connect(stop_event_loops)

    # run qt event loop integrated with asyncio
    try:
        QtAsyncio.run()
    except Exception as e:
        print("Application exit:", e)
