from BPSimpy.Parameter import Parameter
from BPSimpy import utility
import xml.etree.ElementTree as ET
from lxml import etree, objectify

class PriorityParameter(Parameter):

    def __init__(self):
        super().__init__()
        self.priorityPointer = None
        self.pointerPriority= None
        self.pointerInterruptible= None

    ## METHOD TO CHECK PRIORITY-PARAMETER TAG
    def checkPriorityParametersTag(self):
        if self.priorityPointer is None:
            self.addPriorityParameterTag()

    ## METHOD TO ADD PRIORITY-PARAMETER TAG
    def addPriorityParameterTag(self):
        self.priorityPointer= etree.SubElement(self.elementRefPointer, utility.BPSIM + "PriorityParameters")
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: PriorityParameters added")

    ## METHOD TO ADD INTERRUPTIBLE
    def addInterruptible(self, bool):
        if bool==None:
            raise ValueError("ERROR: To add Interruptible insert value")
        elif super().checkBooleanParameter(bool)==False:
            raise ValueError("ERROR: Interruptible requires BooleanParameters")
        else:
            self.checkPriorityParametersTag()
            if self.pointerInterruptible is None:
                self.pointerInterruptible=etree.SubElement(self.priorityPointer, utility.BPSIM + "Interruptible")
            new_parameter=etree.SubElement(self.pointerInterruptible, utility.BPSIM + "BooleanParameters", attrib={"value": str(bool)})
            utility.write_on_file(self.write, self.tree)
            if self.verbosity==0:
                print("INFO: Interruptible added BooleanParameter ", {"value":bool} )

    ## METHOD TO SET INTERRUPTIBLE ATTRIBUTES
    def setInterruptible(self, bool):
        if self.pointerInterruptible is None:
            raise ValueError("ERROR: Interruptible not exists")
        if super().checkBooleanParameter(bool)==False:
            raise ValueError("ERROR: Interruptible requires BooleanParameters")
        new_parameter = self.pointerInterruptible.findall("./"+ utility.BPSIM + 'BooleanParameter')
        new_parameter[-1].set('bool',str(bool))
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Interruptible updated" )
    
    ## METHOD TO ADD PRIORITY
    def addPriority(self, value):
        if value==None:
            raise ValueError("ERROR: To add Priority insert value")
        self.type=super().checkParameterType(value)
        if self.type is "NumericParameter" or self.type is "FloatingParameter":
            self.checkPriorityParametersTag()
            if self.pointerPriority is None:
                self.pointerPriority=etree.SubElement(self.priorityPointer, utility.BPSIM + "Priority")
            new_parameter=etree.SubElement(self.pointerPriority, utility.BPSIM + self.type, attrib={"value":str(value)})
            utility.write_on_file(self.write, self.tree)
            if self.verbosity==0:
                print("INFO: Interruptible added " + self.type, {"value":str(value)})
        else:
            raise ValueError("ERROR: Priority requires NumericParameter or FloatingParameter")

    ## METHOD TO SET PRIORITY
    def setPriority(self,value):
        if self.pointerPriority is None:
            raise ValueError("ERROR: Priority not exists")
        type=super().checkParameterType(value)
        if type is not "NumericParameter" or type is not "FloatingParameter":
            raise ValueError("ERROR: Priority requires NumericParameter or FloatingParameter")
        new_parameter = self.pointerPriority.findall("./"+ utility.BPSIM + self.type)
        new_parameter[-1].set('value',str(value))
        utility.write_on_file(self.write, self.tree)
        if self.verbosity==0:
            print("INFO: Priority updated" )