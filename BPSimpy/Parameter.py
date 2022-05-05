from BPSimpy import utility
import datetime 
import xml.etree.ElementTree as ET
from lxml import etree, objectify 
from BPSimpy import Scenario


DISTRIBUTION_PARAMETER = {'BetaDistribution': ['shape', 'scale'], 'BinomialDistribution' : ['probability', 'trials'],
							'ErlangDistribution' : ['mean', 'k'], 'GammaDistribution':['shape', 'scale'], 'LogNormalDistribution':['mean', 'standardDeviation'],
							'NegativeExponentialDistribution':['mean'], 'NormalDistribution':['mean', 'standardDeviation'], 'PoissonDistribution':['mean'],
							'TriangularDistribution':['mode', 'min', 'max'], 'TruncatedNormalDistribution':['mean','standardDeviation','min','max'],
							'UniformDistribution':['min','max'], 'UserDistribution': ['points', 'discrete'], 'WeibullDistribution':['shape','scale']}

class Parameter():

	def __init__(self, verbosity=None):
		self.verbosity=verbosity


	# METHOD TO FILTER PARAMETER ATTRIBUTES
	def filterParameterAttributes(self, value, timeUnit, validFor):
		if timeUnit is not None:
			utility.checkTimeUnit(timeUnit)
		utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
		value=str(value)
		attributes=attributes = {"value": value, "timeUnit": timeUnit, "validFor": validFor}
		return utility.filterNoneAttributes(attributes)

	# METHODS TO CHECK PARAMETER TYPE
	def checkNumericParameter(self, value):
		if type(value) == int:
			return True
		else:
			return False

	def checkFloatingParameter(self, value):
		if type(value) == float:
			return True
		else:
			return False

	def checkDurationParameter(self, value):
		if type(value) == datetime.timedelta:
			return True
		else:
			return False

	def checkDateTimeParameter(self,value):
		if type(value) == datetime.datetime:
			return True
		else:
			return False

	def checkStringParameter(self,value):
		if type(value) == str:
			return True
		else:
			return False

	def checkBooleanParameter(self,value):
		if type(value) == bool:
			return True
		else:
			return False

	def checkParameterType(self, value):
		typeValue = ""
		if self.checkNumericParameter(value):
			typeValue = "NumericParameter"
		elif self.checkFloatingParameter(value):
			typeValue = "FloatingParameter"
		elif self.checkDurationParameter(value):
			typeValue = "DurationParameter" 
		elif self.checkStringParameter(value):
			typeValue = "StringParameter"
		elif self.checkBooleanParameter(value):
			typeValue = "BooleanParameter"
		elif self.checkDateTimeParameter(value):
			typeValue = 'DateTimeParameter'
		else:
			raise ValueError("ERROR: incorrect type")
		return typeValue

	def checkListType(self,listValues, listName):
		if type(listValues) is not list:
			raise ValueError('ERROR: ' + listName + ' must be a list')
		if len(listValues) == 0:
			raise ValueError('ERROR: empty list '+ listName)
			
	def checkEnumParameterType(self, enum_list):
		self.checkListType(enum_list, 'enum_list')
		return all(isinstance(element, type(enum_list[0])) for element in enum_list)

	def checkNameDistribution(self, nameDistribution):
		if nameDistribution not in DISTRIBUTION_PARAMETER.keys():
			raise ValueError('ERROR: ' + nameDistribution + ' is not correct, must be ', list(DISTRIBUTION_PARAMETER.keys()))
		
	def checkDistributionAttributes(self, nameDistribution, attributes):
		for element in list(attributes.keys()):
			if element not in DISTRIBUTION_PARAMETER[nameDistribution]:
				raise ValueError('ERROR: ' + nameDistribution + ' has only ' + str(DISTRIBUTION_PARAMETER.get(nameDistribution)))
		if len(attributes.keys()) != len(DISTRIBUTION_PARAMETER[nameDistribution]):
			raise ValueError('ERROR: insert all ' + nameDistribution + ' parameters: '+ str(DISTRIBUTION_PARAMETER.get(nameDistribution)))		
	
	def checkBooleanType(self, value, nameValue):
		if value is not None and type(value) is not bool:
			raise ValueError('ERROR: ' + nameValue + ' attribute must be boolean')

	def checkNumericDistributionAttributes(self, attributes):
		for key in list(attributes.keys()):
			if not isinstance(attributes.get(key) , (int, float)):
				raise ValueError('ERROR: attribute ' + key + ' needs numeric value')
			if key == 'probability':
				if attributes.get(key) < 0 or attributes.get(key) > 1:
					raise ValueError('ERROR: probability must be between 0 and 1')

	# METHOD TO FILTER DISTRIBUTION ATTRIBUTES
	def filterDistributionAttributes(self, timeUnit, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor):
		self.checkNameDistribution(nameDistribution)
		utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
		if nameDistribution == 'UserDistribution':
			attributes = {'discrete':discrete, 'points':points}
			attributes = utility.filterNoneAttributes(attributes)
			self.checkDistributionAttributes('UserDistribution',attributes)
			self.checkBooleanType(discrete, 'discrete')
		else:
			attributes = {'shape':shape, 'scale':scale, 'probability':probability, 'trials':trials,
								 'mean':mean, 'k':k, 'standardDeviation':standardDeviation, 'mode':mode, 
								 'min':min, 'max':max}
			attributes = utility.filterNoneAttributes(attributes)
			self.checkDistributionAttributes(nameDistribution, attributes)
			self.checkNumericDistributionAttributes(attributes)
		for key in list(attributes.keys()):
			attributes[key] = str(attributes[key])
		if timeUnit is not None:
			utility.checkTimeUnit(timeUnit)
			attributes['timeUnit'] = timeUnit
		if validFor is not None:
			attributes['validFor'] = validFor
		return attributes

	# METHOD TO CREATE DISTRIBUTION DATAPOINTS
	def createUserDistributionDataPoint(self, points, pointer, discrete, timeUnit):
		attrib = {'discrete': str(discrete)}
		user_parameter = etree.SubElement(pointer, utility.BPSIM + 'UserDistribution', attrib = attrib)
		if points is not None:
			utility.checkDataFrameType(points)
			#if sum(points['probability']) != 1:
			#	raise ValueError('ERROR: The sum of all data point probabilities must be equal to 1.0.')
			#else:
			new_points = points.apply(tuple, axis=1).tolist()
			for i in range(len(new_points)):
				new_parameter1= etree.SubElement(user_parameter, utility.BPSIM + 'UserDistributionDataPoint', attrib = {'probability': str(new_points[i][0])})
				value = new_points[i][1]
				typeValue = self.checkParameterType(value)
				if typeValue == "DurationParameter":
					value = utility.getDurationType(value)
					timeUnit = None
				new_value = etree.SubElement(new_parameter1, utility.BPSIM + typeValue, attrib = {'value': str(value)})
	
	# METHODS TO ADD PARAMETERS			
	def addParameterWithEnumList(self, value, timeUnit, validFor, tag, enum_list, pointer, parameterPointer, name, type):
		attributes = {}
		if value is None and enum_list is None:
			raise ValueError('ERROR: Insert value or enum_list')
		if value is not None and enum_list is not None:
			raise ValueError('ERROR: Insert only value or only enum_list')
		if name is not None:
			attributes['name'] = name
		if type is not None:
			attributes['type'] = type
		if parameterPointer is None:
			parameterPointer = etree.SubElement(pointer, utility.BPSIM + tag, attrib = attributes)
		attrib = {}
		if enum_list is not None: 
			if not self.checkEnumParameterType(enum_list):
				raise ValueError('ERROR: Elements in enum_list must be the same type')
			if len(enum_list)>1:
				typeValue = "EnumParameter"
				enumParameter = etree.SubElement(parameterPointer, utility.BPSIM+typeValue)
				self.addEnumParameter(enum_list, enumParameter)
				typeValue = 'EnumParameter'
				attrib['enum_list'] = enum_list
			if len(enum_list) == 1:
				if self.verbosity==0 or self.verbosity==1:
					print('WARNING: enum_list has only one element so it is insered as ConstantParameter')
				value = enum_list[0]
				typeValue = self.checkParameterType(value)
				attrib = self.addNewParameterValue(typeValue, value, parameterPointer,name, type, timeUnit, validFor)
		else:
			typeValue = self.checkParameterType(value)
			attrib = self.addNewParameterValue(typeValue, value, parameterPointer,name, type, timeUnit, validFor)
		utility.write_on_file(self.write, self.tree)
		return parameterPointer, typeValue, attrib

	def addNewParameterValue(self, typeValue, value, pointer, name, type,timeUnit=None, validFor=None):
		if typeValue == "DurationParameter":
			value = utility.getDurationType(value)
			timeUnit = None	
		attrib = self.filterParameterAttributes(value, timeUnit, validFor)
		new_parameter= etree.SubElement(pointer, utility.BPSIM + typeValue, attrib=attrib)
		return attrib

	def addEnumParameter(self, enum_list, enumParameter):
		for element in enum_list:
			typeValue = self.checkParameterType(element)
			if typeValue == "DurationParameter":
				element = utility.getDurationType(element)
			attributes = {}
			attributes['value'] = str(element)
			new_parameter = etree.SubElement(enumParameter, utility.BPSIM+typeValue, attrib = attributes)

	def addExpressionParameter(self, expression, pointer, typeValue):
		if self.checkStringParameter(expression):
			new_parameter = etree.SubElement(pointer, utility.BPSIM+typeValue, attrib = {"value":expression})
		else:
			raise ValueError("ERROR: expression must be XPATH string")
	
	# METHODS TO SET PARAMETERS
	def setParameterWithEnumList(self, type, pointer, attrib, value = None, enum_list = None, timeUnit = None, validFor = None):
		if value is not None and enum_list is not None:
			raise ValueError('ERROR: insert only value or only enum_list')
		if value is not None and enum_list is None:
			self.setValue(value, pointer, timeUnit, validFor,type)
		if value is None and enum_list is not None:
			pointer.remove(pointer.findall("./" + utility.BPSIM + type)[-1])
			self.setEnumList(pointer, enum_list)
		utility.write_on_file(self.write, self.tree)

	def setValue(self, value, pointer, timeUnit, validFor,type):
		typeValue= self.checkParameterType(value)
		enumParameter = pointer.findall("./" + utility.BPSIM + 'EnumParameter')
		if len(enumParameter)==0:
			newTimeParameter=pointer.findall("./" + utility.BPSIM + type)
			attrib = self.filterParameterAttributes(value, timeUnit, validFor)
			if typeValue == 'NumericParameter':
				pointer.remove(newTimeParameter[-1])
				newTimeParameter=etree.SubElement(pointer, utility.BPSIM + typeValue,attrib=attrib)
			elif typeValue == 'FloatingParameter':
				pointer.remove(newTimeParameter[-1])
				newTimeParameter=etree.SubElement(pointer, utility.BPSIM + typeValue,attrib=attrib)
			elif typeValue == 'DurationParameter':
				value = utility.getDurationType(value)
				if 'timeUnit' in attrib:
					del attrib['timeUnit']
				pointer.remove(newTimeParameter[-1])
				newTimeParameter=etree.SubElement(pointer, utility.BPSIM + typeValue,attrib=attrib)
		else:
			pointer.remove(enumParameter[-1])
			attrib = self.addNewParameterValue(typeValue, value, pointer, timeUnit, validFor)

	def setEnumList(self, pointer, enum_list):
		if not self.checkEnumParameterType(enum_list):
			raise ValueError('ERROR: Elements in enum_list must be the same type')
		enumParameter = etree.SubElement(pointer, utility.BPSIM+'EnumParameter')
		if len(enum_list) > 1:
			typeValue = self.addEnumParameter(enum_list, enumParameter)
		elif len(enum_list) == 1:
			pointer.remove(enumParameter)
			for element in pointer.getchildren():
				pointer.remove(element)
			if self.verbosity==0 or self.verbosity==1:
				print('WARNING: enum_list has only one element so it is insered as ConstantParameter')
			value = enum_list[0]
			typeValue = super().checkParameterType(value)
			self.addNewParameterValue(typeValue, value,pointer)