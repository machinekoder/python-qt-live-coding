# -*- coding: utf-8 -*-
import pytest
import shutil
import os
from qtpy.QtCore import QUrl
from qtpy.QtTest import QSignalSpy


SIGNAL_WAIT_TIMEOUT = 50


@pytest.fixture
def watcher():
    from livecoding import FileWatcher

    return FileWatcher()


def test_creating_and_writing_file_in_directory_emits_signal(qtbot, tmpdir, watcher):
    watcher.fileUrl = QUrl('file://' + str(tmpdir))
    watcher.enabled = True
    watcher.recursive = True
    spy = QSignalSpy(watcher.fileChanged)

    f = tmpdir.join('test.txt')
    f.write('foo')

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) == 1


def test_changing_file_emits_signal(qtbot, tmpdir, watcher):
    f = tmpdir.join('test.txt')
    f.write('foo')
    watcher.recursive = False
    watcher.fileUrl = QUrl('file://' + str(f))
    watcher.enabled = True
    spy = QSignalSpy(watcher.fileChanged)

    f.write('bar')

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) == 1


def test_creating_and_writing_file_on_filter_list_doesnt_emit_signal(
    qtbot, tmpdir, watcher
):
    watcher.nameFilters = ['.#*']
    watcher.fileUrl = QUrl('file://' + str(tmpdir))
    watcher.enabled = True
    watcher.recursive = True
    spy = QSignalSpy(watcher.fileChanged)

    f = tmpdir.join('.#test.txt')
    f.write('foo')

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) == 0


def test_renaming_file_emits_signal(qtbot, tmpdir, watcher):
    f = tmpdir.join('supp')
    f.write('pncp0A')
    watcher.recursive = True
    watcher.fileUrl = QUrl('file://' + str(tmpdir))
    watcher.enabled = True
    spy = QSignalSpy(watcher.fileChanged)

    os.rename(str(f), os.path.join(str(tmpdir), 'energist'))

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) > 0


def test_deleting_file_emits_signal(qtbot, tmpdir, watcher):
    f = tmpdir.join('lowered')
    f.write('pncp0A')
    watcher.recursive = True
    watcher.fileUrl = QUrl('file://' + str(tmpdir))
    watcher.enabled = True
    spy = QSignalSpy(watcher.fileChanged)

    os.remove(str(f))

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) == 1


def test_deleting_directory_emits_signal(qtbot, tmpdir, watcher):
    subdir = tmpdir.mkdir('flukily')
    f = subdir.join("yeasts")
    f.write("Wlb2Msh")  # need to create a file inside the tmpdir to force creation
    watcher.recursive = True
    watcher.fileUrl = QUrl('file://' + str(tmpdir))
    watcher.enabled = True
    spy = QSignalSpy(watcher.fileChanged)

    shutil.rmtree(str(subdir))

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) == 1


def test_creating_file_in_subdirectory_emits_signal(qtbot, tmpdir, watcher):
    subdir = tmpdir.mkdir('sub')
    watcher.recursive = True
    watcher.fileUrl = QUrl('file://' + str(tmpdir))
    watcher.enabled = True
    spy = QSignalSpy(watcher.fileChanged)

    f = subdir.join('hagglers.foo')
    f.write('DNsqu')

    spy.wait(SIGNAL_WAIT_TIMEOUT)
    assert len(spy) == 1
