import json
from pickle import NONE
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.Value import Value


class DiscreteValueTest(unittest.TestCase, GeneralTests[DiscreteValue]):
    value =  DiscreteValue("a")
    value1 =  DiscreteValue("a")
    valueb =  DiscreteValue("b")

    serialized = "\"a\"";
    jackson =  ObjectMapper();

    def testSerialize(self):
        print(str(self.jackson.toJson(self.value)))
        self.assertEqual(json.loads(self.serialized), self.jackson.toJson(self.value))
    
    def testEmpty(self):
        self.assertRaises(ValueError, lambda:DiscreteValue(""))
        
    def testDeserialize(self) :
        self.assertEqual(self.value, self.jackson.parse(json.loads(self.serialized), DiscreteValue))
 
    def testDeserializeFromValue(self):
        self.assertEqual(self.value, self.jackson.parse(json.loads(self.serialized), Value))
        
    def getGeneralTestData(self)->List[List[DiscreteValue]] :
        return [ [self.value, self.value1], [self.valueb]]

    def getGeneralTestStrings(self)->List[str]:
        return [self.serialized, "\"b\""]
    