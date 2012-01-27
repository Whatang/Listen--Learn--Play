'''
Created on 26 Jan 2012

@author: Mike Thomas

 Listen, Learn, Play - a musicians' music player.
    Copyright (C) 2012 Michael Thomas

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import os
from PyQt4.QtGui import QApplication, QMainWindow, QDesktopServices, QFileDialog, QIcon, QPixmap, QTransform
from PyQt4.QtCore import pyqtSignature, QTimer, Qt
from PyQt4.phonon import Phonon
sys.path.append("Images")
from ui_llp import Ui_MainWindow
from MarkedScene import MarkedScene

WINDOW_TITLE = "Listen, Learn, Play"
TICK_INTERVAL = 10
SPOOL_INTERVAL = 40

class LlpMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(LlpMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.playIcon = QIcon()
        self.playIcon.addPixmap(QPixmap(":/Images/Play"))
        self.pauseIcon = QIcon()
        self.pauseIcon.addPixmap(QPixmap(":/Images/Pause"))
        self._filename = None
        self._total = 0
        self._oldMs = 0
        self._beatsLeft = 0
        self._beatTimer = None
        self._rewinding = None
        self._forwarding = None
        self._wasPlaying = False
        self._scene = MarkedScene(self)
        self._media = Phonon.MediaObject(self)
        self._media.totalTimeChanged.connect(self._totalChanged)
        self._media.stateChanged.connect(self._mediaStateChanged)
        self._media.setTickInterval(TICK_INTERVAL)
        self._media.metaDataChanged.connect(self.printMeta)
        self._audio = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self._media.tick.connect(self._tick)
        self._media.prefinishMarkReached.connect(self._prefinish)
        self._media.finished.connect(self._finish)
        Phonon.createPath(self._media, self._audio)
        self.volumeSlider.setAudioOutput(self._audio)
        self.markView.setScene(self._scene)
        self._scene.currentChanged.connect(self.setCurrent)
        self._tick(0)
        self._checkButtons()
        self.addActions([self.actionPlay, self.actionMark,
                         self.actionMark_2, self.actionCountIn,
                         self.actionHome, self.actionEnd,
                         self.actionNextMark, self.actionPreviousMark,
                         self.actionLoop, self.actionSelection,
                         self.actionOpen, self.actionToggleMute,
                         self.actionVolumeUp, self.actionVolumeDown])

    def printMeta(self):
        for k, v in self._media.metaData().iteritems():
            print str(k), str(v)

    @pyqtSignature("")
    def on_actionOpen_triggered(self):
        if self._media.state() == Phonon.PlayingState:
            self._media.pause()
        if self._filename is not None:
            directory = os.path.dirname(self._filename)
        else:
            loc = QDesktopServices.MusicLocation
            directory = QDesktopServices.storageLocation(loc)
        caption = "Open a music file"
        fname = QFileDialog.getOpenFileName(parent = self,
                                            caption = caption,
                                            directory = directory,
                                            filter = "Music files (*.mp3)")
        if len(fname) == 0:
            return
        self._filename = str(fname)
        self._media.setCurrentSource(Phonon.MediaSource(fname))
        self._scene.newSong()
        self._media.pause() # Makes sure tick signals are emitted
        base = os.path.splitext(os.path.basename(self._filename))[0]
        self.setWindowTitle(WINDOW_TITLE + " - " + base)


    @pyqtSignature("")
    def on_actionPlay_triggered(self):
        if not self.playButton.isEnabled():
            return
        if self._media.state() == Phonon.PlayingState:
            self._media.pause()
        elif self._media.state() in (Phonon.PausedState, Phonon.StoppedState):
            self._media.play()

    def _mediaStateChanged(self, newState):
        self._checkButtons(newState)
        if newState == Phonon.ErrorState:
            self._totalChanged(0)

    def _checkButtons(self, state = None, ms = None):
        if state is None:
            state = self._media.state()
        if ms is None:
            ms = self._media.currentTime()
        if state in (Phonon.LoadingState, Phonon.BufferingState,
                     Phonon.ErrorState):
            self.controlsFrame.setEnabled(False)
            self.markFrame.setEnabled(False)
            self.rightFrame.setEnabled(False)
        else:
            self.controlsFrame.setEnabled(True)
            self.markFrame.setEnabled(True)
            self.rightFrame.setEnabled(True)
            if (state == Phonon.PlayingState
                or ((self._rewinding or self._forwarding)
                    and self._wasPlaying)):
                self.playButton.setIcon(self.pauseIcon)
                self.countButton.setEnabled(False)
                self.selectionButton.setEnabled(False)
                self.loopButton.setEnabled(False)
            else:
                self.playButton.setIcon(self.playIcon)
                self.countButton.setEnabled(True)
                self.selectionButton.setEnabled(True)
                self.loopButton.setEnabled(True)
            beforeEnd = (ms < self._total)
            self.playButton.setEnabled(beforeEnd)
            self.countButton.setEnabled(self.countButton.isEnabled()
                                        and beforeEnd)
            self.endButton.setEnabled(beforeEnd)
            self.forwardButton.setEnabled(beforeEnd)
            if not beforeEnd and self._forwarding:
                self.on_forwardButton_released()
            afterStart = (ms != 0)
            self.startButton.setEnabled(afterStart)
            self.rewindButton.setEnabled(afterStart)
            if not afterStart and self._rewinding:
                self.on_rewindButton_released()

    @pyqtSignature("")
    def on_actionHome_triggered(self):
        if not self.startButton.isEnabled():
            return
        if self.selectionButton.isChecked() and self._scene.begin is not None:
            self._media.seek(self._scene.begin)
        else:
            self._media.seek(0)

    @pyqtSignature("")
    def on_actionEnd_triggered(self):
        if not self.endButton.isEnabled():
            return
        if self.selectionButton.isChecked() and self._scene.end is not None:
            self._media.seek(self._scene.end)
        else:
            self._media.seek(self._total)

    @pyqtSignature("")
    def on_rewindButton_pressed(self):
        self._rewinding = QTimer(self)
        self._rewinding.setInterval(TICK_INTERVAL)
        self._rewinding.timeout.connect(self._rewinder)
        self._wasPlaying = (self._media.state() == Phonon.PlayingState)
        self._media.pause()
        self._rewinding.start()

    def _rewinder(self):
        newPos = max(0, self._oldMs - SPOOL_INTERVAL)
        self._media.seek(newPos)

    @pyqtSignature("")
    def on_rewindButton_released(self):
        if self._rewinding:
            self._rewinding.stop()
        self._rewinding = None
        if self._wasPlaying:
            self._media.play()


    @pyqtSignature("")
    def on_forwardButton_pressed(self):
        self._forwarding = QTimer(self)
        self._forwarding.setInterval(TICK_INTERVAL)
        self._forwarding.timeout.connect(self._forwarder)
        self._wasPlaying = (self._media.state() == Phonon.PlayingState)
        self._media.pause()
        self._forwarding.start()


    def _forwarder(self):
        newPos = min(self._total, self._oldMs + SPOOL_INTERVAL)
        self._media.seek(newPos)

    @pyqtSignature("")
    def on_forwardButton_released(self):
        if self._forwarding:
            self._forwarding.stop()
        self._forwarding = None
        if self._wasPlaying:
            self._media.play()

    def _tick(self, ms):
        seconds = ms / 1000.0
        if self._total == 0:
            self.positionIndicator.setText("--")
        else:
            self.positionIndicator.setText("%.2f" % seconds)
        if ms < self._oldMs or ms == self._total or self._oldMs == 0:
            self._checkButtons(ms = ms)
        self._oldMs = ms
        self._scene.setCurrent(ms)

    def setCurrent(self, ms):
        self._media.seek(ms)

    def _totalChanged(self, total):
        self._total = total
        if total > 0:
            self.markView.setEnabled(True)
            self.controlsFrame.setEnabled(True)
            self.markFrame.setEnabled(True)
            self.rightFrame.setEnabled(True)
            self.totalLabel.setText("%.2f" % (total / 1000.0))
            self._scene.setTotal(total)
            self._tick(self._media.currentTime())
            self.markView.setSceneRect(self._scene.sceneRect())
            print self._scene.sceneRect()
            sx = float(self.markView.width() - 3) / self._scene.width()
            height = self.markView.height() - 3
            for scrollBar in self.markView.scrollBarWidgets(Qt.AlignBottom | Qt.AlignTop):
                height -= scrollBar.height()
            sy = float(height) / self._scene.height()
            transform = QTransform(sx, 0, 0,
                                   0, sy, 0,
                                   0, 0, 1)
            self.markView.setTransform(transform)
        else:
            self.totalLabel.setText("--")
            self._scene.setTotal(total)
            self._tick(0)
            self.markView.setSceneRect(0, 0, 0, 0)
            self.markView.setEnabled(False)
            self.controlsFrame.setEnabled(False)
            self.markFrame.setEnabled(False)
            self.rightFrame.setEnabled(False)

    @pyqtSignature("")
    def on_setBeginButton_clicked(self):
        self._scene.begin = self._oldMs

    @pyqtSignature("")
    def on_setEndButton_clicked(self):
        self._scene.end = self._oldMs
        self._media.setPrefinishMark(self._total - self._oldMs)

    @pyqtSignature("")
    def on_actionMark_triggered(self):
        if self.markButton.isEnabled():
            self._scene.toggleMark(self._oldMs)

    @pyqtSignature("")
    def on_actionNextMark_triggered(self):
        if self.nextMarkButton.isEnabled():
            mark = self._scene.getNextMark(self._oldMs)
            self._media.seek(mark)

    @pyqtSignature("")
    def on_actionPreviousMark_triggered(self):
        if self.prevMarkButton.isEnabled():
            mark = self._scene.getPreviousMark(self._oldMs)
            self._media.seek(mark)

    def _prefinish(self):
        if self.selectionButton.isChecked():
            self._media.pause()
            if self.loopButton.isChecked():
                self._media.seek(self._scene.begin)
                self._media.play()

    def _finish(self):
        if self.loopButton.isChecked() and not self.selectionButton.isChecked():
            self._media.pause()
            self._media.seek(0)
            self._media.play()

    @pyqtSignature("bool")
    def on_selectionButton_toggled(self, onOff):
        if onOff:
            self.selectionButton.setText("Selection")
        else:
            self.selectionButton.setText("Song")

    @pyqtSignature("")
    def on_actionSelection_triggered(self):
        if self.selectionButton.isEnabled():
            self.selectionButton.toggle()

    @pyqtSignature("bool")
    def on_loopButton_toggled(self, onOff):
        if onOff:
            self.loopButton.setText("Loop")
        else:
            self.loopButton.setText("Once")

    @pyqtSignature("")
    def on_actionLoop_triggered(self):
        if self.loopButton.isEnabled():
            self.loopButton.toggle()

    @pyqtSignature("")
    def on_actionCountIn_triggered(self):
        if not self.countButton.isEnabled():
            return
        numBeats = self.beatsBox.value()
        if numBeats == 0:
            self.actionPlay.trigger()
            self.playButton.setFocus()
            return
        bpm = self.bpmBox.value()
        interval = 60000.0 / bpm
        self._beatsLeft = numBeats
        self._beatTimer = QTimer(self)
        self._beatTimer.setInterval(interval)
        self._beatTimer.timeout.connect(self._beat)
        self.controlsFrame.setEnabled(False)
        self.rightFrame.setEnabled(False)
        self.markFrame.setEnabled(False)
        self.actionOpen.setEnabled(False)
        self.openButton.setEnabled(False)
        self._beatTimer.start(interval)

    def _beat(self):
        if self._beatsLeft <= 0:
            self._beatTimer.stop()
            self.controlsFrame.setEnabled(True)
            self.rightFrame.setEnabled(True)
            self.markFrame.setEnabled(True)
            self.actionOpen.setEnabled(True)
            self.openButton.setEnabled(True)
            self.actionPlay.trigger()
            self.playButton.setFocus()
        else:
            self._scene.flash()
        self._beatsLeft -= 1

    @pyqtSignature("")
    def on_actionToggleMute_triggered(self):
        self._audio.setMuted(not self._audio.isMuted())

    @pyqtSignature("")
    def on_actionVolumeUp_triggered(self):
        newVolume = min(self.volumeSlider.maximumVolume(),
                        self._audio.volume() + self.volumeSlider.pageStep() / 100.0)
        self._audio.setVolume(newVolume)

    @pyqtSignature("")
    def on_actionVolumeDown_triggered(self):
        newVolume = max(0,
                        self._audio.volume() - self.volumeSlider.pageStep() / 100.0)
        self._audio.setVolume(newVolume)
def main():
    app = QApplication(sys.argv)
    mainWindow = LlpMainWindow()
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
