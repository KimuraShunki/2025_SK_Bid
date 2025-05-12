import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.ValueSet import ValueSet


class DiscreteValueSetTest(unittest.TestCase):

    A = DiscreteValue("a");
    A1 = DiscreteValue("a");
    B = DiscreteValue("b");
    values:List[DiscreteValue]  = [A, B]
    valuesReverse = [B, A]

    set1 = DiscreteValueSet(values)
    setReverse = DiscreteValueSet(valuesReverse)
    asString = "{\"values\":[\"a\",\"b\"]}"
    # String asString = "{\"DiscreteValueSet
    # \":[\"a\",\"b\"]}";
    asString1 = "[\"a\",\"b\"]"

    # SPECIAL. note that the "numbers" have no leading "=" and therefore are
    # parsed as discrete values.
    discretenumbers = "{\"values\":[\"0\",\"1\"]}"
    jackson = ObjectMapper()

    def  testSerialize(self) :
        jsonobj = self.jackson.toJson(self.set1)
        print(jsonobj)
        self.assertEqual(json.loads(self.asString), jsonobj)

    def testDeserialize(self):
        p = self.jackson.parse(json.loads(self.asString), DiscreteValueSet)
        print(p)
        self.assertEqual(self.set1, p)

    def testDeserializeNumberValues(self):
        p = self.jackson.parse(json.loads(self.discretenumbers), DiscreteValueSet)
        print(p)
        self.assertEqual("0", p.get(0).getValue()) # not the number but string
        self.assertEquals("1", p.get(1).getValue())

    def testEquality(self):
        self.assertEqual(self.set1, self.setReverse)

    def testHashCodeInsensitiveToOrder(self):
        self.assertEqual(hash(self.set1), hash(self.setReverse))

    def testSize(self):
        self.assertEqual(2, self.set1.size())

    def testGet(self): 
        self.assertEqual(self.A, self.set1.get(0))
        self.assertEqual(self.B, self.set1.get(1))
        self.assertEqual(self.A, self.set1.get(0))
        self.assertEqual(self.B, self.set1.get(1))

    def testgetValues(self):
        self.assertEqual(self.values, self.set1.getValues())

    def testConstructor2(self):
        self.assertEqual(self.set1, DiscreteValueSet([self.A, self.B]))

    def testContains(self):
        self.assertTrue(self.set1.contains(self.A))
        self.assertTrue(self.set1.contains(self.A1))
        self.assertTrue(self.set1.contains(self.B))
        self.assertFalse(self.set1.contains(DiscreteValue("c")))
        self.assertFalse(self.set1.contains(None))

    def testiterator1(self) :
        it = iter(self.set1);
        self.assertEqual(self.A, next(it));
        self.assertEqual(self.B, next(it));
        self.assertRaises(StopIteration, lambda: next(it))

    def testiterator2(self): 
        it = iter(self.setReverse)
        self.assertEqual(self.B, next(it))
        self.assertEqual(self.A, next(it));
        self.assertRaises(StopIteration,lambda: next(it))
