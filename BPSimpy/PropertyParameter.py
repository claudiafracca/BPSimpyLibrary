from BPSimpy.Parameter import Parameter
from BPSimpy import utility
import xml.etree.ElementTree as ET
from lxml import etree, objectify

class PropertyParameter(Parameter):

	def __init__(self):
		super().__init__()
		self.propertyPointer = None
		self.queueLengthPointer = None
		self.pointer= None
		self.nameDistribution = None

		
	## METHOD TO ADD PROPERTY AS CONSTANT, DISTRIBUTION, ENUMERATION, EXPRESSION
	def addProperty(self, name, type=None, value=None, enum_list=None,timeUnit = None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression=None):
		self.checkPropertyParametersTag()
		attrib = {}
		if value is None and nameDistribution is None and enum_list is None and expression is None:
			raise ValueError('ERROR: to add Property insert value or enum_list or nameDistribution or expression')
		if ((value is not None and nameDistribution is None) or (enum_list is not None and nameDistribution is None)) and expression is None:
			## ADD CONSTANT PARAMETER OR ENUM
			self.pointer, self.typeValue, self.propertyAttrib = super().addParameterWithEnumList(value, timeUnit, None, "Property", enum_list,self.propertyPointer,None, name, type)
			if self.verbosity==0:
				print("INFO: Property added " + "Name: " +name + " " +self.typeValue, self.propertyAttrib)
		elif nameDistribution is not None and value is None and enum_list is None and expression is None:
			## ADD DISTRIBUTION
			self.nameDistribution = nameDistribution
			self.typeValue = self.nameDistribution
			self.propertyAttrib= super().filterDistributionAttributes(timeUnit, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor)
			if name is not None:
				attrib['name'] = name
			if type is not None:
				attrib['type'] = type
			self.pointer=etree.SubElement(self.propertyPointer, utility.BPSIM + "Property", attrib = attrib)
			if nameDistribution == 'UserDistribution':
				super().createUserDistributionDataPoint(points, self.propertyPointer, discrete, timeUnit)
			else:
				new_parameter= etree.SubElement(self.pointer, utility.BPSIM + nameDistribution, attrib = self.propertyAttrib)
			if self.verbosity==0:
				if nameDistribution != 'UserDistribution':
					print("INFO: Property added " + name + " " + nameDistribution, self.propertyAttrib)
				else:
					print("INFO: Property added " + name + " " + nameDistribution + " Discrete: ",self.propertyAttrib['discrete'], " Points: ", points.to_dict())
		elif value is None and nameDistribution is None and enum_list is None and expression is  not None:
			## ADD EXPRESSION
			if super().checkStringParameter(expression):
				if name is not None:
					attrib['name'] = name
				if type is not None:
					attrib['type'] = type
				self.pointer=etree.SubElement(self.propertyPointer, utility.BPSIM + "Property", attrib = attrib)
				self.typeValue = "ExpressionParameter"
				new_parameter= etree.SubElement(self.pointer, utility.BPSIM + self.typeValue, attrib = {"value": expression})
				if self.verbosity==0:
					print("INFO: Property " + name + " added ExpressionParameter ", str({"value": expression}) )
			else:
				raise ValueError("ERROR: ExpressionParameter must be a String")
		else:
			raise ValueError('ERROR: to add Property insert value or enum_list or nameDistribution or expression')
		utility.write_on_file(self.write, self.tree)

	## METHOD TO SET PROPERTY ATTRIBUTE
	def setProperty(self, name, type=None, value=None, enum_list=None,timeUnit = None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None):
		if self.pointer is None:
			raise ValueError("ERROR: Property not exist")
		if value is None and nameDistribution is None and enum_list is None and expression is None:
			raise ValueError('ERROR: to set Property insert value or enum_list or nameDistribution or expression')
		self.pointer.attrib['name'] = name
		if type is not None:
			self.pointer.attrib['type'] = type
		if nameDistribution is None and expression is None:
			if self.typeValue == self.nameDistribution:
				self.propertyAttrib = {}
			super().setParameterWithEnumList(self.typeValue, self.pointer, self.propertyAttrib,value,enum_list, timeUnit, None)
		newProperty=self.pointer.find("./" + utility.BPSIM + self.typeValue)
		self.pointer.remove(newProperty)
		if value is None and nameDistribution is not None and enum_list is None and expression is None:
			super().checkNameDistribution(nameDistribution)
			newPropertyAttrib= super().filterDistributionAttributes(timeUnit,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor)
			if nameDistribution == 'UserDistribution':
				super().createUserDistributionDataPoint(points, self.pointer, discrete, timeUnit)
			else:
				new_parameter= etree.SubElement(self.pointer, utility.BPSIM + nameDistribution, attrib = newPropertyAttrib)
		elif value is None and nameDistribution is None and enum_list is None and expression is  not None:
			if super().checkStringParameter(expression):
				self.typeValue = "ExpressionParameter"
				newProperty= etree.SubElement(self.pointer, utility.BPSIM + self.typeValue, attrib = {"value": expression})
			else:
				raise ValueError("ERROR: ExpressionParameter must be a String")
		else:
			raise ValueError('ERROR: to set Property insert value or enum_list or nameDistribution or expression')
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Property updated")

	## METHOD TO ADD QUEUELENGTH
	def addQueueLength(self, resultRequest): 
		self.checkPropertyParametersTag()
		if self.queueLengthPointer is None:
			self.queueLengthPointer=etree.SubElement(self.propertyPointer, utility.BPSIM + "QueueLength")
		result = etree.SubElement(self.queueLengthPointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(resultRequest)
		result.text=resultRequest
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: QueueLength added ResultRequest: ", resultRequest)

	## METHOD TO SET QUEUELENGTH
	def setQueueLength(self, resultRequest):
		if self.queueLengthPointer is None:
			raise ValueError("ERROR: QueueLength not exist")
		result = self.queueLengthPointer.findall("./"+ utility.BPSIM + 'ResultRequest')
		self.queueLengthPointer.remove(result[-1])
		new_result = etree.SubElement(self.queueLengthPointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(resultRequest)
		new_result.text=resultRequest
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest updated")

	## METHOD TO ADD PROPERTYPARAMETERS TAG
	def addPropertyParameterTag(self):
		self.propertyPointer= etree.SubElement(self.elementRefPointer, utility.BPSIM + "PropertyParameters")
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: PropertyParameters added")

	## METHOD TO CHECK PROPERTYPARAMETERS TAG
	def checkPropertyParametersTag(self):
		if self.propertyPointer is None:
			self.addPropertyParameterTag()