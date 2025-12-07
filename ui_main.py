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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1010, 581)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(30, 10, 691, 491))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.plotWidget = QWidget(self.verticalLayoutWidget)
        self.plotWidget.setObjectName(u"plotWidget")

        self.verticalLayout.addWidget(self.plotWidget)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(750, 20, 251, 340))
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

        self.updateButton = QPushButton(self.verticalLayoutWidget_2)
        self.updateButton.setObjectName(u"updateButton")

        self.verticalLayout_2.addWidget(self.updateButton)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1010, 33))
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
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"Update", None))
    # retranslateUi

