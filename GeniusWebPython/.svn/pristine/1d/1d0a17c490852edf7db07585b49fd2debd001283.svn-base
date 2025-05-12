import json
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Action import Action
from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.actions.Votes import Votes
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue


class VotesTest (unittest.TestCase) :
    maxDiff = None

    jackson = ObjectMapper();
    votestring = "{\"Votes\":{\"actor\":\"partyA\",\"votes\":[{\"Vote\":{\"actor\":\"partyA\",\"bid\":{\"issuevalues\":{\"is1\":\"val1\"}},\"minPower\":2,\"maxPower\":9}},{\"Vote\":{\"actor\":\"partyA\",\"bid\":{\"issuevalues\":{\"is1\":\"val2\"}},\"minPower\":2,\"maxPower\":9}}]}}";

    partyA = PartyId("partyA");
    partyB = PartyId("partyB");
    bid1 = Bid({"is1": DiscreteValue("val1")})
    bid2 = Bid({"is1": DiscreteValue("val2")})
    voteA1 = Vote(partyA, bid1, 2, 9)
    voteA2 = Vote(partyA, bid2, 2, 9)
    voteB1 = Vote(partyB, bid1, 2, 9)
    voteB2 = Vote(partyB, bid2, 2, 9)

    votes1 = Votes(partyA,set([voteA1, voteA2]))
    votes1a=Votes(partyA,set([voteA1, voteA2]))
    votes2 = Votes(partyB,set([voteB1, voteB2]))

    def testRejectVoteWithIncorrectParty(self):
        self.assertRaises(ValueError, lambda: Votes(self.partyA, set([self.voteB1])) )
 

    def tes1Serialize(self) :
        # FIXME why is this failing half of the time?
        print(str(self.jackson.toJson(self.votes1)));
        self.assertEqual(json.loads(self.votestring), self.jackson.toJson(self.votes1))

    def testDeserialize(self) :
        act = self.jackson.parse(json.loads(self.votestring), Action)
        self.assertEqual(self.votes1, act)

    def testWrongPartyName(self):
        self.assertRaises(ValueError, lambda:\
            Votes(self.partyA, set([self.voteB1, self.voteB2])))

    def testIsExtendingTestExtraVote(self):
        otherVotes = Votes(self.partyA, set([self.voteA1]))
        self.assertTrue(self.votes1.isExtending(otherVotes))

    def testIsExtendingTestNoVotes(self) :
        otherVotes = Votes(self.partyA, set())
        self.assertTrue(self.votes1.isExtending(otherVotes))

    def testIsExtendingTestMissing(self):
        otherVotes = Votes(self.partyA, set([self.voteA1]))
        self.assertFalse(otherVotes.isExtending(self.votes1))

    def testIsExtendingIdenticalVotes(self):
        self.assertTrue(self.votes1.isExtending(self.votes1))

#     @Test
#     public void isReallyExtendingVotesMin() {
#         Vote powervoteA1 = new Vote(partyA, bid1, 1, 9);
#         Votes powerVotes = new Votes(partyA,
#                 new HashSet<>(Arrays.asList(powervoteA1, voteA2)));
#         assertTrue(powerVotes.isExtending(votes1));
#     }
# 
#     @Test
#     public void isReallyExtendingVotesMax() {
#         Vote powervoteA1 = new Vote(partyA, bid1, 2, 10);
#         Votes powerVotes = new Votes(partyA,
#                 new HashSet<>(Arrays.asList(powervoteA1, voteA2)));
#         assertTrue(powerVotes.isExtending(votes1));
#     }
# 
#     @Test
#     public void IsNarrowingOneVoteRemoved() {
#         Votes narrowVotes = new Votes(partyA, Collections.singleton(voteA2));
#         assertFalse(narrowVotes.isExtending(votes1));
#     }
# 
#     @Test
#     public void isNarrowingTestMoreMinPower() {
#         Vote narrowVoteA1 = new Vote(partyA, bid1, 3, 9);
#         Votes narrowVotes = new Votes(partyA,
#                 new HashSet<>(Arrays.asList(narrowVoteA1, voteA2)));
#         assertFalse(narrowVotes.isExtending(votes1));
#         assertTrue(votes1.isExtending(narrowVotes));
#     }
# 
#     @Test
#     public void isNarrowingLessMaxPower() {
#         Vote powervoteA1 = new Vote(partyA, bid1, 2, 8);
#         Votes narrowVotes = new Votes(partyA,
#                 new HashSet<>(Arrays.asList(powervoteA1, voteA2)));
#         assertFalse(narrowVotes.isExtending(votes1));
#         assertTrue(votes1.isExtending(narrowVotes));
#     }
# 
#     @Test(expected = IllegalArgumentException.class)
#     public void testDuplicateBidsNotAllowed() {
#         Vote voteA1similar = new Vote(partyA, bid1, 3, 9);
#         Votes votes = new Votes(partyA,
#                 new HashSet<>(Arrays.asList(voteA1, voteA1similar)));
#     }
# }
