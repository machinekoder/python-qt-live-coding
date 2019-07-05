# -*- coding: utf-8 -*-
import os

from qtpy.QtCore import QObject, Property, Signal, QUrl, Slot


class ProjectBrowser(QObject):
    projectPathChanged = Signal(QUrl)
    qmlFilesChanged = Signal()
    extensionsChanged = Signal()

    def __init__(self, parent=None):
        super(ProjectBrowser, self).__init__(parent)

        path = os.path.dirname(os.path.abspath(__file__))
        self._project_path = QUrl.fromLocalFile(
            os.path.realpath(os.path.join(path, '..'))
        )
        self._qml_files = []
        self._extensions = []

        self.projectPathChanged.connect(self._update_files)
        self.extensionsChanged.connect(self._update_files)

    @Property(QUrl, notify=projectPathChanged)
    def projectPath(self):
        return self._project_path

    @projectPath.setter
    def projectPath(self, value):
        if self._project_path == value:
            return
        self._project_path = value
        self.projectPathChanged.emit(value)

    @Property('QStringList', notify=qmlFilesChanged)
    def qmlFiles(self):
        return self._qml_files

    @Property('QStringList', notify=extensionsChanged)
    def extensions(self):
        return self._extensions

    @extensions.setter
    def extensions(self, value):
        if self._extensions == value:
            return
        self._extensions = value
        self.extensionsChanged.emit()

    @Slot()
    def update(self):
        self._update_files()

    def _update_files(self):
        file_list = []
        root = self._project_path.toLocalFile()
        for subdir, dirs, files in os.walk(root):
            for file in files:
                path = os.path.join(root, subdir, file)
                _, ext = os.path.splitext(path)
                if ext[1:].lower() in self._extensions:
                    file_list.append(path)
        self._qml_files = file_list
        self.qmlFilesChanged.emit()
