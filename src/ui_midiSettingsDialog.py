# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\LLP\src\midiSettingsDialog.ui'
#
# Created: Sat Jan 28 11:13:20 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MidiSettingsDialog(object):
    def setupUi(self, MidiSettingsDialog):
        MidiSettingsDialog.setObjectName(_fromUtf8("MidiSettingsDialog"))
        MidiSettingsDialog.resize(477, 300)
        self.verticalLayout = QtGui.QVBoxLayout(MidiSettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self._midiOnBox = QtGui.QCheckBox(MidiSettingsDialog)
        self._midiOnBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self._midiOnBox.setObjectName(_fromUtf8("_midiOnBox"))
        self.horizontalLayout.addWidget(self._midiOnBox)
        self.label = QtGui.QLabel(MidiSettingsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self._inputSelector = QtGui.QComboBox(MidiSettingsDialog)
        self._inputSelector.setMinimumSize(QtCore.QSize(200, 0))
        self._inputSelector.setObjectName(_fromUtf8("_inputSelector"))
        self.horizontalLayout.addWidget(self._inputSelector)
        self.refreshButton = QtGui.QPushButton(MidiSettingsDialog)
        self.refreshButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/Refresh")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon)
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        self.horizontalLayout.addWidget(self.refreshButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self._settingsTable = QtGui.QTableWidget(MidiSettingsDialog)
        self._settingsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._settingsTable.setTabKeyNavigation(False)
        self._settingsTable.setProperty(_fromUtf8("showDropIndicator"), False)
        self._settingsTable.setDragDropOverwriteMode(False)
        self._settingsTable.setAlternatingRowColors(True)
        self._settingsTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._settingsTable.setGridStyle(QtCore.Qt.NoPen)
        self._settingsTable.setWordWrap(False)
        self._settingsTable.setCornerButtonEnabled(False)
        self._settingsTable.setObjectName(_fromUtf8("_settingsTable"))
        self._settingsTable.setColumnCount(3)
        self._settingsTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self._settingsTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self._settingsTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self._settingsTable.setHorizontalHeaderItem(2, item)
        self._settingsTable.horizontalHeader().setMinimumSectionSize(50)
        self._settingsTable.horizontalHeader().setSortIndicatorShown(True)
        self._settingsTable.horizontalHeader().setStretchLastSection(True)
        self._settingsTable.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self._settingsTable)
        self.buttonBox = QtGui.QDialogButtonBox(MidiSettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Open|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self._inputSelector)

        self.retranslateUi(MidiSettingsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MidiSettingsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MidiSettingsDialog.reject)
        QtCore.QObject.connect(self._midiOnBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self._inputSelector.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MidiSettingsDialog)

    def retranslateUi(self, MidiSettingsDialog):
        MidiSettingsDialog.setWindowTitle(QtGui.QApplication.translate("MidiSettingsDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self._midiOnBox.setToolTip(QtGui.QApplication.translate("MidiSettingsDialog", "Use MIDI input to control LLP", None, QtGui.QApplication.UnicodeUTF8))
        self._midiOnBox.setText(QtGui.QApplication.translate("MidiSettingsDialog", "Enable MIDI control", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MidiSettingsDialog", "MIDI Input", None, QtGui.QApplication.UnicodeUTF8))
        self._inputSelector.setToolTip(QtGui.QApplication.translate("MidiSettingsDialog", "Select a MIDI input device", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setToolTip(QtGui.QApplication.translate("MidiSettingsDialog", "Refresh the list of MIDI inputs", None, QtGui.QApplication.UnicodeUTF8))
        self._settingsTable.setSortingEnabled(True)
        self._settingsTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MidiSettingsDialog", "Operation", None, QtGui.QApplication.UnicodeUTF8))
        self._settingsTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MidiSettingsDialog", "Shortcut", None, QtGui.QApplication.UnicodeUTF8))
        self._settingsTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MidiSettingsDialog", "MIDI Setting", None, QtGui.QApplication.UnicodeUTF8))

import llp_rc
