import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.party.Capabilities import Capabilities       
from unitpy.GeneralTests import GeneralTests
from typing import List


class CapabilitiesTest(unittest.TestCase, GeneralTests[Capabilities]):
    pyson = ObjectMapper()
    
    capjson= {"behaviours":["SAOP"], "profiles":["geniusweb.profile.utilityspace.LinearAdditive"]}
    
    capabilities1 = Capabilities( set([ "SAOP"]), set(['geniusweb.profile.utilityspace.LinearAdditive']))
    capabilities1a= Capabilities( set([ "SAOP"]), set(['geniusweb.profile.utilityspace.LinearAdditive']))
    capabilities2 = Capabilities( set([ "SEB"]), set(['geniusweb.profile.utilityspace.LinearAdditive']))
    capabilities3 = Capabilities( set([ "SEB", "SAOP"]), set(['geniusweb.profile.utilityspace.LinearAdditive']))
    capabilities4 = Capabilities( set([ "SAOP"]), set(['geniusweb.profile.PartialOrdering']))
    
    def getGeneralTestData(self) -> List[List[Capabilities]]:
        return [[self.capabilities1, self.capabilities1a], [self.capabilities2], [self.capabilities3], [self.capabilities4]]
   
    def getGeneralTestStrings(self) -> List[str]:
        return ["Capabilities.*geniusweb.profile.utilityspace.LinearAdditive.*SAOP.*",
                "Capabilities.*geniusweb.profile.utilityspace.LinearAdditive.*SEB.*",
                "Capabilities.*geniusweb.profile.utilityspace.LinearAdditive.*S.*,.*S.*",
                "Capabilities.*geniusweb.profile.PartialOrdering.*SAOP.*"]
        
    def testSerialize(self):
        print(str(self.pyson.toJson(self.capabilities1)))
        self.assertEqual(self.capjson, self.pyson.toJson(self.capabilities1))
        
    def testDeserialize(self):
        self.assertEqual(self.capabilities1, self.pyson.parse(self.capjson, Capabilities))
        
    def testbehaviours(self):
        self.assertEqual(set(["SEB", "SAOP"]), self.capabilities3.getBehaviours())
        
