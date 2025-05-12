import unittest
from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from geniusweb.events.SessionStarted import SessionStarted
from geniusweb.actions.PartyId import PartyId
from typing import List
from geniusweb.events.NegotiationEvent import NegotiationEvent
import json

class SessionStartedTest(unittest.TestCase, GeneralTests[SessionStarted]):

    pyson = ObjectMapper()

    SESSIONNR = 1
    NOW = 101
    NOW1 = NOW + 1

    PARTY1 = PartyId("party1")
    PARTY2 = PartyId("party2")

    parties = [PARTY1, PARTY2]

    sessionStartedLater = SessionStarted(SESSIONNR, parties, NOW1)
    othersessionStarted = SessionStarted(SESSIONNR + 1, parties, NOW)

    sessionStarted = SessionStarted(SESSIONNR, parties, NOW)
    sessionStarted1 = SessionStarted(SESSIONNR, parties, NOW)
    # jackson expected format.
    sessionstartedstring = "{\"SessionStarted\":{\"sessionNumber\":1,\"parties\":[\"party1\",\"party2\"],\"time\":101}}"
    # "{\"sessionstarted\":{\"time\":101,\"sessionNumber\":1,\"parties\":[\"party1\",\"party2\"]}}";
    expectedstring = "SessionStarted.*101.*"

    def getGeneralTestData(self) -> List[List[SessionStarted]]:
        mylist = []
        mylist.append([self.sessionStarted, self.sessionStarted1])
        mylist.append([self.sessionStartedLater])
        mylist.append([self.othersessionStarted])
        return mylist

    def getGeneralTestStrings(self) -> List[str]:
        return ["SessionStarted.*" + str(self.SESSIONNR) + ".*" + str(self.NOW) + ".*",\
                "SessionStarted.*" + str(self.SESSIONNR) + ".*" + str(self.NOW1) + ".*",\
                "SessionStarted.*" + str(self.SESSIONNR + 1) + ".*" + str(self.NOW) + ".*"]

    def testSerialize(self):
        print(self.sessionstartedstring)
        self.assertEqual(json.loads(self.sessionstartedstring), self.pyson.toJson(self.sessionStarted))

    def testDeserialize(self):
        evt = self.pyson.parse(json.loads(self.sessionstartedstring), NegotiationEvent)        
        self.assertEqual(SessionStarted, type(evt))
        event = evt
        # compare fields, as sessionended is a derived/new inner class
        self.assertEqual(self.NOW, event.getTime())
        self.assertEqual(self.SESSIONNR, event.getSessionNumber())
        self.assertEqual(2, len(event.getParties()))

