# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\LLP\src\llp.ui'
#
# Created: Thu Jan 26 13:44:38 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(450, 97)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.openButton = QtGui.QPushButton(self.centralwidget)
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.horizontalLayout_2.addWidget(self.openButton)
        self.seekSlider = phonon.Phonon.SeekSlider(self.centralwidget)
        self.seekSlider.setIconVisible(False)
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))
        self.horizontalLayout_2.addWidget(self.seekSlider)
        self.positionIndicator = QtGui.QLabel(self.centralwidget)
        self.positionIndicator.setObjectName(_fromUtf8("positionIndicator"))
        self.horizontalLayout_2.addWidget(self.positionIndicator)
        self.dividerLabel = QtGui.QLabel(self.centralwidget)
        self.dividerLabel.setObjectName(_fromUtf8("dividerLabel"))
        self.horizontalLayout_2.addWidget(self.dividerLabel)
        self.totalLabel = QtGui.QLabel(self.centralwidget)
        self.totalLabel.setObjectName(_fromUtf8("totalLabel"))
        self.horizontalLayout_2.addWidget(self.totalLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout.addWidget(self.startButton)
        self.rewindButton = QtGui.QPushButton(self.centralwidget)
        self.rewindButton.setObjectName(_fromUtf8("rewindButton"))
        self.horizontalLayout.addWidget(self.rewindButton)
        self.playButton = QtGui.QPushButton(self.centralwidget)
        self.playButton.setObjectName(_fromUtf8("playButton"))
        self.horizontalLayout.addWidget(self.playButton)
        self.forwardButton = QtGui.QPushButton(self.centralwidget)
        self.forwardButton.setObjectName(_fromUtf8("forwardButton"))
        self.horizontalLayout.addWidget(self.forwardButton)
        self.endButton = QtGui.QPushButton(self.centralwidget)
        self.endButton.setObjectName(_fromUtf8("endButton"))
        self.horizontalLayout.addWidget(self.endButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.volumeSlider = phonon.Phonon.VolumeSlider(self.centralwidget)
        self.volumeSlider.setOrientation(QtCore.Qt.Vertical)
        self.volumeSlider.setMuteVisible(True)
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        self.horizontalLayout_3.addWidget(self.volumeSlider)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 450, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.openButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.actionOpen.trigger)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Listen, Learn, Play", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.positionIndicator.setText(QtGui.QApplication.translate("MainWindow", "--", None, QtGui.QApplication.UnicodeUTF8))
        self.dividerLabel.setText(QtGui.QApplication.translate("MainWindow", "/", None, QtGui.QApplication.UnicodeUTF8))
        self.totalLabel.setText(QtGui.QApplication.translate("MainWindow", "--", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.rewindButton.setText(QtGui.QApplication.translate("MainWindow", "Rewind", None, QtGui.QApplication.UnicodeUTF8))
        self.playButton.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.forwardButton.setText(QtGui.QApplication.translate("MainWindow", "Fast Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.endButton.setText(QtGui.QApplication.translate("MainWindow", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import phonon
