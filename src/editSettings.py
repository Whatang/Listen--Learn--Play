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

from ui_midiSettingsDialog import Ui_MidiSettingsDialog

class EditSettings(QDialog, Ui_MidiSettingsDialog):
    '''
    classdocs
    '''


    def __init__(self, settings, parent = None):
        '''
        Constructor
        '''
        super(EditSettings, self).__init__(parent)
        self.setupUi(self)
        self._settings = settings
        self._newMidi = dict((action, settings.getMidi(action))
                             for action in settings.iterActions()
                             if settings.getMidi(action))
        midiOn = settings.midiDevice != -1
        self._midiOnBox.setChecked(midiOn)
        self._inputSelector.setEnabled(midiOn)
        self._inputLabel.setEnabled(midiOn)
        self._refreshButton.setEnabled(midiOn)
        self._midiInput = None
        self._lastMidi = -1
        self._originalMidi = -1
        if self._settings.midiDevice != -1:
            self._originalMidi = self._settings.midiDevice
            self._settings.closeMidiDevice()
            self._openNewMidi(self._originalMidi)
        self._populateMidiInputs()
        self._settingsTable.setSortingEnabled(False)
        self._settingsTable.setRowCount(len(settings))
        def addItem(r, c, text):
            item = QTableWidgetItem(text)
            item.setData(ACTION_ROLE, QVariant(r))
            self._settingsTable.setItem(r, c, item)
        for row, action in enumerate(settings.iterActions()):
            addItem(row, 0, settings.getDescription(action))
            addItem(row, 1, settings.getShortcut(action).toString())
            addItem(row, 2, settings.getMidiAsString(action))
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
            del self._midiInput
            self._midiInput = None
        self._populateMidiInputs()

    def _selectNewMidi(self, index):
        device_id = self._inputSelector.itemData(index, role = Qt.UserRole)
        device_id = device_id.toInt()[0]
        self._openNewMidi(device_id)
        if device_id == -1:
            self._midiOnBox.setChecked(False)

    def _openNewMidi(self, device_id):
        del self._midiInput
        if device_id == -1:
            self._midiInput = None
        else:
            self._midiInput = midi.Input(device_id, 0)
        self._lastMidi = device_id

    def _itemDoubleClicked(self, item):
        column = item.column()
        if ((column == 0)
            or (column == 1)
            or (column == 2 and self._midiInput == None)):
            return
        actionIndex = item.data(ACTION_ROLE).toInt()[0]
        action = self._settings[actionIndex]
        if column == 2:
            # Set MIDI
            dlg = MidiLearnDialog(self._midiInput, self)
            if dlg.exec_():
                midiData = dlg.getMidiData()
                self._newMidi[action] = midiData
                item.setText(self._settings.midiToString(action, midiData))
    def closeEvent(self, unusedEvent):
        self.reject()

    def accept(self):
        del self._midiInput
        for action in self._settings.iterActions():
            self._settings.setMidi(action, self._newMidi.get(action, None))
        if self._midiOnBox.isChecked() and self._lastMidi != -1:
            self._settings.openMidiDevice(self._lastMidi)
        super(EditSettings, self).accept()

    def reject(self):
        del self._midiInput
        if self._originalMidi != -1:
            self._settings.openMidiDevice(self._originalMidi)
        super(EditSettings, self).reject()
