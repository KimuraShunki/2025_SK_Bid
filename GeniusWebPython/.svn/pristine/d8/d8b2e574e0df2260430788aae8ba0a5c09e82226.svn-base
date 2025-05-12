from decimal import Decimal
from typing import Dict, List
import unittest
from unittest.mock import Mock

from tudelft.utilities.immutablelist.Range import Range
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.Offer import Offer
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.NumberValueSet import NumberValueSet
from geniusweb.issuevalue.Value import Value
from geniusweb.issuevalue.ValueSet import ValueSet
from geniusweb.opponentmodel.FrequencyOpponentModel import FrequencyOpponentModel
from geniusweb.progress.Progress import Progress


class FrequencyOppModelTest (unittest.TestCase, GeneralTests[FrequencyOpponentModel]):
	ISS1 = "issue1"
	ISS2 = "issue2";
	I1V1 = DiscreteValue("i1v1")
	I1V2 = DiscreteValue("i1v2");
	I2V1 = DiscreteValue("i2v1")
	I2V2 = DiscreteValue("i2v2")
	I1V2b = DiscreteValue("i1v2b");
	progress = Mock(Progress);
	other = PartyId("other")
	HALF = Decimal("0.5")
	# list:List[List[Bid]]  = []

	def setUp(self):
		issues:Dict[str, ValueSet] = {}
		discretevalues1:List[DiscreteValue] = []
		discretevalues1.append(self.I1V1);
		discretevalues1.append(self.I1V2);
		values1 = DiscreteValueSet(discretevalues1)
		issues[self.ISS1] = values1
		values2 = NumberValueSet(Range(Decimal(0), Decimal(10), Decimal("0.3")))
		issues[self.ISS2] = values2
		self.domain = Domain("test", issues)
		self.domain2 = Domain("test2", issues)

		# slightly different issue1
		issues = {}
		discretevalues1 = []
		discretevalues1.append(self.I1V1)
		discretevalues1.append(self.I1V2b)
		values1 = DiscreteValueSet(discretevalues1)
		issues[self.ISS1] = values1
		values2 = NumberValueSet(Range(Decimal(0), Decimal(10), Decimal("0.3")))
		issues[self.ISS2] = values2
		self.domain3 = Domain("test", issues)

		# all bids are for domain
		issuevalues:Dict[str, Value] = {}
		issuevalues[self.ISS1] = self.I1V1
		issuevalues[self.ISS2] = NumberValue(Decimal("1.2"))
		self.bid1 = Bid(issuevalues)

		issuevalues[self.ISS1] = self.I1V1
		issuevalues[self.ISS2] = NumberValue(Decimal("1.5"))
		self.bid2 = Bid(issuevalues)

		issuevalues[self.ISS1] = self.I1V2
		issuevalues[self.ISS2] = NumberValue(Decimal("1.5"))
		self.bid3 = Bid(issuevalues)

		self.oppModel1 = FrequencyOpponentModel.create().With(self.domain, None)
		self.oppModel1b = FrequencyOpponentModel.create().With(self.domain, None)
		self.oppModel2 = FrequencyOpponentModel.create().With(self.domain2, None)
		self.oppModel3 = FrequencyOpponentModel.create().With(self.domain3, None)
		self.oppModel4 = self.oppModel3.WithAction(Offer(self.other, self.bid1), self.progress)

	# Override
	def getGeneralTestData(self) -> List[List[FrequencyOpponentModel]]:
		return [[self.oppModel1, self.oppModel1b],
				[self.oppModel2], [self.oppModel3], 	[self.oppModel4]]

	# Override
	def getGeneralTestStrings(self) -> List[str]:
		return ["FrequencyOpponentModel\\[0,\\{issue.=\\{\\}, issue.=\\{\\}\\}\\]",
				"FrequencyOpponentModel\\[0,\\{issue.=\\{\\}, issue.=\\{\\}\\}\\]",
				"FrequencyOpponentModel\\[0,\\{issue.=\\{\\}, issue.=\\{\\}\\}\\]",
				"FrequencyOpponentModel\\[1,\\{issue.*, issue.*"]

	def testsmokeTestNull(self):
		self.assertRaises(ValueError, lambda:FrequencyOpponentModel.create().With(None, None))

	def testsmokeTest(self):
		FrequencyOpponentModel.create().With(self.domain, None)

	def testEmptyModel(self):
		oppModel = FrequencyOpponentModel.create().With(self.domain, None)
		self.assertEqual(1, oppModel.getUtility(self.bid1))
		self.assertEqual(1, oppModel.getUtility(self.bid2))
		
	def testEmptyModelPartialBid(self):
		oppModel = FrequencyOpponentModel.create().With(self.domain, None)
		bid = Bid({})
		self.assertEqual(1, oppModel.getUtility(bid))

	def testPartialUtility(self):
		freqs:Dict[str, Dict[Value, int]] = {}
		freqs1:Dict[Value, int] = {}
		freqs2:Dict[Value, int] = {}

		freqs1[self.I1V1] = 2
		freqs1[self.I1V2] = 0
		freqs2[self.I2V1] = 1
		freqs2[self.I2V2] = 1

		freqs[self.ISS1] = freqs1
		freqs[self.ISS2] = freqs2
		total = Decimal(2)

		oppModel = FrequencyOpponentModel(self.domain, 	freqs, total, None)

		E = 0.0000001
		self.assertAlmostEqual(0.5, oppModel.getUtility(Bid({self.ISS1: self.I1V1})), None, E)
		self.assertAlmostEqual(0, oppModel.getUtility(Bid({self.ISS1: self.I1V2})))
		self.assertAlmostEqual(0.25,
				oppModel.getUtility(Bid({self.ISS2:self.I2V1})), None, E)
		self.assertAlmostEqual(0.25, oppModel.getUtility(Bid({self.ISS2: self.I2V2})))

	def testUpdate(self):
		oppModel = self.oppModel1.WithAction(Offer(self.other, self.bid1),
				self.progress);
		self.assertEqual(1, oppModel.getUtility(self.bid1))
		self.assertEqual(0, oppModel.getUtility(self.bid3))
		# bid2 has 1 of 2 issue values same as bid1.
		self.assertTrue(0.5, oppModel.getUtility(self.bid2))

	def testUpdate2(self):
		# bid1 and bid2 both want I1V1. They differ on the number value.
		# bid3 wants I1V2 but does have the number value from bid2
		oppModel = self.oppModel1\
				.WithAction(Offer(self.other, self.bid1), self.progress)\
				.WithAction(Offer(self.other, self.bid2), self.progress)
		self.assertEqual(0.75, oppModel.getUtility(self.bid1))
		self.assertEqual(0.75, oppModel.getUtility(self.bid2))
		self.assertEqual(0.25, oppModel.getUtility(self.bid3)) 

	def testPartialBidUpdate(self):
		oppModel = self.oppModel1.WithAction(Offer(self.other, self.bid1),
				self.progress)
		partialbid = Bid({self.ISS1: self.I1V1})
		oppModel.WithAction(Offer(self.other, partialbid), self.progress)

	def testGetCounts(self):
		self.assertEqual({}, self.oppModel1.getCounts(self.ISS1))
		self.assertEquals({}, self.oppModel1.getCounts(self.ISS2))

		values1:Dict[str, Value] = {}
		values1[self.ISS1] = self.I1V1
		values1[self.ISS2] = self.I2V1
		offer1 = Offer(self.other, Bid(values1))

		oppmod = self.oppModel1.WithAction(offer1, self.progress)

		self.assertEqual(1, oppmod.getCounts(self.ISS1)[self.I1V1])
		self.assertFalse(self.I1V2 in oppmod.getCounts(self.ISS1))
		self.assertEquals(1, oppmod.getCounts(self.ISS2)[self.I2V1])
		self.assertFalse(self.I2V2 in oppmod.getCounts(self.ISS2))

		# same identical bid. Counts should go to 2
		oppmod = oppmod.WithAction(offer1, self.progress)

		self.assertEquals(2, oppmod.getCounts(self.ISS1)[self.I1V1])
		self.assertEquals(2, oppmod.getCounts(self.ISS2)[self.I2V1])

		values2:Dict[str, Value] = {}
		values2[self.ISS1] = self.I1V2
		values2[self.ISS2] = self.I2V2
		offer2 = Offer(self.other, Bid(values2))

		# Other bid. with value2 for both issues
		oppmod = oppmod.WithAction(offer2, self.progress)

		self.assertEqual(2, oppmod.getCounts(self.ISS1)[self.I1V1])
		self.assertEqual(2, oppmod.getCounts(self.ISS2)[self.I2V1])
		self.assertEqual(1, oppmod.getCounts(self.ISS1)[self.I1V2])
		self.assertEqual(1, oppmod.getCounts(self.ISS2)[self.I2V2])

	def testStableName(self):
		name = self.oppModel1.getName()
		self.assertNotEqual(None, name)
		self.assertEqual(name, self.oppModel1.getName())
		
