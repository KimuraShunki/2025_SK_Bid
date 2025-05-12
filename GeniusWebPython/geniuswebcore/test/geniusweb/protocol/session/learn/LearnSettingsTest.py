import json
from typing import List
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from tudelft_utilities_logging.Reporter import Reporter
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.deadline.DeadlineRounds import DeadlineRounds
from geniusweb.protocol.session.SessionSettings import SessionSettings
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.learn.LearnSettings import LearnSettings
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class LearnSettingsTest (unittest.TestCase, GeneralTests[LearnSettings]):
	jackson = ObjectMapper()
	
	serialized = "{\"LearnSettings\":{\"participants\":[{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"party1\",\"parameters\":{\"persistentstate\":\"6bb5f909-0079-43ac-a8ac-a31794391074\",\"negotiationdata\":[\"12b5f909-0079-43ac-a8ac-a31794391012\"]}},\"profile\":\"http://prof1\"}]}}],\"deadline\":{\"DeadlineRounds\":{\"rounds\":10,\"durationms\":10000}}}}"

	def setUp(self):
		self.params = Parameters()
		self.params = self.params.With("persistentstate",
				"6bb5f909-0079-43ac-a8ac-a31794391074")
		self.params = self.params.With("negotiationdata",
				["12b5f909-0079-43ac-a8ac-a31794391012"])

		# define participants
		self.participants = self.createTeam(self.params, 1)

		# participants2
# 		ProfileRef profile2 = new ProfileRef("http://prof2");
# 		PartyWithProfile partywithp2 = new PartyWithProfile(party1, profile2);
# 		List<PartyWithProfile> team2pp = Arrays.asList(partywithp2);
# 		TeamInfo team2 = new TeamInfo(team2pp);
		self.participants2 = self.createTeam(self.params, 2)

		self.deadline = DeadlineRounds(10, 10000)
		self.deadline2 = DeadlineRounds(20, 10000)

		self.settings1 =  LearnSettings(self.participants, self.deadline)
		self.settings1a =  LearnSettings(self.participants, self.deadline)
		self.settings2 =  LearnSettings(self.participants2, self.deadline)
		self.settings3 =  LearnSettings(self.participants, self.deadline2)


	def createTeam(self, params:Parameters,  partynr:int) -> List[TeamInfo] :
		'''
		@param params  the parameters for the party
		@param partynr the serialnr for the party, eg 1 or 2.
		@return a List of TeamInfo with just 1 team.
		'''
		party1ref = PartyRef(URI("party" + str(partynr)))
		party1 = PartyWithParameters(party1ref, params)
		profile1 = ProfileRef(URI("http://prof" + str(partynr)))
		partywithp1 = PartyWithProfile(party1, profile1)
		team1pp = [partywithp1]
		team1 = TeamInfo(team1pp)
		return [team1]

	def getGeneralTestData(self) ->List[List[LearnSettings]]:
		return [[self.settings1, self.settings1a],[self.settings2], [self.settings3]]

	def getGeneralTestStrings(self)->List[str]:
		return [
				"LearnSettings.TeamInfo.*PartyWithProfile.*PartyRef.*party1.*persistentstate=6b.*, negotiationdata=\\[12.*..*ProfileRef.*prof1.*,DeadlineRounds.*10,10000.*",
				"LearnSettings.TeamInfo.*PartyWithProfile.*PartyRef.*party2.*persistentstate=6b.*, negotiationdata=\\[12.*..*ProfileRef.*prof2.*,DeadlineRounds.*10,10000.*",
				"LearnSettings.TeamInfo.*PartyWithProfile.*PartyRef.*party1.*persistentstate=6b.*, negotiationdata=\\[12.*..*ProfileRef.*prof1.*,DeadlineRounds.*20,10000.*"]

	def testNullParticipants(self):
		self.assertRaises(ValueError, lambda:LearnSettings(None, self.deadline))

	def testNullDeadline(self):
		self.assertRaises(ValueError, lambda:LearnSettings(self.participants, None))

	def testgetMaxRuntimeTest(self):
		self.assertEqual(10, self.settings1.getMaxRunTime(), 0.00000001)

	def testgetProtocolTest(self):
		# this will throw if not Learn protocol or another problem.
		protocol = self.settings1.getProtocol(Mock(Reporter))


	def testbadPersistentTest(self):
		# hack. #1933.
		newparams = self.params.With("persistentstate",
				"\"notproperUUID\"")
		participants = self.createTeam(newparams, 1)

		self.assertRaises(ValueError, lambda:LearnSettings(participants, self.deadline))

	def testpersistentNotStringTest(self):
		newparams = self.params.With("persistentstate", 32)
		participants = self.createTeam(newparams, 1)

		self.assertRaises(ValueError, lambda: LearnSettings(participants, self.deadline))

	def testpersistentWithoutQuotesTest(self) :
		newparams = self.params.With("persistentstate",
				"6bb5f909-0079-43ac-a8ac-a31794391074")
		participants = self.createTeam(newparams, 1)

		LearnSettings(participants, self.deadline)

	def testpersistentExtraQuoteTest(self) :
		newparams = self.params.With("persistentstate",
				"\"6bb5f909-0079-43ac-a8ac-a31794391074\"")
		participants = self.createTeam(newparams, 1)

		self.assertRaises(ValueError, lambda:LearnSettings(participants, self.deadline))

	def testnegotiationDataNotList(self):
		newparams = self.params.With("negotiationdata",
				"\"12b5f909-0079-43ac-a8ac-a31794391012\"")
		participants = self.createTeam(newparams, 1)
		self.assertRaises(ValueError, lambda:LearnSettings(participants, self.deadline))

	def testnegotiationDataBadContents(self):
		newparams = self.params.With("negotiationdata", "\"bad\"")
		participants = self.createTeam(newparams, 1)
		self.assertRaises(ValueError, lambda: LearnSettings(participants, self.deadline))

	def testnegotiationDataNotString(self):
		newparams = self.params.With("negotiationdata", 12)
		participants = self.createTeam(newparams, 1)
		self.assertRaises(ValueError, lambda:LearnSettings(participants,self.deadline))

	def testgetTeamsTest(self):
		self.assertEqual(self.participants, self.settings1.getTeams())
		self.assertEqual(1, self.settings1.getTeamSize())

	def testgetDeadlineTest(self):
		self.assertEqual(self.deadline, self.settings1.getDeadline())

	def testwithTeamTest(self):
		newset = self.settings1.With(self.participants2[0])
		self.assertEqual(2, len(newset.getTeams()))

	def testDeserialize(self) :
		obj = self.jackson.parse(json.loads(self.serialized), SessionSettings)
		print(obj)
		self.assertEqual(self.settings1, obj)

	def testSerialize(self):
		jsonobj = self.jackson.toJson(self.settings1);
		print(jsonobj)
		self.assertEqual(json.loads(self.serialized), jsonobj)

