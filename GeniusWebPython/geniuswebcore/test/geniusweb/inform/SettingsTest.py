from typing import Dict, Any, List
from geniusweb.inform.Settings import Settings
from unitpy.GeneralTests import GeneralTests
from geniusweb.actions.PartyId import PartyId
from datetime import datetime
from pyson.ObjectMapper import ObjectMapper
from geniusweb.references.ProfileRef import ProfileRef
from uri.uri import URI
from geniusweb.references.ProtocolRef import ProtocolRef
from geniusweb.progress.ProgressRounds import ProgressRounds
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
import json
from geniusweb.inform.Inform import Inform
import unittest

class SettingsTest(unittest.TestCase, GeneralTests[Settings]):

    id1 = PartyId("party1")
    id2 = PartyId("party2")

    asJson = "{\"Settings\":"\
            + "{\"id\":\"party1\",\"profile\":\"ws:profile1\","\
            + "\"protocol\":\"ws:localhost/protocol1\","\
            + "\"progress\":{\"ProgressRounds\":{\"duration\":10,\"currentRound\":0,\"endtime\":999}},"\
            + "\"parameters\":{}}}"

    date = datetime.fromtimestamp(999/1000.)
    jackson = ObjectMapper()

    # we can't mock because we want to test the serializer
    profile1 = ProfileRef( URI("ws:profile1"))
    # jackson.readValue(serialized, Profile.class);

    protocol1 = ProtocolRef(URI("ws:localhost/protocol1"))
    protocol1a = ProtocolRef(URI("ws:localhost/protocol1"))
    protocol2 = ProtocolRef(URI("ws:localhost/protocol2"))
    progress1 = ProgressRounds(10, 0, date)
    progress1a = ProgressRounds(10, 0, date)
    progress2 = ProgressRounds(12, 0, date)

    settings1 = Parameters()
    settings2 = Parameters().With("a", 1)

    negoinfo1 = Settings(id1, profile1, protocol1, progress1, settings1)
    negoinfo1a = Settings(id1, profile1, protocol1a, progress1a,settings1)
    negoinfo2 = Settings(id1, profile1, protocol2, progress1, settings1)
    negoinfo3 = Settings(id1, profile1, protocol1, progress2, settings1)
    negoinfo4 = Settings(id2, profile1, protocol1, progress2, settings1)
    negoinfo5 = Settings(id1, profile1, protocol1, progress1, settings2)

    def getGeneralTestData(self)-> List[List[Settings]] :
        return [[self.negoinfo1, self.negoinfo1a],
                [self.negoinfo2], [self.negoinfo3],
                [self.negoinfo4], [self.negoinfo5]]

    def getGeneralTestStrings(self) -> List[str]:
        return [
                "Settings.*party1.*ProtocolRef.*protocol1.*ProgressRounds.*0.*10.*",
                "Settings.*party1.*ProtocolRef.*protocol2.*ProgressRounds.*0.*10.*",
                "Settings.*party1.*ProtocolRef.*protocol1.*ProgressRounds.*0.*12.*",
                "Settings.*party2.*ProtocolRef.*protocol1.*ProgressRounds.*0.*12.*",
                "Settings.*party1.*ProtocolRef.*protocol1.*ProgressRounds.*0.*10.*"]

    def testSmoke(self): 
        PartyRef(URI("ws:localhost"))
    
    def testNull(self):
        self.assertRaises(ValueError,lambda: PartyRef(None))
  
    def testSerialize(self):
        json1 = self.jackson.toJson(self.negoinfo1)
        print(json1)
        self.assertEqual(json.loads(self.asJson), json1)
        
    def testDeserialize(self):
        p = self.jackson.parse(json.loads(self.asJson), Inform)
        print(p)
        self.assertEqual(self.negoinfo1, p)

    def testGeneralDict(self):
        val = self.jackson.parse(json.loads("{\"a\":0.3,\"b\":{\"x\":3},\"c\":[1,2,3]}"), 
                                 Dict[str,Any])
        print(val)
