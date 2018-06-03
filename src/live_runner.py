#!/usr/bin/env python
# coding=utf-8

import sys
import os
import signal
import argparse

from PyQt5.QtCore import QTimer, QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

import livecoding
from livecoding import PythonReloader


class LiveCodingGui(QObject):
    def __init__(self, args, parent=None):
        super(LiveCodingGui, self).__init__(parent)

        livecoding.register_types()

        if args.live:
            qml_main = './live.qml'
        else:
            qml_main = './init.qml'

        self._engine = QQmlApplicationEngine()
        self._engine.addImportPath(os.path.abspath('.'))
        self._engine.rootContext().setContextProperty('parsedArguments', vars(args))
        if args.live:
            global reloader  # necessary to make reloading work, prevents garbage collection
            reloader = PythonReloader(__file__)
            self._engine.rootContext().setContextProperty(PythonReloader.__name__, reloader)
            self._engine.rootContext().setContextProperty('projectPath', os.path.dirname(os.path.realpath(__file__)))
        self._engine.load(qml_main)

        self._start_check_timer()

    def _start_check_timer(self):
        self._timer = QTimer()
        self._timer.timeout.connect(lambda : None)
        self._timer.start(100)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *args: LiveCodingGui.shutdown())

    parser = argparse.ArgumentParser(description="""
            Live Coding example UI
            """)
    parser.add_argument('-l', '--live', help='The live coding version of this application', action='store_true', default=True)
    arguments, unknown = parser.parse_known_args()

    app = QApplication(sys.argv)
    app.setOrganizationName('Machine Koder')
    app.setOrganizationDomain('machinekoder.com')
    app.setApplicationName('Live Coding example')
    # app.setWindowIcon(QIcon('./icons/application/png/icon.png'))

    gui = LiveCodingGui(arguments)

    sys.exit(app.exec_())
