"""
Created on 28 Jan 2012

@author: Mike Thomas

"""

from PyQt4.QtGui import QDialog
from ui_midiLearnDialog import Ui_midiLearnDialog

from midiMessages import MidiControlThread


class MidiLearnDialog(QDialog, Ui_midiLearnDialog):
    def __init__(self, deviceId, parent=None):
        super(MidiLearnDialog, self).__init__(parent)
        self.setupUi(self)
        self.thread = MidiControlThread(deviceId)
        self._midiData = None
        self.buttonBox.clicked.connect(self._buttonClicked)

    def exec_(self):
        self.thread.midiReceived.connect(self._midiReceived)
        self.thread.start()
        return super(MidiLearnDialog, self).exec_()

    def reject(self):
        self.thread.close()
        self.thread.wait()
        super(MidiLearnDialog, self).reject()

    def accept(self):
        self.thread.close()
        self.thread.wait()
        super(MidiLearnDialog, self).accept()

    def _midiReceived(self, midiMsg):
        self._midiData = midiMsg
        self.accept()

    def getMidiData(self):
        return self._midiData

    def _buttonClicked(self, button):
        if button == self.buttonBox.button(self.buttonBox.Discard):
            self._midiData = None
            self.accept()
