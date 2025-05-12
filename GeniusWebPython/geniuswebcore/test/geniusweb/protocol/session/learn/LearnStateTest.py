import unittest
from unittest.mock import Mock

from uri.uri import URI

from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.LearningDone import LearningDone
from geniusweb.actions.PartyId import PartyId
from geniusweb.deadline.DeadlineTime import DeadlineTime
from geniusweb.inform.Agreements import Agreements
from geniusweb.progress.Progress import Progress
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.learn.LearnSettings import LearnSettings
from geniusweb.protocol.session.learn.LearnState import LearnState
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class LearnStateTest(unittest.TestCase):

	PARTY2 = "party2"
	PARTY1 = "party1"
	party1id = PartyId(PARTY1)
	party2id = PartyId(PARTY2)
	deadline = DeadlineTime(10000)
	partyprofile1 = Mock(PartyWithProfile)
	partyprofile2 = Mock(PartyWithProfile)
	progressnotdone = Mock(Progress)
	progressdone = Mock(Progress);

	def setUp(self):
		self.params = Parameters()
		self.params = self.params.With("persistentstate",
				"6bb5f909-0079-43ac-a8ac-a31794391074")
		self.params = self.params.With("negotiationdata",
				["12b5f909-0079-43ac-a8ac-a31794391012"])
		
		self.progressnotdone.isPastDeadline = Mock(return_value=False)
		self.progressdone.isPastDeadline = Mock(return_value=True)

		# define team1
		party1ref = PartyRef(URI(self.PARTY1))
		party1 = PartyWithParameters(party1ref, self.params)
		profile1 = ProfileRef(URI("http://prof1"))
		partywithp1 = PartyWithProfile(party1, profile1)
		team1pp = [partywithp1]
		self.team1 = TeamInfo(team1pp)

		# define team2
		party2ref = PartyRef(URI(self.PARTY2))
		party2 = PartyWithParameters(party2ref, self.params)
		profile2 = ProfileRef(URI("http://prof2"))
		partywithp2 = PartyWithProfile(party2, profile2)
		team2pp = [partywithp2]
		self.team2 = TeamInfo(team2pp)

		participants = [self.team1, self.team2]
		settings = LearnSettings(participants, self.deadline)
		self.state = LearnState([], [], None, settings)

		self.connectedstate = self.state.WithParty(self.party1id, self.partyprofile1)\
				.WithParty(self.party2id, self.partyprofile2).WithProgress(self.progressnotdone)

	def testsmokeTestNull(self):
		self.assertRaises(ValueError, lambda:LearnState([], [], None, None))

	def testsmokeTest(self):
		settings = Mock(LearnSettings)
		LearnState([], [], None, settings)

	def testgetAgreementsTest(self):
		self.assertEqual(Agreements(), self.state.getAgreements())

	def testisFinalTest(self):
		# initial state is false, because we check
		# that there are no learningDone reports
		self.assertFalse(self.state.isFinal(0))
		# not final because there are connected parties not yet done.
		self.assertFalse(self.connectedstate.isFinal(0))
		finalstate = self.connectedstate.WithProgress(self.progressdone)
		self.assertTrue(finalstate.isFinal(0))

		errorstate = self.connectedstate\
				.WithException(ProtocolException("test", self.party1id))
		self.assertTrue(errorstate.isFinal(0))

	def testcheckActionTest(self):
		# check basic illegal actions in Learning
		self.assertNotEqual(None, self.connectedstate.checkAction(self.party1id, None))
		self.assertNotEqual(None, self.connectedstate.checkAction(PartyId("unknown"), None))
		self.assertNotEqual(None, self.connectedstate.checkAction(self.party1id,
				EndNegotiation(self.party1id)))
		self.assertNotEqual(None, self.connectedstate.checkAction(self.party1id,
				LearningDone(self.party2id)))

		# check a good action is allowed
		self.assertEqual(None, self.connectedstate.checkAction(self.party1id,
				LearningDone(self.party1id)))

		# no learning twice not ok
		learned = self.connectedstate.WithAction(self.party1id,
				LearningDone(self.party1id))
		self.assertNotEqual(None,
				learned.checkAction(self.party1id, LearningDone(self.party1id)))

	def testLearnDoneActionTest(self):
		learned = self.connectedstate.WithAction(self.party1id,
				LearningDone(self.party1id))

	def testisFinalWhenAllLearned(self):
		learned = self.connectedstate\
			.WithAction(self.party1id, LearningDone(self.party1id))\
			.WithAction(self.party2id, LearningDone(self.party2id))
		self.assertTrue(learned.isFinal(0))

	def testgetResultTest(self):
		res = self.connectedstate.getResults()[0]
		self.assertEqual(0, len(res.getAgreements().getMap()))
