import unittest
from unitpy.GeneralTests import GeneralTests
from geniusweb.protocol.tournament.Team import Team
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyWithParameters import PartyWithParameters
from typing import List
from uri.uri import URI

class TeamTest(unittest.TestCase, GeneralTests[Team]):
    
    def setUp(self):
        self.partyref1 = PartyRef(URI("party1"))
        self.partyref2 = PartyRef(URI("party2"))
        self.params1 = Parameters().With("a", 1)
        self.pwithp1 = PartyWithParameters(self.partyref1, self.params1)
        self.pwithp2 = PartyWithParameters(self.partyref2, self.params1)
        self.team1 = Team([self.pwithp1])
        self.team1a = Team([self.pwithp1])
        self.team2 = Team([self.pwithp2])

        #@Override
    def getGeneralTestData(self) -> List[List[Team]]:
        return [[self.team1, self.team1a],[self.team2]]

    #@Override
    def getGeneralTestStrings(self) -> List[str]:
        return [".PartyRef.party1..a=1..",".PartyRef.party2..a=1.."]

    #@Test
    def testGet(self):
        self.assertEqual([self.pwithp1], self.team1.getParties())
        