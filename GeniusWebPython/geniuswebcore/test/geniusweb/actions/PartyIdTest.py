import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.PartyId import PartyId


#FIXME support and test serialization
class PartyIdTest (unittest.TestCase) :

	pyson=ObjectMapper()
	party=PartyId("a")
	party1=PartyId("a")
	party2=PartyId("b")
	

	def testRestrictions(self):
		self.assertRaises(ValueError, lambda : PartyId(""))

	def testRestrictions2(self):
		self.assertRaises(ValueError, lambda:PartyId("@2"))

	def testRestrictions3(self) :
		self.assertRaises(ValueError, lambda:PartyId("_12"))
		

	def testRestrictions4(self):
		self.assertRaises(ValueError, lambda :PartyId("12A"))

	def testRestrictions5(self):
		self.assertRaises(ValueError,lambda :PartyId(" fds "))

	def testRestrictions6(self):
		PartyId("A_1_23_ok")

	def testRestrictions7(self):
		PartyId("a_1_23_ok")

	def testGetName(self):
		self.assertEqual("a", self.party1.getName());


	def testSerialize(self):
		print(str(self.pyson.toJson(self.party1)))
		self.assertEqual("a",self.pyson.toJson(self.party))
		
	def testDeserialize(self):
		self.assertEqual(self.party, self.pyson.parse("a", PartyId))


	def testRepr(self):
		self.assertEqual("a", repr(self.party))
		
	def testEqual(self):
		self.assertEqual(self.party, self.party1)
		self.assertNotEqual(self.party1, self.party2)
		self.assertEqual(hash(self.party), hash(self.party1))
		self.assertNotEqual(hash(self.party), hash(self.party2))
		