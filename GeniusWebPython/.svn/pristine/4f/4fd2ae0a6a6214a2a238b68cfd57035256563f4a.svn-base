import unittest

from pyson.ObjectMapper import ObjectMapper
from geniusweb.events.ActionEvent import ActionEvent 
from unitpy.GeneralTests import GeneralTests
from geniusweb.actions.PartyId import PartyId
from geniusweb.actions.EndNegotiation import EndNegotiation
from typing import List
import json
from geniusweb.events.NegotiationEvent import NegotiationEvent
from unittest.mock import Mock

class ActionEventTest(unittest.TestCase, GeneralTests[ActionEvent]):
    NOW = 101
    pyson = ObjectMapper()
    string = "{\"ActionEvent\":{\"action\":{\"EndNegotiation\":{\"actor\":\"party1\"}},\"time\":101}}"
    pid = PartyId("party1");
    action = EndNegotiation(pid);
    evt = ActionEvent(action, NOW);
    evt1 = ActionEvent(action, NOW);
    evtb = ActionEvent(action, NOW + 1);
    
    def getGeneralTestData(self) -> List[List[ActionEvent]]:
        return [[self.evt, self.evt1], [self.evtb]]
                
    def getGeneralTestStrings(self):
        return "ActionEvent\\[.*" + str(self.NOW) + ".*EndNegotiation.*\\]",\
               "ActionEvent\\[.*" + str(self.NOW + 1) + ".*EndNegotiation.*\\]"
   
    def testSmoke(self):
        action1 = Mock(EndNegotiation)
        evt = ActionEvent(action1, 0)
    
    def testserialize(self):
        json1 = self.pyson.toJson(self.evt)
        print(json1)
        self.assertEqual(json.loads(self.string), json1)

    def testdeserializeTestReadActionEvent(self):
        evt1 = self.pyson.parse(json.loads(self.string), ActionEvent)
        print(evt1)
        # compare fields, as evt is a derived/new inner class
        self.assertEqual(EndNegotiation, type(evt1.getAction()))
        self.assertEqual(101, evt1.getTime())
    
    def testdeserializeTestReadEvent(self): 
        self.assertEqual(self.evt1, self.pyson.parse(json.loads(self.string), ActionEvent))
        evt1 = self.pyson.parse(json.loads(self.string), NegotiationEvent)
        self.assertEqual(ActionEvent, type(evt1))
        ev1 = evt1
        self.assertEqual(EndNegotiation, type(ev1.getAction()))
        self.assertEqual(101, ev1.getTime())
