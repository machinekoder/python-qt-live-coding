# coding=utf-8
import sys
import os
import signal
import traceback

from python_qt_binding.QtCore import QTimer, QObject
from python_qt_binding.QtGui import QIcon
from python_qt_binding.QtWidgets import QApplication
from python_qt_binding.QtQml import QQmlApplicationEngine

from .register_qml_types import register_types
from .pythonreloader import PythonReloader
from .moduleloader import recursively_register_types

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))


class LiveCodingGui(QObject):
    def __init__(self, args, main_file, parent=None):
        super(LiveCodingGui, self).__init__(parent)
        sys.excepthook = self._display_error

        register_types()

        qml_main = os.path.join(MODULE_PATH, 'live.qml')

        project_path = os.path.realpath(args.path)
        recursively_register_types(project_path)

        self._engine = QQmlApplicationEngine()
        self._engine.addImportPath(os.path.abspath('.'))
        self._engine.rootContext().setContextProperty('parsedArguments', vars(args))

        global reloader  # necessary to make reloading work, prevents garbage collection
        reloader = PythonReloader(main_file)
        self._engine.rootContext().setContextProperty(PythonReloader.__name__, reloader)
        self._engine.rootContext().setContextProperty('userProjectPath', project_path)

        self._engine.load(qml_main)

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
        sys.stderr.write("FATAL ERROR: An unexpected error occurred:\n{}\n\n{}\n".format(evalue, tb))


def main(main_file, arguments):
    signal.signal(signal.SIGINT, lambda *args: LiveCodingGui.shutdown())

    app = QApplication(sys.argv)
    app.setOrganizationName('Machine Koder')
    app.setOrganizationDomain('machinekoder.com')
    app.setApplicationName('Python Qt Live Coding')
    app.setWindowIcon(QIcon(os.path.join(MODULE_PATH, 'icon.png')))

    # noinspection PyUnusedLocal
    gui = LiveCodingGui(arguments, main_file)

    sys.exit(app.exec_())
