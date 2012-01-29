'''
Created on 27 Jan 2012

@author: Mike Thomas

'''

from PyQt4.QtGui import QKeySequence
from midiMessages import (MidiControlThread, MidiRecogniser,
                          MidiMessage, SysExMessage)

class AbstractOperation(object):
    def shortcut(self):
        raise NotImplementedError()

    @classmethod
    def numActions(cls):
        raise NotImplementedError()

    @classmethod
    def unparametrise(cls, midiMsg):
        return midiMsg


class SingleAction(AbstractOperation):
    def __init__(self, action):
        super(SingleAction, self).__init__()
        self.action = action

    def shortcut(self):
        return self.action.shortcut()

    @classmethod
    def numActions(cls):
        return 1

    def trigger(self):
        self.action.trigger()


class ActionPair(AbstractOperation):
    def __init__(self, actionOn, actionOff, shortcut):
        super(ActionPair, self).__init__()
        self.actionOn = actionOn
        self.actionOff = actionOff
        self._shortcut = QKeySequence(shortcut)

    def shortcut(self):
        return self._shortcut

    @classmethod
    def numActions(cls):
        return 2

class PairedMidi(object):
    def __init__(self, midiOn, midiOff):
        self.midiOn = midiOn
        self.midiOff = midiOff

    def unparamString(self):
        return self.midiOn.unparamString() + "/" + self.midiOff.unparamString()

class ParameterAction(AbstractOperation):
    def __init__(self, method, outputMin, outputMax):
        super(ParameterAction, self).__init__()
        self._method = method
        self._outputMin = outputMin
        self._outputRange = outputMax - outputMin

    def setValue(self, value):
        self._method(value)

    def shortcut(self):
        return None

    @classmethod
    def numActions(cls):
        return 1

    def trigger(self, value):
        value = float(value) / 127
        value = self._outputMin + value * self._outputRange
        self._method(value)

    @classmethod
    def unparametrise(cls, midiMsg):
        if not midiMsg.hasFreeParameter():
            return midiMsg.makeParametrised()
        else:
            return midiMsg


class ControlSet(object):
    '''
    classdocs
    '''


    def __init__(self, midiDevice = -1):
        '''
        Constructor
        '''
        self.midiDevice = midiDevice
        self._midiThread = None
        self._midiRecogniser = MidiRecogniser()
        self._midi = {}
        self._actions = []
        self._descriptions = {}
        self._actionPairs = set()
        self._parameterActions = set()
        self._shortcuts = {}

    def _addAction(self, action, description):
        if action not in self._actions:
            self._actions.append(action)
            self._descriptions[action] = description
            self._shortcuts[action] = action.shortcut()

    def addSingleAction(self, action, description):
        self._addAction(SingleAction(action), description)

    def addActionPair(self, actionOn, actionOff, shortcut, description):
        actionPair = ActionPair(actionOn, actionOff, shortcut)
        self._actionPairs.add(actionPair)
        self._addAction(actionPair, description)

    def addParameterAction(self, method, description, outputMin, outputMax):
        parameterAction = ParameterAction(method, outputMin, outputMax)
        self._parameterActions.add(parameterAction)
        self._addAction(parameterAction, description)

    def __getitem__(self, index):
        return self._actions[index]

    def __len__(self):
        return len(self._actions)

    def iterActions(self):
        return iter(self._actions)

    def getDescription(self, action):
        return self._descriptions.get(action, "")

    def getShortcutString(self, action):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        shortcut = self._shortcuts[action]
        if shortcut is None:
            return ""
        else:
            return shortcut.toString()

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
        return self._midi[action].unparamString()

    def isValidMidi(self, action, midiMsg):
        if isinstance(midiMsg, SysExMessage):
            return False
        elif action in self._actionPairs:
            return isinstance(midiMsg, PairedMidi)
        else:
            return isinstance(midiMsg, MidiMessage)

    def setMidi(self, action, midiData):
        if action not in self._descriptions:
            raise KeyError("Unrecognised action")
        if midiData is None and action in self._midi:
            midiData = self._midi[action]
            if action.numActions() == 1:
                self._midiRecogniser.removeMessageTarget(midiData)
            else:
                self._midiRecogniser.removeMessageTarget(midiData.midiOn)
                self._midiRecogniser.removeMessageTarget(midiData.midiOff)
            del self._midi[action]
        elif midiData is not None:
            if action.numActions() == 1:
                if (action in self._parameterActions
                    and not midiData.hasFreeParameter()):
                    midiData = midiData.makeParametrised()
                self._midi[action] = midiData
                self._midiRecogniser.addMessageTarget(midiData, action)
            elif not isinstance(midiData, PairedMidi):
                raise TypeError("On/Off actions require two MIDI messages")
            else:
                self._midi[action] = midiData
                self._midiRecogniser.addMessageTarget(midiData.midiOn,
                                                      action.actionOn)
                self._midiRecogniser.addMessageTarget(midiData.midiOff,
                                                      action.actionOff)


    def openMidiDevice(self, deviceId):
        self.midiDevice = deviceId
        if self._midiThread is not None:
            self.closeMidiDevice()
        self._midiThread = MidiControlThread(deviceId)
        self._midiThread.midiReceived.connect(self.midiToAction)
        self._midiThread.start()

    def closeMidiDevice(self):
        if self._midiThread is not None:
            self._midiThread.close()
            self._midiThread.wait()

    def midiToAction(self, midiData):
        target = self._midiRecogniser.getTarget(midiData)
        if target is None:
            return
        if target in self._parameterActions:
            target.trigger(midiData.parameterValue())
        else:
            target.trigger()


