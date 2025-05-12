import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Agreements import Agreements
from geniusweb.inform.Inform import Inform
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue


class AgreementsTest(unittest.TestCase):
    pyson=ObjectMapper()
    id1 = PartyId("party1")
    id2 = PartyId("party2")
    bid1 = Bid({"issue1":DiscreteValue("value1")})
    bid2 = Bid({"issue2":DiscreteValue("value1")})

    agrees  = Agreements({id1: bid1 })
    agrees1  = Agreements({id1: bid1 })
    agrees2 = Agreements({ id2: bid1 })
    agrees3 = Agreements({ id1: bid2 })
    
    agrees1json:dict={"party1":{"issuevalues":{"issue1":"value1"}}}
    
    def testNull(self) :
        Agreements();

    def testNone(self) :
        self.assertRaises(ValueError, lambda:Agreements(None))

    def testWithAlreadyActed(self) :
        self.assertRaises(ValueError, lambda:self.agrees1.With(self.agrees1))

    def testWith(self):
        agrees = self.agrees1.With(self.agrees2);
        self.assertEquals(self.bid1, agrees.getMap()[self.id1]);
        self.assertEquals(self.bid1, agrees.getMap()[self.id2]);

    def testSerialize(self):
        print(str(self.pyson.toJson(self.agrees1)))
        self.assertEqual(self.agrees1json, self.pyson.toJson(self.agrees1))
        
    def testDeserialize(self):
        self.assertEqual(self.agrees1, self.pyson.parse(self.agrees1json, Agreements))
        
    def testRepr(self):
        self.assertEqual('Agreements{party1=Bid{issue1="value1"}}', repr(self.agrees))
        
    def testEqual(self):
        self.assertEqual(self.agrees, self.agrees1)
        self.assertNotEqual(self.agrees, self.agrees2)
        self.assertNotEqual(self.agrees, self.agrees3)
        self.assertEqual(hash(self.agrees), hash(self.agrees1))
        self.assertNotEqual(hash(self.agrees), hash(self.agrees2))
        self.assertNotEqual(hash(self.agrees), hash(self.agrees3))
        
        