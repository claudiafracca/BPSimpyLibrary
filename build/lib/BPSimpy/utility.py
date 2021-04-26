import xml.etree.ElementTree 
from lxml import etree,objectify
import datetime
import dateutil.parser 
import enum
import isodate
import pandas
	
BPSIM='{http://www.bpsim.org/schemas/1.0}'
BPMN2='{http://www.omg.org/spec/BPMN/20100524/MODEL}'

class TimeUnit(enum.Enum):
		minutes = 'min'
		milliseconds = 'ms'
		seconds = 's'
		hour = 'hour'
		days = 'day'
		year = 'year'

class PropertyType(enum.Enum):
		string = 'string'
		boolean= 'boolean'
		long= 'long'
		double= 'double'
		duration= 'duration'
		dataTime= 'dataTime'

class ResultRequest(enum.Enum):
		min='min'
		max='max'
		mean='mean'
		count='count'
		sum='sum'

#CHECK RESULT REQUEST
def checkResultRequest(value):
	for element in ResultRequest:  
		if value is element.value:
			return True
	raise ValueError('ERROR: Need ResultRequest: min, max, mean, count, sum')


#CHECK PROPERTY-TYPE
def checkPropertyType(value):
	for element in PropertyType:  
		if value is element.value:
			return True
	raise ValueError('ERROR: Need PropertyType: string, boolean, long, double, duration, dataTime')


#CHECK TIME-UNIT
def checkTimeUnit(value):
	for element in TimeUnit:  
		if value is element.value:
			return True
	raise ValueError('ERROR: Need TimeUnit type: min, ms, s, hour, day, year')


## DELETE NONE ATTRIBUTES
def filterNoneAttributes(attributes):
	for key in list(attributes.keys()):
		if attributes.get(key) is None:
			attributes.pop(key)
	return attributes


# FUNCTION TO WRITE/UPDATE ON FILE
def write_on_file(write, tree):
	etree.indent(write)
	tree.write('BPSIM_output.xml', xml_declaration=True, encoding='UTF-8', method='xml', pretty_print=True)

# FUNCTION TO TRANSFORM DURATION-PARAMETERS IN ISO8601
def getDurationType(value):
	if not isinstance(value, datetime.timedelta):
		raise ValueError("ERROR: value must be a datetime.timedelta object")
	value = isodate.duration_isoformat(value)
	return value

# FUNCTION TO TRANSFORM DATETIME-PARAMETERS IN ISO8601
def getDateTimeType(value):
	if not isinstance(value, datetime.datetime):
		raise ValueError("ERROR: value must be a datetime object")
	value = isodate.datetime_isoformat(value)
	return value

# CHECK DATA-FRAME OBJECT
def checkDataFrameType(value):
	if not isinstance(value, pandas.DataFrame):
		raise ValueError('ERROR: value must be a pandas DataFrame object')

#CHECK XML-TREE OBJECT
def checkXMLtreeType(value):
	if not isinstance(value, list):
		raise ValueError('ERROR: tree_list must be a list')
	for element in value:
		if not isinstance(element, etree._Element):
			raise ValueError('ERROR: value must be lxml.etree.Element')

# CHECK NAMESPACE
def checkNameSpace(name, value):
	if not isinstance(name, str) or not isinstance(value,str):
		raise ValueError('ERROR: name and value must be string type')

# ADD VENDOR-EXTENSION TO ELEMENT PARAMETER AND SCENARIO
def addVendorExtension(name, tree_list, pointer, nsValue):
	attrib = {'name':name}
	vendorExtensionPointer=etree.SubElement(pointer, BPSIM + "VendorExtension", attrib=attrib)
	checkXMLtreeType(tree_list)
	for element in tree_list:
		root = etree.SubElement(vendorExtensionPointer, '{'+nsValue+'}'+ element.tag)
		for child in element:
			new_child = etree.SubElement(root, '{'+nsValue+'}'+ child.tag, child.attrib)
			new_child.text=child.text

# CHECK IF CALENDAR EXISTS
def checkCalendar(calendars, validFor, verbosity):
	if validFor not in calendars and validFor is not None:
		if verbosity==0 or verbosity==1:
			print("WARNING: " + validFor + " not exists, remember to add to the Scenario")

# AUX FUNCTION TO CREATE-BPMN-ELEMENT-DICT
def getChild(process, dictionary):
	for child in process:
		dictionary[child.attrib.get('id')] = child.attrib.get('name')
		if len(list(child)) > 0:
			getChild(child, dictionary)

# FUNCTION TO CREATE A DICTIONARY FOR ALL ELEMENTS OF BPMN
def createBPMNelementDict(write):
	dictionary = {}
	processList = write.findall(BPMN2+'process')
	resourceList = write.findall(BPMN2+'resource')
	for process in processList:
		dictionary[process.attrib.get('id')] = process.attrib.get('name')
		getChild(process, dictionary)
	for resource in resourceList:
		dictionary[resource.attrib.get('id')] = resource.attrib.get('name')
	return dictionary, processList, resourceList
