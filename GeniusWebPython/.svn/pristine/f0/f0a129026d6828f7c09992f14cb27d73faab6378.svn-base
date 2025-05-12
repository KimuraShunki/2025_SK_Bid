from typing import List, Dict
import unittest
from unittest.mock import Mock

from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.actions.Votes import Votes
from geniusweb.issuevalue.Bid import Bid
from geniusweb.voting.CollectedVotes import CollectedVotes


class CollectedVotesTest (unittest.TestCase, GeneralTests[CollectedVotes]):

	bidA = Mock(Bid)
	bidB = Mock(Bid)
	a = Mock(Bid)
	b = Mock(Bid)
	c = Mock(Bid)
	d = Mock(Bid)
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")
	party4 = PartyId("party4")

	partyP = PartyId("partyP")
	partyQ = PartyId("partyQ")
	partyR = PartyId("partyR")
	partyS = PartyId("partyS")

	votePA2 = Vote(partyP, bidA, 2, 9)
	voteQA2 = Vote(partyQ, bidA, 2, 9)
	voteQA3 = Vote(partyQ, bidA, 3, 9)
	voteQB3 = Vote(partyQ, bidB, 3, 9)
	voteQB2 = Vote(partyQ, bidB, 2, 9)
	voteRA2 = Vote(partyR, bidA, 2, 9)
	voteRA3 = Vote(partyR, bidA, 3, 9)
	voteRA4 = Vote(partyR, bidA, 4, 9)
	voteRB2 = Vote(partyR, bidB, 2, 9)

	allpowers:Dict[PartyId,int]  = {}

	cv1 = CollectedVotes({},	{})
	cv1a = CollectedVotes({},	{})

	votes = Votes(partyP, set([votePA2]))
	cv2 = CollectedVotes({partyP: votes},{partyP: 1})

	
	allpowers[partyP]= 1
	allpowers[partyQ]=1
	allpowers[partyR]= 1
	allpowers[partyS]=1


	def getGeneralTestData(self)->List[List[CollectedVotes]]:
		return [[self.cv1, self.cv1a], [self.cv2]]

	def getGeneralTestStrings(self)->List[str] :
		return ["CollectedVotes.\\{\\}.*\\{\\}.*",
				"CollectedVotes.\\{partyP=Votes.*Vote.partyP.*Mock.*,2.*\\}.*\\{partyP=1\\}.*"]


	def testGetAllBids(self):
		allvotes:Dict[PartyId, Vote]  = {}
		allvotes[self.partyP]= Votes(self.partyP, set([self.votePA2]))
		allvotes[self.partyQ]= Votes(self.partyQ,
				set([self.voteQA2, self.voteQB3]))

		allbids:Dict[Bid, Set[Vote]]  = CollectedVotes(allvotes, self.allpowers)\
				.getAllBids()
		self.assertEqual(2, len(allbids))
		self.assertEqual(set([self.votePA2, self.voteQA2]),
				allbids.get(self.bidA))
		self.assertEqual(set([self.voteQB3]), allbids.get(self.bidB))

	def testGetMaxSubset2(self):
		votes = set([self.votePA2, self.voteQA2])
		cv = CollectedVotes({},self.allpowers)
		parties = cv._getMaxPowerGroup(votes)
		self.assertEqual(set([self.partyP, self.partyQ]), parties)

		# test the optimized code similarly
		parties = cv._getMaxPowerGroupBreathFirst(votes)
		self.assertEqual(set([self.partyP, self.partyQ]), parties)

	def testGetMaxSubset3(self): 
		votes = set([self.votePA2, self.voteQA2, self.voteRA4])
		cv = CollectedVotes({},self.allpowers)

		parties = cv._getMaxPowerGroup(votes)
		# party R wants 4 votes so we can't satisfy
		self.assertEqual(set([self.partyP, self.partyQ]), parties)

		# test the optimized code similarly
		parties = cv._getMaxPowerGroupBreathFirst(votes)
		self.assertEqual(set([self.partyP, self.partyQ]), parties)

	def  testGetMaxSubset3b(self):
		votes = set([self.votePA2, self.voteQA2, self.voteRA3])
		cv = CollectedVotes({},self.allpowers)
		parties = cv._getMaxPowerGroup(votes)
		# party R wants 4 votes so we can't satisfy
		self.assertEqual(set([self.partyP, self.partyQ, self.partyR]),
				parties)

		# test the optimized code similarly
		parties = cv._getMaxPowerGroupBreathFirst(votes)
		self.assertEquals(set([self.partyP, self.partyQ, self.partyR]),
				parties)

	def  testNoConsensus(self):
		votes = set([self.voteQA3, self.voteRA3])
		cv =CollectedVotes({},	self.allpowers)
		self.assertEqual(set(), cv._getMaxPowerGroup(votes))
		self.assertEqual(set(),	cv._getMaxPowerGroupBreathFirst(votes))

	def testGetMaxAgreements(self) :
		allvotes:Map[PartyId, Votes] = {}
		allvotes[self.partyP]= Votes(self.partyP, set([self.votePA2]))
		allvotes[self.partyQ]= Votes(self.partyQ,
				set([self.voteQA2, self.voteQB2]))
		allvotes[self.partyR]= Votes(self.partyR,
				set([self.voteRA4, self.voteRB2]))

		allagrees:Map[Bid, Set[PartyId]]  = CollectedVotes(allvotes,
				self.allpowers).getMaxAgreements()
		self.assertEquals(set([self.partyP, self.partyQ]),
				allagrees.get(self.bidA))
		self.assertEqual(set([self.partyQ, self.partyR]),
				allagrees.get(self.bidB))


	def testGetNoAgreements(self) :
		allvotes:Dict[PartyId, Votes]  = {}
		allvotes[self.partyP]= Votes(self.partyP, set([self.votePA2]))
		allagrees  = CollectedVotes(allvotes, self.allpowers).getMaxAgreements()
		self.assertEquals({}, allagrees)

	def testgetConsensusGroupsTest(self):
		cv = CollectedVotes({},self.allpowers)

		consensus = cv._getConsensusGroups(
				set([self.votePA2, self.voteQA2]))
		# should give 1 solution: both parties join in.
		print(consensus)
		self.assertEqual(1, len(consensus))
		self.assertEqual(2, len(next(iter(consensus))))

	def testgetConsensusGroupsTestPQR(self):
		cv = CollectedVotes({},self.allpowers)

		consensus = cv._getConsensusGroups(
				set([self.votePA2, self.voteQA2, self.voteRA4]))
		# should give 1 solution: P and Q join in. 4 is unreachable.
		print(consensus)
		self.assertEqual(1, len(consensus))
		self.assertEqual(2, len(next(iter(consensus))))

	def testgetConsensusGroupsTestPQR2(self):
		cv = CollectedVotes({},self.allpowers)

		consensus = cv._getConsensusGroups(
				set([self.votePA2, self.voteQA2, self.voteRA2]))
		# should give 4 solutions: P+Q, P+R, Q+R and P+Q+R
		print(consensus)
		self.assertEqual(4, len(consensus))

	def testgetConsensusGroupsTestRExtraPower(self) :
		# give R extra power to reach the 4 if other 2 join
		allpowers = {self.partyP: 1, self.partyQ: 1, self.partyR: 2}

		cv = CollectedVotes({}, allpowers)

		consensus = cv._getConsensusGroups(
				set([self.votePA2, self.voteQA2, self.voteRA4]))
		# should give solutions P+Q and P+Q+R
		print(consensus)
		self.assertEqual(2, len(consensus))
		lengths = set([ len(con) for con in consensus ])
		self.assertEqual(set([2,3]), lengths)
	
	def testWith(self):
		allvotes:Map[PartyId, Votes]  = {}
		allvotes[self.partyP]=  Votes(self.partyP, set([self.votePA2]))
		cv = CollectedVotes(allvotes, self.allpowers)
		self.assertEqual(1, len(cv.getVotes().keys()))
		cv = cv.With(Votes(self.partyQ, set([self.voteQA2])), 2)
		self.assertEquals(2, len(cv.getVotes().keys()))

	def testWithout(self):
		allvotes:Map[PartyId, Votes]  = {}
		allvotes[self.partyP]= Votes(self.partyP, set([self.votePA2]))
		allvotes[self.partyQ]= Votes(self.partyQ,
				set([self.voteQA2, self.voteQB2]))
		allvotes[self.partyR]= Votes(self.partyR,
				set([self.voteRA4, self.voteRB2]))

		# give R extra power to reach the 4 if other 2 join
		allpowers = {self.partyP: 1,self.partyQ: 1,self.partyR: 2}

		cv =  CollectedVotes(allvotes, allpowers)

		self.assertEqual(3, len(cv.getVotes()))
		cv = cv.Without(set([self.partyP, self.partyQ]))
		self.assertEqual(1, len(cv.getVotes()))
		self.assertEqual(1, len(cv.getPowers()))

	def testgetConsensusGroupMaxPower(self):
		P = Vote(self.partyP, self.bidA, 2, 3)
		Q = Vote(self.partyQ, self.bidA, 2, 3)
		R = Vote(self.partyR, self.bidA, 2, 3)
		S = Vote(self.partyS, self.bidA, 2, 3)
		allvotes:Map[PartyId, Votes]  = {}
		allvotes[self.partyP]= Votes(self.partyP, set([P]))
		allvotes[self.partyQ]= Votes(self.partyQ, set([Q]))
		allvotes[self.partyR]= Votes(self.partyR, set([R]))
		allvotes[self.partyS]= Votes(self.partyS, set([S]))

		cv = CollectedVotes(allvotes, self.allpowers)
		consensus = cv._getConsensusGroups(
				set([P, Q, R, S]))
		print(consensus)
		# check that all are size 2 or 3.
		for set1 in consensus:
			self.assertTrue(len(set1) == 2 or len(set1) == 3)

	def testgetConsensusGroupMaxPowerModifiedPartyPowers(self):
		# party R gets power 2.
		P = Vote(self.partyP, self.bidA, 2, 3)
		Q = Vote(self.partyQ, self.bidA, 2, 3)
		R = Vote(self.partyR, self.bidA, 2, 3)
		allvotes:Map[PartyId, Votes]  = {}
		allvotes[self.partyP]= Votes(self.partyP, set([P]))
		allvotes[self.partyQ]= Votes(self.partyQ, set([Q]))
		allvotes[self.partyR]= Votes(self.partyR, set([R]))

		powers={self.partyP: 1,self.partyQ: 1, self.partyR: 2}

		cv = CollectedVotes(allvotes, powers)
		consensus = cv._getConsensusGroups(set([P, Q, R]))
		print(consensus)
		# R has power 2 now. That means groups of size 3 are not posisble.
		# check that all are size 2.
		for set1 in consensus:
			self.assertTrue(len(set1) == 2)

	def testRandomOrderOfSet(self):
		# this test that a Set of parties does not have
		# the fixed order of the list #1878
		# not really testing our code but crucial for proper working.
		list1 = [self.partyQ, self.partyR, self.partyS]
		# #1878 does Set randomize somewhat?
		parties = set(list1)
		self.assertNotEquals(list1, [parties])

		list2 = [list]
		list2.append(self.partyP)
		parties = set(list2)
		self.assertNotEquals(list2, [parties])
