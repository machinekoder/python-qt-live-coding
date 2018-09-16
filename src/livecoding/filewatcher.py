# -*- coding: utf-8 -*-
import os
from fnmatch import fnmatch

from python_qt_binding.QtCore import (
    QObject, pyqtProperty, pyqtSignal, QFileSystemWatcher, QUrl, QDirIterator, qWarning
)


class FileWatcher(QObject):

    fileUrlChanged = pyqtSignal(QUrl)
    enabledChanged = pyqtSignal(bool)
    recursiveChanged = pyqtSignal(bool)
    nameFiltersChanged = pyqtSignal('QStringList')
    fileChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(FileWatcher, self).__init__(parent)

        self._file_url = QUrl()
        self._enabled = True
        self._recursive = False
        self._name_filters = []

        self._file_system_watcher = QFileSystemWatcher()

        self.fileUrlChanged.connect(self._update_watched_file)
        self.enabledChanged.connect(self._update_watched_file)
        self.recursiveChanged.connect(self._update_watched_file)
        self.nameFiltersChanged.connect(self._update_watched_file)
        self._file_system_watcher.fileChanged.connect(self._on_watched_file_changed)
        self._file_system_watcher.directoryChanged.connect(self._on_watched_directory_changed)

    @pyqtProperty(QUrl, notify=fileUrlChanged)
    def fileUrl(self):
        return self._file_url

    @fileUrl.setter
    def fileUrl(self, value):
        if self._file_url == value:
            return
        self._file_url = value
        self.fileUrlChanged.emit(value)

    @pyqtProperty(bool, notify=enabledChanged)
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if self._enabled == value:
            return
        self._enabled = value
        self.enabledChanged.emit(value)

    @pyqtProperty(bool, notify=recursiveChanged)
    def recursive(self):
        return self._recursive

    @recursive.setter
    def recursive(self, value):
        if self._recursive == value:
            return
        self._recursive = value
        self.recursiveChanged.emit(value)

    @pyqtProperty('QStringList', notify=nameFiltersChanged)
    def nameFilters(self):
        return self._name_filters

    @nameFilters.setter
    def nameFilters(self, value):
        if self._name_filters == value:  # note: we compare the reference here, not the actual list
            return
        self._name_filters = value
        self.nameFiltersChanged.emit(value)

    def _update_watched_file(self):
        files = self._file_system_watcher.files()
        if any(files):
            self._file_system_watcher.removePaths(files)
        directories = self._file_system_watcher.directories()
        if any(directories):
            self._file_system_watcher.removePaths(directories)

        if not self._file_url.isValid() or not self._enabled:
            return

        if not self._file_url.isLocalFile():
            qWarning('Can only watch local files')

        local_file = self._file_url.toLocalFile()
        if local_file is '':
            return False

        if self._recursive and os.path.isdir(local_file):
            new_paths = {local_file}
            self._file_system_watcher.addPath(local_file)

            it = QDirIterator(local_file, QDirIterator.Subdirectories | QDirIterator.FollowSymlinks)
            while it.hasNext():
                filepath = it.next()
                filename = os.path.basename(filepath)
                filtered = False
                for wildcard in self._name_filters:
                    if fnmatch(filename, wildcard):
                        filtered = True
                        break
                if filename == '..' or filename == '.' or filtered:
                    continue
                self._file_system_watcher.addPath(filepath)
                new_paths.add(filepath)

            return new_paths != set(files).union(set(directories))

        elif os.path.exists(local_file):
            self._file_system_watcher.addPath(local_file)

        else:
            qWarning('File to watch does not exist')
        return False

    def _on_watched_file_changed(self):
        if self._enabled:
            self.fileChanged.emit()

    def _on_watched_directory_changed(self, _):
        if self._update_watched_file():
            self._on_watched_file_changed()
