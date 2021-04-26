from setuptools import find_packages, setup

setup(
    name='BPSimpy',
    packages=find_packages(include=['BPSimpy']),
    version='0.1.0',
    description='BPSim Library',
    author='Angelica Bianconi, Francesca Meneghello, Claudia Fracca, Massimiliano De Leoni',
    install_requires=['elementpath','lxml','datetime','pandas','icalendar', 'isodate']
)