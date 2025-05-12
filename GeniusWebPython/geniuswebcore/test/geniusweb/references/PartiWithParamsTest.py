import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters


class PartiWithParamsTest (unittest.TestCase, GeneralTests[PartyWithParameters]):
	serialized = "{\"partyref\":\"ws:party1\",\"parameters\":{\"a\":1}}";

	party1 =  PartyRef( URI("ws:party1"))
	party2 =  PartyRef( URI("ws:party2"))
	param1 =  Parameters()
	param2 =  Parameters().With("a", 1)
	party1param1 =  PartyWithParameters(party1, param1)
	party1param1a = PartyWithParameters(party1, param1)
	party1param2 =  PartyWithParameters(party1, param2)

	def getGeneralTestData(self)->List[List[PartyWithParameters]]:
		return [[	self.party1param1, self.party1param1a, self.party1param1a],
				[self.party1param2]]

	def getGeneralTestStrings(self) ->List[str] :
		return ["PartyRef.ws:party1.","PartyRef.ws:party1.\\{a=1\\}"]

	def testSerialize(self) :
		jackson = ObjectMapper()

		jsonobj = jackson.toJson(self.party1param2)
		print(jsonobj)
		self.assertEqual(json.loads(self.serialized), jsonobj)

	def testDeserialize(self):
		jackson = ObjectMapper()
		p = jackson.parse(json.loads(self.serialized), PartyWithParameters)
		print(p)
		self.assertEqual(self.party1param2, p)
