# coding=utf-8
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='python-qt-live-coding',
    version='0.2.2',
    packages=['livecoding'],
    package_dir={'': 'src'},
    url='https://github.com/machinekoder/python-qt-live-coding/',
    license='MIT',
    author='Alexander Rössler',
    author_email='alex@machinekoder.com',
    description='Live coding for Python, Qt and QML',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'six', 'python_qt_binding'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov',
            'pytest-qt'
        ]
    },
    scripts=[
        'bin/python_qt_live_coding'
    ],
    include_package_data=True,
)
