import unittest
from decimal import Decimal

from geniusweb.issuevalue.ValueDeserializer import ValueDeserializer
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.NumberValue import NumberValue

class ValueDeserializerTest(unittest.TestCase):
       
    val = ValueDeserializer()
    
    def testValueDeserializer(self):
        #self.assertEqual(DiscreteValue(123),self.val.deserialize(123,1))
        self.assertEqual(DiscreteValue("123"),self.val.deserialize("123",1))
        self.assertEqual(NumberValue(Decimal(123)), self.val.deserialize(123,1))
        self.assertRaises(ValueError,lambda: self.val.deserialize([1,2,3],1))
