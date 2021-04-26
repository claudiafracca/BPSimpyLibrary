from BPSimpy import utility

class ScenarioParameters:
	
	def __init__(self, replication=None, seed=None, baseTimeUnit=None, baseCurrencyUnit=None, showResultRequestColumn=None,expressionLanguage=None, baseResultFrequency = None, baseResultFrequencyCumul = None, traceOutput= None, traceFormat= None, verbosity=None):
		self.replication=replication
		self.seed=seed
		self.baseTimeUnit=baseTimeUnit
		self.baseCurrencyUnit=baseCurrencyUnit
		self.showResultRequestColumn=showResultRequestColumn
		self.expressionLanguage=expressionLanguage
		self.baseResultFrequency=baseResultFrequency 
		self.baseResultFrequencyCumul= baseResultFrequencyCumul
		self.traceOutput= traceOutput  
		self.traceFormat=traceFormat
		self.verbosity=verbosity 

	# METHOD TO FILTER SCENARIO PARAMETERS ATTRIBUTES
	def filterScenarioParametersAttributes(self):
		attributes={"replication": self.replication, "seed":self.seed, "baseTimeUnit":self.baseTimeUnit,"baseCurrencyUnit":self.baseCurrencyUnit, "showResultRequestColumn":self.showResultRequestColumn,"expressionLanguage":self.expressionLanguage,
		"baseResultFrequency":self.baseResultFrequency, "baseResultFrequencyCumul":self.baseResultFrequencyCumul, "traceOutput":self.traceOutput, "traceFormat":self.traceFormat}
		attributes = utility.filterNoneAttributes(attributes)
		if self.replication is not None:
			attributes["replication"] = str(self.replication)
		if self.baseResultFrequency is not None: 
			self.baseResultFrequency = utility.getDurationType(self.baseResultFrequency)
			attributes["baseResultFrequency"] = self.baseResultFrequency
		if self.baseTimeUnit is not None:
			utility.checkTimeUnit(self.baseTimeUnit)
		return attributes

	# METHODS TO SET ALL ATTRIBUTES
	def setReplication(self, replication):
		if replication is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		if type(replication) == int:
			self.replication=replication
		else: 
			raise ValueError("ERROR: Invalid value. Replication must be int type")
		if self.verbosity==0:
			print("INFO: updated Replication of ScenarioParameters")

	def setSeed(self, seed):
		if seed is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		if type(seed) == float or type(seed) == int:
			self.seed=seed
		else:
			raise ValueError("ERROR: Invalid value. Seed must be long type")
		if self.verbosity==0:
			print("INFO: updated Seed of ScenarioParameters")

	def setBaseTimeUnit(self, baseTimeUnit):
		if baseTimeUnit is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		utility.checkTimeUnit(baseTimeUnit)
		self.baseTimeUnit=baseTimeUnit
		if self.verbosity==0:
			print("INFO: updated BaseTimeUnit of ScenarioParameters")

	def setBaseCurrentyUnit(self, baseCurrencyUnit):
		if baseCurrencyUnit is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		if type(baseCurrencyUnit) == str:
			self.baseCurrencyUnit=baseCurrencyUnit
		else: 
			raise ValueError("ERROR: Invalid value. BaseCurrentyUnit must be string type")
		if self.verbosity==0:
			print("INFO: updated BaseCurrentyUnit of ScenarioParameters")

	def setShowResultRequestColumn(self, showResultRequestColumn):
		if showResultRequestColumn is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		self.showResultRequestColumn=showResultRequestColumn
		if self.verbosity==0:
			print("INFO: updated ShowResultRequestColumn of ScenarioParameters")

	def setExpressionLanguage(self, expressionLanguage):
		if expressionLanguage is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		self.expressionLanguage=expressionLanguage
		if self.verbosity==0:
			print("INFO: updated expressionLanguage of ScenarioParameters")

	def setBaseResultFrequency(self, baseResultFrequency):
		if baseResultFrequency is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		self.baseResultFrequency=utility.getDurationType(baseResultFrequency)
		if self.verbosity==0:
			print("INFO: updated BaseResultFrequency of ScenarioParameters")

	def setBaseResultFrequencyCumul(self, baseResultFrequencyCumul):
		if baseResultFrequencyCumul is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		if type(baseResultFrequencyCumul) == bool:
			self.baseResultFrequencyCumul=baseResultFrequencyCumul
		else:
			raise ValueError("ERROR: Invalid value. BaseResultFrequencyCumul must be boolean type")
		if self.verbosity==0:
			print("INFO: updated BaseResultFrequencyCumul of ScenarioParameters")

	def setTraceOutput(self, traceOutput):
		if traceOutput is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		if type(traceOutput) == bool:
			self.traceOutput=traceOutput
		else:
			raise ValueError("ERROR: Invalid value. TraceOutput must be boolean type")
		if self.verbosity==0:
			print("INFO: updated TraceOutput of ScenarioParameters")

	def setTraceFormat(self, traceFormat):
		if traceFormat is None:
			raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
		if type(traceFormat) == str:
			self.traceFormat=traceFormat
		else: 
			raise ValueError("ERROR: Invalid value. TraceFormat must be string type")
		if self.verbosity==0:
			print("INFO: updated TraceFormat of ScenarioParameters")

		