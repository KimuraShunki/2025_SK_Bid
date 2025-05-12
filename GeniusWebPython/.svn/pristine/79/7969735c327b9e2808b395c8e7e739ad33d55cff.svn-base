from _decimal import Decimal
import json
from typing import List, Any
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.Value import Value


class NumberValueTest(unittest.TestCase, GeneralTests[NumberValue]):
    value =  NumberValue(Decimal("12.31"))
    value1 =  NumberValue(Decimal("12.31"))
    value1c = NumberValue(Decimal("1.231E+1"))
    valueb =  NumberValue(Decimal("12.310000000000000001"))
    serialized = "12.31"

    bigserialized = "8748703924870439218876954320948372058"
    bigvalue = NumberValue(Decimal(bigserialized))
    jackson = ObjectMapper()

    def getGeneralTestData(self)->List[List[NumberValue]]:
        return [ [self.value, self.value1, self.value1c], [self.valueb]]
    
    def  getGeneralTestStrings(self)->List[str]:
        return ["12.31", "12.310000000000000001"]

    def testSerialize(self) :
        self.assertEquals(json.loads(self.serialized), self.jackson.toJson(self.value))

    def testDeserialize(self):
        self.assertEqual(self.value, self.jackson.parse(json.loads(self.serialized), NumberValue))

    def  testDeserializeFromValue(self):
        self.assertEqual(self.value, self.jackson.parse(json.loads(self.serialized), Value))

    def testBigSerialize(self):
        self.assertEqual(json.loads(self.bigserialized), self.jackson.toJson(self.bigvalue))

    def testBigDeserialize(self):
        self.assertEquals(self.bigvalue,
                self.jackson.parse(json.loads(self.bigserialized), NumberValue))

    def testSerializeShorts(self):
        print(self.jackson.toJson([ 1, 2, 3, 4, 5 ]))

    def testDeserializeShorts(self) :
        list = self.jackson.parse(json.loads("[1,2,3,4,5]"),List[Any])
        print(list)
        print(list[0].__class__)

    def testDeserializeMix(self):
        list = self.jackson.parse(json.loads('["short",1,2,3,4,5]'), List[Any])
        print(list)
        print(list[0].__class__)

    def testDeserializePlainNumber(self):
        '''
        Showing that we CAN deserialize big numbers without double quotes
        correctly, if we tell jackson upfront that it's a BigDecimal.
        '''
        valstr = "483958743698732691487326987569213874694328974329874328947320984372498327493827432987231874681273648127";
        val = self.jackson.parse(valstr, Decimal)
        self.assertEqual(valstr, str(val))


    def testNumberBlab(self):
        # jackson.enable(DeserializationFeature.USE_BIG_DECIMAL_FOR_FLOATS);
        self.assertEqual(self.value, self.jackson.parse(json.loads("12.31"), Value))
        
    def testNonNumber(self):
        self.assertRaises(ValueError, lambda: NumberValue("abc"))

    def testDeserializeScientificNotation(self):
        valstr = "9E+2";
        val = self.jackson.parse(json.loads(valstr), Value)
        # self.assertEqual(valstr, str(val)) FIXME? 
        self.assertEqual(val, NumberValue(Decimal("900")))
    