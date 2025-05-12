import json
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Agreements import Agreements
from geniusweb.inform.Finished import Finished
from geniusweb.inform.Inform import Inform
from geniusweb.issuevalue.Bid import Bid


class FinishedTest(unittest.TestCase):
    pyson=ObjectMapper()
    id1 = PartyId("party1")
    id2 = PartyId("party2")
    
    bid1 = Bid({})
    agrees  = Agreements({id1: bid1, id2:bid1 })
    agrees2 = Agreements({id2: bid1, id2:bid1 })

    finished  = Finished(agrees)
    finished1  = Finished(agrees)
    finished2  = Finished(agrees2)
    
    finishedjson:dict={'Finished':{'agreements':{'party1':{'issuevalues':{}},'party2':{'issuevalues':{}}}}}
    

    def testNone(self) :
        self.assertRaises(ValueError, lambda:Finished(None))

    def testSerialize(self):
        print(str(self.pyson.toJson(self.finished1)))
        self.assertEqual(self.finishedjson, self.pyson.toJson(self.finished))
        
    def testDeserialize(self):
        self.assertEqual(self.finished, self.pyson.parse(self.finishedjson, Inform))
    
    def testRepr(self):
        self.assertEqual("Finished[Agreements{party1=Bid{}, party2=Bid{}}]", repr(self.finished))
        
    def testEqual(self):
        self.assertEqual(self.finished, self.finished1)
        self.assertNotEqual(self.finished, self.finished2)
        self.assertEqual(hash(self.finished), hash(self.finished1))
        self.assertNotEqual(hash(self.finished), hash(self.finished2))
        
        