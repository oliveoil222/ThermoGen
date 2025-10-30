# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DemoUI_Basic.ui'
##
## Cleaned and enhanced for ThermoGen project
## Restores unit selectors, default values, and ensures compatibility with main.py
################################################################################

from PySide6.QtCore import (QCoreApplication, QRect, QMetaObject, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel, QLayout, QPushButton,
    QVBoxLayout, QWidget)

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

        # ────────────────────────────────
        # Top: Auto / Manual Toggle
        # ────────────────────────────────
        self.TopHalfLayout = QHBoxLayout()
        self.TopHalfLayout.setObjectName(u"TopHalfLayout")
        self.TopHalfLayout.setContentsMargins(-1, 25, -1, 25)

        self.AutoManualToggleVertLayout = QVBoxLayout()
        self.AutoManualToggleVertLayout.setSpacing(0)
        self.AutoManualToggleVertLayout.setObjectName(u"AutoManualToggleVertLayout")
        self.AutoManualToggleVertLayout.setContentsMargins(25, -1, -1, -1)

        self.autoToggleBox = QCheckBox(self.verticalLayoutWidget)
        self.autoToggleBox.setObjectName(u"autoToggleBox")
        self.AutoManualToggleVertLayout.addWidget(self.autoToggleBox)

        self.manualToggleBox = QCheckBox(self.verticalLayoutWidget)
        self.manualToggleBox.setObjectName(u"manualToggleBox")
        self.AutoManualToggleVertLayout.addWidget(self.manualToggleBox)

        self.TopHalfLayout.addLayout(self.AutoManualToggleVertLayout)
        self.MainLayout.addLayout(self.TopHalfLayout)

        # ────────────────────────────────
        # Separator Line
        # ────────────────────────────────
        self.HorizLine = QFrame(self.verticalLayoutWidget)
        self.HorizLine.setObjectName(u"HorizLine")
        self.HorizLine.setLineWidth(0)
        self.HorizLine.setMidLineWidth(2)
        self.HorizLine.setFrameShape(QFrame.Shape.HLine)
        self.HorizLine.setFrameShadow(QFrame.Shadow.Sunken)
        self.MainLayout.addWidget(self.HorizLine)

        # ────────────────────────────────
        # Bottom: Temperature & Pressure Layout
        # ────────────────────────────────
        self.BottomHalfLayout = QHBoxLayout()
        self.BottomHalfLayout.setObjectName(u"BottomHalfLayout")

        self.TempPressureLayout = QHBoxLayout()
        self.TempPressureLayout.setObjectName(u"TempPressureLayout")

        # ─── Temperature Box ───
        self.TempLayoutBox = QGroupBox(self.verticalLayoutWidget)
        self.TempLayoutBox.setObjectName(u"TempLayoutBox")
        self.TempLayoutBox.setEnabled(True)
        self.TempLayoutBox.setStyleSheet(u"QGroupBox#TempLayoutBox {border:0;}")

        font = QFont()
        font.setPointSize(16)
        self.tempTextLabel = QLabel(self.TempLayoutBox)
        self.tempTextLabel.setObjectName(u"tempTextLabel")
        self.tempTextLabel.setGeometry(QRect(0, 9, 171, 31))
        self.tempTextLabel.setFont(font)
        self.tempTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tempValueSelector = QDoubleSpinBox(self.TempLayoutBox)
        self.tempValueSelector.setObjectName(u"tempValueSelector")
        self.tempValueSelector.setGeometry(QRect(30, 72, 111, 21))
        self.tempValueSelector.setMinimum(25.0)
        self.tempValueSelector.setMaximum(1000.0)
        self.tempValueSelector.setValue(25.0)  # default temperature

        self.tempUnitSelector = QComboBox(self.TempLayoutBox)
        self.tempUnitSelector.setObjectName(u"tempUnitSelector")
        self.tempUnitSelector.setGeometry(QRect(30, 100, 111, 22))
        self.tempUnitSelector.addItems(["°C", "°F"])
        self.tempUnitSelector.setCurrentIndex(0)

        self.tempSubmitButton = QPushButton(self.TempLayoutBox)
        self.tempSubmitButton.setObjectName(u"tempSubmitButton")
        self.tempSubmitButton.setGeometry(QRect(30, 130, 111, 24))

        self.TempPressureLayout.addWidget(self.TempLayoutBox)

        # ─── Pressure Box ───
        self.PressureLayoutBox = QGroupBox(self.verticalLayoutWidget)
        self.PressureLayoutBox.setObjectName(u"PressureLayoutBox")
        self.PressureLayoutBox.setStyleSheet(u"QGroupBox#PressureLayoutBox {border:0;}")

        self.pressureTextLabel = QLabel(self.PressureLayoutBox)
        self.pressureTextLabel.setObjectName(u"pressureTextLabel")
        self.pressureTextLabel.setGeometry(QRect(0, 9, 171, 31))
        font2 = QFont()
        font2.setPointSize(16)
        self.pressureTextLabel.setFont(font2)
        self.pressureTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pressureValueSelector = QDoubleSpinBox(self.PressureLayoutBox)
        self.pressureValueSelector.setObjectName(u"pressureValueSelector")
        self.pressureValueSelector.setGeometry(QRect(30, 72, 111, 21))
        self.pressureValueSelector.setMinimum(0.0)
        self.pressureValueSelector.setMaximum(1000.0)
        self.pressureValueSelector.setValue(760.0)  # default pressure in Torr

        self.pressureUnitSelector = QComboBox(self.PressureLayoutBox)
        self.pressureUnitSelector.setObjectName(u"pressureUnitSelector")
        self.pressureUnitSelector.setGeometry(QRect(30, 100, 111, 22))
        self.pressureUnitSelector.addItems(["Torr", "Pascal", "Bar"])
        self.pressureUnitSelector.setCurrentIndex(0)

        self.pressureSubmitButton = QPushButton(self.PressureLayoutBox)
        self.pressureSubmitButton.setObjectName(u"pressureSubmitButton")
        self.pressureSubmitButton.setGeometry(QRect(30, 130, 111, 24))

        self.TempPressureLayout.addWidget(self.PressureLayoutBox)
        self.BottomHalfLayout.addLayout(self.TempPressureLayout)
        self.MainLayout.addLayout(self.BottomHalfLayout)

        self.retranslateUi(TechDemoMainWindow)
        QMetaObject.connectSlotsByName(TechDemoMainWindow)

    # ────────────────────────────────
    # Translation / Label Text
    # ────────────────────────────────
    def retranslateUi(self, TechDemoMainWindow):
        _translate = QCoreApplication.translate
        TechDemoMainWindow.setWindowTitle(_translate("TechDemoMainWindow", "ThermoGen Control Interface"))
        self.autoToggleBox.setText(_translate("TechDemoMainWindow", "Automatic"))
        self.manualToggleBox.setText(_translate("TechDemoMainWindow", "Manual"))
        self.tempTextLabel.setText(_translate("TechDemoMainWindow", "Temperature"))
        self.tempSubmitButton.setText(_translate("TechDemoMainWindow", "Submit"))
        self.pressureTextLabel.setText(_translate("TechDemoMainWindow", "Pressure"))
        self.pressureSubmitButton.setText(_translate("TechDemoMainWindow", "Submit"))
