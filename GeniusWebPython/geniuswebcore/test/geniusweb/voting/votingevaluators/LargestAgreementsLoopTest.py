import json
from typing import List
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.actions.Votes import Votes
from geniusweb.issuevalue.Bid import Bid
from geniusweb.voting.CollectedVotes import CollectedVotes
from geniusweb.voting.VotingEvaluator import VotingEvaluator
from geniusweb.voting.votingevaluators.LargestAgreementsLoop import LargestAgreementsLoop


class LargestAgreementsLoopTest(unittest.TestCase, GeneralTests[LargestAgreementsLoop]):
	jackson = ObjectMapper()

	a = Mock(Bid)
	b = Mock(Bid)
	c = Mock(Bid)
	d = Mock(Bid)


	lal1 = LargestAgreementsLoop()
	lal1a = LargestAgreementsLoop()
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")
	party4 = PartyId("party4")
	votes1 = Mock(Votes)
	lal2 = LargestAgreementsLoop().create(
			CollectedVotes({party1:votes1}, {party1: 1}))

	lalstring = "{\"LargestAgreementsLoop\":{}}"

	def getGeneralTestData(self)-> List[List[LargestAgreementsLoop]] :
		return [[self.lal1, self.lal1a], [self.lal2]] 

	def getGeneralTestStrings(self)-> List[str]:
		return ["LargestAgreementsLoop", "LargestAgreementsLoop"]

	def testserializeAcceptTest(self):
		# we use lal2 to also check we don't serialize the contents
		print(self.jackson.toJson(self.lal2))
		self.assertEqual(json.loads(self.lalstring), self.jackson.toJson(self.lal2))

	def testdeserializeAcceptTest(self):
		eval = self.jackson.parse(json.loads(self.lalstring),VotingEvaluator)
		# it should deserialize as the empty lal1 because we ignore the fields.
		self.assertEquals(self.lal1, eval)

	def testCollectVotes(self):
		vote1AB = Votes(self.party1, set([Vote(self.party1, self.a, 2, 9), 
								Vote(self.party1, self.b, 2, 9)]))
		vote2AB = Votes(self.party2, set([Vote(self.party2, self.a, 2, 9),
								Vote(self.party2,self.b, 2, 9)]))
		vote3C = Votes(self.party3,
				set([Vote(self.party3, self.c, 2, 9)]))
		vote4AC = Votes(self.party4, set([Vote(self.party4, self.a, 2, 9),
								Vote(self.party4, self.c, 2, 9)]))
		# party 1,2,4 vote for A, party 1,2 vote for B, party 3,4 vote for C.
		# the biggest vote is P,Q,S
		votes = {}
		votes[self.party1]= vote1AB
		votes[self.party2]= vote2AB
		votes[self.party3]= vote3C
		votes[self.party4]= vote4AC

		actions1 = [[vote1AB, vote2AB, vote3C, vote4AC]];
		power = {}
		power[self.party1]=1
		power[self.party2]=1
		power[self.party3]= 1
		power[self.party4]= 1
		agrees = LargestAgreementsLoop().create(
				CollectedVotes(votes, power)).getAgreements()
		print(agrees)

		# biggest agreement is party 1,2,4 for bid a.
		self.assertEqual(set([self.party1, self.party2, self.party4]),
				agrees.getMap().keys())
