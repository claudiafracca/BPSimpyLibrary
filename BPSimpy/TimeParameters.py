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

class TimeParameters(Parameter):

	def __init__(self):
		super().__init__()
		self.timePointer = None
		self.processingTimePointer = None
		self.waitTimePointer = None
		self.queueTimePointer = None
		self.transferTimePointer = None
		self.validationTimePointer = None
		self.reworkTimePointer = None
		self.setupTimePointer = None
		self.lagtimePointer = None
		self.durationPointer = None
		self.elapsedTimePointer = None
		self.nameDistribution = None

	# METHOD TO ADD TIMEPARAMETERS TAG
	def addTimePointer(self):
		self.timePointer= etree.SubElement(self.elementRefPointer, utility.BPSIM + "TimeParameters")
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: TimeParameters added")
	
	# METHOD TO CHECK TIMEPARAMETERS TAG
	def checkTimeParametersTag(self):
		if self.timePointer is None:
			self.addTimePointer()

	# METHODS TO ADD TIME PARAMETERS
	#(PROCESSING TIME - WAIT TIME - QUEUE TIME - TRANSFER TIME - VALIDATION TIME - REWORK TIME - SETUP TIME)
	def addTimeParameter(self, pointer, name, value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression):
		nameDistributionTime = None
		if value is None and nameDistribution is None and enum_list is None and expression is None:
			raise ValueError('ERROR: Insert value or enum_list or nameDistribution or expression')
		if (value is not None or enum_list is not None) and (nameDistribution is None and expression is None):
			pointer, typeValue, attributes = super().addParameterWithEnumList(value, timeUnit, validFor, name, enum_list,self.timePointer,pointer, None, None)
			if self.verbosity==0:
				print("INFO: "+ name + " added " + typeValue, attributes)
		elif nameDistribution is not None and value is None and enum_list is None and expression is None:
			nameDistributionTime = nameDistribution
			typeValue = nameDistributionTime
			attributes= super().filterDistributionAttributes(timeUnit, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor)
			if pointer is None:
				pointer=etree.SubElement(self.timePointer, utility.BPSIM + name)
			if nameDistribution == 'UserDistribution':
				super().createUserDistributionDataPoint(points, pointer, discrete, timeUnit, validFor)
			else:
				new_parameter= etree.SubElement(pointer, utility.BPSIM + nameDistribution, attrib = attributes)
			if self.verbosity==0:
				if nameDistribution != 'UserDistribution':
					print("INFO: " + name + " added " + nameDistribution, attributes)
				else:
					print("INFO: " + name + " added " + nameDistribution + " Discrete: ",attributes['discrete'], " Points: ", points.to_dict())
			utility.write_on_file(self.write, self.tree)
		elif value is None and nameDistribution is None and enum_list is None and expression is not None:
			if pointer is None:
				pointer=etree.SubElement(self.timePointer, utility.BPSIM + name)
			new_parameter= etree.SubElement(pointer, utility.BPSIM + "ExpressionParameter", attrib = {"value": expression})
			if self.verbosity==0:
				print("INFO: " + name + " added ExpressionParameter ", {"value": expression})
		else:
			raise ValueError("ERROR: for " + name +" insert value or enum_list or nameDistribution or expression")
		return pointer, typeValue, attributes, nameDistributionTime
	
	def addProcessingTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.processingTimePointer, self.typeValuePT, self.processingTimeAttrib, self.nameDistributionPT= self.addTimeParameter(self.processingTimePointer, "ProcessingTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
		
	def addWaitTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.waitTimePointer, self.typeValueWT, self.waitTimeAttrib,self.nameDistributionWT = self.addTimeParameter(self.waitTimePointer, "WaitTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)

	def addTransferTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.transferTimePointer, self.typeValueTT, self.transferTimeAttrib,self.nameDistributionTT = self.addTimeParameter(self.transferTimePointer, "TransferTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)

	def addQueueTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.queueTimePointer, self.typeValueQT, self.queueTimeAttrib,self.nameDistributionQT = self.addTimeParameter(self.queueTimePointer, "QueueTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)

	def addSetupTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.setupTimePointer, self.typeValueST, self.setupTimeAttrib,self.nameDistributionST = self.addTimeParameter(self.setupTimePointer, "SetupTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)

	def addValidationTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.validationTimePointer, self.typeValueVT, self.validationTimeAttrib,self.nameDistributionVT = self.addTimeParameter(self.validationTimePointer, "ValidationTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)

	def addReworkTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None):
		self.checkTimeParametersTag()
		self.reworkTimePointer, self.typeValueRT, self.reworkTimeAttrib,self.nameDistributionRT = self.addTimeParameter(self.reworkTimePointer, "ReworkTime", value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)

	def addTimeParameterResultRequest(self, result_request,pointer,tag):
		self.checkTimeParametersTag()
		if pointer is None:
			pointer=etree.SubElement(self.timePointer, utility.BPSIM + tag)
		request=etree.SubElement(pointer, utility.BPSIM + "ResultRequest")
		request.text=result_request
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest added ", result_request)
		return pointer

	def addProcessingTimeResultRequest(self,result_request):
		self.processingTimePointer=self.addTimeParameterResultRequest(result_request,self.processingTimePointer, "ProcessingTime")
	
	def addWaitTimeResultRequest(self,result_request):
		self.waitTimePointer = self.addTimeParameterResultRequest(result_request,self.waitTimePointer, "WaitTime")

	def addQueueTimeResultRequest(self,result_request):
		self.queueTimePointer=self.addTimeParameterResultRequest(result_request,self.queueTimePointer, "QueueTime")
	
	def addTransferTimeResultRequest(self,result_request):
		self.transferTimePointer=self.addTimeParameterResultRequest(result_request,self.transferTimePointer, "TransferTime")

	def addValidationTimeResultRequest(self,result_request):
		self.validationTimePointer=self.addTimeParameterResultRequest(result_request,self.validationTimePointer, "ValidationTime")

	def addReworkTimeResultRequest(self,result_request):
		self.reworkTimePointer=self.addTimeParameterResultRequest(result_request,self.reworkTimePointer, "ReworkTime")
	
	def addSetupTimeResultRequest(self,result_request):
		self.setupTimePointer=self.addTimeParameterResultRequest(result_request,self.setupTimePointer, "SetupTime")
	
	# METHODS TO SET TIME PARAMETERS
	#(PROCESSING TIME - WAIT TIME - QUEUE TIME - TRANSFER TIME - VALIDATION TIME - REWORK TIME - SETUP TIME)
	def setTimeParameter(self, pointer, name, typeValue, nameDistributionTime, attributes, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request):
		if pointer is None:
			raise ValueError("ERROR: "+name+" not exist")
		if value is None and nameDistribution is None and enum_list is None and result_request is None and expression is None:
			raise ValueError('ERROR: Add value or nameDistribution or enum_list or expression or result_request')
		if nameDistribution is None and result_request is None and expression is None:
			if typeValue == nameDistributionTime:
				attributes = {}
			super().setParameterWithEnumList(typeValue, pointer, attributes,value,enum_list, timeUnit, validFor)
		newProcessingTime=pointer.findall("./" + utility.BPSIM + typeValue)
		if len(newProcessingTime) > 0:
			pointer.remove(newProcessingTime[-1])
		if value is None and nameDistribution is not None and enum_list is None and result_request is None and expression is None:
			super().checkNameDistribution(nameDistribution)
			newProcessingTimeAttrib= super().filterDistributionAttributes(timeUnit,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, validFor)
			if nameDistribution == 'UserDistribution':
				super().createUserDistributionDataPoint(points, pointer, discrete, timeUnit)
			else:
				new_parameter= etree.SubElement(pointer, utility.BPSIM + nameDistribution, attrib = newProcessingTimeAttrib)
		elif result_request is not None:
			utility.checkResultRequest(result_request)
			attributes = {'value':value,'timeUnit': timeUnit, 'validFor': validFor,'nameDistribution':nameDistribution,'shape':shape, 
							'scale':scale, 'probability':probability, 'trials':trials,
							'mean':mean, 'k':k, 'standardDeviation':standardDeviation, 'mode':mode, 
							'min':min, 'max':max, 'discrete': discrete, 'points':points,'enum_list':enum_list,'expression':expression} 
			utility.filterNoneAttributes(attributes)
			if len(attributes)==0:
				typeValue = "ResultRequest"
				self.addTimeParameterResultRequest(result_request, pointer, typeValue)
			else:
				raise ValueError("ERROR: Insert only result_request")
		elif expression is not None and result_request is None and value is None and nameDistribution is None and enum_list is None:
			if super().checkStringParameter(expression):
				typeValue='ExpressionParameter'
				new_parameter= etree.SubElement(pointer, utility.BPSIM + typeValue, attrib = {'value':expression})
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: "+name+" updated")
	
	def setProcessingTime(self, value = None, enum_list = None, timeUnit = None, validFor = None,nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None,result_request = None):
		self.setTimeParameter(self.processingTimePointer, "ProcessingTime", self.typeValuePT, self.nameDistributionPT, self.processingTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
		
	def setWaitTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list=None, expression=None, result_request = None):
		self.setTimeParameter(self.waitTimePointer, "WaitTime", self.typeValueWT, self.nameDistributionWT, self.waitTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)

	def setTransferTime(self, value = None, enum_list = None, timeUnit = None, validFor = None,nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None,result_request = None):
		self.setTimeParameter(self.transferTimePointer, "TransferTime", self.typeValueTT, self.nameDistributionTT, self.transferTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)

	def setQueueTime(self, value = None, enum_list = None, timeUnit = None, validFor = None,nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None,result_request = None):
		self.setTimeParameter(self.queueTimePointer, "QueueTime", self.typeValueQT, self.nameDistributionQT, self.queueTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)

	def setSetupTime(self, value = None, enum_list = None, timeUnit = None, validFor = None,nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None,result_request = None):
		self.setTimeParameter(self.setupTimePointer, "SetupTime", self.typeValueST, self.nameDistributionST, self.setupTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)

	def setValidationTime(self, value = None, enum_list = None, timeUnit = None, validFor = None,nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None,result_request = None):
		self.setTimeParameter(self.validationTimePointer, "ValidationTime", self.typeValueVT, self.nameDistributionVT, self.validationTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
	
	def setReworkTime(self, value = None, enum_list = None, timeUnit = None, validFor = None, nameDistribution=None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression = None,result_request = None):
		self.setTimeParameter(self.reworkTimePointer, "ReworkTime", self.typeValueRT, self.nameDistributionRT, self.reworkTimeAttrib, value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
	
	def setTimeParameterResultRequest(self, result_request, value, enum_list, timeUnit, validFor, pointer, typeValue):
		utility.checkResultRequest(result_request)
		attributes={'value':value,'enum_list':enum_list,'timeUnit':timeUnit,'validFor':validFor}
		attributes = utility.filterNoneAttributes(attributes)
		if len(attributes) == 0:
			new_parameter = pointer.findall("./" + utility.BPSIM + typeValue)
			pointer.remove(new_parameter[-1])
			typeValue = "ResultRequest"
			new_parameter=etree.SubElement(pointer, utility.BPSIM + typeValue)
			new_parameter.text = result_request
		else:
			raise ValueError("ERROR: insert only result_request")
		utility.write_on_file(self.write, self.tree)

	# METHODS TO ADD TIME PARAMETERS THAT HAVE ONLY RESULT REQUEST
	#(LAGTIME - DURATION - ELAPSEDTIME)
	def addLagTime(self, result_request):
		self.checkTimeParametersTag()
		if self.lagtimePointer is None:
			self.lagtimePointer=etree.SubElement(self.timePointer, utility.BPSIM + "LagTime")
		request=etree.SubElement(self.lagtimePointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(result_request)
		request.text=result_request
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: LagTime added ResultRequest:", result_request)

	def addDuration(self, result_request):
		self.checkTimeParametersTag()
		if self.durationPointer is None:
			self.durationPointer=etree.SubElement(self.timePointer, utility.BPSIM + "Duration")
		request=etree.SubElement(self.durationPointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(result_request)
		request.text=result_request
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: Duration added ResultRequest:", result_request)

	def addElapsedTime(self, result_request):
		self.checkTimeParametersTag()
		if self.elapsedTimePointer is None:
			self.elapsedTimePointer=etree.SubElement(self.timePointer, utility.BPSIM + "ElapsedTime")
		request=etree.SubElement(self.elapsedTimePointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(result_request)
		request.text=result_request
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ElapsedTime added ResultRequest:", result_request)

	# METHODS TO SET TIME PARAMETERS THAT HAVE ONLY RESULT REQUEST
	#(LAGTIME - DURATION - ELAPSEDTIME)

	def setLagTime(self, resultRequest):
		if self.lagtimePointer is None:
			raise ValueError("ERROR: LagTime not exist")
		result = self.lagtimePointer.findall("./"+ utility.BPSIM + 'ResultRequest')
		self.lagtimePointer.remove(result[-1])
		new_result = etree.SubElement(self.lagtimePointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(resultRequest)
		new_result.text=resultRequest
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest updated")

	def setDuration(self, resultRequest):
		if self.durationPointer is None:
			raise ValueError("EERROR: Duration not exist")
		result = self.durationPointer.findall("./"+ utility.BPSIM + 'ResultRequest')
		self.durationPointer.remove(result[-1])
		new_result = etree.SubElement(self.durationPointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(resultRequest)
		new_result.text=resultRequest
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest updated")

	def setElapsedTime(self, resultRequest):
		if self.elapsedTimePointer is None:
			raise ValueError("ERROR: ElapsedTime not exist")
		result = self.elapsedTimePointer.findall("./"+ utility.BPSIM + 'ResultRequest')
		self.elapsedTimePointer.remove(result[-1])
		new_result = etree.SubElement(self.elapsedTimePointer, utility.BPSIM + "ResultRequest")
		utility.checkResultRequest(resultRequest)
		new_result.text=resultRequest
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ResultRequest updated")
