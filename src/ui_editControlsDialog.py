# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Mike_2\Eclipse workspace\LLP\src\editControlsDialog.ui'
#
# Created: Sun Jan 29 16:55:39 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EditControlsDialog(object):
    def setupUi(self, EditControlsDialog):
        EditControlsDialog.setObjectName(_fromUtf8("EditControlsDialog"))
        EditControlsDialog.resize(441, 300)
        self.verticalLayout = QtGui.QVBoxLayout(EditControlsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self._midiOnBox = QtGui.QCheckBox(EditControlsDialog)
        self._midiOnBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self._midiOnBox.setObjectName(_fromUtf8("_midiOnBox"))
        self.horizontalLayout.addWidget(self._midiOnBox)
        self._inputLabel = QtGui.QLabel(EditControlsDialog)
        self._inputLabel.setObjectName(_fromUtf8("_inputLabel"))
        self.horizontalLayout.addWidget(self._inputLabel)
        self._inputSelector = QtGui.QComboBox(EditControlsDialog)
        self._inputSelector.setMinimumSize(QtCore.QSize(200, 0))
        self._inputSelector.setObjectName(_fromUtf8("_inputSelector"))
        self.horizontalLayout.addWidget(self._inputSelector)
        self._refreshButton = QtGui.QPushButton(EditControlsDialog)
        self._refreshButton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Images/Refresh")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._refreshButton.setIcon(icon)
        self._refreshButton.setObjectName(_fromUtf8("_refreshButton"))
        self.horizontalLayout.addWidget(self._refreshButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self._settingsTable = QtGui.QTableWidget(EditControlsDialog)
        self._settingsTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self._settingsTable.setTabKeyNavigation(False)
        self._settingsTable.setProperty(_fromUtf8("showDropIndicator"), False)
        self._settingsTable.setDragDropOverwriteMode(False)
        self._settingsTable.setAlternatingRowColors(True)
        self._settingsTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self._settingsTable.setTextElideMode(QtCore.Qt.ElideNone)
        self._settingsTable.setShowGrid(False)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.fileBox = QtGui.QDialogButtonBox(EditControlsDialog)
        self.fileBox.setStandardButtons(QtGui.QDialogButtonBox.Open|QtGui.QDialogButtonBox.Save)
        self.fileBox.setObjectName(_fromUtf8("fileBox"))
        self.horizontalLayout_2.addWidget(self.fileBox)
        self.buttonBox = QtGui.QDialogButtonBox(EditControlsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self._inputLabel.setBuddy(self._inputSelector)

        self.retranslateUi(EditControlsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EditControlsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EditControlsDialog.reject)
        QtCore.QObject.connect(self._midiOnBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self._inputSelector.setEnabled)
        QtCore.QObject.connect(self._midiOnBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self._refreshButton.setEnabled)
        QtCore.QObject.connect(self._midiOnBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self._inputLabel.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(EditControlsDialog)

    def retranslateUi(self, EditControlsDialog):
        EditControlsDialog.setWindowTitle(QtGui.QApplication.translate("EditControlsDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self._midiOnBox.setToolTip(QtGui.QApplication.translate("EditControlsDialog", "Use MIDI input to control LLP", None, QtGui.QApplication.UnicodeUTF8))
        self._midiOnBox.setText(QtGui.QApplication.translate("EditControlsDialog", "Enable MIDI control", None, QtGui.QApplication.UnicodeUTF8))
        self._inputLabel.setText(QtGui.QApplication.translate("EditControlsDialog", "MIDI Input", None, QtGui.QApplication.UnicodeUTF8))
        self._inputSelector.setToolTip(QtGui.QApplication.translate("EditControlsDialog", "Select a MIDI input device", None, QtGui.QApplication.UnicodeUTF8))
        self._refreshButton.setToolTip(QtGui.QApplication.translate("EditControlsDialog", "Refresh the list of MIDI inputs", None, QtGui.QApplication.UnicodeUTF8))
        self._settingsTable.setSortingEnabled(True)
        self._settingsTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("EditControlsDialog", "Operation", None, QtGui.QApplication.UnicodeUTF8))
        self._settingsTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("EditControlsDialog", "Shortcut", None, QtGui.QApplication.UnicodeUTF8))
        self._settingsTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("EditControlsDialog", "MIDI Setting", None, QtGui.QApplication.UnicodeUTF8))

import llp_rc
