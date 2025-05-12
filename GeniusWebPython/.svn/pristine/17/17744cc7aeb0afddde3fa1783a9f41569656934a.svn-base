from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Action import Action
from geniusweb.actions.LearningDone import LearningDone
from geniusweb.actions.PartyId import PartyId


class OfferTest (unittest.TestCase) :
	actor=PartyId("myid")
	actor2=PartyId("otherid")
	learningdone=LearningDone(actor)
	learningdone1=LearningDone(actor)
	learningdone2=LearningDone(actor2)
	
	pyson=ObjectMapper()

	def testSerialize(self):
		self.assertEqual({'LearningDone': {'actor': 'myid'}},	self.pyson.toJson(self.learningdone))
		
	def testDeserialize(self):
		jsonenego= self.pyson.toJson(self.learningdone)
		self.assertEqual(self.learningdone, self.pyson.parse(jsonenego, Action))
		
	def testRepr(self):
		self.assertEqual("LearningDone[myid]", repr(self.learningdone))
		
	def testEqual(self):
		self.assertEqual(self.learningdone, self.learningdone1)
		self.assertNotEqual(self.learningdone, self.learningdone2)
		self.assertEqual(hash(self.learningdone), hash(self.learningdone1))
		self.assertNotEqual(hash(self.learningdone), hash(self.learningdone2))
		