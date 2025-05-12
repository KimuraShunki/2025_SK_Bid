from typing import List
import unittest
from unittest.mock import Mock

from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.Action import Action
from geniusweb.actions.PartyId import PartyId
from geniusweb.progress.ProgressTime import ProgressTime
from geniusweb.protocol.CurrentNegoState import CurrentNegoState
from geniusweb.protocol.session.saop.SAOPSettings import SAOPSettings
from geniusweb.protocol.session.saop.SAOPState import SAOPState


class CurrentNegoStateTest (unittest.TestCase,GeneralTests[CurrentNegoState]):
    party1 = PartyId("party1")
    party2 = PartyId("party2")
    actions1:List[Action] = []

    connections = [party1]
    connections2 = [party1, party2]

    progresstime = Mock(ProgressTime)
    settings = Mock(SAOPSettings)

    saop1 = SAOPState(actions1, connections2, progresstime,
            settings)
    saop2 = SAOPState(actions1, connections, progresstime,
            settings)

    state1 = CurrentNegoState(saop1, 1234)
    state1a = CurrentNegoState(saop1,1234)
    state2 = CurrentNegoState(saop2,1234)

    def getGeneralTestData(self)->List[List[CurrentNegoState]] :
        return [[self.state1, self.state1a],[self.state2]]

    def getGeneralTestStrings(self)->List[str] :
        return [
                "CurrentNegoState.*1234.*SAOPState.*party1.*party2.*ProgressTime.*SAOPSettings.*",
                "CurrentNegoState.*1234.*SAOPState.*party1.*ProgressTime.*SAOPSettings.*"]

