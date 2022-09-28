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

from BPSimpy.ControlParameters import ControlParameters
from BPSimpy.TimeParameters import TimeParameters	
from BPSimpy.PropertyParameter import PropertyParameter	
from BPSimpy.ResourceParameter import ResourceParameter
from BPSimpy.PriorityParameter import PriorityParameter
from BPSimpy.CostParameter import CostParameter
from BPSimpy import utility
from BPSimpy import BPSim

import xml.etree.ElementTree 
from lxml import etree,objectify


APPLICABILITY={ "Time": ["task"], "InterTriggerTimer": ['startevent','eventbasedgateway','intermediatecatchevent','boundaryevent'] , "TriggerCount": ['startevent','eventbasedgateway'],
"Probability":['sequenceflow','boundaryevent'], "Quantity": ['resource'], "Property": ['startevent','endevent','intermediateevent', 'subprocess','sequenceflow','boundaryevent', "task", 'transaction'
 'callactivity', 'sequenceflow', 'messageflow'],
"Selection": ["task"], "Priority": ["task"], "Interruptible": ["task"],"Availability": ['resource'],"Role": ['resource'],"Cost": ['task','subprocess', 'transaction','callactivity','resource', 'process'],
"Condition": ['sequenceflow','boundaryevent']}

REQUEST={"QueueLength":["min", "max", "mean"], "Time":["min", "max", "mean", "count", "sum"], "interTriggerTimer":["min", "max", "mean", "sum", "count"],
"triggerCount":["count"], "selection": ["min", "max"], "cost": ["sum"]}

REQUEST_APPLICABILITY={"Time": ["task","resource", "resourcerole", "process"], "triggerCount": ['startevent','eventbasedgateway', 'event', "gateway", "task", "sequenceflow", "process","resource"]}

class ElementParameter(ControlParameters, TimeParameters, ResourceParameter, PropertyParameter, PriorityParameter, CostParameter):

	def __init__(self, elementRef, elementRefPointer, write, tree, scenario, root, verbosity):
		super().__init__()
		self.elementRef=elementRef
		self.elementRefPointer=elementRefPointer ## puntatore all'albero xml			
		self.write=write
		self.tree=tree
		self.root=root
		self.applicability = None
		self.isSubprocessElement = None
		self.vendorNamespace = None
		self.scenario=scenario
		self.verbosity=verbosity
		

	## METHODS TO ADD AND SET VENDOR-EXTENSION
	def setVendorNameSpace(self,value):
		self.vendorNamespace = value

	def addVendorExtension(self, name, tree_list):
		if self.vendorNamespace not in self.write.attrib.values():
			raise ValueError('ERROR: add VendorExtension after adding xmlns')
		utility.addVendorExtension(name, tree_list, self.elementRefPointer, self.vendorNamespace)
		utility.write_on_file(self.write, self.tree)
		if self.verbosity==0:
			print("INFO: ElementParameters VendorExtension added " + name)
			for tree in tree_list:
				etree.dump(tree)

	## METHOD TO GET THE ID OF ELEMENT-PARAMETER
	def getElementRef(self):
		return self.elementRef

	## METHODS TO GET, SET, CHECK APPLICABILITY OF ELEMENT-PARAMETER	
	def setApplicability(self, applicability, isSubprocessElement):
		self.applicability = applicability.replace(utility.BPMN2, "")
		self.isSubprocessElement = isSubprocessElement

	def getApplicability(self):
		return self.applicability

	def checkApplicability(self, element):
		valid=False
		for app in APPLICABILITY[element]:
			if app in self.applicability.lower():
				valid=True
		return valid

	def checkResultRequestApplicability(self,element):
		valid = False
		for resultApp in REQUEST_APPLICABILITY[element]:
			if resultApp in self.applicability.lower():
				valid = True
		return valid

	#METHODS TO ADD ALL PARAMETERS

	def addProcessingTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addProcessingTime(value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete,points, enum_list, expression)
			else:
				raise ValueError('ERROR: Processing time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for ProcessingTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit': timeUnit, 'validFor': validFor,'nameDistribution':nameDistribution,'shape':shape, 
							'scale':scale, 'probability':probability, 'trials':trials,
							'mean':mean, 'k':k, 'standardDeviation':standardDeviation, 'mode':mode, 
							'min':min, 'max':max, 'discrete': discrete, 'points':points,'enum_list':enum_list, 'expression':expression} 
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addProcessingTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")

	def addWaitTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addWaitTime(value, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
			else:
				raise ValueError('ERROR: Wait time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for WaitTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit':timeUnit,'validFor': validFor, 'enum_list': enum_list}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addWaitTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")


	def addTransferTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addTransferTime(value, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
			else:
				raise ValueError('ERROR: Transfer time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for TransferTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit':timeUnit,'validFor': validFor, 'enum_list': enum_list}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addTransferTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")
	
	def addQueueTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addQueueTime(value, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
			else:
				raise ValueError('ERROR: Queue time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for QueueTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit':timeUnit,'validFor': validFor, 'enum_list': enum_list}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addQueueTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")

	def addSetupTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addSetupTime(value, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
			else:
				raise ValueError('ERROR: Setup time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for SetupTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit':timeUnit,'validFor': validFor, 'enum_list': enum_list}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addSetupTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")

	def addValidationTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addValidationTime(value, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
			else:
				raise ValueError('ERROR: Validation time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for ValidationTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit':timeUnit,'validFor': validFor, 'enum_list': enum_list}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addValidationTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")

	def addReworkTime(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("Time"):
				super().addReworkTime(value, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list, expression)
			else:
				raise ValueError('ERROR: Rework time can be assigned only to task element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['Time']:
				raise ValueError("ERROR: for ReworkTime result_request must be " + str(REQUEST["Time"]))
			attributes = {'value':value,'timeUnit':timeUnit,'validFor': validFor, 'enum_list': enum_list}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('Time'):
				super().addReworkTimeResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['Time']) + " element")

	
	def addLagTime(self, result_request):
		utility.checkResultRequest(result_request)
		if result_request in REQUEST["Time"] and self.checkResultRequestApplicability("Time"):
			super().addLagTime(result_request)
		else:
			raise ValueError("ERROR: LagTime requires ", REQUEST["Time"])

	
	def addDuration(self, result_request):
		utility.checkResultRequest(result_request)
		if result_request in REQUEST["Time"] and self.checkResultRequestApplicability("Time"):
			super().addDuration(result_request)
		else:
			raise ValueError("ERROR: Duration requires ", REQUEST["Time"])

	def addElapsedTime(self, result_request):
		utility.checkResultRequest(result_request)
		if result_request in REQUEST["Time"] and self.checkResultRequestApplicability("Time"):
			super().addElapsedTime(result_request)
		else:
			raise ValueError("ERROR: ElapsedTime requires ", REQUEST["Time"])


	def addInterTriggerTimer(self, value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, result_request=None):
		if result_request is None:
			if self.checkApplicability("InterTriggerTimer"):
				super().addInterTriggerTimer(value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, enum_list)
			else:
				raise ValueError('ERROR: InterTriggerTimer can be assigned only to startEvent element')
		else:
			if result_request not in REQUEST['interTriggerTimer']:
				raise ValueError("ERROR: for InterTriggerTimer result_request must be " + str(REQUEST["interTriggerTimer"]))
			attributes = {'value':value,'timeUnit': timeUnit, 'validFor': validFor,'nameDistribution':nameDistribution,'shape':shape, 
							'scale':scale, 'probability':probability, 'trials':trials,
							'mean':mean, 'k':k, 'standardDeviation':standardDeviation, 'mode':mode, 
							'min':min, 'max':max, 'discrete': discrete, 'points':points,'enum_list':enum_list} 
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkApplicability("InterTriggerTimer"):
				super().addInterTriggerTimerResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(APPLICABILITY["InterTriggerTimer"]) + " element")

	def addTriggerCount(self, value=None, validFor=None, result_request = None):
		if result_request is None:
			if self.checkApplicability("TriggerCount"):
				super().addTriggerCount(value, validFor)
			else:
				raise ValueError('ERROR: TriggerCount can be assigned only to startEvent element')
		else:
			utility.checkResultRequest(result_request)
			if result_request not in REQUEST['triggerCount']:
				raise ValueError("ERROR: for TriggerCount result_request must be " + str(REQUEST['triggerCount']))
			attributes = {'value':value, 'validFor':validFor}
			utility.filterNoneAttributes(attributes)
			if len(attributes) == 0 and self.checkResultRequestApplicability('triggerCount'):
				super().addInterTriggerCountResultRequest(result_request)
			elif len(attributes) > 0:
				raise ValueError("ERROR: for ResultRequest insert only result_request parameter")
			else:
				raise ValueError("ERROR: result_request can be insert only to " + str(REQUEST_APPLICABILITY['triggerCount']) + " element")
	
	def auxGateway(self, subProcess):
		for child in subProcess:
			if child.tag==utility.BPMN2 + "subProcess":
				self.auxGateway(child)
			else:
				if child.get("id")==self.elementRef:
					self.element=child
					

	def addProbability(self, value):
		checkGateway=False
		dict1, dict2, dict3=self.scenario.createProcessElementDict()
		process= self.write.find(utility.BPMN2+'process')
		xor_id=None
		
		for element in process.findall(utility.BPMN2 + "sequenceFlow"):
			if element.get("id")==self.elementRef:
				xor_id= element.get("sourceRef")
				if "exclusiveGateway" in dict1[xor_id]:
					checkGateway=True
		
		if checkGateway is not True:
			self.element=None
			for subProcess in process.findall(utility.BPMN2 + "subProcess"):
				self.auxGateway(subProcess)
			if self.element is not None:
				xor_id= self.element.get("sourceRef")
				if  "exclusiveGateway" in dict3[xor_id]:
					checkGateway=True

		if checkGateway is  True:
			if  xor_id not in self.scenario.getXor():
				self.scenario.addXor(xor_id)
			self.scenario.setXor(value, xor_id, self.elementRef)

		if self.checkApplicability("Probability"):
			super().addProbability(value)
		elif self.isSubprocessElement is True and 'startevent' in self.applicability.lower():
			super().addProbability(value)
		else:
			raise ValueError('ERROR: Probability can be assigned only to sequenceFlow element')
		
	def addQuantity(self, value, validFor = None):
		if self.checkApplicability("Quantity"):
			super().addQuantity(value, validFor)
		else:
			raise ValueError('ERROR: Quantity can be assigned only to resource element')


	def addProperty(self, name, type=None, value=None, enum_list=None,timeUnit = None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, expression=None):
		if self.checkApplicability("Property"):
			super().addProperty(name, type, value, enum_list, timeUnit, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression)
		else:
			raise ValueError('ERROR: Property can be assigned only to ', str(APPLICABILITY["Property"]))

	def addSelection(self, value=None, expression=None, result_request=None):
		if self.checkApplicability("Selection"):
			if result_request is not None and result_request not in REQUEST["selection"]:
				raise ValueError('ERROR: ResultRequest for UnitCost accepts min or max')
			super().addSelection(value, expression,result_request)
		else:
			raise ValueError('ERROR: Selection can be assigned only to task element')

	def addAvailability(self,value,validFor=None):
		if self.checkApplicability("Availability"):
			super().addAvailability(value, validFor)
		else:
			raise ValueError('ERROR: Availability can be assigned only to resource element')
		
	def addRole(self,value):
		if self.checkApplicability("Role"):
			super().addRole(value)
		else:
			raise ValueError('ERROR: Role can be assigned only to resource element')

	def addPriority(self, value):
		if self.checkApplicability("Priority"):
			super().addPriority(value)
		else:
			raise ValueError('ERROR: Priority can be assigned only to task element')

	def addInterruptible(self, value):
		if self.checkApplicability("Interruptible"):
			super().addInterruptible(value)
		else:
			raise ValueError('ERROR: Interruptible can be assigned only to task element')

	def addFixedCost(self,value=None, validFor=None,result_request = None):
		if self.checkApplicability("Cost"):
			if result_request is not None and result_request not in REQUEST["cost"]:
				raise ValueError('ERROR: ResultRequest for FixedCost accepts only sum')
			super().addFixedCost(value, validFor, result_request)
		else:
			raise ValueError('ERROR: FixedCost can be assigned only to task, subprocess, transaction, callactivity, resource element')
	
	def addUnitCost(self,value=None,validFor=None,result_request=None):
		if self.checkApplicability("Cost"):
			if result_request is not None and result_request not in REQUEST["cost"]:
				raise ValueError('ERROR: ResultRequest for UnitCost accepts only sum')
			super().addUnitCost(value, validFor, result_request)
		else:
			raise ValueError('ERROR: UnitCost can be assigned only to task, subprocess, transaction, callactivity, resource element')

	def addQueueLength(self, result_request):
		utility.checkResultRequest(result_request)
		if result_request in REQUEST["QueueLength"] and self.checkApplicability("Property"):
			super().addQueueLength(result_request)
		else:
			raise ValueError("ERROR: QueueLength requires ", REQUEST["QueueLength"])

	def addCondition(self, value=None, expression=None):
		if self.checkApplicability("Condition"):
			super().addCondition(value, expression)
		else:
			raise ValueError('ERROR: Condition can be assigned only to sequenceFlow element')
	
	def setTriggerCount(self, value=None, validFor=None, result_request = None):
		if self.checkApplicability("TriggerCount") or result_request in REQUEST['triggerCount']:
			super().setTriggerCount(value,validFor,result_request)
		else:
			raise ValueError("ERROR: result_request must be 'count' or value must be assigned only to startEvent")
	
	def setProcessingTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setProcessingTime(value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete,points, enum_list, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))
	
	def setWaitTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setWaitTime(value, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete,points, enum_list, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))

	def setQueueTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setQueueTime(value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))

	def setTransferTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setTransferTime(value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))

	def setSetupTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setSetupTime(value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))

	def setValidationTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setValidationTime(value, enum_list, timeUnit, validFor,nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))

	def setReworkTime(self,value=None, timeUnit=None, validFor=None, nameDistribution = None, shape = None, scale = None, probability = None, trials = None, mean = None, k = None, standardDeviation = None, mode = None, min = None, max = None, discrete = None, points = None, enum_list = None, expression=None, result_request = None):
		if self.checkApplicability("Time") or result_request in REQUEST['Time']:
			super().setReworkTime(value, enum_list, timeUnit, validFor, nameDistribution, shape, scale, probability, trials, mean, k, standardDeviation, mode, min, max, discrete, points, expression,result_request)
		else:
			raise ValueError("ERROR: result_request must be "+ str(REQUEST["Time"])+" or value must be assigned only to " + str(APPLICABILITY["Time"]))


	### METHOD TO REMOVE ELEMENT-PARAMETER AND SINGLE PARAMETER

	def remove(self):
		parent=self.elementRefPointer.getparent()
		for child in parent:
			if child==self.elementRefPointer:
				parent.remove(child)
		if self.verbosity==0:
			print("INFO: ElementParameters ", {'elementRef': self.elementRef},  " removed")
		utility.write_on_file(self.write, self.tree)

	
	def removeParameter(self, parameter, remove):
		parent=self.elementRefPointer.find("./" + utility.BPSIM + parameter)
		element=self.elementRefPointer.find("./" + utility.BPSIM + parameter + "/" + utility.BPSIM + remove)
		if  element is None:
			if self.verbosity==0 or self.verbosity==1:
				print("WARNING:", remove, "does not exist")
		else:
			parent.remove(element)
			if self.verbosity==0:
				print("INFO:", remove ,"removed")
			if len(parent.getchildren())==0:
				self.elementRefPointer.remove(parent)
				if self.verbosity==0:
					print("INFO:", parameter, "removed")
			if len(self.elementRefPointer.getchildren())==0:
				self.remove()
			
	### REMOVE CONTROL-PARAMETERS
	def removeTriggerCount(self):
		self.removeParameter("ControlParameters","TriggerCount")

	def removeInterTriggerTimer(self):
		self.removeParameter("ControlParameters","InterTriggerTimer")

	def removeCondition(self):
		self.removeParameter("ControlParameters","Condition")

	def removeProbability(self):
		self.removeParameter("ControlParameters", "Probability")

	##REMOVE RESOURCE-PARAMETERS
	def removeSelection(self):
		self.removeParameter("ResourceParameters","Selection")

	def removeQuantity(self):
		self.removeParameter("ResourceParameters","Quantity")

	def removeSelection(self):
		self.removeParameter("ResourceParameters","Avaibility")

	def removeSelection(self):
		self.removeParameter("ResourceParameters","Role")
	
	##REMOVE PROPERTY-PARAMETERS
	def removeProperty(self):
		self.removeParameter("PropertyParameters","Property")

	def removeQueueLength(self):
		self.removeParameter("PropertyParameters","QueueLength")


	## REMOVE COST-PARAMETERS
	def removeFixedCost(self):
		self.removeParameter("CostParameters","FixedCost")

	def removeUnitCost(self):
		self.removeParameter("CostParameters","UnitCost")	

	## REMOVE TIME-PARAMETERS
	def removeSetupTime(self):
		self.removeParameter("TimeParameters","SetupTime")	
	
	def removeReworkTime(self):
		self.removeParameter("TimeParameters","ReworkTime")	
	
	def removeValidationTime(self):
		self.removeParameter("TimeParameters","ValidationTime")	

	def removeTransferTime(self):
		self.removeParameter("TimeParameters","TransferTime")	

	def removeQueueTime(self):
		self.removeParameter("TimeParameters","QueueTime")	

	def removeLagTime(self):
		self.removeParameter("TimeParameters","LagTime")
	
	def removeDuration(self):
		self.removeParameter("TimeParameters","Duration")

	def removeElapsedTime(self):
		self.removeParameter("TimeParameters","ElapsedTime")

	def removeWaitTime(self):
		self.removeParameter("TimeParameters","WaitTime")

	def removeProcessingTime(self):
		self.removeParameter("TimeParameters","ProcessingTime")



	