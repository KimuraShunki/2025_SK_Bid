import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.references.PartyRef import PartyRef


class PartyRefTest (unittest.TestCase, GeneralTests[PartyRef]):

	asJson = "\"ws:localhost/party1\""

	party1 =  PartyRef( URI("ws:localhost/party1"))
	party1a = PartyRef( URI("ws:localhost/party1"))
	party2 = PartyRef(URI("ws:localhost/party2"))
	party3 = PartyRef( URI("http:localhost/party3"))


	def getGeneralTestData(self) -> List[List[PartyRef]]:
		return [ [self.party1, self.party1a],[self.party2], [self.party3]]

	def getGeneralTestStrings(self) -> List[str] :
		return ["PartyRef.*party1.", "PartyRef.*party2.",
				"PartyRef.*party3."]

	def testSmoke(self) :
		PartyRef(URI("ws:localhost"))

	def testNull(self):
		self.assertRaises(ValueError, lambda:PartyRef(None))

	def testSerialize(self) :
		jackson = ObjectMapper()

		jsonobj = jackson.toJson(self.party1)
		print(json.dumps(jsonobj))
		self.assertEqual(self.asJson, json.dumps(jsonobj))

	def testDeserialize(self):
		jackson = ObjectMapper()
		p = jackson.parse(json.loads(self.asJson), PartyRef);
		print(p)
		self.assertEqual(self.party1, p)
