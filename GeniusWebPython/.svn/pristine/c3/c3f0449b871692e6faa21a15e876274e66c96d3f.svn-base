from time import sleep, time
from typing import cast
import unittest
from unittest.mock import Mock

from tudelft_utilities_logging.Reporter import Reporter
from uri.uri import URI

from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.LearningDone import LearningDone
from geniusweb.actions.PartyId import PartyId
from geniusweb.deadline.DeadlineTime import DeadlineTime
from geniusweb.inform.Finished import Finished
from geniusweb.protocol.partyconnection.ProtocolToPartyConn import ProtocolToPartyConn
from geniusweb.protocol.partyconnection.ProtocolToPartyConnFactory import ProtocolToPartyConnFactory
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.learn.Learn import Learn
from geniusweb.protocol.session.learn.LearnSettings import LearnSettings
from geniusweb.protocol.session.learn.LearnState import LearnState
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class LearnTest(unittest.TestCase):

	reporter = Mock(Reporter)
	params = Parameters()
	deadline = DeadlineTime(1800)
	party1id = PartyId("party1")
	party2id = PartyId("party2")

	def setUp(self):
		self.conn1 = Mock(ProtocolToPartyConn)
		self.conn2 = Mock(ProtocolToPartyConn)
		self.params = self.params.With("persistentstate",
				"6bb5f909-0079-43ac-a8ac-a31794391074")
		self.params = self.params.With("negotiationdata",
				["12b5f909-0079-43ac-a8ac-a31794391012"])

	def testsmokeTest(self):
		Learn(Mock(LearnState), Mock(Reporter))

	def testgetDescrTest(self):
		l = Learn(Mock(LearnState), Mock(Reporter))

		self.assertNotEqual(None, l.getDescription())

	def testgetStateTest(self) :
		state = Mock(LearnState)
		l = Learn(state, Mock(Reporter))
		self.assertEqual(state, l.getState())

	def testgetRefTest(self):
		l = Learn(Mock(LearnState), Mock(Reporter))
		self.assertEqual("Learn", str(l.getRef().getURI().getPath()))

	def testfinalStateNotificationTest(self):
		# check that listeners get notified when session ends.
		pass

	def testStartStopBasic(self) :
		learn = self.createBasicLearn()
		factory = self.createFactory()
		learn.start(factory)
		#extra, check if start worked ok
		self.assertEqual(None, learn.getState().getError())
		self.assertFalse(learn.getState().isFinal(time()*1000))
		sleep(2.000)
		self.assertTrue(learn.getState().isFinal(time()*1000))

	def testStartStopLearn(self):
		learn = self.createBasicLearn();
		factory = self.createFactory()
		learn.start(factory)
		self.assertFalse(learn.getState().isFinal(time()*1000))

		# Instead of mocking connectin we call actionRequest directly
		learn._actionRequest(self.conn1, LearningDone(self.party1id))
		self.assertFalse(learn.getState().isFinal(time()*1000))
		learn._actionRequest(self.conn2, LearningDone(self.party2id))
		self.assertTrue(learn.getState().isFinal(time()*1000))

	def testAddParty(self):
		l = Learn(Mock(LearnState), Mock(Reporter))
		self.assertRaises(ValueError, lambda:l.addParticipant(Mock(PartyWithProfile)))
	

	def testisFinishSentNormally(self):
		learn = self.createBasicLearn()
		factory = self.createFactory()
		learn.start(factory)
		learn._actionRequest(self.conn1,  LearningDone(self.party1id))
		learn._actionRequest(self.conn2, LearningDone(self.party2id))
		
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list \
			if isinstance(call[0][0],Finished)]))
		self.assertEqual(1, len([call for call in self.conn2.send.call_args_list \
			if isinstance(call[0][0],Finished)]))

	def testisFinishSentInError(self):
		learn = self.createBasicLearn()
		factory = self.createFactory()
		learn.start(factory)
		learn._actionRequest(self.conn1, EndNegotiation(self.party1id))
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list \
			if isinstance(call[0][0],Finished)]))
		self.assertEqual(1, len([call for call in self.conn2.send.call_args_list \
			if isinstance(call[0][0],Finished)]))

	def createBasicLearn(self)->Learn:
		team1 = self.createTeam(1)
		team2 = self.createTeam(2)
		settings = LearnSettings([team1, team2],self.deadline)
		return cast(Learn, settings.getProtocol(self.reporter))

	def createTeam( self, nr:int) -> TeamInfo :
		party1ref = PartyRef(URI("party" + str(nr)))
		party1 = PartyWithParameters(party1ref, self.params)
		profile1 = ProfileRef(URI("prof" + str(nr)))
		partywithp1 = PartyWithProfile(party1, profile1)
		team1pp = [partywithp1]
		team = TeamInfo(team1pp)
		return team

	def createFactory(self )->ProtocolToPartyConnFactory :
		self.conn1.getParty=Mock(return_value=self.party1id)
		self.conn2.getParty=Mock(return_value=self.party2id)

		factory = Mock(	ProtocolToPartyConnFactory)
		# connections = mock(List.class);
		connections = [self.conn1, self.conn2]
		factory.connectAll=Mock(return_value=connections)
		return factory;

