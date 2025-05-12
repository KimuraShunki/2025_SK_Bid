import json
from typing import List
from unittest import mock
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.actions.Votes import Votes
from geniusweb.inform.Voting import Voting
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.session.mopac.PartyStates import PartyStates
from geniusweb.protocol.session.mopac.phase.OfferPhase import OfferPhase
from geniusweb.protocol.session.mopac.phase.OptInPhase import OptInPhase
from geniusweb.protocol.session.mopac.phase.Phase import PHASE_MINTIME, Phase
from geniusweb.protocol.session.mopac.phase.VotingPhase import VotingPhase
from geniusweb.voting.votingevaluators.LargestAgreement import LargestAgreement
from geniusweb.voting.votingevaluators.LargestAgreementsLoop import LargestAgreementsLoop


class VotingPhaseTest (unittest.TestCase, GeneralTests[VotingPhase]):
	jackson = ObjectMapper()
	'''
	We also test defaultPhase here.
	'''
	DEADLINE = 10
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")

	# private final OfferPhase prevPhase = mock(OfferPhase.class);

	evaluator = LargestAgreement()
	evaluator2 = LargestAgreementsLoop()
	
	# just a test bid
	bid = Bid({"issue":  DiscreteValue("yes")})
	vote = Vote(party1, bid, 2, 3);
	votes = Votes(party1, set([vote]))

	prevPhase = [ Offer(party1, bid)]

	serialized = "{\"VotingPhase\":{\"offers\":[],\"partyStates\":{\"powers\":{\"party2\":3,\"party1\":2,\"party3\":3},\"notYetActed\":[\"party2\",\"party1\",\"party3\"],\"actions\":[],\"agreements\":{},\"walkedAway\":[],\"exceptions\":{}},\"deadline\":10,\"evaluator\":{\"LargestAgreement\":{}}}}"
	
	def setUp(self):
		self.powers:Dict[PartyId, int]  = {}
		self.powers[self.party1]=2
		self.powers[self.party2]= 3
		self.states2 = PartyStates(self.powers)
		self.powers[self.party3]= 3
		self.states = PartyStates(self.powers)

		self.phase = VotingPhase(self.prevPhase, self.states, self.DEADLINE, self.evaluator)

		# in these phases we just don't set prevPhase.
		# this to avoid serialization troubles.
		self.phase1 =  VotingPhase([], self.states, 10, self.evaluator);
		self.phase1a =  VotingPhase([], self.states, 10, self.evaluator);
		self.phase2 =  VotingPhase([], self.states2, 10, self.evaluator);
		self.phase3 =  VotingPhase([], self.states, 20, self.evaluator);
		self.phase4 =  VotingPhase([], self.states, 10, self.evaluator2);


	def  getGeneralTestData(self)-> List[List[VotingPhase]]:
		return [[self.phase1, self.phase1a],
				[self.phase2], [self.phase3],
				[self.phase4]]

	def getGeneralTestStrings(self)->List[str] :
		return [
				"VotingPhase.*PartyStates.*party., party., party.*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreement.*",
				"VotingPhase.*PartyStates.*party., party.*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreement.*",
				"VotingPhase.*PartyStates.*party., party., party.*\\[\\],Agreements.*\\[\\],\\{\\}.*],20,LargestAgreement.*",
				"VotingPhase.*PartyStates.*party., party., party.*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreementsLoop.*"]

	def testsmokeTest(self):
		pass

	def testInitState(self):
		self.assertEqual(3, len(self.phase.getPartyStates().getNotYetActed()))

	def testInform(self) :
		# when(prevPhase.getOffers()).thenReturn(Arrays.asList(bid));
		self.assertEqual(Voting([Offer(self.party1, self.bid)], self.powers),
				self.phase.getInform())

	def testisFinalTest(self):
		self.assertFalse(self.phase.isFinal(1))
		self.assertTrue(self.phase.isFinal(10))
	
	def testisFinalTestActorNotYetActed(self):
		actedstate = Mock(PartyStates)
		actedstate.getNotYetActed=Mock(return_value=set([self.party1]))
		testphase = OfferPhase(actedstate, 10, self.evaluator)
		self.assertFalse(testphase.isFinal(1))

	def testisFinalTestAllActorsActed(self):
		actedstate = Mock(PartyStates)
		actedstate.getNotYetActed=Mock(return_value=set())
		testphase = OfferPhase(actedstate, 10, self.evaluator)
		self.assertTrue(testphase.isFinal(1))

	def testcheckIncorrectActorTest(self) :
		self.assertRaises(ProtocolException, 
			lambda:self.phase._checkAction(self.party1, 
								EndNegotiation(self.party2), 1))

	def testcheckNotAllowedActionTest(self) :
		self.assertRaises(ProtocolException, 
			lambda:self.phase._checkAction(self.party1, Votes(self.party2, set()), 1))

	def testFinish(self):
		ph = self.phase.finish()
		self.assertEqual(0, len(ph.getPartyStates().getNotYetActed()))
		self.assertEquals(3, len(ph.getPartyStates().getExceptions()))
		self.assertEqual(0, len(self.phase.getPartyStates().getAgreements().getMap()))

	def testNextWrong(self):
		# state is not final, should not work
		self.assertRaises(ValueError, lambda:self.phase.next(1, 1000))

	def testNextNoParties(self):
		ph = self.phase.finish()
		# no parties are left now, all failed
		# but this is not part of the next() check.
		next = ph.next(1, 1000)
		self.assertTrue(isinstance(next, OptInPhase))
		# no remaining parties, since finish kicked all
		self.assertEqual(0, len(next.getPartyStates().getNotYetActed()))

	def testAllowed(self):
		self.phase.With(self.party1, self.votes, 1)

	def testgetVotesTest(self):
		self.assertEqual([], self.phase.getVotes())
		vts = self.phase.With(self.party1, self.votes, 1).getVotes()
		self.assertEquals([self.votes], vts)

	def testNextTooShortDuration(self):
		self.assertRaises(ValueError, 
			lambda:self.phase.next(1, PHASE_MINTIME - 1))

	def testNextNotFinished(self):
		self.assertRaises(ValueError, lambda:self.phase.next(1, PHASE_MINTIME + 1))

	def testNext(self):
		self.assertRaises(ValueError, lambda:self.phase.next(11, PHASE_MINTIME + 1))


	def testDeserialize(self):
		obj = self.jackson.parse(json.loads(self.serialized), Phase)
		print(obj)
		self.assertEqual(self.phase1, obj)

	def testSerialize(self):
		jsonobj = self.jackson.toJson(self.phase1)
		print(jsonobj);
		#FIXME how can we test this. The order of the notYetActed set is randomizing
		#self.assertEqual(json.loads(self.serialized), jsonobj)
