import json
from typing import List, Dict
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.actions.Votes import Votes
from geniusweb.inform.OptIn import OptIn
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.session.mopac.PartyStates import PartyStates
from geniusweb.protocol.session.mopac.phase.OfferPhase import OfferPhase
from geniusweb.protocol.session.mopac.phase.OptInPhase import OptInPhase
from geniusweb.protocol.session.mopac.phase.Phase import Phase, PHASE_MINTIME
from geniusweb.voting.votingevaluators.LargestAgreement import LargestAgreement
from geniusweb.voting.votingevaluators.LargestAgreementsLoop import LargestAgreementsLoop


class OptInPhaseTest(unittest.TestCase, GeneralTests[OptInPhase]):
	'''
	We also test defaultPhase here.
	'''
	jackson = ObjectMapper()

	DEADLINE = 10
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")


	evaluator = LargestAgreement()
	evaluator2 = LargestAgreementsLoop()

	# just a test bid
	bid = Bid({"issue":  DiscreteValue("yes")})
	vote = Vote(party1, bid, 2, 3)
	votes = Votes(party1, set([vote]))

	prevVotes = [votes]

	serialized = "{\"OptInPhase\":{\"votes\":[],\"partyStates\":{\"powers\":{\"party2\":3,\"party1\":2,\"party3\":3},\"notYetActed\":[\"party2\",\"party1\",\"party3\"],\"actions\":[],\"agreements\":{},\"walkedAway\":[],\"exceptions\":{}},\"deadline\":10,\"evaluator\":{\"LargestAgreement\":{}}}}"
	
	def setUp(self) :
		self.powers:Dict[PartyId, int]  = {}
		self.powers[self.party1]= 2
		self.powers[self.party2]= 3
		self.states2 = PartyStates(self.powers)
		self.powers[self.party3]=3
		self.states =  PartyStates(self.powers)

		self.phase = OptInPhase(self.prevVotes, self.states, self.DEADLINE, self.evaluator)

		# in these phases we just don't set prevPhase.
		# this to avoid serialization troubles.
		self.phase1 =  OptInPhase([], self.states, 10, self.evaluator)
		self.phase1a =  OptInPhase([], self.states, 10, self.evaluator)
		self.phase2 =  OptInPhase([], self.states2, 10, self.evaluator)
		self.phase3 =  OptInPhase([], self.states, 20, self.evaluator)
		self.phase4 =  OptInPhase([], self.states, 10, self.evaluator2)

	def  getGeneralTestData(self)->List[List[OptInPhase]]:
		return [[self.phase1, self.phase1a],
				[self.phase2], [self.phase3],
				[self.phase4]]


	def  getGeneralTestStrings(self) ->List[str]:
		return [
				"OptInPhase.*PartyStates.*party., party., party..*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreement.*",
				"OptInPhase.*PartyStates.*party., party.*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreement.*",
				"OptInPhase.*PartyStates.*party., party., party..*\\[\\],Agreements.*\\[\\],\\{\\}.*],20,LargestAgreement.*",
				"OptInPhase.*PartyStates.*party., party., party..*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreementsLoop.*"]


	def testsmokeTest(self):
		pass

	def testInitState(self):
		self.assertEqual(3, len(self.phase.getPartyStates().getNotYetActed()))

	def testInform(self) :
		# when(prevPhase.getVotes()).thenReturn(Arrays.asList(votes));
		self.assertEqual(OptIn([self.votes]), self.phase.getInform())

	def testisFinalTest(self):
		self.assertFalse(self.phase.isFinal(1))
		self.assertTrue(self.phase.isFinal(10))

	def testisFinalTestActorNotYetActed(self):
		actedstate = Mock(PartyStates)
		actedstate.getNotYetActed=Mock(return_value=set([self.party1]))
		testphase =  OfferPhase(actedstate, 10, self.evaluator)
		self.assertFalse(testphase.isFinal(1))

	def testisFinalTestAllActorsActed(self):
		actedstate = Mock(PartyStates)
		actedstate.getNotYetActed=Mock(return_value=set([]))
		testphase = OfferPhase(actedstate, 10, self.evaluator)
		self.assertTrue(testphase.isFinal(1))

	def testcheckIncorrectActorTest(self) :
		self.assertRaises(ProtocolException, 
			lambda:self.phase._checkAction(self.party1, EndNegotiation(self.party2), 1))

	def testcheckNotAllowedActionTest(self) :
		self.assertRaises(ProtocolException, lambda:self.phase._checkAction(self.party1, Votes(self.party2, set([])), 1))

	def testFinish(self):
		ph = self.phase.finish()
		self.assertEqual(0,len(ph.getPartyStates().getNotYetActed()))
		self.assertEqual(3, len(ph.getPartyStates().getExceptions()))
		self.assertEqual(0,len(self.phase.getPartyStates().getAgreements().getMap()))
	
	def testNextWrong(self):
		# state is not final, should not work
		self.assertRaises(ValueError, lambda:self.phase.next(1, 1000))

	def testNextNoParties(self) :
		ph = self.phase.finish()
		# no parties are left now, all failed
		# but this is not part of the next() check.
		next = ph.next(1, 1000)
		self.assertTrue(isinstance(next, OfferPhase))
		# no remaining parties, since finish kicked all
		self.assertEqual(0, len(next.getPartyStates().getNotYetActed()))

	def testAllowed(self):
		# when(prevPhase.getVotes()).thenReturn(Arrays.asList(votes));
		self.phase.With(self.party1, self.votes, 1)

	def testAllowedNarrowingVote(self):
		# the previous vote was maxPower=3,
		# so this is an illegal narrowing of the previous vote
		newVote = Vote(self.party1, self.bid, 2, 2)
		newVotes = Votes(self.party1, set([newVote]))

		# when(prevPhase.getVotes()).thenReturn(Arrays.asList(votes));

		# check that party1 was kicked
		newphase = self.phase.With(self.party1, newVotes, 1)
		self.assertTrue(
				self.party1 in newphase.getPartyStates().getExceptions())

	def testNextTooShortDuration(self) :
		self.assertRaises(ValueError, 
			lambda:self.phase.next(1, PHASE_MINTIME - 1))
		

	def testNextNotFinished(self):
		self.assertRaises(ValueError, 
			lambda:self.phase.next(1, PHASE_MINTIME + 1))

	def testNext(self):
		self.assertRaises(ValueError, 
			lambda:self.phase.next(11, PHASE_MINTIME + 1))

	def testDeserialize(self):
		obj = self.jackson.parse(json.loads(self.serialized), Phase)
		print(obj)
		self.assertEqual(self.phase1, obj)

	def testSerialize(self):
		jsonobj = self.jackson.toJson(self.phase1)
		print(jsonobj);
		#FIXME how can we test this. The order of the notYetActed set is randomizing
		#self.assertEqual(json.loads(self.serialized), jsonobj)

