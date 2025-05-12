from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper
from tudelft.utilities.immutablelist.Range import Range

from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.NumberValueSet import NumberValueSet
from geniusweb.issuevalue.ValueSet import ValueSet


class NumberValueSetTest(unittest.TestCase):
    pyson=ObjectMapper()
    val = NumberValueSet(Range(Decimal('12.2'), Decimal('12.6'), Decimal('0.3')))
    val1 = NumberValueSet(Range(Decimal('12.2'), Decimal('12.6'), Decimal('0.3')))
    val2 = NumberValueSet(Range(Decimal('12.2'), Decimal('12.7'), Decimal('0.3')))
    valjson = {"range":{"low":12.2,"high":12.6,"step":0.3}}

    def testInit(self):
        self.assertRaises(ValueError, lambda: NumberValueSet(range(1,5)))
        
    def testSerialize(self):
        print(str(self.pyson.toJson(self.val)))
        self.assertEqual(self.valjson, self.pyson.toJson(self.val))
        
    def testDeserialize(self):
        set:NumberValueSet= self.pyson.parse(self.valjson, ValueSet)
        self.assertEqual(self.val, set)
        self.assertTrue(isinstance(set.getRange().getLow(), Decimal))
        
    def testIterator(self):
        self.assertTrue(NumberValue(Decimal('12.2')) in self.val)
        
    def testGetter(self):
        set=NumberValueSet(Range(Decimal("900"),Decimal("1800"), Decimal("300")))
        print (str(set.get(1)))
        
    def testRepr(self):
        self.assertEqual("NumberValueSet[12.2,12.6,0.3]", repr(self.val))
        
    def testEqual(self):
        self.assertEqual(self.val, self.val1)
        self.assertNotEqual(self.val, self.val2)
        self.assertEqual(hash(self.val), hash(self.val1))
        self.assertNotEqual(hash(self.val), hash(self.val2))
        