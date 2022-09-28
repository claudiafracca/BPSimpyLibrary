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

from BPSimpy.Parameter import Parameter
from BPSimpy import utility
import xml.etree.ElementTree as ET
from lxml import etree, objectify

class ResourceParameter(Parameter):

	def __init__(self):
		super().__init__()
		self.resourcePointer = None
		self.quantityPointer = None
		self.selectionPointer = None
		self.availabilityPointer = None
		self.rolePointer = None

	# METHOD TO ADD RESOURCEPARAMETERS TAG
	def addResourcePointer(self):
		self.resourcePointer= etree.SubElement(self.elementRefPointer, utility.BPSIM + "ResourceParameters")
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResourceParameters added")

	# METHOD TO CHECK RESOURCEPARAMETERS TAG
	def checkResourceParametersTag(self):
		if self.resourcePointer is None:
			self.addResourcePointer()

	# METHODS TO ADD RESOURCE PARAMETER (QUANTITY - SELECTION - AVAILABILITY - ROLE)
	def addQuantity(self, value, validFor = None):
		self.checkResourceParametersTag()
		if super().checkNumericParameter(value):
			typeValue = "NumericParameter"
			utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
			self.quantityAttrib = {"value": str(value), "validFor": validFor}
			self.quantityAttrib = utility.filterNoneAttributes(self.quantityAttrib)
			if self.quantityPointer is None:
				self.quantityPointer=etree.SubElement(self.resourcePointer, utility.BPSIM + "Quantity")
			new_parameter= etree.SubElement(self.quantityPointer, utility.BPSIM + typeValue, attrib=self.quantityAttrib)
			utility.write_on_file(self.write, self.tree)
			if self.verbosity==0:
				print("INFO: Quantity added " + typeValue, self.quantityAttrib)
		else:
			raise ValueError("ERROR: Type of Quantity is not correct, must be NumericParameter")

	def addSelection(self, value= None, expression=None, result_request=None):
		self.checkResourceParametersTag()
		self.addSelectionParameter(value, expression, result_request)
		utility.write_on_file(self.write, self.tree)
		if result_request is None:
			if self.verbosity==0:
				print("INFO: Selection added " + self.typeValueS + " ", self.selectionAttrib)
		else:
			if self.verbosity==0:
				print("INFO: Selection added " + self.typeValueS + " ", result_request)

	def addSelectionParameter(self, value, expression, result_request):
		if value!= None and expression==None and result_request==None:
			if super().checkNumericParameter(value):
				self.typeValueS = 'NumericParameter'
				self.addSelectionValue(value,self.typeValueS)
			elif super().checkStringParameter(value):
				self.typeValueS = 'StringParameter'
				self.addSelectionValue(value,self.typeValueS)
			else:
				raise ValueError('ERROR: Type of Selection is not correct, must be NumericParameter, StringParameter or ExpressionParameter')
		elif value== None and expression!=None and result_request==None:
			if super().checkStringParameter(expression):
				self.typeValueS='ExpressionParameter'
				self.addSelectionValue(expression, self.typeValueS)
			else:
				raise ValueError("ERROR: ExpressionParameters must be a string")
		elif value== None and expression==None and result_request!=None:
			if self.selectionPointer is None:
				self.selectionPointer = etree.SubElement(self.resourcePointer, utility.BPSIM+"Selection")
			self.typeValueS = "ResultRequest"
			new_parameter= etree.SubElement(self.selectionPointer, utility.BPSIM + self.typeValueS)
			new_parameter.text=result_request
		else:
			raise ValueError("ERROR: Selection requires NumericParameter, StringParameter, ExpressionParameter or ResultRequest") 
	
	def addSelectionValue(self,value,typeValue):
		self.selectionAttrib = {"value":str(value)}
		if self.selectionPointer is None:
			self.selectionPointer = etree.SubElement(self.resourcePointer, utility.BPSIM+"Selection")
		new_parameter= etree.SubElement(self.selectionPointer, utility.BPSIM + typeValue, attrib = self.selectionAttrib)

	def addAvailability(self,value,validFor):
		self.checkResourceParametersTag()
		if super().checkBooleanParameter(value):
			typeValue = "BooleanParameter"
			utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
			self.availabilityAttrib = {"value": str(value), "validFor": validFor}
			self.availabilityAttrib = utility.filterNoneAttributes(self.availabilityAttrib)
			if self.availabilityPointer is None:
				self.availabilityPointer=etree.SubElement(self.resourcePointer, utility.BPSIM + "Availability")
			new_parameter= etree.SubElement(self.availabilityPointer, utility.BPSIM + typeValue, attrib=self.availabilityAttrib)
			utility.write_on_file(self.write, self.tree)
			if self.verbosity==0:
				print("INFO: Availability added " + typeValue, self.availabilityAttrib)
		else:
			raise ValueError("ERROR: Type of Availability is not correct, must be BooleanParameter")

	def addRole(self,value):
		self.checkResourceParametersTag()
		super().checkListType(value, 'value')
		if not all(isinstance(element, str) for element in value):
			raise ValueError('ERROR: Role in value must be all StringParameter')
		for role in value:
			typeValue = "StringParameter"
			attributes = {}
			attributes['value'] = role
			if self.rolePointer is None:
				self.rolePointer = etree.SubElement(self.resourcePointer, utility.BPSIM+'Role')
			new_parameter = etree.SubElement(self.rolePointer, utility.BPSIM+typeValue, attrib = attributes)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Role added " + typeValue, value)

	# METHODS TO SET RESOURCE PARAMETER (QUANTITY - SELECTION - AVAILABILITY - ROLE)
	def setSelection(self, value = None, expression = None, result_request = None):
		if self.selectionPointer is None:
			raise ValueError("ERROR: Selection not exixts")
		new_parameter = self.selectionPointer.findall("./" + utility.BPSIM + self.typeValueS)
		self.selectionPointer.remove(new_parameter[-1])
		self.addSelectionParameter(value, expression, result_request)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Selection updated ")

	
	def setQuantity(self, value, validFor = None):
		if self.quantityPointer is None:
			raise ValueError("ERROR: Quantity not exist")
		if not super().checkNumericParameter(value):
			raise ValueError("ERROR: Type of Quantity is not correct, must be NumericParameter")
		newQuantity=self.quantityPointer.findall("./" + utility.BPSIM + 'NumericParameter')
		newQuantity[-1].set('value',str(value))
		if validFor is not None:
			utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
			newQuantity[-1].set('validFor', validFor)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Quantity updated")

	def setAvailability(self,value,validFor=None):
		if self.availabilityPointer is None:
			raise ValueError("ERROR: Availability not exist")
		if not super().checkBooleanParameter(value):
			raise ValueError("ERROR: Type of Availability is not correct, must be BooleanParameter")
		newAvailability=self.availabilityPointer.findall("./" + utility.BPSIM + 'BooleanParameter')
		newAvailability[-1].set('value',str(value))
		if validFor is not None:
			utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
			newAvailability[-1].set('validFor', validFor)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Availability updated")

	def setRole(self,value):
		if self.rolePointer is None:
			raise ValueError("ERROR: Role not exist")
		super().checkListType(value, 'value')
		if not all(isinstance(element, str) for element in value):
			raise ValueError('ERROR: Role in value must be all StringParameter')
		self.resourcePointer.remove(self.rolePointer)
		self.rolePointer = etree.SubElement(self.resourcePointer, utility.BPSIM+'Role')
		for role in value:
			typeValue = "StringParameter"
			attributes = {}
			attributes['value'] = role
			new_parameter = etree.SubElement(self.rolePointer, utility.BPSIM+typeValue, attrib = attributes)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Role updated")
