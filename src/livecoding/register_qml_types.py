# coding=utf-8
from python_qt_binding.QtQml import qmlRegisterType, qmlRegisterSingletonType

from .projectbrowser import ProjectBrowser
from .filewatcher import FileWatcher
from .livecoding import LiveCoding

MODULE_NAME = 'livecoding'


def register_types():
    qmlRegisterType(ProjectBrowser, MODULE_NAME, 1, 0, ProjectBrowser.__name__)
    qmlRegisterType(FileWatcher, MODULE_NAME, 1, 0, FileWatcher.__name__)
    qmlRegisterSingletonType(LiveCoding, MODULE_NAME, 1, 0, LiveCoding.__name__,
                             LiveCoding.qml_singleton_provider)
