# coding=utf-8
import sys

import pytest

from livecoding import recursively_register_types


@pytest.fixture
def project_dir(tmpdir):
    path = tmpdir.mkdir('module1')
    file = path.join('__init__.py')
    file.write('''\
def register_types():
    print('registered module1')
    ''')
    file = path.join('bla.py')
    file.write('# nothing here')

    path = path.mkdir('module2')
    file = path.join('__init__.py')
    file.write('''\
def register_types():
    print('registered module2')
    ''')

    path = tmpdir.mkdir('other_dir')
    file = path.join('__init__.py')
    file.write('''\
print('bar')
    ''')
    return str(tmpdir)


def test_loader_registers_all_modules_in_subdir_correctly(project_dir):
    recursively_register_types(project_dir)

    assert 'module1' in sys.modules.keys()
    assert 'module1.module2' in sys.modules.keys()
