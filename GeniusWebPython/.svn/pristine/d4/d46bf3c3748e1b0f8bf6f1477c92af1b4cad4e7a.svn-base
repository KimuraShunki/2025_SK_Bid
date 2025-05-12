from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Accept import Accept
from geniusweb.actions.Action import Action
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.NumberValue import NumberValue


class OfferTest (unittest.TestCase) :
	pyson=ObjectMapper()
	actor=PartyId("myid")
	bid=Bid({'fte':NumberValue(Decimal(3)), 'leasecar':DiscreteValue('yes')})
	bid2=Bid({'fte':NumberValue(Decimal(3)), 'leasecar':DiscreteValue('no')})
	accept=Accept(actor, bid)
	accept2=Accept(actor, bid2)

	def testSerialize(self):
		print(str(self.pyson.toJson(self.accept)))
		self.assertEqual({'Accept': {'actor': 'myid', 'bid': {'issuevalues':{'fte': 3, 'leasecar': "yes"}}}},\
						self.pyson.toJson(self.accept))
		
	def testDeserialize(self):
		jsonoffer= self.pyson.toJson(self.accept)
		self.assertEqual(self.accept, self.pyson.parse(jsonoffer, Action))
	
	def testRepr(self):
		self.assertEqual('Accept[myid,Bid{fte=3, leasecar="yes"}]', repr(self.accept))
		
	def testEqual(self):
		self.assertEqual(self.accept, self.accept)
		self.assertNotEqual(self.accept, self.accept2)
		self.assertEqual(hash(self.accept), hash(self.accept))
		self.assertNotEqual(hash(self.accept), hash(self.accept2))
		