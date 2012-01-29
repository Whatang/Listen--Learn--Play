'''
Created on 28 Jan 2012

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QThread
from ui_midiLearnDialog import Ui_midiLearnDialog

class MidiLearner(QThread):
    def __init__(self, midiDevice):
        super(MidiLearner, self).__init__()
        self._midiDevice = midiDevice
        self.midiData = None
        self.running = False

    def run(self):
        self.running = True
        while self._midiDevice.poll():
            self._midiDevice.read(1)
        while self.running:
            self.msleep(10)
            if self._midiDevice.poll():
                self.midiData = self._midiDevice.read(1)[0][0]
                return


class MidiLearnDialog(QDialog, Ui_midiLearnDialog):
    def __init__(self, midiDevice, parent = None):
        super(MidiLearnDialog, self).__init__(parent)
        self.setupUi(self)
        self.thread = MidiLearner(midiDevice)

    def exec_(self):
        self.thread.finished.connect(self.accept)
        self.thread.start()
        return super(MidiLearnDialog, self).exec_()

    def reject(self):
        self.thread.running = False
        super(MidiLearnDialog, self).reject()

    def getMidiData(self):
        return self.thread.midiData
