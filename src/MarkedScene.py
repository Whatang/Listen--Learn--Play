'''
Created on 26 Jan 2012

@author: Mike Thomas

'''

from PyQt4.QtGui import QGraphicsScene, QPen, QBrush
from PyQt4.Qt import Qt, QTimer

class MarkedScene(QGraphicsScene):
    '''
    classdocs
    '''


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
        self._total = 0
        self.setSceneRect(0, 0, 0, 100)
        self._flasher = self.addRect(0, 0, 0, 0, pen = Qt.blue, brush = Qt.blue)
        self._flasher.setVisible(False)
        self._flasher.setOpacity(0.5)


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
        self.setSceneRect(0, 0, total + 1, 100)
        self._currentMarker.setVisible(total > 0)
        self._flasher.setRect(0, 0, total + 1, 100)
        self._total = total

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
        if self.end is not None and position > self.end and self.end >= theMark:
            theMark = self.end
        elif self.begin is not None and position > self.begin and self.begin >= theMark:
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

