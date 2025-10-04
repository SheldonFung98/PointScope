from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools import setup, find_packages
import os


setup(
    name='PointScope',
    python_requires=">=3",
    version='1.0',
    author="Sheldon Fung",
    url="https://github.com/SheldonFung98/PointScope",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'open3d>=0.10.0',
        'vedo==2025.5.3',
    ],
)