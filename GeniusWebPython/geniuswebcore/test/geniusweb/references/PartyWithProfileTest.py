import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class PartyWithProfileTest (unittest.TestCase,  GeneralTests[PartyWithProfile]):

	serialized = "{\"party\":{\"partyref\":\"ws:party1\",\"parameters\":{}},\"profile\":\"ws:profile1\"}"

	party1 = PartyRef(URI("ws:party1"))
	party1a =  PartyRef( URI("ws:party1"))
	party2 =  PartyRef( URI("ws:party2"))
	party3 = PartyRef( URI("http:party3"))

	profile1 = ProfileRef(URI("ws:profile1"))
	profile2 = ProfileRef( URI("ws:profile2"))

	settings1 =  Parameters()
	settings2 =  Parameters({"a": 1})

	party1withparams1 =  PartyWithParameters(party1,settings1)
	party1withparams2 =  PartyWithParameters(party1,settings2)
	party2withparams1 =  PartyWithParameters(party2,settings1)

	partyprof1 =  PartyWithProfile(party1withparams1, profile1)
	partyprof1a =  PartyWithProfile(party1withparams1, profile1)
	partyprof2 =  PartyWithProfile(party2withparams1, profile1)
	partyprof3 =  PartyWithProfile(party1withparams1, profile2)
	partyprof4 =  PartyWithProfile(party1withparams2, profile1)


	def getGeneralTestData(self) -> List[List[PartyWithProfile]] :
		return [[self.partyprof1, self.partyprof1a], [self.partyprof2],[self.partyprof3],
				[self.partyprof4]]

	def getGeneralTestStrings(self) -> List[str] :
		return [
				"PartyWithProfile.PartyRef.ws:party1.,ProfileRef.ws:profile1.*",
				"PartyWithProfile.PartyRef.ws:party2.,ProfileRef.ws:profile1.*",
				"PartyWithProfile.PartyRef.ws:party1.,ProfileRef.ws:profile2.*",
				"PartyWithProfile.PartyRef.ws:party1.{a=1},ProfileRef.ws:profile1.*"]

	def testSmoke(self) :
		pass

	def testNull(self) :
		self.assertRaises(ValueError, lambda:PartyWithProfile(None, None))

	def testSerialize(self) :
		jackson = ObjectMapper()

		jsonobj = jackson.toJson(self.partyprof1);
		print(str(jsonobj))
		self.assertEqual(json.loads(self.serialized), jsonobj);

	def testDeserialize(self):
		jackson = ObjectMapper()
		p = jackson.parse(json.loads(self.serialized),	PartyWithProfile)
		print(str(p))
		self.assertEqual(self.partyprof1, p)
