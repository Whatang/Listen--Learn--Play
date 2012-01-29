'''
Created on 27 Jan 2012

@author: Mike Thomas

'''


NORMAL = 0
SET_PARAMETER = 1

from pygame import midi
from PyQt4.QtCore import QThread, pyqtSignal

class MidiControlThread(QThread):
    def __init__(self, deviceId):
        self._deviceId = deviceId
        self._running = False
        super(MidiControlThread, self).__init__()

    midiMessage = pyqtSignal(list)

    def run(self):
        self._running = True
        midiIn = midi.Input(self._deviceId, 0)
        while self._running:
            self.msleep(10)
            while midiIn.poll():
                midiData = midiIn.read(1)[0][0]
                print ["%02x" % x for x in midiData]
                self.midiMessage.emit(midiData)
        del midiIn

    def close(self):
        self._running = False


class ControlSettings(object):
    '''
    classdocs
    '''


    def __init__(self, midiDevice = -1):
        '''
        Constructor
        '''
        self.midiDevice = midiDevice
        self._midiThread = None
        self._actions = []
        self._descriptions = {}
        self._midi = {}
        self._actionTypes = {}

    def addAction(self, action, description, actionType = NORMAL):
        if action not in self._actions:
            self._actions.append(action)
            self._descriptions[action] = description
            self._actionTypes[action] = actionType

    def __getitem__(self, index):
        return self._actions[index]

    def __len__(self):
        return len(self._actions)

    def iterActions(self):
        return iter(self._actions)

    def getDescription(self, action):
        return self._descriptions.get(action, "")

    def getShortcut(self, action):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        return action.shortcut()

    def setShortcut(self, action, shortcut):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        action.setShortcut(shortcut)

    def getMidi(self, action):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        return self._midi.get(action, None)

    def getMidiAsString(self, action):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        if action not in self._midi:
            return ""
        return self.midiToString(action, self._midi[action])

    def setMidi(self, action, midiData):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        if midiData is None and action in self._midi:
            del self._midi[action]
        elif midiData is not None:
            self._midi[action] = midiData

    def midiToString(self, action, midiData):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        return str(midiData)

    def openMidiDevice(self, device_id):
        self.midiDevice = device_id
        if self._midiThread is not None:
            self.closeMidiDevice()
        self._midiThread = MidiControlThread(device_id)
        self._midiThread.midiMessage.connect(self.midiToAction)
        self._midiThread.start()

    def closeMidiDevice(self):
        if self._midiThread is not None:
            self._midiThread.close()
            self._midiThread.wait()

    def midiToAction(self, midiData):
        for action in self.iterActions():
            if self._midi.get(action, None) == midiData:
                action.trigger()


