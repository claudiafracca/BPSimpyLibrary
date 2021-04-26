import datetime
from BPSimpy import utility
import xml.etree.ElementTree as ET
from lxml import etree, objectify 
from BPSimpy.Parameter import Parameter

class ControlParameters(Parameter):

	def __init__(self):
		super().__init__()
		self.controlPointer = None
		self.triggerTimePointer = None
		self.triggerCountPointer = None
		self.probabilityPointer = None
		self.conditionPointer= None

	## METHOD TO ADD CONTROL-PARAMETER TAG
	def addControl(self):
		self.controlPointer=etree.SubElement(self.elementRefPointer, utility.BPSIM + "ControlParameters")
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ControlParameters added")

	## METHOD TO CHECK CONTROL-PARAMETER TAG
	def checkControlParametersTag(self):
		if self.controlPointer is None:
			self.addControl()

	## METHODS TO ADD AND SET INTERTRIGGERTIME AS CONSTANT, DISTRIBUTION, ENUMERATION
	def addInterTriggerTimer(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None):
		self.checkControlParametersTag()
		if value is None and nameDistribution is None and enum_list is None:
			raise ValueError('ERROR: To add InterTriggerTimer insert value or enum_list or nameDistribution')
		if value is not None and nameDistribution is None or enum_list is not None and nameDistribution is None:
			self.triggerTimePointer,self.typeValueTT, self.triggerTimerAttrib = super().addParameterWithEnumList(value, timeUnit, validFor, "InterTriggerTimer", enum_list,self.controlPointer, self.triggerTimePointer,None, None)
			if self.verbosity==0:
				print("INFO: InterTriggerTimer added " + self.typeValueTT + " ", self.triggerTimerAttrib)
		elif nameDistribution is not None and value is None and enum_list is None:
			self.nameDistribution = nameDistribution
			self.typeValueTT = self.nameDistribution
			self.triggerTimerAttrib= super().filterDistributionAttributes(timeUnit, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor)
			if self.triggerTimePointer is None:
				self.triggerTimePointer=etree.SubElement(self.controlPointer, utility.BPSIM + "InterTriggerTimer")
			if nameDistribution == 'UserDistribution':
				super().createUserDistributionDataPoint(points, self.triggerTimePointer, discrete, timeUnit)
			else:
				new_parameter= etree.SubElement(self.triggerTimePointer, utility.BPSIM + nameDistribution, attrib = self.triggerTimerAttrib)
			if self.verbosity==0:
				if nameDistribution != 'UserDistribution':
					print("INFO: InterTriggerTimer added " + nameDistribution, self.triggerTimerAttrib)
				else:
					print("INFO: InterTriggerTimer added " + nameDistribution + " Discrete: ",self.triggerTimerAttrib['discrete'], " Points: ", points.to_dict())
			utility.write_on_file(self.write, self.tree)
		elif nameDistribution is not None and value is not None and enum_list is not None:
			raise ValueError('ERROR: for InterTriggerTimer insert value or enum_list or nameDistribution')
	
	def setInterTriggerTimer(self, value=None, enum_list = None,timeUnit = None, validFor = None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None,result_request=None):
		if self.triggerTimePointer is None:
			raise ValueError("ERROR: TriggerTimer not exist")
		if value is None and nameDistribution is None and enum_list is None and result_request is None:
			raise ValueError('ERROR: To set InterTriggerTimer insert value or nameDistribution or enum_list or result_request')
		if nameDistribution is None and result_request is None:
			if self.typeValueTT == self.nameDistribution:
				self.triggerTimerAttrib = {}
			super().setParameterWithEnumList(self.typeValueTT, self.triggerTimePointer, self.triggerTimerAttrib,value,enum_list, timeUnit, validFor)
		newTriggerTimer=self.triggerTimePointer.findall("./" + utility.BPSIM + self.typeValueTT)
		if len(newTriggerTimer) > 0:
			self.triggerTimePointer.remove(newTriggerTimer[-1])
		if value is None and nameDistribution is not None and enum_list is None and result_request is None:
			super().checkNameDistribution(nameDistribution)
			newTriggerTimerAttrib= super().filterDistributionAttributes(timeUnit,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor)
			if nameDistribution == 'UserDistribution':
				super().createUserDistributionDataPoint(points, self.triggerTimePointer, discrete, timeUnit)
			else:
				new_parameter= etree.SubElement(self.triggerTimePointer, utility.BPSIM + nameDistribution, attrib = newTriggerTimerAttrib)
		elif result_request is not None:
			utility.checkResultRequest(result_request)
			if result_request == 'count':
				raise ValueError("ERROR: result_request must be min, max, mean or sum")
			attributes = {'value':value,'timeUnit': timeUnit, 'validFor': validFor,'nameDistribution':nameDistribution,'shape':shape, 
							'scale':scale, 'probability':probability, 'trials':trials,
							'mean':mean, 'k':k, 'standardDeviation':standardDeviation, 'mode':mode, 
							'min':min, 'max':max, 'discrete': discrete, 'points':points,'enum_list':enum_list} 
			utility.filterNoneAttributes(attributes)
			if len(attributes)==0:
				self.addInterTriggerTimerResultRequest(result_request)
			else:
				raise ValueError("ERROR: insert only result_request parameter")
		else:
			raise ValueError('ERROR: if InterTriggerTimer is NumericParameter, FloatingParameter, DurationParameter add value, add nameDistribution otherwise')
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: InterTriggerTimer updated")

	## METHODS TO ADD AND SET TRIGGERCOUNT AS CONSTANT, DISTRIBUTION, ENUMERATION
	def addTriggerCount(self, value=None, validFor=None):
		self.checkControlParametersTag()
		if type(value) == int:
			self.typeValueTC = "NumericParameter"
			self.triggerCountAttrib = {"value": str(value), "validFor": validFor}
			self.triggerCountAttrib = utility.filterNoneAttributes(self.triggerCountAttrib)
			if self.triggerCountPointer is None:
				self.triggerCountPointer=etree.SubElement(self.controlPointer, utility.BPSIM + "TriggerCount")
			new_parameter= etree.SubElement(self.triggerCountPointer, utility.BPSIM + self.typeValueTC, attrib=self.triggerCountAttrib)
			utility.write_on_file(self.write, self.tree)
			utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
			if self.verbosity==0:
				print("INFO: TriggerCount added " + self.typeValueTC + " ", self.triggerCountAttrib)	
		else:
			raise ValueError("ERROR: Type of TriggerCount is not correct, must be NumericParameter")
	
	def setTriggerCount(self, value=None, validFor=None, result_request = None):
		if self.triggerCountPointer is None:
			raise ValueError("ERROR: TriggerCount not exist")
		if value is None and result_request is None:
			raise ValueError("ERROR: insert value or result_request")
		newTriggerCount=self.triggerCountPointer.findall("./" + utility.BPSIM + self.typeValueTC)
		if len(newTriggerCount) > 0:
			self.triggerCountPointer.remove(newTriggerCount[-1])
		if value is not None and result_request is None:
			if not super().checkNumericParameter(value):
				raise ValueError("ERROR: Type of TriggerCount is not correct, must be NumericParameter")
			self.typeValueTC = "NumericParameter"
			newTriggerCount = etree.SubElement(self.triggerCountPointer, utility.BPSIM + "NumericParameter", attrib={'value':str(value)})
			if validFor is not None:
				utility.checkCalendar(self.scenario.getCalendars(), validFor, self.verbosity)
				newTriggerCount.set('validFor', validFor)
		elif value is None and result_request is not None:
			attributes = {'value':value, 'validFor':validFor}
			attributes = utility.filterNoneAttributes(attributes)
			if len(attributes)==0:
				self.typeValueTC="ResultRequest"
				request=etree.SubElement(self.triggerCountPointer, utility.BPSIM + "ResultRequest")
				request.text=result_request
			else:
				raise ValueError("ERROR: insert only result_request parameter")
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: TriggerCount updated")

	## CHECK VALUE FOR PROBABILITY-PARAMETER
	def checkProbability(self, value):
		typeValue = ""
		if super().checkNumericParameter(value):
			typeValue = "NumericParameter"
		elif super().checkFloatingParameter(value):
			typeValue = "FloatingParameter"	
		else:
			raise ValueError("ERROR: Type of Probability is not correct, must be NumericParameter or FloatingParameter")
		if value < 0 or value > 1:
			raise ValueError("ERROR: Probability must be between 0 and 1")
		return typeValue

	## METHODS TO ADD AND SET PROBABILITY
	def addProbability(self, value):
		self.checkControlParametersTag()
		self.typeValuePr = self.checkProbability(value)
		attrib = {"value": str(value)}
		attrib = utility.filterNoneAttributes(attrib)
		if self.probabilityPointer is None:
			self.probabilityPointer=etree.SubElement(self.controlPointer, utility.BPSIM + "Probability")
		new_parameter= etree.SubElement(self.probabilityPointer, utility.BPSIM + self.typeValuePr, attrib=attrib)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Probability added" + self.typeValuePr, attrib)

	def setProbability(self, value):
		if self.probabilityPointer is None:
			raise ValueError("ERROR: Probability not exist")
		typeValue = self.checkProbability(value)
		newProbability=self.probabilityPointer.findall("./" + utility.BPSIM + self.typeValuePr)
		if self.typeValuePr == typeValue:
			newProbability[-1].set('value', str(value))
		elif typeValue == 'NumericParameter':
			self.probabilityPointer.remove(newProbability[-1])
			newProbability=etree.SubElement(self.probabilityPointer, utility.BPSIM + typeValue)
			newProbability.set('value', str(value))
		elif typeValue == 'FloatingParameter':
			self.probabilityPointer.remove(newProbability[-1])
			newProbability=etree.SubElement(self.probabilityPointer, utility.BPSIM + typeValue)
			newProbability.set('value', str(value))
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Probability updated")

	## METHOD TO ADD AND SET RESULT-REQUEST ON TRIGGER-TIMER, TRIGGER-COUNT
	def addInterTriggerTimerResultRequest(self, result_request):
		self.checkControlParametersTag()
		if self.triggerTimePointer is None:
			self.triggerTimePointer=etree.SubElement(self.controlPointer, utility.BPSIM + "InterTriggerTimer")
		request=etree.SubElement(self.triggerTimePointer, utility.BPSIM + "ResultRequest")
		request.text=result_request
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest added ", result_request)

	def setInterTriggerTimerResultRequest(self,result_request):
		if self.triggerTimePointer is None:
			raise ValueError("ERROR: TriggerTimer not exist")
		newTriggerTimer=self.triggerTimePointer.findall("./" + utility.BPSIM + self.typeValueTT)
		if len(newTriggerTimer) > 0:
			self.triggerTimePointer.remove(newTriggerTimer[-1])
		request=etree.SubElement(self.triggerTimePointer, utility.BPSIM + "ResultRequest")
		request.text=result_request
		if self.verbosity==0:
			print("INFO: ResultRequest updated")

	def addInterTriggerCountResultRequest(self, result_request):
		self.checkControlParametersTag()
		if self.triggerCountPointer is None:
			self.triggerCountPointer=etree.SubElement(self.controlPointer, utility.BPSIM + "TriggerCount")
		self.typeValueTC = "ResultRequest"
		request=etree.SubElement(self.triggerCountPointer, utility.BPSIM + "ResultRequest")
		request.text=result_request
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest added ", result_request)

	# METHODS TO ADD AND SET CONDITION
	def addCondition(self, value=None, expression=None):
		self.checkControlParametersTag()
		if (value==None and expression==None) or (value!=None and expression!=None):
			raise ValueError("ERROR: Condition requires BooleanParameter or ExpressionParameter") 
		else:
			if self.conditionPointer is None:
				self.conditionPointer=etree.SubElement(self.controlPointer, utility.BPSIM + "Condition")
			if value is not None:
				if super().checkBooleanParameter(value):
					self.typeValueC = "BooleanParameter"
					condition=etree.SubElement(self.conditionPointer, utility.BPSIM + self.typeValueC, attrib={"value": str(value)})
					if self.verbosity==0:
						print("INFO: Condition added BooleanParameter", {"value": value})
				else:
					raise ValueError("ERROR: value must be BooleanParameter")
			if expression is not None:
				self.typeValueC = "ExpressionParameter"
				super().addExpressionParameter(expression, self.conditionPointer, self.typeValueC)
				if self.verbosity==0:
					print("INFO: Condition added ExpressionParameter", {"expression": expression})
		utility.write_on_file(self.write, self.tree)
		
	def setCondition(self, value = None, expression = None):
		if self.conditionPointer is None:
			raise ValueError("ERROR: Condition not exist")
		if (value==None and expression==None) or (value!=None and expression!=None):
			raise ValueError("ERROR: Insert value or expression")
		newCondition=self.conditionPointer.findall("./" + utility.BPSIM + self.typeValueC)
		self.conditionPointer.remove(newCondition[-1])
		if value is not None:
			if super().checkBooleanParameter(value):
				self.typeValueC = "BooleanParameter"
				newCondition=etree.SubElement(self.conditionPointer, utility.BPSIM + self.typeValueC)
				newCondition.set('value', str(value))
			else:
				raise ValueError("ERROR: value must be BooleanParameter")
		if expression is not None:
			self.typeValueC = "ExpressionParameter"
			super().addExpressionParameter(expression, self.conditionPointer, self.typeValueC)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Condition updated")
	
	
        
