import json
from typing import List
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from tudelft_utilities_logging.ReportToLogger import ReportToLogger
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.deadline.Deadline import Deadline
from geniusweb.deadline.DeadlineRounds import DeadlineRounds
from geniusweb.deadline.DeadlineTime import DeadlineTime
from geniusweb.protocol.session.SessionSettings import SessionSettings
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.mopac.MOPACSettings import MOPACSettings
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef
from geniusweb.voting.votingevaluators.LargestAgreement import LargestAgreement


def mockParty(partyname:str, params: Parameters) -> TeamInfo :
	team = Mock(TeamInfo)
	team.getSize = Mock(return_value=1)
	pwithp = Mock(PartyWithParameters)
	team.getParties = Mock(
		return_value=[PartyWithProfile(pwithp, Mock(ProfileRef))])
	team.__repr__=Mock(return_value=partyname) #type:ignore
	pwithp.__repr__=Mock(return_value=partyname) #type:ignore
	pwithp.getParameters = Mock(return_value=params)
	return team;
	
	
class MOPACSettingsTest (unittest.TestCase, GeneralTests[MOPACSettings]):

	jackson = ObjectMapper()
	noparams = Parameters()
	partyprof1 = mockParty("party1", noparams)
	partyprof2 = mockParty("party2", noparams)
	partyprof3 = mockParty("party3", noparams)
	participants2 = [partyprof1,partyprof2]
	participants3 = [partyprof1, partyprof2,partyprof3]

	ve = LargestAgreement()


	serialized = "{\"MOPACSettings\":{\"participants\":[{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party1\",\"parameters\":{}},\"profile\":\"http://profile1\"}]}},{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party2\",\"parameters\":{}},\"profile\":\"http://profile2\"}]}}],\"deadline\":{\"DeadlineTime\":{\"durationms\":100}},\"votingevaluator\":{\"LargestAgreement\":{}}}}";
	

	def setUp(self):
		self.deadline = Mock(DeadlineTime)
		self.deadline2 = Mock(Deadline)
		self.settings1 = MOPACSettings(self.participants2, self.deadline,self.ve)
		self.settings1a = MOPACSettings(self.participants2, self.deadline, self.ve)
		self.settings2 = MOPACSettings(self.participants3, self.deadline, self.ve)
		self.settings3 = MOPACSettings(self.participants2,self.deadline2,self.ve)
	
		
		self.deadline.getDuration = Mock(return_value=1000)
		self.deadline.__repr__=Mock(return_value="deadline")
		self.deadline2.__repr__=Mock(return_value="deadline2")

		# SERIALIZABLE version with REAL objects. Still no workaround for
		# this...
		self.party1 = PartyWithParameters(
				PartyRef(URI("http://party1")), Parameters())
		self.profile1 = ProfileRef(URI("http://profile1"))
		self.party2 = PartyWithParameters(
				PartyRef(URI("http://party2")), Parameters())
		self.profile2 = ProfileRef(URI("http://profile2"))
		self.partywithprof1 = PartyWithProfile(self.party1, self.profile1);
		self.partywithprof2 = PartyWithProfile(self.party2, self.profile2)
		participants = [
				TeamInfo([self.partywithprof1]),TeamInfo([self.partywithprof2])]

		deadlinetime = DeadlineTime(100)
		self.sersettings = MOPACSettings(participants, deadlinetime, self.ve)

	def getGeneralTestData(self)-> List[List[MOPACSettings]] :
		return [[self.settings1, self.settings1a],
				[self.settings2], [self.settings3]]

	def getGeneralTestStrings(self)-> List[str]:
		return [
				"MOPACSettings.*party1.*party2.*deadline.*LargestAgreement.*",
				"MOPACSettings.*party1.*party2.*deadline.*LargestAgreement.*",
				"MOPACSettings.*party1.*party2.*deadline2.*LargestAgreement.*"]

	def testgetProtocolTest(self):
		self.assertEqual("MOPAC", 
			str(self.settings1.getProtocol(
				ReportToLogger("test")).getRef().getURI()))

	def testconstructorNoDeadlineTest(self):
		self.assertRaises(ValueError, 
			lambda:MOPACSettings(self.participants2, None, self.ve))

	def testMaxRuntime(self):
		self.deadline.getDuration=Mock(return_value=234)
		self.assertEqual(0.234, self.settings1.getMaxRunTime())

	def testMaxRuntimeRounds(self):
		deadline = Mock(DeadlineRounds)
		deadline.getDuration=Mock(return_value=12000)

		settings = MOPACSettings(self.participants2, deadline, self.ve)

		self.assertEqual(12, settings.getMaxRunTime())

	def testDeserialize(self):
		obj = self.jackson.parse(json.loads(self.serialized),
				SessionSettings)
		print(obj)
		self.assertEqual(self.sersettings, obj);

	def testSerialize(self):
		string = self.jackson.toJson(self.sersettings)
		print(string)
		self.assertEqual(json.loads(self.serialized), string)

	def testWith(self):
		saop = MOPACSettings(self.participants2, self.deadline, self.ve)
		saop2 = saop.With(self.partyprof3)
		self.assertEqual(3, len(saop2.getTeams()))

	def testGetAllParties(self):
		self.assertEqual([self.partywithprof1, self.partywithprof2],
				self.sersettings.getAllParties())
