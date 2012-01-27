'''
Created on 26 Jan 2012

@author: Mike Thomas

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

from PyQt4.QtGui import QGraphicsScene, QPen, QBrush
from PyQt4.QtCore import pyqtSignal
from PyQt4.Qt import Qt, QTimer

class MarkedScene(QGraphicsScene):
    '''
    classdocs
    '''

    currentChanged = pyqtSignal(int)

    def __init__(self, main):
        super(MarkedScene, self).__init__(main)
        self.main = main
        self._currentMarker = self.addLine(0, 0, 0, 100)
        self._currentMarker.setZValue(10)
        self._currentMarker.setVisible(False)
        self._marks = []
        self._markLines = {}
        self._begin = None
        self._end = None
        self._selection = None
        self._windowRange = 0, 0
        self._total = 0
        self._zoom = 1
        self.setSceneRect(0, 0, 0, 100)
        self._flasher = self.addRect(0, 0, 0, 0, pen = Qt.blue, brush = Qt.blue)
        self._flasher.setVisible(False)
        self._flasher.setOpacity(0.5)
        self._theView = self.addRect(-1, -1, 0, 102, pen = Qt.blue)
        self._theView.setBrush(QBrush(Qt.NoBrush))
        self._theView.setZValue(20)
        self._theView.setVisible(False)

    def newSong(self):
        self._marks = []
        for mark in self._markLines.values():
            self.removeItem(mark)
        self._markLines = {}
        self.begin = None
        self.end = None

    def setCurrent(self, ms):
        self._currentMarker.setX(ms)

    def setTotal(self, total):
        self.setSceneRect(0, 0, total, 100)
        self._currentMarker.setVisible(total > 0)
        self._theView.setVisible(total > 0)
        self._flasher.setRect(0, 0, total, 100)
        self._total = total
        self.setZoom(self._zoom)

    def _setBegin(self, position):
        self._begin = position
        if position is not None:
            if self._end is None or self._end < position:
                self._end = position
        self._drawSelection()
    def _getBegin(self):
        return self._begin
    begin = property(fget = _getBegin, fset = _setBegin)

    def _setEnd(self, position):
        self._end = position
        if position is not None:
            if self._begin is None or self._begin > position:
                self._begin = position
        self._drawSelection()
    def _getEnd(self):
        return self._end
    end = property(fget = _getEnd, fset = _setEnd)

    def _drawSelection(self):
        if self.begin is None or self.end is None:
            if self._selection is not None:
                self.removeItem(self._selection)
                self._selection = None
        else:
            if self._selection is None:
                self._selection = self.addRect(0, 0, 0, 0,
                                               pen = QPen(Qt.cyan),
                                               brush = QBrush(Qt.yellow))
                self._selection.setZValue(0)
                self._selection.setOpacity(0.75)
            self._selection.setRect(self.begin, 0, self.end - self.begin, 100)

    def getPreviousMark(self, position):
        theMark = None
        lastMark = 0
        for mark in self._marks:
            if lastMark < mark and position <= mark:
                theMark = lastMark
                break
            lastMark = mark
        else:
            theMark = lastMark
        if (self.end is not None
            and position > self.end
            and self.end >= theMark):
            theMark = self.end
        elif (self.begin is not None
              and position > self.begin
              and self.begin >= theMark):
            theMark = self.begin
        return theMark

    def getNextMark(self, position):
        theMark = None
        lastMark = 0
        for mark in self._marks:
            if lastMark <= mark and position < mark:
                theMark = mark
                break
            lastMark = mark
        else:
            theMark = self._total
        if self.begin is not None and position < self.begin and self.begin <= theMark:
            theMark = self.begin
        elif self.end is not None and position < self.end and self.end <= theMark:
            theMark = self.end
        return theMark

    def _addMark(self, index, position):
        self._marks.insert(index, position)
        self._markLines[position] = self.addLine(position, 0, position, 100, pen = QPen(Qt.red))
        self._markLines[position].setZValue(5)

    def toggleMark(self, position):
        if position == 0 or position == self._total:
            return
        for index, mark in enumerate(self._marks):
            if position == mark:
                self._marks.pop(index)
                self.removeItem(self._markLines.pop(position))
                break
            elif position < mark:
                self._addMark(index, position)
                break
        else:
            self._addMark(len(self._marks), position)

    def flash(self):
        self._flasher.setVisible(True)
        QTimer.singleShot(100, lambda : self._flasher.setVisible(False))

    def mousePressEvent(self, event):
        event.accept()

    def mouseReleaseEvent(self, event):
        button = event.button()
        point = event.scenePos()
        eventTime = min(self._total, max(0, int(point.x() + 0.5)))
        if button == Qt.LeftButton:
            self.currentChanged.emit(eventTime)
        elif button == Qt.MidButton:
            self.begin = eventTime
        elif button == Qt.RightButton:
            self.end = eventTime
        else:
            event.ignore()

    def setZoom(self, zoom):
        self._zoom = zoom
        rect = self._theView.rect()
        rect.setWidth(self._total / zoom)
        self._theView.setRect(rect)
        self._theView.setVisible(zoom > 1)

    def setWindowRange(self, a, b):
        self._windowRange = a, b

    def setWindow(self, value):
        if self._zoom > 1:
            start, end = self._windowRange
            rect = self._theView.rect()
            xpos = (self._total - rect.width()) * (value - start) / (end - start)
            rect.moveLeft(xpos)
            self._theView.setRect(rect)
