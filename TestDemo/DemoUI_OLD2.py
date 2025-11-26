# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DemoUI_Basic.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QDoubleSpinBox,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QPushButton, QRadioButton, QSizePolicy,
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
        self.TopHalfLayout = QHBoxLayout()
        self.TopHalfLayout.setObjectName(u"TopHalfLayout")
        self.TopHalfLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.CurrentPressureTempValues = QVBoxLayout()
        self.CurrentPressureTempValues.setSpacing(5)
        self.CurrentPressureTempValues.setObjectName(u"CurrentPressureTempValues")
        self.CurrentPressureTempValues.setContentsMargins(0, -1, -1, -1)
        self.TempVert = QVBoxLayout()
        self.TempVert.setObjectName(u"TempVert")
        self.TempVert.setContentsMargins(0, -1, -1, -1)
        self.title = QLabel(self.verticalLayoutWidget)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(16)
        self.title.setFont(font)

        self.TempVert.addWidget(self.title)

        self.top_thermo = QLabel(self.verticalLayoutWidget)
        self.top_thermo.setObjectName(u"top_thermo")
        self.top_thermo.setFont(font)
        self.top_thermo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TempVert.addWidget(self.top_thermo)

        self.middle_thermo = QLabel(self.verticalLayoutWidget)
        self.middle_thermo.setObjectName(u"middle_thermo")
        self.middle_thermo.setFont(font)
        self.middle_thermo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TempVert.addWidget(self.middle_thermo)

        self.bottom_thermo = QLabel(self.verticalLayoutWidget)
        self.bottom_thermo.setObjectName(u"bottom_thermo")
        self.bottom_thermo.setFont(font)
        self.bottom_thermo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.TempVert.addWidget(self.bottom_thermo)


        self.CurrentPressureTempValues.addLayout(self.TempVert)

        self.line = QFrame(self.verticalLayoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.CurrentPressureTempValues.addWidget(self.line)

        self.PressureVert = QVBoxLayout()
        self.PressureVert.setObjectName(u"PressureVert")
        self.PressureVert.setContentsMargins(0, -1, -1, -1)
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.PressureVert.addWidget(self.label_4)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.PressureVert.addWidget(self.label_3)


        self.CurrentPressureTempValues.addLayout(self.PressureVert)


        self.horizontalLayout.addLayout(self.CurrentPressureTempValues)

        self.AutoManualToggleVertLayout = QVBoxLayout()
        self.AutoManualToggleVertLayout.setSpacing(5)
        self.AutoManualToggleVertLayout.setObjectName(u"AutoManualToggleVertLayout")
        self.AutoManualToggleTempVertLayout = QVBoxLayout()
        self.AutoManualToggleTempVertLayout.setSpacing(0)
        self.AutoManualToggleTempVertLayout.setObjectName(u"AutoManualToggleTempVertLayout")
        self.AutoManualToggleTempVertLayout.setContentsMargins(25, -1, -1, -1)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.AutoManualToggleTempVertLayout.addWidget(self.label)

        self.radioButton_2 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setFont(font)
        self.radioButton_2.setChecked(True)

        self.AutoManualToggleTempVertLayout.addWidget(self.radioButton_2)

        self.radioButton = QRadioButton(self.verticalLayoutWidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setFont(font)

        self.AutoManualToggleTempVertLayout.addWidget(self.radioButton)


        self.AutoManualToggleVertLayout.addLayout(self.AutoManualToggleTempVertLayout)

        self.line_2 = QFrame(self.verticalLayoutWidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.AutoManualToggleVertLayout.addWidget(self.line_2)

        self.AutoManualTogglePressureVertLayout = QVBoxLayout()
        self.AutoManualTogglePressureVertLayout.setSpacing(0)
        self.AutoManualTogglePressureVertLayout.setObjectName(u"AutoManualTogglePressureVertLayout")
        self.AutoManualTogglePressureVertLayout.setContentsMargins(25, -1, -1, -1)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setMargin(0)

        self.AutoManualTogglePressureVertLayout.addWidget(self.label_2)

        self.radioButton_4 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setFont(font)
        self.radioButton_4.setChecked(True)

        self.AutoManualTogglePressureVertLayout.addWidget(self.radioButton_4)

        self.radioButton_3 = QRadioButton(self.verticalLayoutWidget)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setFont(font)

        self.AutoManualTogglePressureVertLayout.addWidget(self.radioButton_3)


        self.AutoManualToggleVertLayout.addLayout(self.AutoManualTogglePressureVertLayout)


        self.horizontalLayout.addLayout(self.AutoManualToggleVertLayout)


        self.TopHalfLayout.addLayout(self.horizontalLayout)


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
        font1 = QFont()
        font1.setKerning(False)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.TempLayoutBox.setFont(font1)
        self.TempLayoutBox.setStyleSheet(u"QGroupBox#TempLayoutBox {border:0;}")
        self.TempLayoutBox.setFlat(False)
        self.tempTextLabel = QLabel(self.TempLayoutBox)
        self.tempTextLabel.setObjectName(u"tempTextLabel")
        self.tempTextLabel.setGeometry(QRect(0, 9, 171, 31))
        font2 = QFont()
        font2.setPointSize(16)
        font2.setKerning(True)
        font2.setHintingPreference(QFont.PreferDefaultHinting)
        self.tempTextLabel.setFont(font2)
        self.tempTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tempUnitSelector = QComboBox(self.TempLayoutBox)
        self.tempUnitSelector.setObjectName(u"tempUnitSelector")
        self.tempUnitSelector.setGeometry(QRect(30, 100, 111, 22))
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
        self.pressureTextLabel.setFont(font)
        self.pressureTextLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pressureUnitSelector = QComboBox(self.PressureLayoutBox)
        self.pressureUnitSelector.setObjectName(u"pressureUnitSelector")
        self.pressureUnitSelector.setGeometry(QRect(30, 100, 111, 22))
        self.pressureValueSelector = QDoubleSpinBox(self.PressureLayoutBox)
        self.pressureValueSelector.setObjectName(u"pressureValueSelector")
        self.pressureValueSelector.setGeometry(QRect(30, 72, 111, 21))
        self.pressureValueSelector.setMinimum(0.000000000000000)
        self.pressureValueSelector.setMaximum(1000.000000000000000)
        self.pressureSubmitButton = QPushButton(self.PressureLayoutBox)
        self.pressureSubmitButton.setObjectName(u"pressureSubmitButton")
        self.pressureSubmitButton.setGeometry(QRect(30, 130, 111, 24))

        self.TempPressureLayout.addWidget(self.PressureLayoutBox)


        self.BottomHalfLayout.addLayout(self.TempPressureLayout)


        self.MainLayout.addLayout(self.BottomHalfLayout)


        self.retranslateUi(TechDemoMainWindow)

        self.tempUnitSelector.setCurrentIndex(-1)
        self.pressureUnitSelector.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(TechDemoMainWindow)
    # setupUi

    def retranslateUi(self, TechDemoMainWindow):
        TechDemoMainWindow.setWindowTitle(QCoreApplication.translate("TechDemoMainWindow", u"Dialog", None))
        self.title.setText(QCoreApplication.translate("TechDemoMainWindow", u"Current Temperature", None))
        self.top_thermo.setText(QCoreApplication.translate("TechDemoMainWindow", u"25\u00b0C", None))
        self.middle_thermo.setText(QCoreApplication.translate("TechDemoMainWindow", u"25\u00b0C", None))
        self.bottom_thermo.setText(QCoreApplication.translate("TechDemoMainWindow", u"25\u00b0C", None))
        self.label_4.setText(QCoreApplication.translate("TechDemoMainWindow", u"Current Pressure", None))
        self.label_3.setText(QCoreApplication.translate("TechDemoMainWindow", u"760.00 Torr", None))
        self.label.setText(QCoreApplication.translate("TechDemoMainWindow", u"Temperature", None))
        self.radioButton_2.setText(QCoreApplication.translate("TechDemoMainWindow", u"Manual", None))
        self.radioButton.setText(QCoreApplication.translate("TechDemoMainWindow", u"Automatic", None))
        self.label_2.setText(QCoreApplication.translate("TechDemoMainWindow", u"Pressure", None))
        self.radioButton_4.setText(QCoreApplication.translate("TechDemoMainWindow", u"Manual", None))
        self.radioButton_3.setText(QCoreApplication.translate("TechDemoMainWindow", u"Automatic", None))
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

