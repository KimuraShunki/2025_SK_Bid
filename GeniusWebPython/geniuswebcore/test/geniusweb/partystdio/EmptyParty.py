import json
import logging
import sys
from typing import cast, Optional, List

from tudelft_utilities_logging.Reporter import Reporter 

from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Inform import Inform
from geniusweb.issuevalue.Bid import Bid 
from geniusweb.party.Capabilities import Capabilities
from geniusweb.party.DefaultParty import DefaultParty


class EmptyParty (DefaultParty):
    """
    A empty party just for testing PartyStdio.
    """
    def __init__(self, reporter:Reporter):
        super().__init__(reporter)
        self.getReporter().log(logging.INFO,"party is initialized")
        self._lastReceivedBid:Optional[Bid] = None
        self.received:List[Inform]=[]

    # Override
    def notifyChange(self, info: Inform):
        self.getReporter().log(logging.INFO,"received info:"+str(info))
        self.received.append(info)
        self.send(EndNegotiation(PartyId('someone')))

    # Override
    def getCapabilities(self): # -> Capabilities
        return Capabilities( set([ "SAOP"]), set(['geniusweb.profile.utilityspace.LinearAdditive']))

    # Override
    def getDescription(self):
        return "test description"

    # Override
    def terminate(self):
        super().terminate()

