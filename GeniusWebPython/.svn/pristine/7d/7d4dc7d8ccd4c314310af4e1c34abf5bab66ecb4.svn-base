import unittest
from geniusweb.party.DefaultParty import DefaultParty       
from geniusweb.party.Capabilities import Capabilities
from geniusweb.inform.Inform import Inform
      
class MyParty(DefaultParty):
    def getCapabilities(self) -> Capabilities:
        return Capabilities(set(["SAOP"]), set(["geniusweb.profile.Profile"]) )
    
    def getDescription(self) -> str:
        return "blabla"
    
    def notifyChange(self, data:Inform):
        # you'd think the type checker would complain here. data is NOT int
        return 


class DefaultPartyTest(unittest.TestCase):
    def testSmoke(self):
        MyParty()
        
    