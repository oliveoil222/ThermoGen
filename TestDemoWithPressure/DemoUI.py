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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QPushButton, QSizePolicy,
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
        font = QFont()
        font.setKerning(False)
        font.setHintingPreference(QFont.PreferDefaultHinting)
        self.TempLayoutBox.setFont(font)
        self.TempLayoutBox.setStyleSheet(u"QGroupBox#TempLayoutBox {border:0;}")
        self.TempLayoutBox.setFlat(False)
        self.tempTextLabel = QLabel(self.TempLayoutBox)
        self.tempTextLabel.setObjectName(u"tempTextLabel")
        self.tempTextLabel.setGeometry(QRect(0, 9, 171, 31))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setKerning(True)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.tempTextLabel.setFont(font1)
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
        font2 = QFont()
        font2.setPointSize(16)
        self.pressureTextLabel.setFont(font2)
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
        self.autoToggleBox.setText(QCoreApplication.translate("TechDemoMainWindow", u"Automatic", None))
        self.manualToggleBox.setText(QCoreApplication.translate("TechDemoMainWindow", u"Manual", None))
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

