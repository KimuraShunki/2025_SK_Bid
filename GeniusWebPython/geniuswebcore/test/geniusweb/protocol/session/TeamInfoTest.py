import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class TeamInfoTest (unittest.TestCase, GeneralTests[TeamInfo]):

	team1 = TeamInfo([])
	team1a = TeamInfo([])
	parameters = Parameters()
	asString1 = "{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"party1\",\"parameters\":{}},\"profile\":\"profile1\"}]}}";

	partyref = PartyRef(URI("party1"))
	profileref =  ProfileRef(URI("profile1"))
	team2 = TeamInfo( [PartyWithProfile(PartyWithParameters(partyref, parameters),profileref)])
	team2a =  TeamInfo( [ PartyWithProfile(PartyWithParameters(partyref, parameters),
			profileref)]);

	def getGeneralTestData(self)->List[List[TeamInfo]] :
		return [[self.team1, self.team1a],	[self.team2, self.team2a]]

	def getGeneralTestStrings(self) -> List[str]:
		return ["TeamInfo.\\[\\].",
				"TeamInfo.\\[PartyWithProfile.*party1.*profile1.*\\].*"]

	def testSerialize(self) :

		jackson = ObjectMapper()
		print(jackson.toJson(self.team2))
		self.assertEqual(json.loads(self.asString1), jackson.toJson(self.team2))

	def testDeserialize(self) :
		jackson = ObjectMapper()
		read = jackson.parse(json.loads(self.asString1), TeamInfo)
		self.assertEqual(self.team2, read)
