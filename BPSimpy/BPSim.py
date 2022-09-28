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

import xml.etree.ElementTree as ET
from lxml import etree, objectify
from BPSimpy import Scenario 
from BPSimpy import utility

class BPSim:

	##Read file from path and create xml tree
	def __init__(self, path, verbosity=None):
		try:
			file = open(path, "r")
			self.tree = etree.parse(file)
			self.root = self.tree.getroot()
			self.createScenario=False
			self.verbosity=verbosity
			self.addSimulationModel()
			self.dictionary, processList, resourceList=utility.createBPMNelementDict(self.root)
			self.vendorNamespace = None
			self.scenarioList = []
		except FileNotFoundError:
			print("ERROR: File not found")
		except UnicodeDecodeError:
			print('ERROR: format file, BPSim needs xml extensions')
		
		
		

    ## Add simulation model to the BPMN model (Adding the root element and declaring the namespace)
	def addSimulationModel(self):
		self.root.set('{xmlns}bpsim',"http://www.bpsim.org/schemas/1.0")
		self.registerNamespace('bpsim',"http://www.bpsim.org/schemas/1.0")
		self.relationShip=etree.SubElement(self.root, utility.BPMN2 + "relationship", attrib={"type":"BPSimData"})
		self.extension_elements= etree.SubElement(self.relationShip, utility.BPMN2 + "extensionElements")
		self.bpsimData= etree.SubElement(self.extension_elements, utility.BPSIM + "BPSimData")
		utility.write_on_file(self.root, self.tree)
		if self.verbosity==0:
			print("INFO: added simulation model")
    
	def addXmlns(self, name, value):
		utility.checkNameSpace(name,value)
		self.root.set('{xmlns}'+ name, value)
		self.registerNamespace(name,value)
		utility.write_on_file(self.root, self.tree)
		self.vendorNamespace = value
		for scenario in self.scenarioList:
			scenario.setVendorNamespace(value)
			scenario.setVendorNameSpaceToElementParameters(value)

	def getVendorNameSpace(self):
		if self.vendorNamespace is None:
			raise ValueError('ERROR: Vendor namespace not found, to add using addXmlns method')
		return self.vendorNamespace
	
	def registerNamespace(self, tag, value):
		etree.register_namespace(tag, value)

	##Setup a scenario
	def addScenario(self, name=None, id=None, author=None, description=None, created=None, modified=None, version=None, vendor = None, inherits= None):
		scenario= Scenario.Scenario(name, id, author, description, created, modified, version, vendor, inherits, self.verbosity)
		attrib = scenario.filterScenarioAttributes()
		if bool(attrib):
			self.scenarioPointer=etree.SubElement(self.bpsimData, utility.BPSIM + "Scenario", attrib=attrib)
			scenario.setPointer(self.scenarioPointer, self.root, self.tree) 
			if self.vendorNamespace is not None:
				scenario.setVendorNamespace(self.vendorNamespace)
			self.scenarioList.append(scenario)
			utility.write_on_file(self.root, self.tree)
		else: 
			raise ValueError('ERROR: Empty Scenario')
		
		self.createScenario=True
		if self.verbosity==0:
			print("INFO: Added Scenario " + str(attrib))
		return scenario

	# Method to get the Id of BPMN element, given the name. If name is None the method returns a list of element without name,
	# otherwise if there are more element with the same name, it returns a list of id of these elements. Finally if the name is not
	# correct it returns empty list.
	def getIdByName(self, name = None):
		listId = []
		for key in self.dictionary:
			if self.dictionary.get(key) == name:
				listId.append(key)
		return listId

	# Method to get the Name of BPMN element, given the id. If element doesn't have a Name the method retunrs None.
	def getNameById(self, id):
		for key in list(self.dictionary.keys()):
			if key == id:
				if self.dictionary.get(key) == None:
					print("WARNING: Element without name")
					return None
				else:
					return self.dictionary.get(key)	
		if self.verbosity==0 or self.verbosity==1:	
			print("WARNING: Id not found")
			


