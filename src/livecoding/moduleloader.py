import os
import sys

from importlib import import_module, reload


def recursively_register_types(root_path):
    if root_path not in sys.path:
        sys.path.insert(0, root_path)

    for root, dirs, files in os.walk(root_path):
        if '.venv' in root or '__pycache__' in root:
            continue
        for file in files:
            _, ext = os.path.splitext(file)
            if ext != '.py':
                continue

            path = os.path.join(root, file)
            with open(path, 'rt') as f:
                data = f.read()
            if ('QML_IMPORT_NAME' in data and 'QML_IMPORT_MAJOR_VERSION' in data) or (
                file == '__init__.py' and 'def register_types()' in data
            ):
                _register_module(path, root_path)


def _register_module(file_path, root_path):
    path = os.path.relpath(file_path, root_path)
    path = path[:-3] if path.endswith('.py') else os.path.dirname(path)
    name = path.replace('/', '.')
    try:
        if name in sys.modules:
            reload(sys.modules[name])
            module = sys.modules[name]
        else:
            module = import_module(name)
        if hasattr(module, 'register_types'):
            module.register_types()
    except Exception as e:
        print(f'Error importing {name}: {e}')
