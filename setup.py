'''
Copyright 2021, ESTECO s.p.a 

This file is part of BPSimpyLibrary.

BPSimpyLibrary is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation version 3 of the License.

BPSimpyLibrary is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with BPSimpyLibrary. If not, see <https://www.gnu.org/licenses/>.

This project was developed by Angelica Bianconi, Claudia Fracca, Francesca Meneghello with the supervision of  
Fabio Asnicar, Massimiliano de Leoni, Alessandro Turco, as part of the collaboration between ESTECO s.p.a and the University of Padua

'''

from setuptools import find_packages, setup

setup(
    name='BPSimpy',
    packages=find_packages(include=['BPSimpy']),
    version='0.1.0',
    description='BPSim Library',
    author='Angelica Bianconi, Francesca Meneghello, Claudia Fracca, Massimiliano De Leoni, Fabio Asnicar, Alessandro Turco',
    install_requires=['elementpath','lxml>=4.5','datetime','pandas','icalendar', 'isodate']
)