'''
Created on 27 Jan 2012

@author: Mike Thomas

'''


NORMAL = 0
SET_PARAMETER = 1

class ControlSettings(object):
    '''
    classdocs
    '''


    def __init__(self, midiOn = False, midiDevice = None):
        '''
        Constructor
        '''
        self.midiOn = midiOn
        self.midiDevice = midiDevice
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
        return self._midi.get(action, "")

    def setMidi(self, action, midi):
        if midi not in self._descriptions:
            raise KeyError("Unrecognised action")
        self._midi[action] = midi

    def midiToAction(self, midi):
        if midi in self._midi:
            self._midi[midi].trigger()
