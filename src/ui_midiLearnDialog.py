# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\LLP\src\midiLearnDialog.ui'
#
# Created: Sun Jan 29 18:23:46 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_midiLearnDialog(object):
    def setupUi(self, midiLearnDialog):
        midiLearnDialog.setObjectName(_fromUtf8("midiLearnDialog"))
        midiLearnDialog.resize(202, 81)
        self.verticalLayout = QtGui.QVBoxLayout(midiLearnDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(midiLearnDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.discardMessage = QtGui.QLabel(midiLearnDialog)
        self.discardMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.discardMessage.setObjectName(_fromUtf8("discardMessage"))
        self.verticalLayout.addWidget(self.discardMessage)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(midiLearnDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Discard)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(midiLearnDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), midiLearnDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), midiLearnDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(midiLearnDialog)

    def retranslateUi(self, midiLearnDialog):
        midiLearnDialog.setWindowTitle(QtGui.QApplication.translate("midiLearnDialog", "MIDI Learn", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("midiLearnDialog", "Send a MIDI input now", None, QtGui.QApplication.UnicodeUTF8))
        self.discardMessage.setText(QtGui.QApplication.translate("midiLearnDialog", "or press Discard to clear MIDI data", None, QtGui.QApplication.UnicodeUTF8))

