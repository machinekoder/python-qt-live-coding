# -*- coding: utf-8 -*-
import sys
import os
import signal
import traceback

from qtpy.QtCore import QTimer, QObject
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QApplication
from qtpy.QtQml import QQmlApplicationEngine

from .register_qml_types import register_types
from .pythonreloader import PythonReloader
from .moduleloader import recursively_register_types

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))


def start_livecoding_gui(engine, project_path, main_file, live_qml=''):
    """
    Starts the live coding GUI.
    :param engine: The QML engine.
    :param project_path: Path where the projects QML file are located.
    :param main_file: The main application file of the project.
    :param live_qml: Optional live window QML file.
    :return:
    """
    register_types()
    recursively_register_types(project_path)

    global reloader  # necessary to make reloading work, prevents garbage collection
    reloader = PythonReloader(main_file)
    engine.rootContext().setContextProperty(PythonReloader.__name__, reloader)
    engine.rootContext().setContextProperty('userProjectPath', project_path)

    if live_qml:
        qml_main = live_qml
        engine.addImportPath(os.path.join(MODULE_PATH, '..'))
    else:
        qml_main = os.path.join(MODULE_PATH, 'live.qml')
    engine.load(qml_main)


class LiveCodingGui(QObject):
    def __init__(self, args, main_file, parent=None):
        super(LiveCodingGui, self).__init__(parent)
        sys.excepthook = self._display_error

        project_path = os.path.realpath(args.path)

        self._engine = QQmlApplicationEngine()
        self._engine.addImportPath(project_path)
        start_livecoding_gui(self._engine, project_path, main_file)

        self._start_check_timer()

    def _start_check_timer(self):
        self._timer = QTimer()
        self._timer.timeout.connect(lambda: None)
        self._timer.start(100)

    @staticmethod
    def shutdown():
        QApplication.quit()

    @staticmethod
    def _display_error(etype, evalue, etraceback):
        tb = ''.join(traceback.format_exception(etype, evalue, etraceback))
        sys.stderr.write(
            "FATAL ERROR: An unexpected error occurred:\n{}\n\n{}\n".format(evalue, tb)
        )


def main(main_file, arguments):
    signal.signal(signal.SIGINT, lambda *args: LiveCodingGui.shutdown())

    app = QApplication(sys.argv)
    app.setOrganizationName('machinekoder.com')
    app.setOrganizationDomain('machinekoder.com')
    app.setApplicationName('Python Qt Live Coding')
    app.setWindowIcon(QIcon(os.path.join(MODULE_PATH, 'icon.png')))

    _gui = LiveCodingGui(arguments, main_file)  # noqa: F841

    sys.exit(app.exec_())
