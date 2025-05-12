from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Action import Action
from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.PartyId import PartyId


class OfferTest (unittest.TestCase) :
	actor=PartyId("myid")
	actor2=PartyId("otherid")
	endnego=EndNegotiation(actor)
	endnego1=EndNegotiation(actor)
	endnego2=EndNegotiation(actor2)
	
	pyson=ObjectMapper()

	def testSerialize(self):
		self.assertEqual({'EndNegotiation': {'actor': 'myid'}},	self.pyson.toJson(self.endnego))
		
	def testDeserialize(self):
		jsonenego= self.pyson.toJson(self.endnego)
		self.assertEqual(self.endnego, self.pyson.parse(jsonenego, Action))
		
	def testRepr(self):
		self.assertEqual("EndNegotiation[myid]", repr(self.endnego))
		
	def testEqual(self):
		self.assertEqual(self.endnego, self.endnego1)
		self.assertNotEqual(self.endnego, self.endnego2)
		self.assertEqual(hash(self.endnego), hash(self.endnego1))
		self.assertNotEqual(hash(self.endnego), hash(self.endnego2))
		