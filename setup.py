# setup.py
import os
from setuptools import setup, find_packages

def load_requirements(filename):
    with open(filename, encoding='utf-8') as f:
        lines = f.read().splitlines()
        # Filtra linee vuote o commenti
        return [line.strip() for line in lines if line and not line.startswith("#")]

setup(
    name="SISTEMA ALLARME",
    version="0.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=load_requirements("requirement.txt"),
)