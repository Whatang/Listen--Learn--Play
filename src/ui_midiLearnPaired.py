# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\LLP\src\midiLearnPaired.ui'
#
# Created: Sun Jan 29 18:15:57 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MidiLearnPairedDialog(object):
    def setupUi(self, MidiLearnPairedDialog):
        MidiLearnPairedDialog.setObjectName(_fromUtf8("MidiLearnPairedDialog"))
        MidiLearnPairedDialog.resize(202, 110)
        self.verticalLayout = QtGui.QVBoxLayout(MidiLearnPairedDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 2, 1)
        self.firstMidiBox = QtGui.QCheckBox(MidiLearnPairedDialog)
        self.firstMidiBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.firstMidiBox.setCheckable(True)
        self.firstMidiBox.setObjectName(_fromUtf8("firstMidiBox"))
        self.gridLayout.addWidget(self.firstMidiBox, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 2, 1)
        self.secondMidiBox = QtGui.QCheckBox(MidiLearnPairedDialog)
        self.secondMidiBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.secondMidiBox.setCheckable(True)
        self.secondMidiBox.setChecked(False)
        self.secondMidiBox.setObjectName(_fromUtf8("secondMidiBox"))
        self.gridLayout.addWidget(self.secondMidiBox, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label = QtGui.QLabel(MidiLearnPairedDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.buttonBox = QtGui.QDialogButtonBox(MidiLearnPairedDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Discard)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MidiLearnPairedDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MidiLearnPairedDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MidiLearnPairedDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MidiLearnPairedDialog)

    def retranslateUi(self, MidiLearnPairedDialog):
        MidiLearnPairedDialog.setWindowTitle(QtGui.QApplication.translate("MidiLearnPairedDialog", "MIDI Learn", None, QtGui.QApplication.UnicodeUTF8))
        self.firstMidiBox.setText(QtGui.QApplication.translate("MidiLearnPairedDialog", "Send MIDI on data", None, QtGui.QApplication.UnicodeUTF8))
        self.secondMidiBox.setText(QtGui.QApplication.translate("MidiLearnPairedDialog", "Send MIDI off data", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MidiLearnPairedDialog", "or press Discard to clear MIDI data", None, QtGui.QApplication.UnicodeUTF8))

