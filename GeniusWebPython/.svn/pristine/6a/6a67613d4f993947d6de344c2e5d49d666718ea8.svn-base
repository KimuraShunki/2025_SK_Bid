from datetime import datetime
import json
import time
from typing import List
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.actions.Accept import Accept
from geniusweb.actions.Action import Action
from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.deadline.DeadlineTime import DeadlineTime
from geniusweb.issuevalue.Bid import Bid
from geniusweb.progress.ProgressRounds import ProgressRounds
from geniusweb.progress.ProgressTime import ProgressTime
from geniusweb.protocol.NegoState import NegoState
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.partyconnection.ProtocolToPartyConn import ProtocolToPartyConn
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.saop.SAOPSettings import SAOPSettings
from geniusweb.protocol.session.saop.SAOPState import SAOPState
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class SAOPStateTest (unittest.TestCase, GeneralTests[SAOPState]):
	maxDiff =None
	
	NOW = 1000
	party1 = PartyId("party1") 
	party2 = PartyId("party2")
	party3 = PartyId("party3")
	actions1:List[Action]  = []
	action = Mock(Action)
	actions2:List[Action] = [action]

	party1conn = Mock(ProtocolToPartyConn)
	party2conn = Mock(ProtocolToPartyConn)
	party3conn = Mock(ProtocolToPartyConn)

	connections = [party1, party2]
	connections2 = [party1, party3]
	connections3 = [party1, party2, party3]

	progresstime = Mock(ProgressTime)
	progressrounds = Mock(ProgressRounds)
	progressrounds1 = Mock(ProgressRounds)
	settings = Mock(SAOPSettings)

	bid1 = Mock(Bid)
	otherbid = Mock(Bid)
	accept1 = Accept(party1, bid1)
	accept2 = Accept(party2, bid1)
	acceptother = Accept(party2, otherbid)
	offer1 = Offer(party1, bid1)
	endNegotiation1 = EndNegotiation(party1)

	jackson = ObjectMapper()

	serialized = "{\"SAOPState\":{\"actions\":[],\"connections\":[\"party1\",\"party2\"],\"progress\":{\"ProgressTime\":{\"duration\":1000000,\"start\":2000000}},\"settings\":{\"SAOPSettings\":{\"participants\":[{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"party1ref\",\"parameters\":{}},\"profile\":\"prof1\"}]}}],\"deadline\":{\"DeadlineTime\":{\"durationms\":123000}}}},\"partyprofiles\":{},\"error\":null}}"

	party1conn.getParty=Mock(return_value=party1)
	party2conn.getParty=Mock(return_value=party2)
	party3conn.getParty=Mock(return_value=party3)
	# workaround https://github.com/python/mypy/issues/2427
	party1conn.__repr__= Mock(return_value="conn1") #type:ignore 
	party2conn.__repr__=Mock(return_value="conn2") #type:ignore
	party3conn.__repr__=Mock(return_value="conn3") #type:ignore
	action.__repr__=Mock(return_value="act1") #type:ignore

	progresstime.isPastDeadline=Mock(return_value=False) # is default in java
	progressrounds.getTerminationTime=\
		Mock(return_value=datetime.utcfromtimestamp(time.time() + 36000))
	progressrounds1.getTerminationTime=\
		Mock(return_value=datetime.utcfromtimestamp(time.time() + 36000))
	progressrounds.advance=Mock(return_value=progressrounds1)

	state1 = SAOPState(actions1, connections, progresstime, settings)
	state1a = SAOPState(actions1, connections, progresstime, settings)
	state2 = SAOPState(actions2, connections, progresstime, settings)
	state3 = SAOPState(actions1, connections2, progresstime, settings)
	state4 = SAOPState(actions1, connections, progressrounds, settings)

	conns = [party1, party2]
	pwithp = PartyWithParameters(PartyRef(URI("party1ref")), Parameters())
	teams = [PartyWithProfile(pwithp, ProfileRef(URI("prof1")))]
	participants = [ TeamInfo(teams)]
	deadline = DeadlineTime(123000)
	setts = SAOPSettings(participants, deadline)
	state = SAOPState(actions1, conns,
					ProgressTime(1000000, datetime.fromtimestamp(2000000/1000.)), setts)
 	
	def getGeneralTestData(self)->List[List[SAOPState]] :
		return [[self.state1, self.state1a],
				[self.state2], [self.state3],
				[self.state4]]

	def getGeneralTestStrings(self)->List[str] :
		return [
				"SAOPState.*\\[\\].*party1.*party2.*ProgressTime.*",
				"SAOPState.*\\[act1\\].*party1.*party2.*ProgressTime.*",
				"SAOPState.*party1.*party3.*ProgressTime.*",
				"SAOPState.*party1.*party2.*ProgressRounds.*"]

	def constructWith0Connection(self) :
		SAOPState(self.actions1, [], self.progresstime, self.settings, None,
				None)

	def constructWithNoneConnection(self):
		state = SAOPState(self.actions1, None, self.progresstime, self.settings,
				None, None)
		self.assertEqual(0, len(state.getConnections()))

	def testNextActor(self):
		self.assertEqual(self.party1, self.state1._getNextActor())

	def testNextActor2(self):
		conns = [self.party2, self.party3]
		state = SAOPState(self.actions1, conns, self.progresstime, self.settings,
				None, None)
		self.assertEqual(self.party2, state._getNextActor())

	def testNextActorAfterAction(self):
		actions = [self.action]
		state = SAOPState(actions, self.connections, self.progresstime,
				self.settings, None, None)
		self.assertEqual(self.party2, state._getNextActor())

	def testNextActorAfter2Actions(self):
		actions = [self.action, self.action]
		state = SAOPState(actions, self.connections, self.progresstime,
				self.settings, None, None)
		self.assertEqual(self.party1, state._getNextActor())

	def testIsFinal(self):
		self.assertFalse(self.state1.isFinal(self.NOW))
		state = SAOPState(self.actions1, self.connections, self.progresstime,
				self.settings, None, Mock(ProtocolException))
		self.assertTrue(state.isFinal(self.NOW))

	def testWithException(self):
		finalstate1 = self.state1.WithException(Mock(ProtocolException))
		self.assertTrue(finalstate1.isFinal(self.NOW))
		finalstate2 = finalstate1.WithException(Mock(ProtocolException))
		self.assertTrue(finalstate2.isFinal(self.NOW))

	def testIsOfferAgreement1(self):
		actions = [self.offer1]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None)
		self.assertEqual({}, state.getAgreements().getMap())

	def testIsOfferAcceptAgreement(self):
		actions = [self.offer1, self.accept2]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None);
		self.assertEqual({}, state.getAgreements().getMap())

	def testIsOfferAcceptOfferAgreement(self):
		actions = [self.offer1, self.accept1, self.offer1]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None);
		self.assertEqual({},state.getAgreements().getMap())

	def testIsOfferAcceptAcceptAgreement(self) :
		actions = [self.offer1, self.accept1, self.accept2]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None);
		self.assertEquals(self.bid1, state.getAgreements().getMap()[self.party1])
		self.assertTrue(state.isFinal(self.NOW))

	def testIsAcceptOfferAcceptAgreement(self):
		actions = [self.accept1, self.offer1, self.accept2]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None);
		self.assertEqual({},state.getAgreements().getMap())

	def testIsOfferAcceptAcceptotherAgreement(self) :
		actions = [self.offer1, self.accept1, self.acceptother]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None);
		self.assertEqual({},state.getAgreements().getMap())


	def testWithAction(self):
		actn = self.action
		actn.getActor=Mock(return_value=self.party1)
		self.assertRaises(ValueError, lambda:self.state1.WithAction(self.party1, actn))

	def testWithConnection(self):
		state = self.state1.WithParty(self.party3, Mock(PartyWithProfile))
		self.assertEqual(3, len(state.getConnections()))

	def testIsEndNegotiationFinal(self):
		actions = [self.endNegotiation1]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None)
		self.assertEqual({},state.getAgreements().getMap())
		self.assertEqual(None,state.getError())
		self.assertTrue(state.isFinal(self.NOW))

	def testIsProtocolErrorFinal(self):
		state = SAOPState(self.actions1, self.connections3, self.progressrounds,
				self.settings, None,
				ProtocolException("test error", PartyId("test")));
		self.assertTrue(state.isFinal(self.NOW))
		self.assertNotEqual(None, state.getError())

	def testRefuseImmediateAccept(self):
		Noneaccept = Accept(self.party1, None)
		self.assertRaises(ValueError, lambda:self.state1.WithAction(self.party1, Noneaccept))

	def testRefuseNotMyTurn(self):
		actions = [self.offer1]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None)
		self.assertRaises(ValueError, lambda: state.WithAction(self.party1, self.offer1))

	def testRefuseNoneAccept(self):
		actions = [self.offer1]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None);

		Noneaccept = Accept(self.party2, None)
		self.assertRaises(ValueError, lambda:state.WithAction(self.party2, Noneaccept))

	def testRefuseNoneAction(self):
		actions = [self.offer1]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None)
		self.assertRaises(ValueError,  lambda:state.WithAction(self.party2,  None))

	def testCheckGoodAccept(self):
		actions = [self.offer1, self.accept2]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None)

		accept = Accept(self.party3, self.bid1)
		state = state.WithAction(self.party3, accept)
		self.assertTrue(state.isFinal(self.NOW)) 
		self.assertEqual(None,state.getError())
		self.assertEqual(self.bid1, state.getAgreements().getMap().get(self.party1))

	def testCheckGoodSecondAccept(self):
		bid2 = Mock(Bid)
		actions = [self.offer1, Offer(self.party2, bid2),
				Accept(self.party3, bid2)]
		state = SAOPState(actions, self.connections3, self.progressrounds,
				self.settings, None, None)
		accept = Accept(self.party1, bid2)
		state = state.WithAction(self.party1, accept)
		self.assertTrue(state.isFinal(self.NOW));
		self.assertEqual(None,state.getError())
		self.assertEqual(bid2, state.getAgreements().getMap().get(self.party1))

	def testDeserialize(self):
		obj:NegoState = self.jackson.parse(json.loads(self.serialized), NegoState)
		print(obj)
		self.assertEqual(self.state, obj)

	def testSerialize(self):
		jsob = self.jackson.toJson(self.state)
		print(jsob)
		self.assertEqual(json.loads(self.serialized), jsob)
