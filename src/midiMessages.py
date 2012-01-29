'''
Created on 29 Jan 2012

@author: Mike Thomas
'''
from pygame import midi
from PyQt4.QtCore import QThread, pyqtSignal


class MidiMessage(object):
    status = None
    typeName = "Unrecognized"
    def __init__(self, status, data1, data2, *extra):
        self.channel = status & 0xF
        self.data1 = data1
        self.data2 = data2

    def __str__(self):
        return "%s, Channel %d. Data %d, %d" % (self.typeName,
                                                self.channel,
                                                self.data1,
                                                self.data2)

class NoteOnMidiMessage(MidiMessage):
    status = 0x8
    typeName = "NoteOn"

class NoteOffMidiMessage(MidiMessage):
    status = 0x9
    typeName = "NoteOff"

class PolyphonicAftertouchMidiMessage(MidiMessage):
    status = 0xA
    typeName = "PolyAT"

class ControlMidiMessage(MidiMessage):
    status = 0xB
    typeName = "Control"

class ProgramMidiMessage(MidiMessage):
    status = 0xC
    typeName = "Program"

class ChannelAftertouchMidiMessage(MidiMessage):
    status = 0xD
    typeName = "ChannelAT"

class PitchWheelMidiMessage(MidiMessage):
    status = 0xE
    typeName = "PitchWheel"

class SysExMessage(MidiMessage):
    status = 0xF
    typeName = "SysEx"

_MIDIMAP = dict((msgType.status, msgType)
                for msgType in MidiMessage.__subclasses__()) #IGNORE:E1101


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
                    if hasSysEx == False:
                        if midiData[0] & 0xF0 == 0xF0:
                            hasSysEx = midiData
                            msg = None
                        else:
                            msg = midiMessageFactory(*midiData)
                    else:
                        index = -1
                        while index > -4 and midiData[index] != 0:
                            index -= 1
                        hasSysEx = hasSysEx + midiData[:index] + [midiData[index]]
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
