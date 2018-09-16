# -*- coding: utf-8 -*-
import os
import sys

from python_qt_binding.QtCore import (QObject, pyqtSlot)


class PythonReloader(QObject):
    def __init__(self, main, parent=None):
        super(PythonReloader, self).__init__(parent)
        self._main = main

    @pyqtSlot()
    def restart(self):
        import_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
        python_path = os.environ.get('PYTHONPATH', '')
        if import_dir not in python_path:
            python_path += ':{}'.format(import_dir)
        os.environ['PYTHONPATH'] = python_path
        os.execv(self._main, sys.argv)
