# -*- coding: utf-8 -*-
import os

from qtpy.QtQuick import QQuickItem
from qtpy.QtQml import QQmlEngine
from qtpy.QtCore import Slot, QUrl
from qtpy.QtGui import QDesktopServices


class LiveCodingHelper(QQuickItem):
    _engine = None

    def __init__(self, parent=None):
        super(LiveCodingHelper, self).__init__(parent)

    @Slot(QUrl, result=bool)
    def openUrlWithDefaultApplication(self, url):
        return QDesktopServices.openUrl(url)

    @Slot()
    def clearQmlComponentCache(self):
        context = QQmlEngine.contextForObject(self)
        context.engine().clearComponentCache()
        # maybe qmlClearTypeRegistrations

    @Slot(str, result=QUrl)
    def localPathToUrl(self, path):
        abspath = os.path.abspath(os.path.expanduser(path))
        return QUrl.fromLocalFile(abspath)
