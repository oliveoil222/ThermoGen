# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DemoUI_Basic.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                               QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
                               QLabel, QLayout, QPushButton, QSizePolicy,
                               QVBoxLayout, QWidget)
import PySide6.QtAsyncio as QtAsyncio
import asyncio
import windows_toasts
import concurrent.futures

from notify import Worker

notifier = windows_toasts.WindowsToaster("Tech Demo")

currentTemperature = 25.00
currentPressure = 760.00


class Ui_TechDemoMainWindow(object):
    def setupUi(self, TechDemoMainWindow):
        if not TechDemoMainWindow.objectName():
            TechDemoMainWindow.setObjectName(u"TechDemoMainWindow")
        TechDemoMainWindow.resize(500, 529)
        TechDemoMainWindow.setStyleSheet(u"")
        self.verticalLayoutWidget = QWidget(TechDemoMainWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(50, 50, 401, 421))
        self.MainLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.MainLayout.setObjectName(u"MainLayout")
        self.MainLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.TopHalfLayout = QHBoxLayout()
        self.TopHalfLayout.setObjectName(u"TopHalfLayout")
        self.TopHalfLayout.setContentsMargins(-1, 25, -1, 25)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lightTextLabel = QLabel(self.verticalLayoutWidget)
        self.lightTextLabel.setObjectName(u"lightTextLabel")
        self.lightTextLabel.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.lightTextLabel.setFont(font)
        self.lightTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lightTextLabel.setWordWrap(False)
        self.lightTextLabel.setMargin(0)

        self.verticalLayout.addWidget(self.lightTextLabel)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lightToggleOn = QCheckBox(self.verticalLayoutWidget)
        self.lightToggleOn.setObjectName(u"lightToggleOn")

        self.horizontalLayout_2.addWidget(self.lightToggleOn)

        self.lightToggleOff = QCheckBox(self.verticalLayoutWidget)
        self.lightToggleOff.setObjectName(u"lightToggleOff")
        self.lightToggleOff.setMinimumSize(QSize(0, 50))
        self.lightToggleOff.setChecked(True)
        self.horizontalLayout_2.addWidget(self.lightToggleOff)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.lightToggleOn.stateChanged.connect(self.lightOnToggleChanged)
        self.lightToggleOff.stateChanged.connect(self.lightOffToggleChanged)

        self.TopHalfLayout.addLayout(self.verticalLayout)

        self.VertLine = QFrame(self.verticalLayoutWidget)
        self.VertLine.setObjectName(u"VertLine")
        font1 = QFont()
        font1.setBold(False)
        self.VertLine.setFont(font1)
        self.VertLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.VertLine.setLineWidth(0)
        self.VertLine.setMidLineWidth(2)
        self.VertLine.setFrameShape(QFrame.Shape.VLine)

        self.TopHalfLayout.addWidget(self.VertLine)

        self.AutoManualToggleVertLayout = QVBoxLayout()
        self.AutoManualToggleVertLayout.setSpacing(0)
        self.AutoManualToggleVertLayout.setObjectName(u"AutoManualToggleVertLayout")
        self.AutoManualToggleVertLayout.setContentsMargins(25, -1, -1, -1)
        self.autoToggleBox = QCheckBox(self.verticalLayoutWidget)
        self.autoToggleBox.setObjectName(u"autoToggleBox")

        self.AutoManualToggleVertLayout.addWidget(self.autoToggleBox)

        self.manualToggleBox = QCheckBox(self.verticalLayoutWidget)
        self.manualToggleBox.setObjectName(u"manualToggleBox")
        self.autoToggleBox.setChecked(True)

        self.AutoManualToggleVertLayout.addWidget(self.manualToggleBox)

        self.autoToggleBox.stateChanged.connect(self.automaticToggleChanged)
        self.manualToggleBox.stateChanged.connect(self.manualToggleChanged)

        self.TopHalfLayout.addLayout(self.AutoManualToggleVertLayout)

        self.MainLayout.addLayout(self.TopHalfLayout)

        self.HorizLine = QFrame(self.verticalLayoutWidget)
        self.HorizLine.setObjectName(u"HorizLine")
        self.HorizLine.setLineWidth(0)
        self.HorizLine.setMidLineWidth(2)
        self.HorizLine.setFrameShape(QFrame.Shape.HLine)
        self.HorizLine.setFrameShadow(QFrame.Shadow.Sunken)

        self.MainLayout.addWidget(self.HorizLine)

        self.BottomHalfLayout = QHBoxLayout()
        self.BottomHalfLayout.setObjectName(u"BottomHalfLayout")
        self.TempPressureLayout = QHBoxLayout()
        self.TempPressureLayout.setObjectName(u"TempPressureLayout")
        self.TempLayoutBox = QGroupBox(self.verticalLayoutWidget)
        self.TempLayoutBox.setObjectName(u"TempLayoutBox")
        self.TempLayoutBox.setEnabled(True)
        font2 = QFont()
        font2.setKerning(False)
        font2.setHintingPreference(QFont.PreferDefaultHinting)
        self.TempLayoutBox.setFont(font2)
        self.TempLayoutBox.setStyleSheet(u"QGroupBox#TempLayoutBox {border:0;}")
        self.TempLayoutBox.setFlat(False)
        self.tempTextLabel = QLabel(self.TempLayoutBox)
        self.tempTextLabel.setObjectName(u"tempTextLabel")
        self.tempTextLabel.setGeometry(QRect(0, 9, 171, 31))
        font3 = QFont()
        font3.setPointSize(16)
        font3.setKerning(True)
        font3.setHintingPreference(QFont.PreferDefaultHinting)
        self.tempTextLabel.setFont(font3)
        self.tempTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tempUnitSelector = QComboBox(self.TempLayoutBox)
        self.tempUnitSelector.setObjectName(u"tempUnitSelector")
        self.tempUnitSelector.setGeometry(QRect(30, 100, 111, 22))
        self.tempUnitSelector.addItem("Celsius")
        self.tempUnitSelector.addItem("Fahrenheit")
        self.tempUnitSelector.addItem("Kelvin")
        self.tempValueSelector = QDoubleSpinBox(self.TempLayoutBox)
        self.tempValueSelector.setObjectName(u"tempValueSelector")
        self.tempValueSelector.setGeometry(QRect(30, 72, 111, 21))
        self.tempValueSelector.setMinimum(25.000000000000000)
        self.tempValueSelector.setMaximum(1000.000000000000000)
        self.tempSubmitButton = QPushButton(self.TempLayoutBox)
        self.tempSubmitButton.setObjectName(u"tempSubmitButton")
        self.tempSubmitButton.setGeometry(QRect(30, 130, 111, 24))

        self.TempPressureLayout.addWidget(self.TempLayoutBox)

        self.PressureLayoutBox = QGroupBox(self.verticalLayoutWidget)
        self.PressureLayoutBox.setObjectName(u"PressureLayoutBox")
        self.PressureLayoutBox.setStyleSheet(u"QGroupBox#PressureLayoutBox {border:0;}")
        self.pressureTextLabel = QLabel(self.PressureLayoutBox)
        self.pressureTextLabel.setObjectName(u"pressureTextLabel")
        self.pressureTextLabel.setGeometry(QRect(0, 9, 171, 31))
        font4 = QFont()
        font4.setPointSize(16)
        self.pressureTextLabel.setFont(font4)
        self.pressureTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pressureUnitSelector = QComboBox(self.PressureLayoutBox)
        self.pressureUnitSelector.setObjectName(u"pressureUnitSelector")
        self.pressureUnitSelector.setGeometry(QRect(30, 100, 111, 22))
        self.pressureUnitSelector.addItem("Torr")
        self.pressureUnitSelector.addItem("PSI")
        self.pressureUnitSelector.addItem("kPa")
        self.pressureUnitSelector.addItem("atm")
        self.pressureUnitSelector.addItem("bar")
        self.pressureValueSelector = QDoubleSpinBox(self.PressureLayoutBox)
        self.pressureValueSelector.setObjectName(u"pressureValueSelector")
        self.pressureValueSelector.setGeometry(QRect(30, 72, 111, 21))
        self.pressureValueSelector.setMinimum(0.000000000000000)
        self.pressureValueSelector.setMaximum(1000.000000000000000)
        self.pressureValueSelector.setValue(760.00)
        self.pressureSubmitButton = QPushButton(self.PressureLayoutBox)
        self.pressureSubmitButton.setObjectName(u"pressureSubmitButton")
        self.pressureSubmitButton.setGeometry(QRect(30, 130, 111, 24))

        self.pressureUnitSelector.currentIndexChanged.connect(self.changePressureLimits)
        self.tempUnitSelector.currentIndexChanged.connect(self.changeTempLimits)

        self.TempPressureLayout.addWidget(self.PressureLayoutBox)

        self.BottomHalfLayout.addLayout(self.TempPressureLayout)

        self.MainLayout.addLayout(self.BottomHalfLayout)

        self.retranslateUi(TechDemoMainWindow)

        self.tempUnitSelector.setCurrentIndex(0)
        self.pressureUnitSelector.setCurrentIndex(0)

        self.tempSubmitButton.clicked.connect(self.tempSubmitButtonClicked)
        self.pressureSubmitButton.clicked.connect(self.pressureSubmitButtonClicked)

        QMetaObject.connectSlotsByName(TechDemoMainWindow)

    # setupUi

    def retranslateUi(self, TechDemoMainWindow):
        TechDemoMainWindow.setWindowTitle(QCoreApplication.translate("TechDemoMainWindow", u"Tech Demo UI", None))
        self.lightTextLabel.setText(QCoreApplication.translate("TechDemoMainWindow", u"Light Switch", None))
        self.lightToggleOn.setText(QCoreApplication.translate("TechDemoMainWindow", u"On", None))
        self.lightToggleOff.setText(QCoreApplication.translate("TechDemoMainWindow", u"Off", None))
        self.autoToggleBox.setText(QCoreApplication.translate("TechDemoMainWindow", u"Manual", None))
        self.manualToggleBox.setText(QCoreApplication.translate("TechDemoMainWindow", u"Automatic", None))
        self.TempLayoutBox.setTitle("")
        self.tempTextLabel.setText(QCoreApplication.translate("TechDemoMainWindow", u"Temperature", None))
        self.tempUnitSelector.setCurrentText("")
        self.tempValueSelector.setPrefix("")
        self.tempSubmitButton.setText(QCoreApplication.translate("TechDemoMainWindow", u"Submit", None))
        self.PressureLayoutBox.setTitle("")
        self.pressureTextLabel.setText(QCoreApplication.translate("TechDemoMainWindow", u"Pressure", None))
        self.pressureUnitSelector.setCurrentText("")
        self.pressureValueSelector.setPrefix("")
        self.pressureSubmitButton.setText(QCoreApplication.translate("TechDemoMainWindow", u"Submit", None))

    # retranslateUi

    # Connections for toggle checkboxes

    def lightOnToggleChanged(self, state):
        if (state == 2):
            self.lightToggleOff.setChecked(False)
        else:
            self.lightToggleOff.setChecked(True)

    def lightOffToggleChanged(self, state):
        if (state == 2):
            self.lightToggleOn.setChecked(False)
        else:
            self.lightToggleOn.setChecked(True)

    def manualToggleChanged(self, state):
        if (state == 2):
            self.autoToggleBox.setChecked(False)
        else:
            self.autoToggleBox.setChecked(True)

    def automaticToggleChanged(self, state):
        if (state == 2):
            self.manualToggleBox.setChecked(False)
        else:
            self.manualToggleBox.setChecked(True)

    # Limits for input values

    def changeTempLimits(self, index):
        match index:
            case 0:
                self.tempValueSelector.setRange(25.00, 1000.00)
            case 1:
                self.tempValueSelector.setRange(77.00, 1832.00)
            case 2:
                self.tempValueSelector.setRange(298.15, 1273.15)

    def changePressureLimits(self, index):
        match index:
            case 0:
                self.pressureValueSelector.setRange(0.00, 760.00)
            case 1:
                self.pressureValueSelector.setRange(0.00, 14.69)
            case 2:
                self.pressureValueSelector.setRange(0.00, 101.32)
            case 3:
                self.pressureValueSelector.setRange(0.00, 1.00)
            case 4:
                self.pressureValueSelector.setRange(0.00, 1.01)


    def showNotification(self, messageType):
        notification = windows_toasts.Toast()

        if messageType == "success":
            notification.text_fields = ["SUCCESS", "Temperature and pressure reached."]
        elif messageType == "unsafe":
            notification.text_fields = ["FAILURE", "Unsafe environment: Temperature or pressure exceeded 1000."]
        else:
            notification.text_fields = ["FAILURE", "Failed to reach temperature or pressure in safe time."]

        notifier.show_toast(notification)

    def ButtonClickedAsync(self):
        self.Worker = Worker(currentTemperature, currentPressure, self.tempValueSelector.value(), self.pressureValueSelector.value())
        self.Worker.finished.connect(self.showNotification)
        self.Worker.start()

    def tempSubmitButtonClicked(self):
        self.ButtonClickedAsync()

    def pressureSubmitButtonClicked(self):
        self.ButtonClickedAsync()