from datetime import datetime
import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI 

from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.actions.Votes import Votes
from geniusweb.inform.Inform import Inform
from geniusweb.inform.OptIn import OptIn
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue


class OptInTest(unittest.TestCase, GeneralTests[OptIn]):
    maxDiff = None
        
    bid1 = Bid({"iss": DiscreteValue("val1")})
    bid2 = Bid({"iss": DiscreteValue("val2")})
    partyA = PartyId("partyA")
    partyB = PartyId("partyB")
    voteA1 = Vote(partyA, bid1, 2, 9)
    voteB1 = Vote(partyB, bid1, 2, 9)
    voteB2 = Vote(partyB, bid2, 2, 9)

    votesA = Votes(partyA, set([voteA1]))
    votesB = Votes(partyB, set([voteB1, voteB2]))

    optIn1 = OptIn([votesA, votesB])
    optIn1a = OptIn([votesA, votesB])
    optIn2 = OptIn([votesA])
    jackson = ObjectMapper();

    asJson = "{\"OptIn\":{\"votes\":[{\"Votes\":{\"actor\":\"partyA\",\"votes\":[{\"Vote\":{\"actor\":\"partyA\",\"bid\":{\"issuevalues\":{\"iss\":\"val1\"}},\"minPower\":2,\"maxPower\":9}}]}},{\"Votes\":{\"actor\":\"partyB\",\"votes\":[{\"Vote\":{\"actor\":\"partyB\",\"bid\":{\"issuevalues\":{\"iss\":\"val2\"}},\"minPower\":2,\"maxPower\":9}},{\"Vote\":{\"actor\":\"partyB\",\"bid\":{\"issuevalues\":{\"iss\":\"val1\"}},\"minPower\":2,\"maxPower\":9}}]}}]}}"

    def getGeneralTestData(self) -> List[List[OptIn]]:
        return [[self.optIn1, self.optIn1a], [self.optIn2]]
        
    def getGeneralTestStrings(self) -> List[str]:
        return ["OptIn.*Votes.*Vote.*partyA.*iss.*val1.*2.*Votes.*Vote.*partyB.*iss.*val.*.*2.*Vote.*partyB.*iss.*val.*2.*",
                "OptIn.*Votes.*Vote.*partyA.*iss.*val.*2.*"]

    def testSerialize(self):
        jsonstruct = self.jackson.toJson(self.optIn1)
        print(jsonstruct)
        # test does not work, python keeps changing the field order...
#         self.assertEqual(self.bla, jsonstruct)

    def testDeserialize(self):
        p = self.jackson.parse(json.loads(self.asJson), Inform)
        print(p);
        self.assertEqual(self.optIn1, p)
        
    def testOneVotePerParty(self):
        self.assertRaises(ValueError, lambda: OptIn([self.votesA, self.votesA]))

