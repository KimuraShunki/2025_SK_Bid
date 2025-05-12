import unittest

from pyson.ObjectMapper import ObjectMapper
from uri.uri import URI #type:ignore
from geniusweb.references.ProfileRef import ProfileRef


class ProfileRefTest (unittest.TestCase) :
	pyson=ObjectMapper()
	
	
	#NOTICE #38. We work around it here
	ref=ProfileRef(URI("http://local/"))
	ref1=ProfileRef(URI("http://local/"))
	ref2=ProfileRef(URI("http://host"))
	
	reftxt="http://local/" 
	refjson=reftxt

	def testSerialize(self):
		print(str(self.pyson.toJson(self.ref)))
		self.assertEqual(self.refjson, self.pyson.toJson(self.ref))
		
	def testDeserialize(self):
		self.assertEqual(self.ref, self.pyson.parse(self.refjson, ProfileRef))
	
	def testRepr(self):
		self.assertEqual("ProfileRef[http://local/]", repr(self.ref))
		
	def testEqual(self):
		self.assertEqual(self.ref, self.ref1)
		self.assertNotEqual(self.ref, self.ref2)
		self.assertEqual(hash(self.ref), hash(self.ref1))
		self.assertNotEqual(hash(self.ref), hash(self.ref2))
		
		