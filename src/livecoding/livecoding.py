# -*- coding: utf-8 -*-
import os

from python_qt_binding.QtCore import QObject, pyqtSlot, QUrl
from python_qt_binding.QtGui import QDesktopServices


class LiveCoding(QObject):
    _engine = None

    def __init__(self, parent=None):
        super(LiveCoding, self).__init__(parent)

    @staticmethod
    def qml_singleton_provider(engine, _):
        LiveCoding._engine = engine

        return LiveCoding()

    @pyqtSlot(QUrl, result=bool)
    def openUrlWithDefaultApplication(self, url):
        return QDesktopServices.openUrl(url)

    @pyqtSlot()
    def clearQmlComponentCache(self):
        LiveCoding._engine.clearComponentCache()
        # maybe qmlClearTypeRegistrations

    @pyqtSlot(str, result=QUrl)
    def localPathToUrl(self, path):
        abspath = os.path.abspath(os.path.expanduser(path))
        return QUrl.fromLocalFile(abspath)
