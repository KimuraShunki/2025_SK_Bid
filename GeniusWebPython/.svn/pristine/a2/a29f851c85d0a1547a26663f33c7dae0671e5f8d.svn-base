import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.references.Parameters import Parameters


class ParametersTest (unittest.TestCase, GeneralTests[Parameters]) :
	pyson=ObjectMapper()
	params1=Parameters()
	params1a=Parameters()
	params2=Parameters({'a':1, 'b':2.0})

	paramsjson='{"a":1, "b":2.0}'

	def getGeneralTestData(self)-> List[List[Parameters]] :
		return [[ self.params1, self.params1a],[self.params2]]

	def getGeneralTestStrings(self)->List[str]:
		return ["\\{\\}", "\\{a=1, b=2.0\\}"]


	def testGet(self):
		self.assertEqual({'a':1, 'b':2.0}, self.params2.getParameters())
		

	def testGetWrongClass(self):
		self.assertRaises(ValueError, lambda:self.params2.getType("a", str))

	def testGetInteger(self) :
		self.assertEqual(1, self.params2.getType("a", int))
		self.assertEqual(2.0, self.params2.getType("b", float))

	def testGetDouble(self):
		self.assertEquals( 2., self.params2.getDouble("b", 7.0, None, None))
		self.assertEquals(2., self.params2.getDouble("b", 7.0, 0., 4.))

		# test outside range
		self.assertEqual(7., self.params2.getDouble("b", 7., 4., 6.))
		self.assertEqual(7., self.params2.getDouble("b", 7., -2., 1.))

		# test fallback None
		self.assertEqual(None, self.params2.getDouble("b", None, 4., 6.))
		# a is integer!
		self.assertEqual(1, self.params2.getDouble("a", 0., -0., 2.))		

	def testGetDoubleWithErrors(self):
		# a does not contain a double
		self.assertEqual(7., self.params2.getDouble("a", 7., 4., 6.));
		# c does not exist
		self.assertEqual(7., self.params2.getDouble("c", 7., 4., 6.));

	def testWith(self):
		p = self.params2.With("a", 2)
		self.assertEqual(1, self.params2.get("a"))
		self.assertEqual(2., self.params2.get("b"))
		self.assertEqual(2, p.get("a"))
		self.assertEqual(2., p.get("b"))

	def testWithParams(self):
		upd = Parameters().With("a", 2)
		p = self.params2.WithParameters(upd)
		self.assertEqual(1, self.params2.get("a"))
		self.assertEqual(2., self.params2.get("b"))
		self.assertEqual(2, p.get("a"))
		self.assertEqual(2., p.get("b"))

	def testIsEmpty(self) :
		self.assertTrue(self.params1.isEmpty())
		self.assertFalse(self.params2.isEmpty())

	def testContainsKey(self):
		self.assertTrue(self.params2.containsKey("a"))
		self.assertFalse(self.params2.containsKey("c"))


	def testSerialize(self):
		print(str(self.pyson.toJson(self.params2)))
		self.assertEqual(json.loads(self.paramsjson), self.pyson.toJson(self.params2))
		
	def testDeserialize(self):
		self.assertEqual(self.params2, self.pyson.parse(json.loads(self.paramsjson), Parameters))
	
		
	def testWith2(self):
		p=Parameters({'a':1}).With('b', 2)
		self.assertEqual({'a':1, 'b':2}, p.getParameters())
		
	def testParamNotAvailable(self):
		self.assertEqual(None, self.params1.get("nosuchkey"))
		