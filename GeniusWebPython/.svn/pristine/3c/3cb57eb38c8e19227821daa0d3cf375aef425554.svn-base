import unittest
from unitpy.GeneralTests import GeneralTests
from decimal import Decimal
from geniusweb.bidspace.Interval import Interval
from typing import List

class IntervalTest (unittest.TestCase, GeneralTests[Interval]):

	ZERO = Decimal(0)
	ONE = Decimal(1)
	TWO = Decimal(2)
	THREE = Decimal(3)
	TEN = Decimal(10)
	
	int1 = Interval(ZERO, ONE)
	int1a = Interval(ZERO, ONE)
	int2 = Interval(ONE, TEN)
	int3 = Interval(TWO, TEN)

	#Override
	def getGeneralTestData(self)->List[List[Interval]] :
		return [[self.int1, self.int1a], [self.int2],[self.int3]]

	#Override
	def getGeneralTestStrings(self) -> List[str] :
		return ["Interval\\[0,1\\]", "Interval\\[1,10\\]",
				"Interval\\[2,10\\]"]

	def testsmokeTest(self) :
		Interval(self.ZERO, self.ONE)

	def testsmokeTestBad(self):
		i = Interval(self.TEN, self.ONE)
		self.assertTrue(i.isEmpty())

	def testsmokeNull1Test(self):
		self.assertRaises(ValueError, lambda: Interval(None,self.ZERO))

	def testsmokeNull2test(self):
		self.assertRaises(ValueError, lambda:Interval(self.ZERO, None))

	def testMin(self):
		self.assertEqual(Decimal(0), self.int1.getMin())
		self.assertEqual(Decimal(1), self.int2.getMin())

	def testMax(self):
		self.assertEqual(Decimal(1), self.int1.getMax())
		self.assertEqual(Decimal(10), self.int2.getMax())

	def testcontainsTest(self):
		self.assertTrue(self.int1.contains(Decimal(0.3)))
		self.assertFalse(self.int1.contains(Decimal(-0.3)))
		self.assertFalse(self.int1.contains(Decimal(1.3)))

		self.assertFalse(self.int3.contains(self.ZERO))
		self.assertFalse(self.int3.contains(self.ONE))
		self.assertTrue(self.int3.contains(self.TWO));
		self.assertTrue(self.int3.contains(self.THREE));
		self.assertTrue(self.int3.contains(self.TEN));
		self.assertFalse(self.int3.contains(Decimal(10.3)))

	def testIntersect(self) :
		self.assertEqual(self.int1, self.int1.intersect(self.int1))
		self.assertEqual(Interval(self.ONE, self.ONE), self.int1.intersect(self.int2))
		self.assertTrue(self.int1.intersect(self.int3).isEmpty())
		self.assertEqual(Interval(self.ONE, self.TWO),
				Interval(self.ZERO, self.TEN).intersect(Interval(self.ONE, self.TWO)))
		self.assertEqual( Interval(self.ONE, self.TWO),
				Interval(self.ONE, self.TWO).intersect(Interval(self.ZERO, self.TEN)))
		self.assertEqual(Interval(self.ONE, self.TWO),
				Interval(self.ZERO, self.TWO).intersect(Interval(self.ONE, self.TEN)))
		self.assertEqual( Interval(self.ONE, self.TWO),
				Interval(self.ONE, self.TEN).intersect( Interval(self.ZERO, self.TWO)))

	def testsubtractTest(self):
		self.assertEqual(Interval(Decimal(-1), self.ZERO),
				self.int1.subtract(self.ONE))
	
	def testinvertTest(self) :
		self.assertEqual(Interval(Decimal(-10), self.ZERO),
				self.int1.invert(self.int2))
		self.assertEqual(Interval(self.ZERO, self.TEN), self.int2.invert(self.int1))
		self.assertEqual(
				Interval(Decimal(-9), Decimal(8)),
				self.int2.invert(self.int3))
