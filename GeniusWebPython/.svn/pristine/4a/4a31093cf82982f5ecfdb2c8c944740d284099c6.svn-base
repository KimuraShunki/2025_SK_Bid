import unittest
from unittest.mock import Mock
from geniusweb.actions.PartyId import PartyId
from pyson.ObjectMapper import ObjectMapper
from geniusweb.references.ProtocolRef import ProtocolRef
from geniusweb.progress.ProgressRounds import ProgressRounds
from geniusweb.references.Parameters import Parameters
from test.TestConnection import TestConnection
from timedependentparty.TimeDependentParty import TimeDependentParty
from uri.uri import URI
from geniusweb.references.ProfileRef import ProfileRef
from geniusweb.inform.Settings import Settings
from pathlib import Path
from geniusweb.profile.utilityspace.LinearAdditiveUtilitySpace import LinearAdditiveUtilitySpace
import json
from geniusweb.inform.ActionDone import ActionDone
from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.inform.YourTurn import YourTurn
from geniusweb.actions.Offer import Offer
from geniusweb.actions.Accept import Accept
from tudelft_utilities_logging.Reporter import Reporter
from geniusweb.inform.Agreements import Agreements
from geniusweb.inform.Finished import Finished
import logging
from decimal import Decimal
from geniusweb.bidspace.AllBidsList import AllBidsList
import time
from geniusweb.issuevalue.Bid import Bid

class TimeDependentPartyTest (unittest.TestCase):
	otherparty = PartyId("other")
	SAOP="SAOP"
	PROFILE = "test/resources/testprofile.json"
	jackson = ObjectMapper()

	protocol = ProtocolRef(URI("SAOP"))

	def setUp(self) :
		self.connection = TestConnection()
		self.progress = Mock(ProgressRounds)
		self.progress.get=Mock(return_value=0)
		self.parameters =  Parameters()
		class MyTimeDependentParty(TimeDependentParty):
			#Override
			def getDescription(self) ->str:
				return "test"

			#Override
			def getE(self) ->float:
				return 2 # conceder-like
		
		self.party = MyTimeDependentParty()

		self.settings = Settings(PartyId("party1"),
				ProfileRef(URI("file:" + self.PROFILE)), self.protocol, self.progress,
				self.parameters)

		serialized = Path(self.PROFILE).read_text("utf-8")
		self.profile = self.jackson.parse(json.loads(serialized), LinearAdditiveUtilitySpace)


	def testsmokeTest(self):
		pass

	def  testgetDescriptionTest(self):
		self.assertNotEquals(None, self.party.getDescription())

	def testgetCapabilitiesTest(self):
		capabilities = self.party.getCapabilities()
		self.assertFalse(capabilities.getBehaviours()==set(),
				"party does not define protocols")

	def testInformConnection(self):
		self.party.connect(self.connection)
		# Party should not start acting just after an inform
		self.assertEqual(0, len(self.connection.getActions()))

	def testInformSettings(self):
		self.party.connect(self.connection)
		self.connection.notifyListeners(self.settings)
		self.assertEqual(0, len(self.connection.getActions()))

	def testInformAndConnection(self):
		self.party.connect(self.connection)
		self.party.notifyChange(self.settings)
		self.assertEqual(0, len(self.connection.getActions()))

	def testOtherWalksAway(self):
		self.party.connect(self.connection)
		self.party.notifyChange(self.settings)

		self.party.notifyChange(ActionDone(EndNegotiation(self.otherparty)))

		# party should not act at this point
		self.assertEqual(0, len(self.connection.getActions()))

	def testPartyHasFirstTurn(self):
		self.party.connect(self.connection)
		self.party.notifyChange(self.settings)

		self.party.notifyChange(YourTurn())
		self.assertEqual(1, len(self.connection.getActions()))
		self.assertTrue(isinstance(self.connection.getActions()[0], Offer))

	def testPartyAccepts(self):
		self.party.connect(self.connection)
		self.party.notifyChange(self.settings)

		bid = self._findBestBid()
		self.party.notifyChange(ActionDone(Offer(self.otherparty, bid)))
		self.party.notifyChange(YourTurn())
		self.assertEqual(1, len(self.connection.getActions()))
		self.assertTrue(isinstance(self.connection.getActions()[0], Accept))

	def testPartyLogsFinal(self):
		# this log output is optional, this is to show how to check log
		reporter = Mock(Reporter)
		class MyTimeDependentParty(TimeDependentParty):
			def __init__(self, reporter:Reporter):
				super().__init__(reporter)
			#Override
			def getDescription(self) ->str:
				return "test"

			#Override
			def getE(self) ->float:
				return 2 # conceder-like
		

		pty = MyTimeDependentParty(reporter) 
		pty.connect(self.connection)
		pty.notifyChange(self.settings)
		agreements = Mock(Agreements)
		agreements.__str__=Mock(return_value="agree");
		pty.notifyChange(Finished(agreements))
		unittest.mock._Call

		reporter_call_strings = [ a.args[1] for a in reporter.log.call_args_list]
		self.assertTrue( "Final ourcome:Finished[agree]" in reporter_call_strings)

	#Test
	def testPartysUpdatesProgress(self):
		self.party.connect(self.connection)
		self.party.notifyChange(self.settings)

		self.party.notifyChange(YourTurn())
		self.assertTrue( len(self.progress.advance.call_args_list) >0 )

	def testGetCapabilities(self):
		saop=self.SAOP # PYTHON BUG? Why can't I use this directly in assert??
		self.assertTrue(saop in self.party.getCapabilities().getBehaviours())

	def testUtilityTarget(self):
		tdp = TimeDependentParty()
		N02 = Decimal("0.2")
		N043 =Decimal("0.42521212")
		goal = tdp._getUtilityGoal(0.1, 1.2, N02, N043)
		self.assertTrue(goal> N02)
		self.assertTrue(goal<N043)

	def _findBestBid(self)->Bid:
		bestvalue = Decimal(0)
		best = None
		for bid in AllBidsList(self.profile.getDomain()):
			util = self.profile.getUtility(bid)
			if util>bestvalue:
				best = bid
				bestvalue = util
		return best #type:ignore

	def testPartyAcceptsWithDelay(self):
		'''
		Check that delay indeed waits
		
		@throws URISyntaxException
		'''
		self.party.connect(self.connection)

		settingsdelay = Settings(PartyId("party1"),
				 ProfileRef(URI("file:" + self.PROFILE)), self.protocol, self.progress,
				self.parameters.With("delay", 2))

		self.party.notifyChange(settingsdelay);

		bid = self._findBestBid()
		self.party.notifyChange(ActionDone(Offer(self.otherparty, bid)))
		start = round(time.time()*1000)
		self.party.notifyChange( YourTurn())
		end = round(time.time()*1000)
		self.assertEqual(1, len(self.connection.getActions()))
		self.assertTrue(isinstance(self.connection.getActions()[0] , Accept))

		dt = end - start
		self.assertTrue(dt >= 1000)
		self.assertTrue(dt <= 3000)

