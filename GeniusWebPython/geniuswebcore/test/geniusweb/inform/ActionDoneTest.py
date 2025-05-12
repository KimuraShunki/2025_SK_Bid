import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.ActionDone import ActionDone
from geniusweb.inform.Inform import Inform
from geniusweb.inform.YourTurn import YourTurn
from geniusweb.inform.Voting import Voting
from unitpy.GeneralTests import GeneralTests
from geniusweb.profileconnection import ProfileConnectionFactory
from typing import List
import json


class ActionDoneTest(unittest.TestCase, GeneralTests[ActionDone]):

    pyson = ObjectMapper()
    id1 = PartyId("party1")
    id2 = PartyId("party2")
    
    act1 = EndNegotiation(id1)
    act2 = EndNegotiation(id2)
     
    done1 = ActionDone(act1)
    done1a = ActionDone(act1)
    done2 = ActionDone(act2)
    
    actiondonejson = {"ActionDone":{"action":{"EndNegotiation":{"actor":"party1"}}}}
    
    def getGeneralTestData(self) -> List[List[ActionDone]]:
        return [[self.done1, self.done1a], [self.done2]]
    
    def getGeneralTestStrings(self) -> List[str]:
        return ["ActionDone.*EndNegotiation.*party1.*",
                "ActionDone.*EndNegotiation.*party2.*"]

    def testSerializeAccept(self):
        json1 = self.pyson.toJson(self.done1)
        print(json1)
        self.assertEqual(self.actiondonejson, json1)
        
    def testDeserialize(self):
        self.assertEqual(self.done1, self.pyson.parse(self.actiondonejson, Inform))
        
    def testGet(self):
        self.assertEqual(self.act1, self.done1.getAction())
        
        
        