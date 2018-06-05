# coding=utf-8
import os
import sys

from importlib import import_module
from six.moves import reload_module


def recursively_register_types(root_path):
    if root_path not in sys.path:
        sys.path.insert(0, root_path)

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file != '__init__.py':
                continue
            path = os.path.join(root, file)
            with open(path, 'rt') as f:
                data = f.read()
            if 'def register_types()' not in data:
                continue
            _register_module(path, root_path)


def _register_module(file_path, root_path):
    path = os.path.relpath(file_path, root_path)
    name = os.path.dirname(path).replace('/', '.')
    try:
        if name in sys.modules:
            reload_module(sys.modules[name])
            module = sys.modules[name]
        else:
            module = import_module(name)
        module.register_types()
    except Exception as e:
        print('Error importing %s: %s' % (name, e))
