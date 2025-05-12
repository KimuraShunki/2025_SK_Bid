import unittest
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from decimal import Decimal
from typing import Set, Dict
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.profile.utilityspace.DiscreteValueSetUtilities import DiscreteValueSetUtilities
from geniusweb.bidspace.IssueInfo import IssueInfo
from geniusweb.bidspace.Interval import Interval

class IssueInfoTest(unittest.TestCase):

	NAME = "name"
	VAL1 = DiscreteValue("v1")
	VAL2 = DiscreteValue("v2")
	VAL3 = DiscreteValue("v3")
	N03 = Decimal("0.3")
	N04 = Decimal("0.4")
	N05 = Decimal("0.5")
	N06 = Decimal("0.6")
	
	def setUp(self) :
		issuevalues:Set[DiscreteValue]  = set()
		issuevalues.add(self.VAL1)
		issuevalues.add(self.VAL2)
		issuevalues.add(self.VAL3)
		values = DiscreteValueSet(issuevalues)
		valueUtils:Dict[DiscreteValue,Decimal] = {}
		valueUtils[self.VAL1]= self.N03
		valueUtils[self.VAL2]= self.N04
		valueUtils[self.VAL3]= self.N05
		utils = DiscreteValueSetUtilities(valueUtils)
		self.info = IssueInfo(self.NAME, values, utils, self.N06, 6)

	def testsmokeTest(self):
		pass

	def testGetExtremeMin(self):
		self.assertEqual(self.VAL1, self.info.getExtreme(False))
		self.assertEqual(self.VAL3, self.info.getExtreme(True))

	def testgetNameTest(self):
		self.assertEqual(self.NAME, self.info.getName())

	def testgetIntervalTest(self):
		self.assertEqual(Interval(self.N03*self.N06, self.N05*self.N06),
				self.info.getInterval())
