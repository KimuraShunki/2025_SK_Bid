from decimal import Decimal
import unittest
from unittest.mock import Mock

from geniusweb.bidspace.pareto.ParetoPoint import ParetoPoint
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.Value import Value
from geniusweb.profile.utilityspace.LinearAdditive import LinearAdditive


class ParetoPointTest(unittest.TestCase):
	D0_2 = Decimal("0.2")
	D0_1 = Decimal("0.1")
	D0_3 = Decimal("0.3")
	D0_4 = Decimal("0.4")
	D0_5 = Decimal("0.5")
	space1 = Mock(LinearAdditive)	
	space2 = Mock(LinearAdditive)
	bid11 = Mock(Bid)
	bid12 = Mock(Bid)
	bid21 = Mock(Bid)
	bid22 = Mock(Bid)
	
	def setUp(self):
		self.space1.getUtility = Mock(side_effect=lambda b: \
			{self.bid11:self.D0_1, self.bid12:self.D0_1, \
			self.bid21:self.D0_2, self.bid22:self.D0_2 }[b]) 
		self.space2.getUtility = Mock(side_effect=lambda b: \
			{self.bid11:self.D0_1, self.bid12:self.D0_2, \
			self.bid21:self.D0_1, self.bid22:self.D0_2 }[b]) 

		self.point11 = ParetoPoint.create(self.bid11, [self.space1, self.space2])
		self.point12 = ParetoPoint.create(self.bid12, [self.space1, self.space2])
		self.point21 = ParetoPoint.create(self.bid21, [self.space1, self.space2])
		self.point22 = ParetoPoint.create(self.bid22, [self.space1, self.space2])

	def testconstructorTest(self):
		self.assertEqual(self.bid11, self.point11.getBid())
		self.assertEqual(self.bid21, self.point21.getBid())

		self.assertEqual([self.D0_1, self.D0_1], self.point11.getUtilities())
		self.assertEqual([self.D0_2, self.D0_1], self.point21.getUtilities())

	def testdominationTest(self):
		self.assertTrue(self.point11.isDominatedBy(self.point11))
		self.assertTrue(self.point11.isDominatedBy(self.point12))
		self.assertTrue(self.point11.isDominatedBy(self.point21))
		self.assertTrue(self.point11.isDominatedBy(self.point22))

		self.assertFalse(self.point12.isDominatedBy(self.point11))
		self.assertFalse(self.point12.isDominatedBy(self.point21))
		self.assertTrue(self.point12.isDominatedBy(self.point12))
		self.assertTrue(self.point12.isDominatedBy(self.point22))

		self.assertFalse(self.point21.isDominatedBy(self.point11))
		self.assertFalse(self.point21.isDominatedBy(self.point12))
		self.assertTrue(self.point21.isDominatedBy(self.point21))
		self.assertTrue(self.point21.isDominatedBy(self.point22))

		self.assertFalse(self.point22.isDominatedBy(self.point11))
		self.assertFalse(self.point22.isDominatedBy(self.point12))
		self.assertFalse(self.point22.isDominatedBy(self.point21))
		self.assertTrue(self.point22.isDominatedBy(self.point22))

	def testmergeTest(self):
		# partial bid 020_010 has value 0.2 for issue 2 in space1 and 0.1 for
		# issue 2 in space2.
		value1 = Mock(Value)
		value2 = Mock(Value)
		value3 = Mock(Value)

		partialbid020_010 = Bid({"issue2": value2})
		partialbid102_301 = Bid({"issue1": value1, "issue3":value3})
		# merged this should be a bid 122_311 so it has utilities
		# 1+2+2=0.5 in space1 and 3+1+1=0.5 in space2

		self.space1.getUtility = Mock(side_effect=lambda bid:\
			{partialbid020_010:self.D0_2, partialbid102_301:self.D0_3}[bid])
		self.space2.getUtility = Mock(side_effect=lambda bid:
			{partialbid020_010:self.D0_1, partialbid102_301:self.D0_4 }[bid])
	
		p1 = ParetoPoint.create(partialbid020_010, [self.space1, self.space2])
		p2 = ParetoPoint.create(partialbid102_301, [self.space1, self.space2])

		p = p1.merge(p2)
		bid = p.getBid()
		self.assertEqual(self.D0_5, p.getUtilities()[0])
		self.assertEqual(self.D0_5, p.getUtilities()[1])
