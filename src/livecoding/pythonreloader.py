# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import (QObject, pyqtSlot)


class PythonReloader(QObject):
    def __init__(self, main, parent=None):
        super(PythonReloader, self).__init__(parent)
        self._main = main

    @pyqtSlot()
    def restart(self):
        os.execv(self._main, sys.argv)
