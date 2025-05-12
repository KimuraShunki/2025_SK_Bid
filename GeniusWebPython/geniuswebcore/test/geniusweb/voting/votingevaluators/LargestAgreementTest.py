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
from geniusweb.voting.votingevaluators.LargestAgreement import LargestAgreement


class LargestAgreementTest (unittest.TestCase, GeneralTests[LargestAgreement]):
	jackson = ObjectMapper()

	lal1 = LargestAgreement()
	lal1a = LargestAgreement()
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")
	party4 = PartyId("party4")
	votes1 = Mock(Votes)
	lal2 = LargestAgreement()
	# hack for testing only. 
	lal2._allVotes = (CollectedVotes({party1: votes1}, {party1: 1}))

	lalstring = "{\"LargestAgreement\":{}}"

	def getGeneralTestData(self)-> List[List[LargestAgreement]] :
		return [[self.lal1, self.lal1a], [self.lal2]]

	def getGeneralTestStrings(self) ->List[str] :
		return ["LargestAgreement", "LargestAgreement"]

	def testserializeTest(self) :
		# we use lal2 to also check we don't serialize the contents
		print(self.jackson.toJson(self.lal2))
		self.assertEqual(json.loads(self.lalstring), self.jackson.toJson(self.lal2))

	def testdeserializeTest(self):
		eval = self.jackson.parse(json.loads(self.lalstring),
				VotingEvaluator)
		# it should deserialize as the empty lal1 because we ignore the fields.
		self.assertEqual(self.lal1, eval)

	def testCollectVotes(self):
		# we set up a tricky situation where party4 has much more power
		# and therefore party 1+4 >> p1+2+3
		bid1 = Mock(Bid)
		bid2 = Mock(Bid)

		votes = CollectedVotes({},	{})
		votes = votes.With(Votes(self.party1,
				set([Vote(self.party1, bid1, 1, 99),
					Vote(self.party1, bid2, 1, 99)])),
				1)
		votes = votes.With(
				Votes(self.party2,
						set([Vote(self.party2, bid1, 1, 99)])),
				1)
		votes = votes.With(
				Votes(self.party3,
						set([Vote(self.party3, bid1, 1, 99)])),
				1)
		votes = votes.With(
				Votes(self.party4,
						set([Vote(self.party4, bid2, 1, 99)])),
				4)
		la = LargestAgreement()
		la._allVotes=votes
		agreement = la._collectVotes()
		self.assertEqual(set([self.party1, self.party4]),
				agreement.getMap().keys())
