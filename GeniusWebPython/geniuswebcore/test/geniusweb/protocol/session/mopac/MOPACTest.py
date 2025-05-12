from datetime import datetime
import json
import time
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from tudelft.utilities.repository.NoResourcesNowException import NoResourcesNowException
from tudelft_utilities_logging.Reporter import Reporter

from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Inform import Inform
from geniusweb.protocol.partyconnection.ProtocolToPartyConn import ProtocolToPartyConn
from geniusweb.protocol.partyconnection.ProtocolToPartyConnFactory import ProtocolToPartyConnFactory
from geniusweb.protocol.session.mopac.MOPAC import MOPAC
from geniusweb.protocol.session.mopac.MOPACSettings import MOPACSettings
from geniusweb.protocol.session.mopac.MOPACState import MOPACState
from geniusweb.protocol.session.mopac.PartyStates import PartyStates
from geniusweb.protocol.session.mopac.phase.OfferPhase import OfferPhase
from geniusweb.protocol.session.mopac.phase.VotingPhase import VotingPhase


class MOPACTest(unittest.TestCase):

	jackson = ObjectMapper()

	PARTY1ID = PartyId("party1")
	PARTY2ID = PartyId("party2")
	PARTY3ID = PartyId("party3")

	# don't try to mock settings, all parts are needed and mocking
	# makes the test unreadable.
	setstr = "{\"MOPACSettings\":{\"participants\":[" +\
			"{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party1\",\"parameters\":{}},\"profile\":\"http://profile1\"}]}}," +\
			"{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party2\",\"parameters\":{}},\"profile\":\"http://profile2\"}]}}," +\
			"{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party3\",\"parameters\":{}},\"profile\":\"http://profile3\"}]}}]," +\
			"\"deadline\":{\"DeadlineTime\":{\"durationms\":100}},\"votingevaluator\":{\"LargestAgreement\":{}}}}"

	
	logger = Mock(Reporter)
	
	factory = Mock(	ProtocolToPartyConnFactory)

	
	def setUp(self):
		self.conn1 = Mock(ProtocolToPartyConn)
		self.conn2 = Mock(ProtocolToPartyConn)
		self.conn3 = Mock(ProtocolToPartyConn)

		self.settings = self.jackson.parse(json.loads(self.setstr), MOPACSettings)
		self.mopac = self.settings.getProtocol(self.logger)

		self.connections = [self.conn1, self.conn2, self.conn3]
		self.factory.connectAll=Mock(return_value=self.connections)

		# hack the state.with(connection) stuff simplistically

		self.conn1.getParty=Mock(return_value=self.PARTY1ID)
		self.conn2.getParty=Mock(return_value=self.PARTY2ID)
		self.conn3.getParty=Mock(return_value=self.PARTY3ID)

	def testSmoke(self):
		pass

	def testGetDescr(self):
		self.assertNotEqual(None, self.mopac.getDescription())

	def testInitialState(self):
		state = self.mopac.getState()
		self.assertEqual(self.settings, state.getSettings())
		self.assertEqual(0, len(state.getActions()))

	def testProtocol(self):
		self.assertEquals("MOPAC", str(self.mopac.getRef().getURI().getPath()))

	def testWorkingCheckDeadline(self):
		self.mopac.start(self.factory)

		self.assertFalse(self.mopac.getState().isFinal(time.time()*1000))
		# we have deadline in 100ms so check
		time.sleep(200/1000)
		self.assertTrue(self.mopac.getState().isFinal(time.time()*1000))

	def testSubscribedToConnections(self):
		self.mopac.start(self.factory)
		
		self.assertEquals(1, self.conn1.addListener.call_count)
		self.assertEquals(1, self.conn2.addListener.call_count)
		self.assertEquals(1, self.conn3.addListener.call_count)
		

	def testActionIsBroadcast(self):
		self.mopac.start(self.factory)
		offer = Mock(Offer)
		self.mopac._actionRequest(self.conn1, offer, 1)

		# 1 time for YourTurn, one time for ActionDone.
		# but filtering ActionDone here (instead of Action) does not work,
		# maybe bug in Mockito?
		
		self.assertEqual( 2, len([call for call in self.conn1.send.call_args_list
			if isinstance(call[0][0], Inform)]))


	#@Test(expected = RuntimeException.class)
	def testPartyFailsConnect(self):
		'''
		Fatal error occurs, run should fail
		'''
		factory1 = Mock(ProtocolToPartyConnFactory)
		# irrecoverable fail test
		def doExc(conn):
			raise ConnectionError("Failed to connect to parties")
		
		factory1.connectAll.side_effect=doExc
	
		self.assertRaises(ConnectionError, lambda:self.mopac.start(factory1))


	callnr=0

	def testPartyFailsConnect2ndtimeOK(self):
		'''
		Nonfatal error occurs, protocol should retry till success
		'''
		now = time.time()*1000
		factory1 = Mock(ProtocolToPartyConnFactory)
		# recoverable fail, and then success.
		
		this=self
		def doExcThenOk(con): 
			if this.callnr==0:
				this.callnr=1
				raise NoResourcesNowException("try again later",
						datetime.fromtimestamp((now + 100)/1000.))
			return this.connections

		factory1.connectAll.side_effect=doExcThenOk
		
		self.mopac.start(factory1)

	def testProceedsNextPhase(self):
		'''
		Test that in Offer phase, and party does action, the next phase is
		entered.
		'''
		# the state before the last party makes the offer
		offerstate = Mock(MOPACState)
		offerstate.getSettings=Mock(return_value=self.settings)
		offerphase = Mock(OfferPhase)
		offerphase.isFinal=Mock(return_value=False)
		offerstate.getPhase=Mock(return_value=offerphase)
		offerstate.__repr__=Mock(return_value="offerstate")

		# the phase where all parties placed an offer
		finalofferphase = Mock(OfferPhase)
		finalofferphase.isFinal=Mock(return_value=True)
		finalofferstate = Mock(MOPACState)
		finalofferstate.getPhase=Mock(return_value=finalofferphase)
		finalofferstate.finishPhase=Mock(return_value=finalofferstate)
		finalofferstate.__repr__=Mock(return_value="finalofferstate")
		
		#ADD
		finalofferstate.isFinal = Mock(return_value=False)

		offerstate.WithAction=Mock(return_value=finalofferstate)

		# the phase where all parties can start voting.
		# this is the state to be reached.
		now = time.time()*1000
		votingstate = Mock(MOPACState)
		votingphase = Mock(VotingPhase)
		votingpartystates = Mock(PartyStates)
		votingpartystates.getNotYetActed=Mock(return_value=set())
		votingphase.getDeadline=Mock(return_value=now + 100)
		votingphase.getPartyStates=Mock(return_value=votingpartystates)
		votingstate.getPhase=Mock(return_value=votingphase)
		votingstate.__repr__=Mock(return_value="voringstate")

		finalofferstate.nextPhase=Mock(return_value=votingstate)

		mopac = MOPAC(offerstate, self.logger)
		action = Mock(Offer)
		mopac._actionRequest(self.conn3, action, now)

		# check that the action result in reaching the voting phase
		self.assertEqual(votingstate, mopac.getState())

