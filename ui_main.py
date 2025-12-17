# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFormLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1162, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(30, 10, 591, 491))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.plotWidget = QWidget(self.verticalLayoutWidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.verticalLayout.addWidget(self.plotWidget)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(910, 570, 231, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.openButton = QPushButton(self.verticalLayoutWidget_2)
        self.openButton.setObjectName(u"openButton")

        self.verticalLayout_2.addWidget(self.openButton)

        self.fileLabel = QLabel(self.verticalLayoutWidget_2)
        self.fileLabel.setObjectName(u"fileLabel")

        self.verticalLayout_2.addWidget(self.fileLabel)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(640, 10, 261, 171))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.baselineLabel = QLabel(self.verticalLayoutWidget_3)
        self.baselineLabel.setObjectName(u"baselineLabel")

        self.verticalLayout_3.addWidget(self.baselineLabel)

        self.baselineBox = QComboBox(self.verticalLayoutWidget_3)
        self.baselineBox.addItem("")
        self.baselineBox.addItem("")
        self.baselineBox.addItem("")
        self.baselineBox.addItem("")
        self.baselineBox.addItem("")
        self.baselineBox.addItem("")
        self.baselineBox.setObjectName(u"baselineBox")

        self.verticalLayout_3.addWidget(self.baselineBox)

        self.tabWidget = QTabWidget(self.verticalLayoutWidget_3)
        self.tabWidget.setObjectName(u"tabWidget")
        self.baselineAirTab = QWidget()
        self.baselineAirTab.setObjectName(u"baselineAirTab")
        self.formLayoutWidget_5 = QWidget(self.baselineAirTab)
        self.formLayoutWidget_5.setObjectName(u"formLayoutWidget_5")
        self.formLayoutWidget_5.setGeometry(QRect(0, 0, 251, 82))
        self.formLayout_5 = QFormLayout(self.formLayoutWidget_5)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.airLambdaLabel = QLabel(self.formLayoutWidget_5)
        self.airLambdaLabel.setObjectName(u"airLambdaLabel")

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.LabelRole, self.airLambdaLabel)

        self.airPorderLabel = QLabel(self.formLayoutWidget_5)
        self.airPorderLabel.setObjectName(u"airPorderLabel")

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.LabelRole, self.airPorderLabel)

        self.airLambdaSpinBox = QDoubleSpinBox(self.formLayoutWidget_5)
        self.airLambdaSpinBox.setObjectName(u"airLambdaSpinBox")
        self.airLambdaSpinBox.setMinimum(10.000000000000000)
        self.airLambdaSpinBox.setMaximum(100000000.000000000000000)

        self.formLayout_5.setWidget(0, QFormLayout.ItemRole.FieldRole, self.airLambdaSpinBox)

        self.airPorderSlider = QSlider(self.formLayoutWidget_5)
        self.airPorderSlider.setObjectName(u"airPorderSlider")
        self.airPorderSlider.setMinimum(1)
        self.airPorderSlider.setMaximum(3)
        self.airPorderSlider.setOrientation(Qt.Orientation.Horizontal)
        self.airPorderSlider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.airPorderSlider.setTickInterval(1)

        self.formLayout_5.setWidget(1, QFormLayout.ItemRole.FieldRole, self.airPorderSlider)

        self.airItermaxLabel = QLabel(self.formLayoutWidget_5)
        self.airItermaxLabel.setObjectName(u"airItermaxLabel")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.LabelRole, self.airItermaxLabel)

        self.airItermaxSpinBox = QSpinBox(self.formLayoutWidget_5)
        self.airItermaxSpinBox.setObjectName(u"airItermaxSpinBox")

        self.formLayout_5.setWidget(2, QFormLayout.ItemRole.FieldRole, self.airItermaxSpinBox)

        self.tabWidget.addTab(self.baselineAirTab, "")
        self.baselinePolyTab = QWidget()
        self.baselinePolyTab.setObjectName(u"baselinePolyTab")
        self.formLayoutWidget_3 = QWidget(self.baselinePolyTab)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(0, 0, 251, 51))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.polyOrderLabel = QLabel(self.formLayoutWidget_3)
        self.polyOrderLabel.setObjectName(u"polyOrderLabel")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.polyOrderLabel)

        self.polyOrderSlider = QSlider(self.formLayoutWidget_3)
        self.polyOrderSlider.setObjectName(u"polyOrderSlider")
        self.polyOrderSlider.setMinimum(1)
        self.polyOrderSlider.setMaximum(7)
        self.polyOrderSlider.setOrientation(Qt.Orientation.Horizontal)
        self.polyOrderSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.polyOrderSlider.setTickInterval(1)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.polyOrderSlider)

        self.tabWidget.addTab(self.baselinePolyTab, "")
        self.baselinePiecewiseTab = QWidget()
        self.baselinePiecewiseTab.setObjectName(u"baselinePiecewiseTab")
        self.formLayoutWidget_4 = QWidget(self.baselinePiecewiseTab)
        self.formLayoutWidget_4.setObjectName(u"formLayoutWidget_4")
        self.formLayoutWidget_4.setGeometry(QRect(0, 0, 251, 53))
        self.formLayout_4 = QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.piecewiseKnotsLabel = QLabel(self.formLayoutWidget_4)
        self.piecewiseKnotsLabel.setObjectName(u"piecewiseKnotsLabel")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.piecewiseKnotsLabel)

        self.piecewiseKnotsSpinBox = QSpinBox(self.formLayoutWidget_4)
        self.piecewiseKnotsSpinBox.setObjectName(u"piecewiseKnotsSpinBox")
        self.piecewiseKnotsSpinBox.setMinimum(3)
        self.piecewiseKnotsSpinBox.setMaximum(50)
        self.piecewiseKnotsSpinBox.setValue(10)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.piecewiseKnotsSpinBox)

        self.piecewiseDegreeLabel = QLabel(self.formLayoutWidget_4)
        self.piecewiseDegreeLabel.setObjectName(u"piecewiseDegreeLabel")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.piecewiseDegreeLabel)

        self.piecewiseDegreeSlider = QSlider(self.formLayoutWidget_4)
        self.piecewiseDegreeSlider.setObjectName(u"piecewiseDegreeSlider")
        self.piecewiseDegreeSlider.setMinimum(1)
        self.piecewiseDegreeSlider.setMaximum(5)
        self.piecewiseDegreeSlider.setSingleStep(0)
        self.piecewiseDegreeSlider.setOrientation(Qt.Orientation.Horizontal)
        self.piecewiseDegreeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.piecewiseDegreeSlider.setTickInterval(1)

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.piecewiseDegreeSlider)

        self.tabWidget.addTab(self.baselinePiecewiseTab, "")
        self.baselineSavitzkyTab = QWidget()
        self.baselineSavitzkyTab.setObjectName(u"baselineSavitzkyTab")
        self.formLayoutWidget_2 = QWidget(self.baselineSavitzkyTab)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(0, 0, 251, 81))
        self.formLayout = QFormLayout(self.formLayoutWidget_2)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.savitzkyWinLenLabel = QLabel(self.formLayoutWidget_2)
        self.savitzkyWinLenLabel.setObjectName(u"savitzkyWinLenLabel")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.savitzkyWinLenLabel)

        self.savitzkyWinLenSpinBox = QSpinBox(self.formLayoutWidget_2)
        self.savitzkyWinLenSpinBox.setObjectName(u"savitzkyWinLenSpinBox")
        self.savitzkyWinLenSpinBox.setMinimum(5)
        self.savitzkyWinLenSpinBox.setMaximum(301)
        self.savitzkyWinLenSpinBox.setSingleStep(2)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.savitzkyWinLenSpinBox)

        self.savitzkyPolyorderLabel = QLabel(self.formLayoutWidget_2)
        self.savitzkyPolyorderLabel.setObjectName(u"savitzkyPolyorderLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.savitzkyPolyorderLabel)

        self.savitzkyPolyorderSlider = QSlider(self.formLayoutWidget_2)
        self.savitzkyPolyorderSlider.setObjectName(u"savitzkyPolyorderSlider")
        self.savitzkyPolyorderSlider.setMinimum(3)
        self.savitzkyPolyorderSlider.setMaximum(5)
        self.savitzkyPolyorderSlider.setOrientation(Qt.Orientation.Horizontal)
        self.savitzkyPolyorderSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.savitzkyPolyorderSlider.setTickInterval(1)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.savitzkyPolyorderSlider)

        self.tabWidget.addTab(self.baselineSavitzkyTab, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.updateButton = QPushButton(self.centralwidget)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setGeometry(QRect(910, 630, 249, 26))
        self.formLayoutWidget = QWidget(self.centralwidget)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(640, 210, 281, 81))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.xAxisLabel = QLabel(self.formLayoutWidget)
        self.xAxisLabel.setObjectName(u"xAxisLabel")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.xAxisLabel)

        self.xAxisLine = QLineEdit(self.formLayoutWidget)
        self.xAxisLine.setObjectName(u"xAxisLine")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.xAxisLine)

        self.yAxisLabel = QLabel(self.formLayoutWidget)
        self.yAxisLabel.setObjectName(u"yAxisLabel")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.yAxisLabel)

        self.yAxisLine = QLineEdit(self.formLayoutWidget)
        self.yAxisLine.setObjectName(u"yAxisLine")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.yAxisLine)

        self.titleLabel = QLabel(self.formLayoutWidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.LabelRole, self.titleLabel)

        self.titleLine = QLineEdit(self.formLayoutWidget)
        self.titleLine.setObjectName(u"titleLine")

        self.formLayout_3.setWidget(2, QFormLayout.ItemRole.FieldRole, self.titleLine)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1162, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"Open File", None))
        self.fileLabel.setText(QCoreApplication.translate("MainWindow", u"No File Loaded", None))
        self.baselineLabel.setText(QCoreApplication.translate("MainWindow", u"Baseline Correction", None))
        self.baselineBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.baselineBox.setItemText(1, QCoreApplication.translate("MainWindow", u"airPLS", None))
        self.baselineBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Rubber Band", None))
        self.baselineBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Polynomial", None))
        self.baselineBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Piecewise Spline", None))
        self.baselineBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Savitzky\u2013Golay", None))

        self.airLambdaLabel.setText(QCoreApplication.translate("MainWindow", u"Lambda", None))
        self.airPorderLabel.setText(QCoreApplication.translate("MainWindow", u"porder", None))
        self.airItermaxLabel.setText(QCoreApplication.translate("MainWindow", u"itermax", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.baselineAirTab), QCoreApplication.translate("MainWindow", u"airPLS", None))
        self.polyOrderLabel.setText(QCoreApplication.translate("MainWindow", u"Order", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.baselinePolyTab), QCoreApplication.translate("MainWindow", u"Polynomial", None))
        self.piecewiseKnotsLabel.setText(QCoreApplication.translate("MainWindow", u"N_knots", None))
        self.piecewiseDegreeLabel.setText(QCoreApplication.translate("MainWindow", u"Degree", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.baselinePiecewiseTab), QCoreApplication.translate("MainWindow", u"Piecewise", None))
        self.savitzkyWinLenLabel.setText(QCoreApplication.translate("MainWindow", u"Window Length", None))
        self.savitzkyPolyorderLabel.setText(QCoreApplication.translate("MainWindow", u"Polyorder", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.baselineSavitzkyTab), QCoreApplication.translate("MainWindow", u"Savitzky-Golay", None))
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.xAxisLabel.setText(QCoreApplication.translate("MainWindow", u"X Axis Label", None))
        self.yAxisLabel.setText(QCoreApplication.translate("MainWindow", u"Y Axis Label", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Title", None))
    # retranslateUi

