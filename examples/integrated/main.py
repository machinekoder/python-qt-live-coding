# -*- coding: utf-8 -*-
import os
import sys
import signal
import argparse

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtQml import QQmlApplicationEngine

from livecoding import start_livecoding_gui

PROJECT_PATH = os.path.dirname(os.path.realpath(__name__))


class MyApp(QObject, object):
    def __init__(self, live, parent=None):
        super(MyApp, self).__init__(parent)

        self._engine = QQmlApplicationEngine()
        self._engine.addImportPath(PROJECT_PATH)
        if live:
            start_livecoding_gui(
                self._engine, PROJECT_PATH, __file__, live_qml='./live.qml'
            )  # live_qml is optional and can be used to customize the live coding environment
        else:
            qml_main = os.path.join(PROJECT_PATH, 'main.qml')
            self._engine.load(qml_main)

        self._start_check_timer()

    def _start_check_timer(self):
        self._timer = QTimer()
        self._timer.timeout.connect(lambda: None)
        self._timer.start(100)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda *args: QGuiApplication.quit())

    parser = argparse.ArgumentParser(
        description="""
            Example App
            """
    )
    parser.add_argument(
        '-l',
        '--live',
        help='The live coding version of this application',
        action='store_true',
    )
    args = parser.parse_args()

    app = QGuiApplication(sys.argv)

    gui = MyApp(live=args.live)

    sys.exit(app.exec_())
