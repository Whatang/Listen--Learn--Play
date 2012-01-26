'''
Created on 26 Jan 2012

@author: Mike Thomas

'''

from PyQt4.QtGui import QGraphicsScene, QGraphicsLineItem

class MarkedScene(QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self, main):
        super(MarkedScene, self).__init__(main)
        self.main = main
        self._currentMarker = QGraphicsLineItem(scene = self)
        self._currentMarker.setLine(0, 0, 0, 100)
        self._currentMarker.setVisible(False)
        self._beginMarker = QGraphicsLineItem(scene = self)
        self._beginMarker.setLine(0, 0, 0, 100)
        self._beginMarker.setVisible(False)
        self._endMarker = QGraphicsLineItem(scene = self)
        self._endMarker.setLine(0, 0, 0, 100)
        self._endMarker.setVisible(False)
        self.setSceneRect(0, 0, 0, 100)

    def setCurrent(self, ms):
        self._currentMarker.setX(ms)

    def setTotal(self, total):
        self.setSceneRect(0, 0, total + 1, 100)
        self._currentMarker.setVisible(total > 0)
