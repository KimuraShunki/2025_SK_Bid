from geniusweb.events.TournamentStarted import TournamentStarted
import unittest
from unitpy.GeneralTests import GeneralTests
from pyson.ObjectMapper import ObjectMapper
from typing import List
from geniusweb.events.NegotiationEvent import NegotiationEvent
import json

class TournamentStartedTest(unittest.TestCase, GeneralTests[TournamentStarted]):
    pyson = ObjectMapper()
    
    SESSIONNR = 1
    NOW = 101
    NOW1 = NOW + 1
    NSESSIONS = 5

    tournamentStarted = TournamentStarted(NSESSIONS, NOW)
    tournamentStarteda = TournamentStarted(NSESSIONS, NOW)
    otherTournamentStarted = TournamentStarted(NSESSIONS + 1, NOW)
    tournamentStartedLater = TournamentStarted(NSESSIONS, NOW1)
    
    tournamentstartedstring = '{"TournamentStarted":{"time":101,"numberOfSessions":5}}'
    
    def getGeneralTestData(self) -> List[List[TournamentStarted]]:
        mylist = []
        mylist.append([self.tournamentStarted, self.tournamentStarteda])
        mylist.append([self.otherTournamentStarted])
        mylist.append([self.tournamentStartedLater])
        return mylist

    def getGeneralTestStrings(self) -> List[str]:
        return ["TournamentStarted\\[.*" + str(self.NOW) + ".*" + str(self.NSESSIONS) + ".*\\]",\
                "TournamentStarted\\[.*" + str(self.NOW) + ".*" + str(self.NSESSIONS + 1) + ".*\\]",\
                "TournamentStarted\\[.*" + str(self.NOW1) + ".*" + str(self.NSESSIONS) + ".*\\]"]

    def testserializeTournamentStarted(self):
        print(self.tournamentstartedstring)
        self.assertEqual(json.loads(self.tournamentstartedstring), self.pyson.toJson(self.tournamentStarted))
 
    def testdeserializeTournamentStarted(self):
        evt = self.pyson.parse(json.loads(self.tournamentstartedstring), NegotiationEvent)
        self.assertEqual(TournamentStarted, type(evt))
        event = evt
        # compare fields, as sessionended is a derived/new inner class
        self.assertEqual(self.NSESSIONS, event.getNumberOfSessions())
        self.assertEqual(self.NOW, event.getTime())

    def testNullTime(self):
        TournamentStarted(self.NSESSIONS, 0)

    def testNegativeTime(self):
        self.assertRaises(ValueError, lambda: TournamentStarted(self.NSESSIONS, -1))