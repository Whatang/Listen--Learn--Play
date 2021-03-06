"""
Created on 27 Jan 2012

@author: Mike Thomas

"""
from PyQt4.QtGui import QDialog, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt4.QtCore import QVariant, Qt
from pygame import midi
from midiLearnDialog import MidiLearnDialog
from midiLearnPairedDialog import MidiLearnPairedDialog

ACTION_ROLE = Qt.UserRole + 1


def getInputDevices():
    for i in xrange(midi.get_count()):
        info = midi.get_device_info(i)
        (unusedInterface, name, isInput,
         unusedIsOutput, unusedOpened) = info
        if isInput:
            yield i, name

from ui_editControlsDialog import Ui_EditControlsDialog


class EditControlsDialog(QDialog, Ui_EditControlsDialog):
    """
    classdocs
    """

    def __init__(self, controls, parent=None):
        """
        Constructor
        """
        super(EditControlsDialog, self).__init__(parent)
        self.setupUi(self)
        self._controls = controls
        self._newMidi = dict((action, controls.getMidi(action))
                             for action in controls.iterActions()
                             if controls.getMidi(action))
        midiOn = controls.midiDevice != -1
        self._midiOnBox.setChecked(midiOn)
        self._inputSelector.setEnabled(midiOn)
        self._inputLabel.setEnabled(midiOn)
        self._refreshButton.setEnabled(midiOn)
        self._midiInput = -1
        self._lastMidi = -1
        self._originalMidi = -1
        if self._controls.midiDevice != -1:
            self._originalMidi = self._controls.midiDevice
            self._controls.closeMidiDevice()
            self._openNewMidi(self._originalMidi)
        self._populateMidiInputs()
        self._settingsTable.setSortingEnabled(False)
        self._settingsTable.setRowCount(len(controls))

        def addItem(r, c, text, tip=None):
            item = QTableWidgetItem(text)
            if tip:
                item.setToolTip(tip)
            item.setData(ACTION_ROLE, QVariant(r))
            self._settingsTable.setItem(r, c, item)
        for row, action in enumerate(controls.iterActions()):
            addItem(row, 0, controls.getDescription(action))
            addItem(row, 1, controls.getShortcutString(action))
            addItem(row, 2, controls.getMidiAsString(action),
                    "Double click to edit assigned MIDI control")
        self._settingsTable.setSortingEnabled(True)
        self._refreshButton.clicked.connect(self._populateMidiInputs)
        self._inputSelector.currentIndexChanged.connect(self._selectNewMidi)
        self._midiOnBox.toggled.connect(self._midiOnToggled)
        self._settingsTable.itemDoubleClicked.connect(self._itemDoubleClicked)
        self.fileBox.button(self.fileBox.Save).clicked.connect(self._save)
        self.fileBox.button(self.fileBox.Open).clicked.connect(self._load)

    def _populateMidiInputs(self):
        self._inputSelector.blockSignals(True)
        self._inputSelector.clear()
        if self._midiOnBox.isChecked():
            self._inputSelector.addItem("No device selected",
                                        userData=QVariant(-1))
            for j, (i, info) in enumerate(getInputDevices()):
                self._inputSelector.addItem(info, userData=QVariant(i))
                if i == self._lastMidi:
                    self._inputSelector.setCurrentIndex(j + 1)
        else:
            self._inputSelector.addItem("---")
        self._inputSelector.blockSignals(False)

    def _midiOnToggled(self, onOff):
        if not onOff:
            self._midiInput = -1
        self._populateMidiInputs()

    def _selectNewMidi(self, index):
        deviceId = self._inputSelector.itemData(index, role=Qt.UserRole)
        deviceId = deviceId.toInt()[0]
        self._openNewMidi(deviceId)
        if deviceId == -1:
            self._midiOnBox.setChecked(False)

    def _openNewMidi(self, deviceId):
        self._midiInput = deviceId
        self._lastMidi = deviceId

    def _itemDoubleClicked(self, item):
        column = item.column()
        if ((column == 0)
            or (column == 1)
                or (column == 2 and self._midiInput == -1)):
            return
        actionIndex = item.data(ACTION_ROLE).toInt()[0]
        action = self._controls[actionIndex]
        if column == 2:
            # Learn MIDI
            if action.numActions() == 1:
                dlg = MidiLearnDialog(self._midiInput, self)
            else:
                dlg = MidiLearnPairedDialog(self._midiInput, self)
            if dlg.exec_():
                midiData = dlg.getMidiData()
                if midiData is None:
                    self._newMidi[action] = None
                    item.setText("")
                elif self._controls.isValidMidi(action, midiData):
                    midiData = action.unparametrise(midiData)
                    self._newMidi[action] = midiData
                    item.setText(midiData.unparamString())
                else:
                    QMessageBox.warning(self, "Bad MIDI",
                                        "The given MIDI message is invalid "
                                        "for this operation.")

    def closeEvent(self, unusedEvent):
        self.reject()

    def accept(self):
        for action in self._controls.iterActions():
            self._controls.setMidi(action, self._newMidi.get(action, None))
        if self._midiOnBox.isChecked() and self._midiInput != -1:
            self._controls.openMidiDevice(self._midiInput)
        super(EditControlsDialog, self).accept()

    def reject(self):
        if self._originalMidi != -1:
            self._controls.openMidiDevice(self._originalMidi)
        super(EditControlsDialog, self).reject()

    def _save(self):
        caption = "Save settings file"
        directory = ""
        fname = QFileDialog.getSaveFileName(parent=self,
                                            caption=caption,
                                            directory=directory,
                                            filter="Settings files (*.llp)")
        if not fname:
            return
        fname = str(fname)
        with open(fname, 'wb') as handle:
            self._controls.save(handle, self._newMidi)

    def _load(self):
        caption = "Open settings file"
        directory = ""
        fname = QFileDialog.getOpenFileName(parent=self,
                                            caption=caption,
                                            directory=directory,
                                            filter="Settings files (*.llp)")
        if not fname:
            return
        fname = str(fname)
        with open(fname) as handle:
            newMidi = self._controls.load(handle)
        self._settingsTable.setSortingEnabled(False)
        for row in xrange(self._settingsTable.rowCount()):
            item = self._settingsTable.item(row, 2)
            actionNum = item.data(ACTION_ROLE).toInt()[0]
            action = self._controls[actionNum]
            midiData = newMidi[action]
            self._newMidi[action] = midiData
            if midiData is None:
                item.setText("")
            else:
                midiData = action.unparametrise(midiData)
                item.setText(midiData.unparamString())
