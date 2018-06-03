# -*- coding: utf-8 -*-
import pytest
from PyQt5.QtCore import QUrl
from PyQt5.QtTest import QSignalSpy


@pytest.fixture
def watcher():
    from livecoding import FileWatcher
    return FileWatcher()


def test_creating_and_writing_file_in_directory_emits_signal(qtbot, tmpdir, watcher):
    subdir = tmpdir.mkdir('sub')
    watcher.fileUrl = QUrl('file://' + str(subdir))
    watcher.enabled = True
    watcher.recursive = True

    spy = QSignalSpy(watcher.fileChanged)

    path = str(subdir.join('test.txt'))
    with open(path, 'wt') as f:
        f.write('foo')

    spy.wait(100)
    assert len(spy) == 1


def test_changing_file_emits_signal(qtbot, tmpdir, watcher):
    subdir = tmpdir.mkdir('sub')
    path = str(subdir.join('test.txt'))
    watcher.recursive = False

    with open(path, 'wt') as f:
        f.write('foo')

    watcher.fileUrl = QUrl('file://' + path)
    watcher.enabled = True

    spy = QSignalSpy(watcher.fileChanged)
    with open(path, 'at') as f:
        f.write('bar')
    spy.wait(100)
    assert len(spy) == 1


def test_creating_and_writing_file_on_filter_list_doesnt_emit_signal(qtbot, tmpdir, watcher):
    subdir = tmpdir.mkdir('sub')
    watcher.nameFilters = ['.#*']
    watcher.fileUrl = QUrl('file://' + str(subdir))
    watcher.enabled = True
    watcher.recursive = True

    spy = QSignalSpy(watcher.fileChanged)
    assert len(spy) == 0  # I don't why this is necessary, but it is

    path = str(subdir.join('.#test.txt'))
    with open(path, 'wt') as f:
        f.write('foo')

    spy.wait(100)
    assert len(spy) == 0


# TODO: add more tests for creating file in subdirectory, deleting files, ...
