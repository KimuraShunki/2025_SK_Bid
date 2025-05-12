import json
from typing import List
from unittest import mock
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from tudelft_utilities_logging.ReportToLogger import ReportToLogger
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.deadline.Deadline import Deadline
from geniusweb.deadline.DeadlineRounds import DeadlineRounds
from geniusweb.deadline.DeadlineTime import DeadlineTime
from geniusweb.protocol.NegoSettings import NegoSettings
from geniusweb.protocol.session.SessionSettings import SessionSettings
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.saop.SAOPSettings import SAOPSettings
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class SAOPSettingsTest (unittest.TestCase, GeneralTests[SAOPSettings]):

	partyprof1 = Mock(TeamInfo)
	partyprof2 = Mock(TeamInfo)
	partyprof3 = Mock(TeamInfo)
	participants2:List[TeamInfo] = [partyprof1,partyprof2]
	participants3:List[TeamInfo] = [partyprof1, partyprof2, partyprof3]

	deadline = Mock(DeadlineTime)
	deadline2 = Mock(Deadline)
	settings1 = SAOPSettings(participants2, deadline)
	settings1a = SAOPSettings(participants2, deadline)
	settings2 = SAOPSettings(participants3, deadline)
	settings3 = SAOPSettings(participants2, deadline2)
	jackson = ObjectMapper()

	serialized = "{\"SAOPSettings\":{\"participants\":[{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party1\",\"parameters\":{}},\"profile\":\"http://profile1\"}]}},{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party2\",\"parameters\":{}},\"profile\":\"http://profile2\"}]}}],\"deadline\":{\"DeadlineTime\":{\"durationms\":100}}}}";

	deadline.getDuration=Mock(return_value=1000)
	#work around mypy bug
	deadline.__repr__=Mock(return_value="deadline") #type:ignore
	deadline2.__repr__=Mock(return_value="deadline2") #type:ignore

	partyprof1.getSize=Mock(return_value=1)
	partyprof2.getSize=Mock(return_value=1)
	partyprof3.getSize=Mock(return_value=1)

	partyprof1.__repr__=Mock(return_value="party and profile 1") #type:ignore
	partyprof2.__repr__=Mock(return_value="party and profile 2") #type:ignore
	partyprof3.__repr__=Mock(return_value="party and profile 3") #type:ignore

	# SERIALIZABLE version with REAL objects. Still no workaround for
	# this...
	party1 = PartyWithParameters(PartyRef(URI("http://party1")), Parameters())
	profile1 = ProfileRef(URI("http://profile1"))
	party2 = PartyWithParameters(PartyRef(URI("http://party2")), Parameters())
	profile2 = ProfileRef(URI("http://profile2"))
	partywithprof1 = TeamInfo([PartyWithProfile(party1, profile1)])
	partywithprof2 = TeamInfo([PartyWithProfile(party2, profile2)])
	participants = [partywithprof1,	partywithprof2]

	deadlinetime = DeadlineTime(100)
	sersettings = SAOPSettings(participants, deadlinetime)


	def getGeneralTestData(self) -> List[List[SAOPSettings]] :
		return [[self.settings1, self.settings1a],
			[self.settings2], [self.settings3]]

	def getGeneralTestStrings(self)-> List[str]:
		return [
				"SAOPSettings.party and profile 1, party and profile 2.,deadline.",
				"SAOPSettings.party and profile 1, party and profile 2, party and profile 3.,deadline.",
				"SAOPSettings.party and profile 1, party and profile 2.,deadline2."]

	def testGetProtocol(self):
		self.assertEqual("SAOP", str(self.settings1.getProtocol(ReportToLogger("test"))
				.getRef().getURI()))

	def testConstructorNoDeadline(self):
		self.assertRaises(ValueError, lambda:SAOPSettings(self.participants2, None))

	def testMaxRuntime(self):
		self.deadline.getDuration=Mock(return_value=234000) 
		self.assertEqual(234, self.settings1.getMaxRunTime())

	def testMaxRuntimeRounds(self):
		deadline = Mock(DeadlineRounds)
		deadline.getDuration=Mock(return_value=12000)

		settings = SAOPSettings(self.participants2, deadline)

		self.assertEqual(12, settings.getMaxRunTime())
	
	def testDeserialize(self) :
		obj = self.jackson.parse(json.loads(self.serialized),SessionSettings);
		print(obj)
		self.assertEqual(self.sersettings, obj)

	def testDeserializeAsNego(self) :
		obj = self.jackson.parse(json.loads(self.serialized),NegoSettings);
		print(obj)
		self.assertEqual(self.sersettings, obj)


	def testSerialize(self):
		jsonobj = self.jackson.toJson(self.sersettings)
		print(jsonobj)
		self.assertEqual(json.loads(self.serialized), jsonobj)

	def testWith(self):
		saop = SAOPSettings(self.participants2, self.deadline)
		saop2 = saop.With(self.partyprof3);
		self.assertEqual(3, len(saop2.getTeams()))
