from decimal import Decimal
from typing import Set, Dict
import unittest
from unittest.mock import Mock

from geniusweb.bidspace.pareto.PartialPareto import PartialPareto
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.NumberValueSet import NumberValueSet
from geniusweb.issuevalue.Value import Value
from geniusweb.issuevalue.ValueSet import ValueSet
from geniusweb.profile.utilityspace.LinearAdditive import LinearAdditive


class PartialParetoTest(unittest.TestCase):
	D0_0 = Decimal(0)
	D0_2 = Decimal("0.2")
	D0_1 = Decimal("0.1")
	D0_3 = Decimal("0.3")
	D0_4 = Decimal("0.4")
	D0_5 = Decimal("0.5")

	space1 = Mock(LinearAdditive)
	space2 = Mock(LinearAdditive)

	domain = Mock(Domain)
	issues:Set[str] = set(["issue1", "issue2"])
	value1a = Mock(Value)
	value1b = Mock(Value)
	value2a = Mock(Value) 
	value2b = Mock(Value)

	def setUp(self):

		map:Dict[str, Value] = {}
		map["issue1"] = self.value1a
		self.bid10 = Bid(map)
		map["issue1"] = self.value1b
		self.bid20 = Bid(map)

		map = {}
		map["issue2"] = self.value2a
		self.bid01 = Bid(map)
		map["issue2"] = self.value2b
		self.bid02 = Bid(map)

		self.space1.getUtility = Mock(side_effect=lambda b: \
			{self.bid10:self.D0_1, self.bid20:self.D0_2, \
			self.bid01:self.D0_0, self.bid02:self.D0_0 }[b]) 
		self.space2.getUtility = Mock(side_effect=lambda b: \
			{self.bid10:self.D0_0, self.bid20:self.D0_0, \
			self.bid01:self.D0_0, self.bid02:self.D0_2 }[b]) 

		self.space1.getDomain = Mock(return_value=self.domain)
		self.domain.getIssues = Mock(return_value=self.issues)
		self.issue1valueset = DiscreteValueSet([self.value1a, self.value1b])
		self.domain.getValues = Mock(side_effect=lambda iss:\
					{"issue1":self.issue1valueset, "issue2":self.issue2valueset}[iss])
			
		# by putting the best value first in the list now,
		# we may trigger a different evaluation path in the PartialPareto
		# algorithm, improving coverage
		self.issue2valueset = DiscreteValueSet([self.value2b, self.value2a])

	def testOneIssueTest(self):
		pp = PartialPareto.create([self.space1, self.space2], ["issue1"])
		# bid22 is best for both. Check that's the only remaining point
		self.assertEqual(1, len(pp.getPoints()))
		map:Dict[str, Value] = {}
		map["issue1"] = self.value1b
		# there is no value for issue2 because we asked to exclude it from the
		# pareto.
		self.assertEqual(Bid(map), pp.getPoints()[0].getBid())

	def testTwoIssuesTest(self):
		pp = PartialPareto.create([self.space1, self.space2],
				["issue1", "issue2"])
		# bid22 is best for both. Check that's the only remaining point
		self.assertEqual(1, len(pp.getPoints()))
		map:Dict[str, Value] = {}
		map["issue1"] = self.value1b
		map["issue2"] = self.value2b
		self.assertEqual(Bid(map), pp.getPoints()[0].getBid())
