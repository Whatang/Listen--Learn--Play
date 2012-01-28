'''
Created on 27 Jan 2012

@author: Mike Thomas

'''
from PyQt4.QtGui import QDialog, QTableWidgetItem
from PyQt4.QtCore import QVariant, Qt
from pygame import midi

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
        self._midiOnBox.setChecked(settings.midiOn)
        self._inputSelector.setEnabled(settings.midiOn)
        for i, info in getInputDevices():
            self._inputSelector.addItem(info, userData = QVariant(i))
        self._settingsTable.setSortingEnabled(False)
        self._settingsTable.setRowCount(len(settings))
        def addItem(r, c, text):
            item = QTableWidgetItem(text)
            item.setData(ACTION_ROLE, QVariant(r))
            self._settingsTable.setItem(r, c, item)
        for row, action in enumerate(settings.iterActions()):
            addItem(row, 0, settings.getDescription(action))
            addItem(row, 1, settings.getShortcut(action).toString())
            addItem(row, 2, settings.getMidi(action))
        self._settingsTable.setSortingEnabled(True)
