from decimal import Decimal
from typing import Dict, List
import unittest
from unittest.mock import Mock

from tudelft.utilities.immutablelist.Range import Range

from geniusweb.bidspace.pareto.GenericPareto import GenericPareto
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.NumberValueSet import NumberValueSet
from geniusweb.issuevalue.Value import Value
from geniusweb.issuevalue.ValueSet import ValueSet
from geniusweb.profile.PartialOrdering import PartialOrdering


class GenericParetoTest(unittest.TestCase):
	I1V2 = DiscreteValue("i1v2")
	I1V1 = DiscreteValue("i1v1")
	I2V1 = NumberValue(Decimal("2.00"))
	I2V2 = NumberValue(Decimal("2.45"))
	I2V3 = NumberValue(Decimal("2.90"))
	DOMAINNAME = "testdomain"
	ISSUE1 = "issue1"
	ISSUE2 = "issue2"
	issues:Dict[str, ValueSet] = {}

	def setUp(self):
		discretevalues1 = []
		discretevalues1.append(self.I1V1)
		discretevalues1.append(self.I1V2)
		values1 = DiscreteValueSet(discretevalues1)
		self.issues[self.ISSUE1] = values1

		values2 = NumberValueSet(Range(Decimal(2), Decimal(3), Decimal("0.45")))
		self.issues[self.ISSUE2] = values2

		self.domain = Domain(self.DOMAINNAME, self.issues)

		issuevalues:Dict[str, Value] = {}
		issuevalues[self.ISSUE1] = self.I1V1
		issuevalues[self.ISSUE2] = self.I2V1
		self.bid1 = Bid(issuevalues)
		issuevalues[self.ISSUE1] = self.I1V1
		issuevalues[self.ISSUE2] = self.I2V2
		self.bid2 = Bid(issuevalues)
		issuevalues[self.ISSUE1] = self.I1V2
		issuevalues[self.ISSUE2] = self.I2V1
		self.bid3 = Bid(issuevalues)

		self.profile1 = Mock(PartialOrdering)
		self.profile2 = Mock(PartialOrdering)
		self.profile3 = Mock(PartialOrdering)
		self.profile1.getDomain = Mock(return_value=self.domain)
		self.profile2.getDomain = Mock(return_value=self.domain)
		self.profile3.getDomain = Mock(return_value=self.domain)

		self.pareto = GenericPareto([self.profile1, self.profile2])

	def testgenericParetoTest(self):

		# fefault: there is no preference at all, all isPreferredOrEqual
		# returns false and we can't remove pareto points.

		profiles:List[PartialOrdering] = [self.profile1, self.profile2]
		# In python we need to set also False values
		self.profile1.isPreferredOrEqual = Mock(return_value=False)
		self.profile2.isPreferredOrEqual = Mock(return_value=False)
		pareto = GenericPareto(profiles)

		points = pareto.getPoints()
		self.assertEqual(6, len(points))

	def testgenericParetoTest1(self):

		# both prefer bid1 over any other bid.
		self.profile1.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid1
		self.profile2.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid1

		points = self.pareto.getPoints()
		self.assertEqual(1, len(points))
		self.assertEqual(self.bid1, next(iter(points)))

	def testgenericParetoTest2(self):

		# both prefer bid2 over any other bid.
		self.profile1.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid2
		self.profile2.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid2

		points = self.pareto.getPoints()
		# since both prefer bid2, bid is pareto point.
		self.assertEqual(1, len(points))
		self.assertEqual(self.bid2, next(iter(points)))

	def testgenericParetoTest3(self):
		# profile1 prefers bid1, profile2 prefers bid2.
		# now neither bid1 nor bid2 are dominating each other
		# and nor does bid1 or bid2 dominate anything else.
		self.profile1.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid1
		self.profile2.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid2

		points = self.pareto.getPoints()
		# since both prefer bid2, bid is pareto point.
		self.assertEquals(6, len(points))

	def testgenericParetoTest4(self):

		# profile1 prefers bid1, profile2 prefers bid2.
		# but they both hate bid3.
		self.profile1.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b1 == self.bid1 or b2 == self.bid3
		self.profile2.isPreferredOrEqual.side_effect = \
			lambda b1, b2: b2 == self.bid3 or b1 == self.bid2

		points = self.pareto.getPoints()
		# both hate bid3 but don't agree on bid1/2. bid3 is ruled out.
		self.assertEqual(5, len(points))

	def testNullNotOk(self):
		self.assertRaises(ValueError,
			lambda:GenericPareto([self.profile1, None, self.profile1]))

	def testImmutable(self):
		list = [self.profile1, self.profile2]
		pareto = GenericPareto(list)
		# if we modify the list, the pareto should not change
		list.append(self.profile3)
		self.assertEqual(2, len(pareto.getProfiles()))

	# in python we just copy the list so adding should  do nothing
	def testGetParetoAndAdd(self):
		list = self.pareto.getProfiles()
		list.append(self.profile3)
		self.assertEqual(2, len(self.pareto.getProfiles()))

	def testGetPointsAndAdd(self):
		self.assertEqual(1, len(self.pareto.getPoints()))
		list = self.pareto.getPoints()
		list.add(self.bid1)
		self.assertEqual(1, len(self.pareto.getPoints()))
