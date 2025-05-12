from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Action import Action
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.NumberValue import NumberValue


class OfferTest (unittest.TestCase) :
	actor=PartyId("myid")
	# HACK currently bid requires all values same type
	bid=Bid({'fte':NumberValue(Decimal(3)), 'leasecar':DiscreteValue('yes')})
	bid2=Bid({'fte':NumberValue(Decimal(3)), 'leasecar':DiscreteValue('no')})
	offer=Offer(actor, bid)
	offer1=Offer(actor, bid)
	offer2=Offer(actor, bid2)
	pyson=ObjectMapper()

	def testSerialize(self):
		print(str(self.pyson.toJson(self.offer)))
		self.assertEqual({'Offer': {'actor': 'myid', 'bid': {'issuevalues':{'fte': 3, 'leasecar': "yes"}}}},\
						self.pyson.toJson(self.offer))
		
	def testDeserialize(self):
		jsonoffer= self.pyson.toJson(self.offer)
		self.assertEqual(self.offer, self.pyson.parse(jsonoffer, Action))
		
	def testRepr(self):
		self.assertEqual('Offer[myid,Bid{fte=3, leasecar="yes"}]', repr(self.offer))
		
	def testEqual(self):
		self.assertEqual(self.offer, self.offer1)
		self.assertNotEqual(self.offer, self.offer2)
		self.assertEqual(hash(self.offer), hash(self.offer))
		self.assertNotEqual(hash(self.offer), hash(self.offer2))
		