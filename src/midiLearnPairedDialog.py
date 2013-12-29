"""
Created on 29 Jan 2012

@author: Mike Thomas

"""

from PyQt4.QtGui import QDialog
from ui_midiLearnPaired import Ui_MidiLearnPairedDialog
from midiMessages import MidiControlThread
from controlSet import PairedMidi

class MidiLearnPairedDialog(QDialog, Ui_MidiLearnPairedDialog):
    """
    classdocs
    """


    def __init__(self, midiDeviceId, parent = None):
        """
        Constructor
        """
        super(MidiLearnPairedDialog, self).__init__(parent)
        self.setupUi(self)
        self.secondMidiBox.setDisabled(True)
        self.thread = MidiControlThread(midiDeviceId)
        self._midiData = []
        self.buttonBox.clicked.connect(self._buttonClicked)

    def exec_(self):
        self.thread.midiReceived.connect(self._midiReceived)
        self.thread.start()
        return super(MidiLearnPairedDialog, self).exec_()

    def reject(self):
        self.thread.close()
        self.thread.wait()
        super(MidiLearnPairedDialog, self).reject()

    def accept(self):
        self.thread.close()
        self.thread.wait()
        super(MidiLearnPairedDialog, self).accept()

    def _midiReceived(self, midiMsg):
        self._midiData.append(midiMsg)
        if len(self._midiData) == 1:
            self.firstMidiBox.setChecked(True)
            self.firstMidiBox.setEnabled(False)
            self.secondMidiBox.setEnabled(True)
        else:
            self.secondMidiBox.setChecked(True)
            self.secondMidiBox.setEnabled(False)
            self._midiData = PairedMidi(*self._midiData)
            self.accept()

    def getMidiData(self):
        return self._midiData

    def _buttonClicked(self, button):
        if button == self.buttonBox.button(self.buttonBox.Discard):
            self._midiData = None
            self.accept()
