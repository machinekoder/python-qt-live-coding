# -*- coding: utf-8 -*-
from qtpy.QtQml import qmlRegisterType

from .projectbrowser import ProjectBrowser
from .filewatcher import FileWatcher
from .live_coding_helper import LiveCodingHelper

MODULE_NAME = 'livecoding'


def register_types():
    qmlRegisterType(ProjectBrowser, MODULE_NAME, 1, 0, ProjectBrowser.__name__)
    qmlRegisterType(FileWatcher, MODULE_NAME, 1, 0, FileWatcher.__name__)
    qmlRegisterType(LiveCodingHelper, MODULE_NAME, 1, 0, LiveCodingHelper.__name__)
