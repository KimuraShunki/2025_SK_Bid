import json
from typing import List, Dict
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.Accept import Accept
from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Votes import Votes
from geniusweb.inform.YourTurn import YourTurn
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.session.mopac.PartyStates import PartyStates
from geniusweb.protocol.session.mopac.phase.OfferPhase import OfferPhase
from geniusweb.protocol.session.mopac.phase.Phase import Phase, PHASE_MINTIME
from geniusweb.protocol.session.mopac.phase.VotingPhase import VotingPhase
from geniusweb.voting.votingevaluators.LargestAgreement import LargestAgreement
from geniusweb.voting.votingevaluators.LargestAgreementsLoop import LargestAgreementsLoop


class OfferPhaseTest(unittest.TestCase, GeneralTests[OfferPhase]):
	'''
	We also test defaultPhase here.
	'''
	maxDiff=None
	
	jackson = ObjectMapper()

	DEADLINE = 10
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")

	powers:Dict[PartyId, int] = {}
	evaluator = LargestAgreement()
	evaluator2 = LargestAgreementsLoop()
	
	# just a test bid
	bid = Bid({"issue": DiscreteValue("yes")})
	offer = Offer(party1, bid)

	serialized = "{\"OfferPhase\":{\"partyStates\":{\"powers\":{\"party2\":3,\"party1\":2,\"party3\":3},\"notYetActed\":[\"party2\",\"party1\",\"party3\"],\"actions\":[],\"agreements\":{},\"walkedAway\":[],\"exceptions\":{}},\"deadline\":10,\"evaluator\":{\"LargestAgreement\":{}}}}"

	powers[party1]= 2
	powers[party2]= 3
	states2 = PartyStates(powers)
	powers[party3]= 3
	states = PartyStates(powers);
	phase = OfferPhase(states, DEADLINE, evaluator)

	phase1 = OfferPhase(states, 10, evaluator)
	phase1a =OfferPhase(states, 10, evaluator)
	phase2 = OfferPhase(states2, 10, evaluator)
	phase3 = OfferPhase(states, 20, evaluator)
	phase4 = OfferPhase(states, 10, evaluator2)

	def getGeneralTestData(self)->List[List[OfferPhase]] :
		return [[self.phase1, self.phase1a],
				[self.phase2], [self.phase3],
				[self.phase4]]

	def getGeneralTestStrings(self)->List[str] :
		return [
				"OfferPhase.*PartyStates.*party., party., party..*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreement.*",
				"OfferPhase.*PartyStates.*party., party..*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreement.*",
				"OfferPhase.*PartyStates.*party., party., party.*\\[\\],Agreements.*\\[\\],\\{\\}.*],20,LargestAgreement.*",
				"OfferPhase.*PartyStates.*party., party., party..*\\[\\],Agreements.*\\[\\],\\{\\}.*],10,LargestAgreementsLoop.*"]

	def testsmokeTest(self) :
		pass
	
	def testInitState(self):
		self.assertEqual(3, len(self.phase.getPartyStates().getNotYetActed()))

	def testInform(self):
		self.assertEqual(YourTurn(), self.phase.getInform())

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

	def testcheckIncorrectActorTest(self):
		self.assertRaises(ProtocolException, lambda:
			self.phase._checkAction(self.party1, EndNegotiation(self.party2), 1))

	def testcheckNotAllowedActionTest(self):
		self.assertRaises(ProtocolException, lambda:
			self.phase._checkAction(self.party1, Votes(self.party2,set()), 1))

	def testException(self):
		newphase = self.phase.WithException(ProtocolException("bla", self.party1))
		self.assertEqual(10, newphase.getDeadline())
		self.assertEqual(0, len(self.phase.getPartyStates().getActions()))

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
		self.assertTrue(isinstance(next, VotingPhase))
		# no remaining parties, since finish kicked all
		self.assertEqual(0, len(next.getPartyStates().getNotYetActed()))

	def testAllowed(self):
		self.phase.With(self.party1, self.offer, 1)

	def testAllowedWrongClass(self):
		try:
			self.phase._checkAction(self.party1, Accept(self.party1, self.bid), 1)
		except ProtocolException as e:
			self.assertTrue("not allowed in OfferPhase" in e.args[0])
			return
		self.fail("checkAction did not throw as expected")

	def testAllowedWrongActor(self):
		try:
			self.phase._checkAction(self.party1, Accept(self.party2, self.bid), 1)
		except ProtocolException as e:
			self.assertTrue("Incorrect actor info in action" in e.args[0])
			return
		self.fail("checkAction did not throw as expected")

	def testAllowedActorAlreadyActed(self):
		testphase = self.phase.With(self.party1, self.offer, 1)
		try:
			testphase._checkAction(self.party1, self.offer, 2)
		except ProtocolException  as e:
			self.assertTrue("can not act anymore" in e.args[0])
			return
		self.fail("checkAction did not throw as expected")

	def testAllowedActorAlreadyActed1(self):
		# as theoprevious test, but using with() instead of checkAction
		testphase = self.phase.With(self.party1, self.offer, 1)

		newphase = testphase.With(self.party1, self.offer, 2)
		# the party must remain as acted, because we can't retract his
		# action...
		self.assertEqual(1, len(newphase.getPartyStates().getActions()))
		self.assertEqual(self.offer, newphase.getPartyStates().getActions()[0])
		self.assertFalse(self.party1 in 
				newphase.getPartyStates().getExceptions())

	def testAllowedActingTooLate(self):
		try:
			self.phase._checkAction(self.party1, self.offer, self.DEADLINE + 1)
		except ProtocolException as e:
			self.assertTrue("passed deadline" in e.args[0])
			return
		self.fail("checkAction did not throw as expected")

	def testgetOffersTest(self) :
		self.assertEquals([], self.phase._getOffers())
		offs = self.phase.With(self.party1, self.offer, 1)._getOffers()
		self.assertEqual(1, len(offs))
		self.assertEquals(self.bid, offs[0].getBid())

	def testNextTooShortDuration(self):
		self.assertRaises(ValueError, lambda:self.phase.next(1, PHASE_MINTIME - 1))

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
