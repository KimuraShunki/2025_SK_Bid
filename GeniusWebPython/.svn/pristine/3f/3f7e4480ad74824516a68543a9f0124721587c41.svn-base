from decimal import Decimal
import json
from typing import Dict
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.Action import Action
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.Vote import Vote
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.Value import Value


class VoteTest (unittest.TestCase) :
    jackson = ObjectMapper()

    id1 = PartyId("party1")
    id2 = PartyId("party2")
    issuevalues: Dict[str, Value]={}
    issuevaluesb: Dict[str, Value] = {}
    bid:Bid 
    bidb:Bid 
    ISSUE1 = "issue1";
    VALUE1 = DiscreteValue("value1");
    ISSUE2 = "issue2";
    VALUE2 = NumberValue(Decimal(10));
    # issue 2 is NUMBER and thus serializes with leading '='
    votestring = "{\"Vote\":{\"actor\":\"party1\",\"bid\":{\"issuevalues\":{\"issue1\":\"value1\",\"issue2\":10}},\"minPower\":1,\"maxPower\":2}}";

    issuevalues[ISSUE1]=VALUE1
    issuevalues[ISSUE2]=VALUE2
    bid = Bid(issuevalues)
    vote1 = Vote(id1, bid, 1, 2)
    vote1a = Vote(id1, bid, 1, 2)

    vote2 = Vote(id2, bid, 1, 2)

    # values swapped, so different issuevalues.
    issuevaluesb[ISSUE1]= VALUE2
    issuevaluesb[ISSUE2]= VALUE2
    bidb = Bid(issuevaluesb)
    vote3 = Vote(id1, bidb, 1, 2)

    vote4 = Vote(id1, bid, 2, 2)
    vote5 =  Vote(id1, bid, 1, 3)


    def testSerialize(self):
        print(self.jackson.toJson(self.vote1))
        self.assertEqual(self.votestring, json.dumps(self.jackson.toJson(self.vote1)).replace(" ",""))


    def testDeserialize(self):
        act = self.jackson.parse(json.loads(self.votestring), Action)
        self.assertEqual(self.vote1, act)

    def testEqual(self):
        self.assertEqual(self.vote1, self.vote1a)
        self.assertNotEqual(self.vote1, self.vote2)
        self.assertEqual(hash(self.vote1), hash(self.vote1a))
        self.assertNotEqual(hash(self.vote1), hash(self.vote2))
