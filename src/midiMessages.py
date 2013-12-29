"""
Created on 29 Jan 2012

@author: Mike Thomas
"""
from pygame import midi
from PyQt4.QtCore import QThread, pyqtSignal


class MidiMessage(object):
    status = None
    typeName = "Unrecognized"

    def __init__(self, channel, data1, data2, *extra):
        self.channel = channel & 0xF
        self.data1 = data1
        self.data2 = data2

    def unparamString(self):
        return "%s Channel %d: Data %d, %d" % (self.typeName,
                                               self.channel,
                                               self.data1,
                                               self.data2)

    def parameterValue(self):
        return self.data2

    def identifyingSequence(self):
        raise NotImplementedError()

    def hasFreeParameter(self):  # IGNORE:R0201
        return True

    def makeParametrised(self):
        return self


class NoteOffMidiMessage(MidiMessage):
    status = 0x8
    typeName = "NoteOff"

    def unparamString(self):
        return "Note %d On, Channel %d" % (self.data1,
                                           self.channel)

    def identifyingSequence(self):
        yield self.status
        yield self.channel
        yield self.data1


class NoteOnMidiMessage(MidiMessage):
    status = 0x9
    typeName = "NoteOn"

    def unparamString(self):
        return "Note %d Off, Channel %d" % (self.data1,
                                            self.channel)

    def identifyingSequence(self):
        yield self.status
        yield self.channel
        yield self.data1


class PolyphonicAftertouchMidiMessage(MidiMessage):
    status = 0xA
    typeName = "PolyAT"

    def unparamString(self):
        return "%s Channel %d, Note %d" % (self.typeName,
                                           self.channel,
                                           self.data1)

    def identifyingSequence(self):
        yield self.status
        yield self.channel
        yield self.data1


class ControlMidiMessage(MidiMessage):
    status = 0xB
    typeName = "Control"

    def unparamString(self):
        return "%s Channel %d. Controller %d, Value %d" % (self.typeName,
                                                           self.channel,
                                                           self.data1,
                                                           self.data2)

    def identifyingSequence(self):
        yield self.status
        yield self.channel
        yield self.data1
        yield self.data2

    def hasFreeParameter(self):
        return False

    def makeParametrised(self):
        return ParametrisedControlMidiMessage(self.channel, self.data1,
                                              None)


class ParametrisedControlMidiMessage(ControlMidiMessage):
    def unparamString(self):
        return "%s Channel %d. Parametrised Controller %d" % (self.typeName,
                                                              self.channel,
                                                              self.data1)

    def identifyingSequence(self):
        yield self.status
        yield self.channel
        yield self.data1

    def hasFreeParameter(self):
        return True

    def makeParametrised(self):
        return self


class ProgramMidiMessage(MidiMessage):
    status = 0xC
    typeName = "Program"

    def unparamString(self):
        return "%s Channel %d. Program %d" % (self.typeName,
                                              self.channel,
                                              self.data1)

    def identifyingSequence(self):
        yield self.status
        yield self.channel
        yield self.data1


class ChannelAftertouchMidiMessage(MidiMessage):
    status = 0xD
    typeName = "ChannelAT"

    def parameterValue(self):
        return self.data1

    def unparamString(self):
        return "%s Channel %d." % (self.typeName, self.channel)

    def identifyingSequence(self):
        yield self.status
        yield self.channel


class PitchWheelMidiMessage(MidiMessage):
    status = 0xE
    typeName = "PitchWheel"

    def parameterValue(self):
        return float(self.data1 + (self.data2 << 8)) / 256

    def unparamString(self):
        return "%s Channel %d." % (self.typeName, self.channel)

    def identifyingSequence(self):
        yield self.status
        yield self.channel


class SysExMessage(MidiMessage):
    status = 0xF
    typeName = "SysEx"

    def identifyingSequence(self):
        raise TypeError()

_MIDIMAP = dict((msgType.status, msgType)
                for msgType in MidiMessage.__subclasses__())  # IGNORE:E1101


def midiMessageFactory(status, data1, data2, *extra):
    msgType = (status & 0xF0) >> 4
    msgType = _MIDIMAP.get(msgType, None)
    if msgType is None:
        return None
    return msgType(status & 0x0F, data1, data2, *extra)


class MidiControlThread(QThread):
    def __init__(self, deviceId):
        self._deviceId = deviceId
        self._running = False
        super(MidiControlThread, self).__init__()

    midiReceived = pyqtSignal(MidiMessage)

    def run(self):
        self._running = True
        midiIn = midi.Input(self._deviceId, 0)
        try:
            hasSysEx = False
            while self._running:
                self.msleep(10)
                while midiIn.poll():
                    midiData = midiIn.read(1)[0][0]
                    if not hasSysEx:
                        if midiData[0] & 0xF0 == 0xF0:
                            hasSysEx = midiData
                            msg = None
                        else:
                            msg = midiMessageFactory(*midiData)
                    else:
                        index = -1
                        while index > -4 and midiData[index] != 0:
                            index -= 1
                        hasSysEx = (hasSysEx +
                                    midiData[:index] + [midiData[index]])
                        if hasSysEx[-1] == 0xF7:
                            msg = SysExMessage(*hasSysEx)
                        else:
                            msg = None
                    if msg is not None:
                        self.midiReceived.emit(msg)
        finally:
            del midiIn

    def close(self):
        self._running = False


class MidiRecogniser(object):
    def __init__(self):
        self._tree = {}

    def addMessageTarget(self, msg, target):
        node = self._tree
        for data in msg.identifyingSequence():
            if data not in node:
                node[data] = {}
            node = node[data]
        node[-1] = target

    def getTarget(self, msg):
        node = self._tree
        for data in msg.identifyingSequence():
            if data not in node:
                if -1 in node:
                    return node[-1]
                return None
            node = node[data]
        return node[-1]

    def removeMessageTarget(self, msg):
        node = self._tree
        visited = []
        for data in msg.identifyingSequence():
            if data not in node:
                return
            visited.append(node)
            node = node[data]
        if -1 not in node:
            return
        visited.append(node)
        nodeToDelete = -1
        while visited:
            parentNode = visited.pop()
            parentNode.pop(nodeToDelete)
            if len(node) != 0:
                break
            nodeToDelete = node
