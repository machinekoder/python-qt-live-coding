# -*- coding: utf-8 -*-
from qtpy.QtCore import QObject, Signal, Property


class Calculator(QObject):

    in1Changed = Signal(float)
    in2Changed = Signal(float)
    outChanged = Signal(float)

    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)

        self._in1 = 0.0
        self._in2 = 0.0
        self._out = 0.0

        self.in1Changed.connect(lambda _: self._calculate())
        self.in2Changed.connect(lambda _: self._calculate())

    @Property(float, notify=in1Changed)
    def in1(self):
        return self._in1

    @in1.setter
    def in1(self, value):
        if value == self._in1:
            return
        self._in1 = value
        self.in1Changed.emit(value)

    @Property(float, notify=in2Changed)
    def in2(self):
        return self._in2

    @in2.setter
    def in2(self, value):
        if value == self._in2:
            return
        self._in2 = value
        self.in2Changed.emit(value)

    @Property(float, notify=outChanged)
    def out(self):
        return self._out

    def _calculate(self):
        self._out = self._in1 + self._in2
        self.outChanged.emit(self._out)
