'''
Created on 27 Jan 2012

@author: Mike Thomas

'''
from PyQt4.QtGui import QDialog, QTableWidgetItem
from PyQt4.QtCore import QVariant, Qt
from pygame import midi
from midiLearnDialog import MidiLearnDialog

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
    '''
    classdocs
    '''


    def __init__(self, controls, parent = None):
        '''
        Constructor
        '''
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
        def addItem(r, c, text):
            item = QTableWidgetItem(text)
            item.setData(ACTION_ROLE, QVariant(r))
            self._settingsTable.setItem(r, c, item)
        for row, action in enumerate(controls.iterActions()):
            addItem(row, 0, controls.getDescription(action))
            addItem(row, 1, controls.getShortcut(action).toString())
            addItem(row, 2, controls.getMidiAsString(action))
        self._settingsTable.setSortingEnabled(True)
        self._refreshButton.clicked.connect(self._populateMidiInputs)
        self._inputSelector.currentIndexChanged.connect(self._selectNewMidi)
        self._midiOnBox.toggled.connect(self._midiOnToggled)
        self._settingsTable.itemDoubleClicked.connect(self._itemDoubleClicked)

    def _populateMidiInputs(self):
        self._inputSelector.blockSignals(True)
        self._inputSelector.clear()
        if self._midiOnBox.isChecked():
            self._inputSelector.addItem("No device selected",
                                        userData = QVariant(-1))
            for j, (i, info) in enumerate(getInputDevices()):
                self._inputSelector.addItem(info, userData = QVariant(i))
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
        deviceId = self._inputSelector.itemData(index, role = Qt.UserRole)
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
            # Set MIDI
            dlg = MidiLearnDialog(self._midiInput, self)
            if dlg.exec_():
                midiData = dlg.getMidiData()
                self._newMidi[action] = midiData
                item.setText(self._controls.midiToString(action, midiData))
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
