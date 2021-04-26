from BPSimpy import utility
import xml.etree.ElementTree as ET
from lxml import etree, objectify
from BPSimpy import ScenarioParameters as sp
from BPSimpy import ElementParameter as e 
import datetime
from icalendar import Calendar, Event


class Scenario:

    def __init__(self, name=None, id=None, author=None, description=None, created=None, modified=None, version=None, vendor = None, inherits=None, verbosity=None):
        self.name=name
        self.id=id
        self.author=author
        self.description=description
        self.created=created
        self.modified=modified
        self.version=version
        self.vendor=vendor
        self.inherits=inherits
        self.write=None ## puntatore alla radice dell'albero
        self.root=None ## puntatore al nodo "scenario"
        self.tree= None ## puntatore all'albero xml 
        self.elementParameters=[] ## puntatori ad ogni blocco inserito
        self.elementParametersList = []
        self.vendorNamespace=None
        self.calendars=[]
        self.xor={}
        self.verbosity=verbosity


    ## METHOD TO PRINT BPSIM_OUTPUT.XML
    def __repr__(self):
        etree.indent(self.root)
        return etree.tostring(self.root, encoding='unicode')

    ## METHOD TO FILTER NONE ATTRIBUTES
    def filterScenarioAttributes(self):
        if self.created is not None:
            self.created = utility.getDateTimeType(self.created)
        if self.modified is not None:
            self.modified=utility.getDateTimeType(self.modified)
        attributes={"id": self.id, "name": self.name, 
                "author": self.author, "description": self.description,
                "created": self.created, "modified": self.modified, 
                "version": self.version, "vendor": self.vendor, "inherits": self.inherits}
        self.attributes = utility.filterNoneAttributes(attributes)

        return self.attributes

    def setPointer(self, root, write, tree):
        self.root = root
        self.write = write
        self.tree= tree

    ## METHOD TO ADD SCENARIO-PARAMETERS
    def addScenarioParameters(self, replication=None, seed=None, baseTimeUnit=None, baseCurrencyUnit=None, showResultRequestColumn=None,expressionLanguage=None, baseResultFrequency = None, baseResultFrequencyCumul = None, traceOutput= None, traceFormat= None): 
        self.ScenarioParameters= sp.ScenarioParameters(replication, seed, baseTimeUnit, baseCurrencyUnit, showResultRequestColumn, expressionLanguage, baseResultFrequency, baseResultFrequencyCumul, traceOutput, traceFormat, self.verbosity)
        self.scenarioParametersAttrib = self.ScenarioParameters.filterScenarioParametersAttributes()
        self.root.insert(0, etree.Element(utility.BPSIM + "ScenarioParameters", attrib=self.scenarioParametersAttrib))
        self.scenarioParametersPointer= self.root.find(utility.BPSIM + "ScenarioParameters")
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Scenario parameters added" + str(self.scenarioParametersAttrib))

    ## METHOD TO ADD VENDOR-EXTENSIONS
    def addVendorExtension(self, name, tree_list):
        if self.vendorNamespace not in self.write.attrib.values():
            raise ValueError('ERROR: To insert VendorExtension first add xmlns')
        utility.addVendorExtension(name, tree_list, self.root, self.vendorNamespace)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Scenario VendorExtension added " + name)
            for tree in tree_list:
                etree.dump(tree)

    def setVendorNamespace(self, value):
        self.vendorNamespace=value

    def setVendorNameSpaceToElementParameters(self, value):
        for element in self.elementParametersList:
            element.setVendorNameSpace(value)
        
    def createProcessElementDict(self):
        processElementDict = {}
        subProcessElementDict = {}
        resourceElementDict = {}
        for process in self.processList:
            processElementDict[process.get('id')] = process.tag
            for child in process:
                processElementDict[child.get('id')] = child.tag
                if child.tag == utility.BPMN2+'subProcess':
                    self.getSubProcess(child, subProcessElementDict)
        for resource in self.resourceList:
            resourceElementDict[resource.get('id')] = resource.tag
        return processElementDict, resourceElementDict ,subProcessElementDict
        

    def setElementParametersApplicability(self, id):
        isSubProcessElement = None
        applicability = None
        processElementDict, resourceElementDict, subProcessElementDict = self.createProcessElementDict()
        for element in self.elementParametersList:
            key = element.getElementRef()
            if key in processElementDict.keys():
                applicability = processElementDict.get(key)
                isSubProcessElement = False
            elif key in subProcessElementDict.keys():
                applicability = subProcessElementDict.get(key)
                isSubProcessElement = True
            elif key in resourceElementDict.keys():
                applicability = resourceElementDict.get(key)
                isSubProcessElement  = False
            element.setApplicability(applicability, isSubProcessElement)


    def getSubProcess(self,subProcess, subProcessDict):
        for child in subProcess:
            subProcessDict[child.attrib.get('id')] = child.tag
            if child.tag == utility.BPMN2+'subProcess':
                self.getSubProcess(child, subProcessDict)

    ## CONTROL ID TO ADD ELEMENTS-PARAMETERS
    ## input can be a list or string
    def getElementParameters(self, input):
        if isinstance(input, list):
            if len(input)==0:
                raise ValueError("ERROR: Incorrect id")
            else:
                id=input[0]  
        else:
            id=input
     
        dictionary, self.processList, self.resourceList=utility.createBPMNelementDict(self.write)
        if id in dictionary:
            for element in self.root.iter(utility.BPSIM + 'ElementParameters'):
                if element.attrib["elementRef"]==id:
                    raise ValueError("ERROR: ElementParameters already exists")

            count=len(self.root.getchildren())-len(self.calendars)
            self.root.insert(count, etree.Element(utility.BPSIM + "ElementParameters", attrib={"elementRef": id}))
            for element in self.root.findall(utility.BPSIM + "ElementParameters"):
                if element.get("elementRef")==id:
                    new_element_pointer= element
            self.elementParameters.append(new_element_pointer)
            new_element=e.ElementParameter(id, new_element_pointer, self.write, self.tree, self, self.root, self.verbosity)
            self.elementParametersList.append(new_element)
            if self.vendorNamespace is not None:
                self.setVendorNameSpaceToElementParameters(self.vendorNamespace)
            self.setElementParametersApplicability(id)
            utility.write_on_file(self.write, self.tree)
            if self.verbosity==0:
                print("INFO: ElementParameters added", str({"elementRef": id}) )
            return new_element
        else:
            raise ValueError("ERROR: Incorrect id")
    
    ## METHODS TO ADD SCENARIO PARAMETERS: START, WARMUP, DURATION

    def addStart(self, value):
        if value is None:
            raise ValueError("ERROR: Insert value of Start")    
        value = utility.getDateTimeType(value)
        self.start={"value": value}
        parameter=etree.SubElement(self.scenarioParametersPointer, utility.BPSIM + "Start") 
        parameter=etree.SubElement(parameter, utility.BPSIM +"DateTimeParameter", self.start)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Start Parameter added" + str(self.start))

    def addDuration(self, value):
        if value is None:
            raise ValueError("ERROR: Insert value of Duration") 
        value = utility.getDurationType(value)
        self.duration={"value": value}
        parameter=etree.SubElement(self.scenarioParametersPointer, utility.BPSIM + "Duration") 
        parameter=etree.SubElement(parameter, utility.BPSIM +"DurationParameter", self.duration)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Duration Parameter added" + str(self.duration))

    def addWarmup(self, value):
        if value is None:
            raise ValueError("ERROR: Insert value of Warmup") 
        value = utility.getDurationType(value)
        self.warmup={"value": value}
        parameter=etree.SubElement(self.scenarioParametersPointer, utility.BPSIM + "Warmup") 
        parameter=etree.SubElement(parameter, utility.BPSIM + "DurationParameter", self.warmup)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Warmup Parameter added" + str(self.warmup))


    ## METHODS TO SET START, WARMUP AND DURATION

    def setStart(self, value):
        if value is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        value = utility.getDateTimeType(value)
        self.start["value"]= value
        element=self.scenarioParametersPointer.find("./" + utility.BPSIM + "Start" + "/" + utility.BPSIM + "DateTimeParameter")
        element.set('value', value)
        utility.write_on_file(self.root, self.tree)
        if self.verbosity==0:
            print("INFO: Start of Scenario update")

    def setDuration(self, value):
        if value is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        value = utility.getDurationType(value)
        self.duration["value"]= value
        element=self.scenarioParametersPointer.find("./" + utility.BPSIM + "Duration" + "/" + utility.BPSIM + "DurationParameter")
        element.set('value', value)
        utility.write_on_file(self.root, self.tree)
        if self.verbosity==0:
            print("INFO: Duration of Scenario updated")

    def setWarmup(self, value):
        if value is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        value = utility.getDurationType(value)
        self.warmup["value"]=value
        element=self.scenarioParametersPointer.find("./" + utility.BPSIM + "Warmup" + "/" +utility.BPSIM + "DurationParameter")
        element.set('value', value)
        utility.write_on_file(self.root, self.tree)
        if self.verbosity==0:
            print("INFO: Warmup of Scenario updated ")

    ## METHODS TO REMOVE START, WARMUP AND DURATION
    
    def removeStart(self):
        if self.start is None:
            print("WARNING: Attribute not found")
        else:
            self.start=None
            self.removeScenarioParameters("Start")
            if self.verbosity==0:
                print("INFO: Start Parameter deleted")
    
    def removeDuration(self):
        if self.duration is None:
            if self.verbosity==0 or self.verbosity==1:
                print("WARNING: Attribute not found")
        else:
            self.duration=None
            self.removeScenarioParameters("Duration")
            if self.verbosity==0:
                print("INFO: Duration Parameter deleted")
    
    def removeWarmup(self):
        if self.warmup is None:
            if self.verbosity==0 or self.verbosity==1:
                print("WARNING: Attribute not found")
        else:
            self.warmup=None
            self.removeScenarioParameters("Warmup")
            if self.verbosity==0:
                print("INFO: Warmup Parameter deleted")
    
    def removeScenarioParametersAttribute(self,key):
        if key not in self.scenarioParametersAttrib:
            if self.verbosity==0 or self.verbosity==1:
                print("WARNING: Attribute not found")
        else: 
            self.scenarioParametersAttrib.pop(key)
            if self.verbosity==0:
                print('INFO: Attribute deleted', key)
        if key in self.scenarioParametersPointer.attrib:
            del self.scenarioParametersPointer.attrib[key]
        utility.write_on_file(self.write, self.tree)

    def removeScenarioParameters(self,key):
        element=self.scenarioParametersPointer.find(utility.BPSIM + key)
        self.scenarioParametersPointer.remove(element)
        utility.write_on_file(self.write, self.tree)


    ## METODI TO MODIFY SCENARIO ATTRIBUTES
    def setName(self, name):
        if name is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.name = name
        self.root.set('name', name)
        utility.write_on_file(self.root, self.tree)
        if self.verbosity==0:
            print("INFO: Name of Scenario updated ")

    def setId(self, id):
        if id is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.id = id
        self.root.set('id', id)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Id of Scenario updated ")

    def setAuthor(self, author):
        if author is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.author = author
        self.root.set('author', author)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Author of Scenario updated ")

    def setDescription(self, description):
        if description is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.description = description
        self.root.set('description', description)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Description of Scenario updated")

    def setCreated(self, created):
        if created is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.created = created
        self.root.set('created', created)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Created of Scenario  updated ")

    def setModified(self, modified):
        if modified is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.modified = modified
        self.root.set('modified', modified)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Modified of Scenario updated ")

    def setVersion(self, version):
        if version is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.version = version
        self.root.set('version', version)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Version of Scenario updated ")
  
    def setVendor(self, vendor):
        if vendor is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.vendor = vendor
        self.root.set('vendor', vendor)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Vendor of Scenario updated ")

    def setInherits(self, inherits):
        if inherits is None:
            raise ValueError("ERROR: Invalid value. Use remove method to make the attribute None")
        self.inherits = inherits
        self.root.set('inherits', inherits)
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Inherits of Scenario updated ")

    def removeScenarioAttribute(self, key):
        if key not in self.attributes:
            print("WARNING: Attribute not found")
        else:
            self.attributes.pop(key)
            if self.verbosity==0:
                print('INFO: attribute deleted', key)
        if key in self.root.attrib:
            del self.root.attrib[key]
        utility.write_on_file(self.write, self.tree)

    def remove(self):
        parent=self.root.getparent()
        for child in parent:
            if child==self.root:
                parent.remove(child)
        if self.verbosity==0:
            print("INFO: Scenario (", self.name, ") removed")
        utility.write_on_file(self.write, self.tree)


    ## METHODS TO MODIFY SCENARIO-PARAMETERS
    def setBaseTimeUnit(self, new):
        self.ScenarioParameters.setBaseTimeUnit(new)
        self.scenarioParametersPointer.set('baseTimeUnit', new)
        utility.write_on_file(self.write, self.tree)

    def setReplication(self, new):
        self.ScenarioParameters.setReplication(new)
        self.scenarioParametersPointer.set('replication', str(new))
        utility.write_on_file(self.write, self.tree)

    def setSeed(self, new):
        self.ScenarioParameters.setSeed(new)
        self.scenarioParametersPointer.set('seed', str(new))
        utility.write_on_file(self.write, self.tree)

    def setBaseCurrentyUnit(self, new):
        self.ScenarioParameters.setBaseCurrentyUnit(new)
        self.scenarioParametersPointer.set('baseCurrentyUnit', new)
        utility.write_on_file(self.write, self.tree)

    def setShowResultRequestColumn(self, new):
        self.ScenarioParameters.setShowResultRequestColumn(new)
        self.scenarioParametersPointer.set('showResultRequestColumn', new)
        utility.write_on_file(self.write, self.tree)

    def setExpressionLanguage(self, new):
        self.ScenarioParameters.setExpressionLanguage(new)
        self.scenarioParametersPointer.set('expressionLanguage', new)
        utility.write_on_file(self.write, self.tree)
    
    def setBaseResultFrequency(self, new):
        self.ScenarioParameters.setBaseResultFrequency(new)
        self.scenarioParametersPointer.set('baseResultFrequency', new)
        utility.write_on_file(self.write, self.tree)

    def setBaseResultFrequencyCumul(self, new):
        self.ScenarioParameters.setBaseResultFrequencyCumul(new)
        self.scenarioParametersPointer.set('baseResultFrequencyCumul', new)
        utility.write_on_file(self.write, self.tree)

    def setTraceOutput(self, new):
        self.ScenarioParameters.setTraceOutput(new)
        self.scenarioParametersPointer.set('traceOutput', new)
        utility.write_on_file(self.write, self.tree)

    def setTraceFormat(self, new):
        self.ScenarioParameters.setTraceFormat(new)
        self.scenarioParametersPointer.set('traceFormat', new)
        utility.write_on_file(self.write, self.tree)

    ### ADD CALENDAR 
    def addCalendar(self, id, name, calendar):
        if id is None or name is None or calendar is None:
             raise ValueError("ERROR: Insert id, name and iCalendar object")
        else:
            attrib={"name":name, "id": id}
            self.calendars.append(id)
            cal= etree.SubElement(self.root, utility.BPSIM + "Calendar", attrib=attrib)
            try:
                cal.text= calendar.to_ical()
            except:
                raise ValueError("ERROR: Insert iCalendar Object")
            cal.text="\n" + cal.text.replace("\r", "")
            utility.write_on_file(self.write, self.tree)
            if self.verbosity==0:
                print("INFO: Calendar  " + str(attrib) +  " added")

    def getCalendars(self):
        return self.calendars

    ## ADD CHECK XOR
    def getXorList(self, id):
        return self.xor[value]

    def getXor(self):
        return self.xor

    def setXor(self, value, idXor, idSequence):
        for sequence in self.xor[idXor]:
            if idSequence== sequence[0]:
                self.xor[idXor].remove(sequence)
                self.xor[idXor].append((idSequence, value))
        tot=0
        for sequence in self.xor[idXor]:
            tot= tot + sequence[1]
        if tot!=1:
            if self.verbosity==0 or self.verbosity==1:
                print("WARNING: Probability of all sequenceFlows must be one")

    def findGateway(self, id, element):
        sequenceFlowList=[]
        process= self.write.find(utility.BPMN2+"process") 
        for gateway in process.findall(utility.BPMN2 + "exclusiveGateway"):
            if gateway.get("id")==id:
                for sequence in gateway.findall(utility.BPMN2 + "outgoing"):
                    sequenceFlowList.append(sequence.text)
        return sequenceFlowList

    def auxfindGateway(self, id, subProcess, sequenceFlowList):
        for child in subProcess:
            if child.tag==utility.BPMN2 + "subProcess":
                self.auxfindGateway(id, child, sequenceFlowList)
            else:
                if child.get("id")==id:
                    for sequence in child.findall(utility.BPMN2 + "outgoing"):
                        sequenceFlowList.append(sequence.text)
        return sequenceFlowList

    def addXor(self, id):
        sequenceFlowList=self.findGateway(id, "process")
        if not sequenceFlowList:
            process= self.write.find(utility.BPMN2+"process") 
            sequenceFlowList=self.auxfindGateway(id, process, sequenceFlowList)
        tuple=[]
        for sequence in sequenceFlowList:
            tuple.append((sequence, 1/len(sequenceFlowList)))
        self.xor[id]= tuple