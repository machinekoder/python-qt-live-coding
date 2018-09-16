# -*- coding: utf-8 -*-
import os

from python_qt_binding.QtCore import QObject, pyqtProperty, pyqtSignal, QUrl, pyqtSlot


class ProjectBrowser(QObject):
    projectPathChanged = pyqtSignal(QUrl)
    qmlFilesChanged = pyqtSignal('QStringList')

    def __init__(self, parent=None):
        super(ProjectBrowser, self).__init__(parent)

        path = os.path.dirname(os.path.abspath(__file__))
        self._project_path = QUrl.fromLocalFile(os.path.realpath(os.path.join(path, '..')))
        self._qml_files = []

        self.update()

        self.projectPathChanged.connect(self._update_files)

    @pyqtProperty(QUrl, notify=projectPathChanged)
    def projectPath(self):
        return self._project_path

    @projectPath.setter
    def projectPath(self, value):
        if self._project_path == value:
            return
        self._project_path = value
        self.projectPathChanged.emit(value)

    @pyqtProperty('QStringList', notify=qmlFilesChanged)
    def qmlFiles(self):
        return self._qml_files

    @pyqtSlot()
    def update(self):
        self._update_files()

    def _update_files(self):
        file_list = []
        root = self._project_path.toLocalFile()
        for subdir, dirs, files in os.walk(root):
            for file in files:
                path = os.path.join(root, subdir, file)
                _, ext = os.path.splitext(path)
                if ext == '.qml':
                    file_list.append(path)
        self._qml_files = file_list
        self.qmlFilesChanged.emit(self._qml_files)
