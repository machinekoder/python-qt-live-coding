# coding=utf-8
from setuptools import setup

setup(
    name='python-qt-live-coding',
    version='0.1.0',
    packages=['livecoding'],
    package_dir={'': 'src'},
    url='https://github.com/machinekoder/python-qt-live-coding/',
    license='MIT',
    author='Alexander Rössler',
    author_email='alex@machinekoder.com',
    description='Live coding for PyQt',
    install_requires=['PyQt5', 'six'],
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
    ]
)
