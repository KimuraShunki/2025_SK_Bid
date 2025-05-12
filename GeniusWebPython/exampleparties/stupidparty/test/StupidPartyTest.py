from datetime import datetime
from decimal import Decimal
from typing import cast, List
import unittest

from geniusweb.actions.Accept import Accept
from geniusweb.actions.Action import Action
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.connection.ConnectionEnd import ConnectionEnd
from geniusweb.inform.ActionDone import ActionDone
from geniusweb.inform.Inform import Inform
from geniusweb.inform.Settings import Settings
from geniusweb.inform.YourTurn import YourTurn
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.progress.ProgressTime import ProgressTime
from geniusweb.references.Parameters import Parameters
from geniusweb.references.ProfileRef import ProfileRef
from geniusweb.references.ProtocolRef import ProtocolRef
from geniusweb.references.Reference import Reference
from tudelft.utilities.listener.DefaultListenable import DefaultListenable
from uri.uri import URI

from stupidparty.StupidParty import StupidParty


class MyConn(ConnectionEnd[Inform, Action], DefaultListenable):
    def __init__(self):
        super().__init__()
        self._actions:List[Action]=[]
    
    def send(self,data:Action ):
        self._actions.append(data)
        
    def getReference(self) -> Reference:
        return cast(Reference,None)

    def getRemoteURI(self)->URI: 
        return URI("whatever")
    
    def close(self):
        pass

    def getError(self) -> Exception:
        return cast(Exception, None)
    
    def getActions(self)-> List[Action]:
        return self._actions
    
class StupidPartyTest(unittest.TestCase):
    def test_smoke(self):
        StupidParty()
        
    def testConnect(self):
        connection = MyConn()
        party=StupidParty()
        party.connect(connection)
        party.disconnect()
        
        
    def testSendInfo(self):
        id1 = PartyId("party1")
        profileref1 = ProfileRef(URI("profile1"))
        protocolref1 = ProtocolRef(URI("protoco1"))
        progress1=ProgressTime(1000, datetime.fromtimestamp(12345))
        parameters1=Parameters()
        settings  = Settings(id1, profileref1, protocolref1, progress1, parameters1 )
        
        connection = MyConn()
        party=StupidParty()
        party.connect(connection)
        connection.notifyListeners(settings)
        party.disconnect()
        self.assertEquals([], connection.getActions())
        
    def testSendYourTurn(self):
        id1 = PartyId("party1")
        profileref1 = ProfileRef(URI("profile1"))
        protocolref1 = ProtocolRef(URI("protoco1"))
        progress1=ProgressTime(1000, datetime.fromtimestamp(12345))
        parameters1=Parameters()
        settings  = Settings(id1, profileref1, protocolref1, progress1, parameters1 )

        connection = MyConn()
        party=StupidParty()
        party.connect(connection)
        connection.notifyListeners(settings)
        connection.notifyListeners(YourTurn())
        party.disconnect()
        
        actions = connection.getActions()
        self.assertEquals(1, len(actions))
        self.assertTrue(isinstance(actions[0], Offer))

    def testSendOfferAndYourTurn(self):
        id1 = PartyId("party1")
        profileref1 = ProfileRef(URI("profile1"))
        protocolref1 = ProtocolRef(URI("protoco1"))
        progress1=ProgressTime(1000, datetime.fromtimestamp(12345))
        parameters1=Parameters()
        settings  = Settings(id1, profileref1, protocolref1, progress1, parameters1 )

        bid=Bid({'a':NumberValue(Decimal(1))})
        offer = Offer(PartyId('other'), bid)

        party=StupidParty()
        
        connection = MyConn()
        party.connect(connection)
        connection.notifyListeners(settings)
        connection.notifyListeners(ActionDone(offer))
        connection.notifyListeners(YourTurn())
        party.disconnect()
        
        actions = connection.getActions()
        self.assertEquals(1, len(actions))
        self.assertEquals(Accept(id1, bid), actions[0])

    def testAccept(self):
        id1 = PartyId("party1")
        bid=Bid({'a':NumberValue(Decimal(1))})
        accept = Accept(id1, bid)
        
        profileref1 = ProfileRef(URI("profile1"))
        protocolref1 = ProtocolRef(URI("protoco1"))
        progress1=ProgressTime(1000, datetime.fromtimestamp(12345))
        parameters1=Parameters()
        settings  = Settings(id1, profileref1, protocolref1, progress1, parameters1 )

        party=StupidParty()

        connection = MyConn()
        party.connect(connection)
        connection.notifyListeners(settings)
        connection.notifyListeners(accept)
        
        party.disconnect()
        
        actions = connection.getActions()
        self.assertEquals(0, len(actions))

    def testYourTurnOfferYourTurn(self):
        me = PartyId("party1")
        other=PartyId('other')
        profileref1 = ProfileRef(URI("profile1"))
        protocolref1 = ProtocolRef(URI("protoco1"))
        progress1=ProgressTime(1000, datetime.fromtimestamp(12345))
        parameters1=Parameters()
        settings  = Settings(me, profileref1, protocolref1, progress1, parameters1 )

        emptybid=Bid({})
        emptyoffer = Offer(me, emptybid)
        bid=Bid({'a':NumberValue(Decimal(1))})
        offer = Offer(other, bid)

        party=StupidParty()
        
        connection = MyConn()
        party.connect(connection)
        connection.notifyListeners(settings)
        connection.notifyListeners(YourTurn())
        connection.notifyListeners(ActionDone(emptyoffer))
        connection.notifyListeners(ActionDone(offer))
        connection.notifyListeners(YourTurn())
        party.disconnect()
        
        actions = connection.getActions()
        # 2 yourturns, so there should eb 2 actions
        self.assertEquals(2, len(actions))
        self.assertEquals(emptyoffer, actions[0])
        self.assertEquals(Accept(me, bid), actions[1])




