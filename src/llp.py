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
from PyQt4.QtCore import pyqtSignature, QTimer
from PyQt4.phonon import Phonon
sys.path.append("Images")
from ui_llp import Ui_MainWindow
from MarkedScene import MarkedScene

WINDOW_TITLE = "Listen, Learn, Play"
TICK_INTERVAL = 10
SPOOL_INTERVAL = 4 * TICK_INTERVAL

class LlpMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        super(LlpMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.PLAY_ICON = QIcon()
        self.PAUSE_ICON = QIcon()
        self.PLAY_ICON.addPixmap(QPixmap(":/Images/Play"))
        self.PAUSE_ICON.addPixmap(QPixmap(":/Images/Pause"))
        self._filename = None
        self._total = 0
        self._oldMs = 0
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
        Phonon.createPath(self._media, self._audio)
        self.seekSlider.setMediaObject(self._media)
        self.volumeSlider.setAudioOutput(self._audio)
        self.markView.setScene(self._scene)
        self._tick(0)
        self._checkButtons()

    def printMeta(self):
        for k, v in self._media.metaData().iteritems():
            print str(k), str(v)

    @pyqtSignature("")
    def on_actionOpen_triggered(self):
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
        self._media.pause() # Makes sure tick signals are emitted
        base = os.path.splitext(os.path.basename(self._filename))[0]
        self.setWindowTitle(WINDOW_TITLE + " - " + base)

    @pyqtSignature("")
    def on_playButton_clicked(self):
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
            self.startButton.setEnabled(False)
            self.rewindButton.setEnabled(False)
            self.playButton.setEnabled(False)
            self.forwardButton.setEnabled(False)
            self.endButton.setEnabled(False)
        else:
            if state == Phonon.PlayingState or ((self._rewinding or self._forwarding) and self._wasPlaying):
                self.playButton.setIcon(self.PAUSE_ICON)
            else:
                self.playButton.setIcon(self.PLAY_ICON)
            beforeEnd = (ms < self._total)
            self.playButton.setEnabled(beforeEnd)
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
    def on_startButton_clicked(self):
        self._media.seek(0)

    @pyqtSignature("")
    def on_endButton_clicked(self):
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


    def _totalChanged(self, total):
        self._total = total
        if total > 0:
            self.markView.setEnabled(True)
            self.totalLabel.setText("%.2f" % (total / 1000.0))
            self._scene.setTotal(total)
            self._tick(self._media.currentTime())
            self.markView.setSceneRect(self._scene.sceneRect())
            self.markView.setTransform(QTransform(float(self.markView.width()) / self._scene.width(),
                                                  0, 0, 0, 1, 0, 0, 0, 1))
        else:
            self.totalLabel.setText("--")
            self._scene.setTotal(total)
            self._tick(0)
            self.markView.setSceneRect(0, 0, 0, 0)
            self.markView.setEnabled(False)



def main():
    app = QApplication(sys.argv)
    mainWindow = LlpMainWindow()
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
