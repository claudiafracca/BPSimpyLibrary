from BPSimpy.Parameter import Parameter
from BPSimpy import utility
import xml.etree.ElementTree as ET
from lxml import etree, objectify

class CostParameter(Parameter):

	def __init__(self):
		super().__init__()
		self.costPointer = None
		self.fixedCostPointer = None
		self.unitCostPointer = None
		
	# METHOD TO ADD COSTPARAMETERS TAG
	def addCostPointer(self):
		self.costPointer= etree.SubElement(self.elementRefPointer, utility.BPSIM + "CostParameters")
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResourceParameters added")
	
	# METHOD TO CHECK COSTPARAMETERS TAG
	def checkCostParametersTag(self):
		if self.costPointer is None:
			self.addCostPointer()

	# METHODS TO ADD COST PARAMETER (FIXEDCOST - UNITCOST)
	def addFixedCost(self,value=None, validFor=None, resultRequest=None):
		self.checkCostParametersTag()
		if self.fixedCostPointer is None:
			self.fixedCostPointer=etree.SubElement(self.costPointer, utility.BPSIM + 'FixedCost')
		self.typeValueFC, self.fixedCostPointer, self.fixedCostAttributes = self.addCostParameter(value,validFor,resultRequest,self.fixedCostPointer, 'FixedCost')
		utility.write_on_file(self.write, self.tree)
		if resultRequest is None:
			if self.verbosity==0:
				print("INFO: FixedCost added " + self.typeValueFC + " ", self.fixedCostAttributes)
		else:
			if self.verbosity==0:
				print("INFO: FixedCost added " + self.typeValueFC + " ", resultRequest)
				
	def addUnitCost(self,value=None,validFor=None, resultRequest=None):
		self.checkCostParametersTag()
		if self.unitCostPointer is None:
			self.unitCostPointer=etree.SubElement(self.costPointer, utility.BPSIM + 'UnitCost')
		self.typeValueUC, self.unitCostPointer, self.unitCostAttributes = self.addCostParameter(value,validFor,resultRequest,self.unitCostPointer, 'UnitCost')
		utility.write_on_file(self.write, self.tree)
		if resultRequest is None:
			if self.verbosity==0:
				print("INFO: UnitCost added " + self.typeValueUC + " ", self.unitCostAttributes)
		else:
			if self.verbosity==0:
				print("INFO: UnitCost added " + self.typeValueUC + " ", resultRequest)
	
	def addCostParameter(self,value,validFor,resultRequest,pointer,name):
		attributes=None
		if value is None and validFor is None and resultRequest is not None:
			typeValue = "ResultRequest"
			new_parameter=etree.SubElement(pointer, utility.BPSIM + typeValue)
			new_parameter.text=resultRequest
		elif value is not None	and resultRequest is None:
			typeValue=super().checkParameterType(value)
			if not super().checkNumericParameter(value) and not super().checkFloatingParameter(value):
				raise ValueError('ERROR: type of '+name+' must be NumericParameter or FloatingParameter')
			utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
			attributes = {"value": str(value), "validFor": validFor}
			attributes = utility.filterNoneAttributes(attributes)
			new_parameter=etree.SubElement(pointer, utility.BPSIM + typeValue, attrib=attributes)
		else:
			raise ValueError('ERROR: insert only value or resultRequest')
		return typeValue, pointer, attributes

	# METHODS TO SET COST PARAMETER (FIXEDCOST - UNITCOST)
	def setFixedCost(self,value= None, validFor = None, resultRequest = None):
		if self.fixedCostPointer is None:
			raise ValueError("ERROR: FixedCost not exists")
		new_parameter= self.fixedCostPointer.findall("./"+ utility.BPSIM + self.typeValueFC)
		self.fixedCostPointer.remove(new_parameter[-1])
		self.typeValueFC, self.fixedCostPointer, self.filterNoneAttributes = self.addCostParameter(value,validFor,resultRequest,self.fixedCostPointer,'FixedCost')
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: FixedCost updated" )

	def setUnitCost(self,value= None, validFor = None, resultRequest = None):
		if self.unitCostPointer is None:
			raise ValueError("ERROR: UnitCost not exists")
		new_parameter= self.unitCostPointer.findall("./"+ utility.BPSIM + self.typeValueUC)
		self.unitCostPointer.remove(new_parameter[-1])
		self.typeValueUC, self.unitCostPointer, self.unitCostAttributes = self.addCostParameter(value,validFor,resultRequest,self.unitCostPointer,'UnitCost')
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: UnitCost updated" )

	