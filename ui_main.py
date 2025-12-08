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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

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
        self.verticalLayoutWidget_2.setGeometry(QRect(900, 10, 251, 229))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.openButton = QPushButton(self.verticalLayoutWidget_2)
        self.openButton.setObjectName(u"openButton")

        self.verticalLayout_2.addWidget(self.openButton)

        self.fileLabel = QLabel(self.verticalLayoutWidget_2)
        self.fileLabel.setObjectName(u"fileLabel")

        self.verticalLayout_2.addWidget(self.fileLabel)

        self.xAxisLabel = QLabel(self.verticalLayoutWidget_2)
        self.xAxisLabel.setObjectName(u"xAxisLabel")

        self.verticalLayout_2.addWidget(self.xAxisLabel)

        self.xAxisLine = QLineEdit(self.verticalLayoutWidget_2)
        self.xAxisLine.setObjectName(u"xAxisLine")

        self.verticalLayout_2.addWidget(self.xAxisLine)

        self.yAxisLabel = QLabel(self.verticalLayoutWidget_2)
        self.yAxisLabel.setObjectName(u"yAxisLabel")

        self.verticalLayout_2.addWidget(self.yAxisLabel)

        self.yAxisLine = QLineEdit(self.verticalLayoutWidget_2)
        self.yAxisLine.setObjectName(u"yAxisLine")

        self.verticalLayout_2.addWidget(self.yAxisLine)

        self.titleLabel = QLabel(self.verticalLayoutWidget_2)
        self.titleLabel.setObjectName(u"titleLabel")

        self.verticalLayout_2.addWidget(self.titleLabel)

        self.titleLine = QLineEdit(self.verticalLayoutWidget_2)
        self.titleLine.setObjectName(u"titleLine")

        self.verticalLayout_2.addWidget(self.titleLine)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(640, 10, 251, 51))
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

        self.updateButton = QPushButton(self.centralwidget)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setGeometry(QRect(910, 630, 249, 26))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1162, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"Open File", None))
        self.fileLabel.setText(QCoreApplication.translate("MainWindow", u"No File Loaded", None))
        self.xAxisLabel.setText(QCoreApplication.translate("MainWindow", u"X Axis Label", None))
        self.yAxisLabel.setText(QCoreApplication.translate("MainWindow", u"Y Axis Label", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.baselineLabel.setText(QCoreApplication.translate("MainWindow", u"Baseline Correction", None))
        self.baselineBox.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.baselineBox.setItemText(1, QCoreApplication.translate("MainWindow", u"airPLS", None))
        self.baselineBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Rubber Band", None))
        self.baselineBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Polynomial", None))
        self.baselineBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Piecewise Spline", None))
        self.baselineBox.setItemText(5, QCoreApplication.translate("MainWindow", u"Savitzky\u2013Golay", None))

        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"Update", None))
    # retranslateUi

