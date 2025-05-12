import json
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Inform import Inform
from geniusweb.inform.Voting import Voting
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from typing import List
from unitpy.GeneralTests import GeneralTests


class VotingTest(unittest.TestCase,GeneralTests[Voting]):
    maxDiff = None

    jackson = ObjectMapper();
    party1 = PartyId("party1");
    bid1 = Bid({"iss": DiscreteValue("val1")})
    bid2 =  Bid({"iss": DiscreteValue("val2")})
    
    powers1 = {party1: 2}
    powers2 = {party1: 3}
    
    voting1 = Voting([Offer(party1, bid1)], powers1)
    voting1a = Voting([Offer(party1, bid1)], powers1)
    voting2 = Voting([ Offer(party1, bid2)], powers1)
    voting3 = Voting([ Offer(party1, bid1)], powers2);
    
    asJson="{\"Voting\":{\"offers\":[{\"Offer\":{\"actor\":\"party1\",\"bid\":{\"issuevalues\":{\"iss\":\"val1\"}}}}],\"powers\":{\"party1\":2}}}"

    def getGeneralTestData(self)-> List[List[Voting]]:
        return [[self.voting1, self.voting1a], [self.voting2], [self.voting3]]
    

    def getGeneralTestStrings(self)-> List[str]:
        return ["Voting.*Bid.*iss.*val1.*party1.*2.*",
                "Voting.*Bid.*iss.*val2.*party1.*2.*",
                "Voting.*Bid.*iss.*val1.*party1.*3.*"]
    

    
    def testGeneralTestData(self):
        self.assertEqual(self.voting1, self.voting1a)
        self.assertEqual(hash(self.voting1), hash(self.voting1a))
        self.assertNotEqual(self.voting1, self.voting2)
        self.assertNotEqual(hash(self.voting1), hash(self.voting2))

    
    def testSerialize(self) :
        jsondict = self.jackson.toJson(self.voting1);
        print(jsondict);
        self.assertEqual(json.loads(self.asJson), jsondict);
    
    def testDeserialize(self):
        p = self.jackson.parse(json.loads(self.asJson), Inform)
        print(p)
        self.assertEqual(self.voting1, p)
    