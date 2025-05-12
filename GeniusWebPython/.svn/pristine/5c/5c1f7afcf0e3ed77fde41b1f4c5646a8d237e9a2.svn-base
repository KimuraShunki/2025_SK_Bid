from datetime import datetime, timedelta
import time
import unittest
from unittest.mock import Mock

from tudelft.utilities.listener.Listener import Listener
from tudelft.utilities.repository.NoResourcesNowException import NoResourcesNowException
from tudelft_utilities_logging.ReportToLogger import ReportToLogger
from uri.uri import URI

from geniusweb.actions.Accept import Accept
from geniusweb.actions.Action import Action
from geniusweb.actions.EndNegotiation import EndNegotiation
from geniusweb.actions.Offer import Offer
from geniusweb.actions.PartyId import PartyId
from geniusweb.deadline.Deadline import Deadline
from geniusweb.deadline.DeadlineTime import DeadlineTime
from geniusweb.events.CurrentState import CurrentState
from geniusweb.inform.ActionDone import ActionDone
from geniusweb.inform.Agreements import Agreements
from geniusweb.inform.Finished import Finished
from geniusweb.inform.Inform import Inform
from geniusweb.inform.Settings import Settings
from geniusweb.inform.YourTurn import YourTurn
from geniusweb.progress.Progress import Progress
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.partyconnection.ProtocolToPartyConn import ProtocolToPartyConn
from geniusweb.protocol.partyconnection.ProtocolToPartyConnFactory import ProtocolToPartyConnFactory
from geniusweb.protocol.partyconnection.ProtocolToPartyConnections import ProtocolToPartyConnections
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.saop.SAOP import SAOP
from geniusweb.protocol.session.saop.SAOPSettings import SAOPSettings
from geniusweb.protocol.session.saop.SAOPState import SAOPState
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef
from geniusweb.references.ProtocolRef import ProtocolRef


class SAOPTest(unittest.TestCase): 
	'''
	This test tests inner workings of the SAOP protocol, AKA 'white box' testing.
	This adds brittleness to this test, because these internal workings may be
	modified as long as the public API remains working. This approach was
	necessary because fully testing the public API directly would lead to
	excessive amounts of Mocking and unfocused tests. (with "focused test" we
	mean that a junit test should test a small part of the code and thus aid in
	locating the actual issue).
	'''
	PARTY2ID = PartyId("party2")
	PARTY1ID = PartyId("party1")
	parameters = Parameters()
	SAOPPROTOCOL = ProtocolRef(URI("SAOP"))

	NOW = 1000
	DEADLINE =1000
	party1ref = PartyRef(URI("party1"))
	party2ref = PartyRef(URI("party2"))
	partywithparam1 = PartyWithParameters(party1ref, parameters)
	partywithparam2 = PartyWithParameters(party2ref, parameters)


	def setUp(self):
		self.state = Mock(SAOPState)
		self.connectedstate = Mock(SAOPState)
		self.failstate = Mock(SAOPState)
		self.finalstate = Mock(SAOPState)
	
		self.settings = Mock(SAOPSettings)
		self.team1 = Mock(TeamInfo)
		self.team2 = Mock(TeamInfo)
		self.conn1 = Mock(ProtocolToPartyConn)
		self.conn2 = Mock(ProtocolToPartyConn);
		self.progress = Mock(Progress)
		self.testlistener = Mock(Listener)
		
		self.deadlinetime = Mock(DeadlineTime)


		self.profile1 = Mock(ProfileRef)
		self.profile2 = Mock(ProfileRef)

		pwp1 = PartyWithProfile(self.partywithparam1, self.profile1);
		pwp2 = PartyWithProfile(self.partywithparam2, self.profile2);
		self.team1.getParties=Mock(return_value=[pwp1])
		self.team2.getParties=Mock(return_value=[pwp2])

		partyprofiles = {}
		partyprofiles[self.PARTY1ID]= self.team1
		partyprofiles[self.PARTY2ID]= self.team2
		
		
		self.pwpmap = {}
		self.pwpmap[self.PARTY1ID]=pwp1
		self.pwpmap[self.PARTY2ID]=pwp2
		self.deadlinetime.getDuration=Mock(return_value=self.DEADLINE)

		teams = []
		teams.append(self.team1);
		teams.append(self.team2);
		self.settings.getTeams=Mock(return_value=teams)
		self.settings.getAllParties=Mock(return_value=[pwp1, pwp2])
		self.settings.getDeadline=Mock(return_value=self.deadlinetime)

		self.factory = Mock(ProtocolToPartyConnFactory)
		# connections = Mock(List);
		connections = [self.conn1, self.conn2]
		self.factory.connectAll=Mock(return_value=connections)

		# hack the state.with(connection) stuff simplistically

		self.conn1.getParty=Mock(return_value=self.PARTY1ID)
		self.conn2.getParty=Mock(return_value=self.PARTY2ID)

		self.MockState(self.connectedstate, "connected state", True)
		self.MockState(self.state, "running state",True);
		
		self.MockState(self.finalstate, "final state",True);
		self.finalstate.isFinal=Mock(return_value=True)
		self.MockState(self.failstate, "fail state", True);
		self.failstate.isFinal=Mock(return_value=True)

		self.connectionswithparties = ProtocolToPartyConnections([self.conn1, self.conn2])

		# HACK thenReturn twice, so that 2nd call to iterator() returns new
		# iterator instead of the old one
		profilesmap = {}
		profilesmap[self.PARTY1ID]= pwp1
		profilesmap[self.PARTY2ID]= pwp2
		self.state.getPartyProfiles=Mock(return_value=profilesmap)

		self.saop = SAOP(self.state, ReportToLogger("test"),
				self.connectionswithparties)
		self.saop.addListener(self.testlistener)


	def MockState(self, state:SAOPState , asText:str, isConnected:bool ) :
		'''
		All states are more or less the same, but are slightly modified
		
		@param state  the state to Mock (must be already
		@param asText short name for the state, for debugging
		@param bool true if parties are connected
		'''
		state.getSettings=Mock(return_value=self.settings) #type:ignore
		if isConnected:
			state.getConnections=Mock(return_value=[self.PARTY1ID, self.PARTY2ID])   #type:ignore
		else:
			state.getConnections=Mock(return_value=[]) #type:ignore
		# when(state.getConnections()).thenReturn(connectionswithparties);

		state.getProgress=Mock(return_value=self.progress)  #type:ignore
		state.WithParty=Mock(return_value=self.connectedstate)  #type:ignore
		state._getNextActor=Mock(return_value=self.PARTY1ID)  #type:ignore
		state.WithAction= Mock(side_effect=lambda pid, act: #type:ignore
				self.finalstate if isinstance(act, EndNegotiation) else\
				state )
					
		state.WithProgress=Mock(return_value=state)  #type:ignore
		state.__repr__=Mock(return_value=asText)  #type:ignore
		state.WithException=Mock(return_value=self.failstate)  #type:ignore
		state.getAgreements=Mock(return_value=Agreements())  #type:ignore

		#explicit default. This differs from Java, where default bools to false
		state.isFinal=Mock(return_value=False)	#type:ignore
		state.getPartyProfiles = Mock(return_value=self.pwpmap) #type:ignore

	def testConstructor(self):
		state1 = Mock(SAOPState)
		dl = Mock(Deadline)
		set = Mock(SAOPSettings)
		state1.getSettings=Mock(return_value=set)
		set.getDeadline=Mock(return_value=dl)
		dl.getDuration=Mock(return_value=1000)
		SAOP(state1, ReportToLogger("test"), self.connectionswithparties)
		self.assertEqual([], self.state.WithException.call_args_list)
		self.assertEqual([], self. testlistener.notifyChange.call_args_list)


	def testConnect(self):
		self.saop._connect(self.factory)

		self.assertEqual(self.connectedstate, self.saop.getState())
		self.assertEqual([], self.state.WithException.call_args_list)
		self.assertEqual([], self.testlistener.notifyChange.call_args_list)
	

	def testConnectFailingConnection(self):
		# override the factory connect to throw IOException. This exception
		# should boil up and cause the connect to fail.
		def __raise(refs):
			raise ConnectionError("Refusing connection")
		self.factory.connectAll=Mock(side_effect=__raise)
		this=self
		self.assertRaises(ConnectionError, lambda:this.saop._connect(this.factory))
		# following was never reached?
		#verify(state, times(0)).with(any(ProtocolException));
		#verify(testlistener, times(0)).notifyChange(any(CurrentState));

	def testConnectRetry(self):
		# override the factory connect to throw NoResourcesNowException and
		# then succeed 2nd time.
		this=self
		
		firsttime=True
		def __throwsThenSucceeds():
			if firsttime:
				firsttime=False
				raise NoResourcesNowException("Refusing connection",\
						datetime.now() + timedelta(seconds=0.5))
			return this.connections
		self.factory.connect=Mock(side_effect=__throwsThenSucceeds)
		
		self.saop._connect(self.factory)

		self.assertEqual(self.connectedstate, self.saop.getState())
		#verify(state, times(0)).with(any(ProtocolException));
		self.assertEqual([],  [e \
			for e in self.state.WithException.call_args_list\
			if not isinstance( e,ProtocolException)])
		self.assertEqual([],self.testlistener.notifyChange.call_args_list) 

	def  testSetup(self) :
		self.saop._setupParties()

		# were the connections attached properly?
		self.assertEqual(1, len(self.conn1.addListener.call_args_list))
		self.assertEqual(1, len(self.conn2.addListener.call_args_list))

		# were the settings send to each party?
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list \
							if isinstance(call[0][0],Settings)]))
		self.assertEqual(
				Settings(self.PARTY1ID, self.profile1, self.SAOPPROTOCOL, self.progress, self.parameters),
				self.conn1.send.call_args_list[0][0][0])

		self.assertEqual(1, len([call for call in self.conn2.send.call_args_list \
							if isinstance(call[0][0],Settings)]))
		self.assertEqual(
				Settings(self.PARTY2ID, self.profile2, self.SAOPPROTOCOL, self.progress, self.parameters),
				self.conn2.send.call_args_list[0][0][0])
				
		self.assertEqual([], self.state.WithException.call_args_list)
		self.assertEqual([], [v for v in self.testlistener.notifyChange.call_args_list if isinstance(v, CurrentState)])
		

	def testActionRequestWrongActor(self):
		self.saop._actionRequest(self.conn2, Mock(EndNegotiation))
		self.assertEqual(1, len([call for call in self.state.WithException.call_args_list\
								 if isinstance(call[0][0], ProtocolException) ]))
		self.assertEqual(1, len([call for call in self.testlistener.notifyChange.call_args_list
							if isinstance(call[0][0], CurrentState)]))

	def testActionRequest(self):
		self.saop._nextTurn()

		self.state._getNextActor=Mock(return_value=self.PARTY1ID)
		self.state.withAction = Mock(return_value=self.finalstate)

		self.saop._actionRequest(self.conn1, Mock(EndNegotiation))

		self.assertEqual([] , [call for call in self.state.WithException.call_args_list
						if isinstance(call[0][0], ProtocolException)])
		#verify(state, times(1)).with(eq(PARTY1ID), any(EndNegotiation));
		self.assertEqual(1, len([call for call in self.state.WithAction.call_args_list
				if call[0][0]==self.PARTY1ID and\
				isinstance(call[0][1], EndNegotiation)]))
		# verify broadcast
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list
				if isinstance(call[0][0], ActionDone)]))
		self.assertEqual(1, len([call for call in self.conn2.send.call_args_list
				if isinstance(call[0][0], ActionDone)]))

		# state.getNextActor() is frozen to PARTY1 by our Mocking
		#verify(conn1, times(1)).send(isA(YourTurn));
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list
				if isinstance(call[0][0], YourTurn)]))
		#verify(conn2, times(0)).send(isA(YourTurn));
		self.assertEqual(0, len([call for call in self.conn2.send.call_args_list
				if isinstance(call[0][0], YourTurn)]))
		#listener should be informed about final state.
		#verify(testlistener, times(0)).notifyChange(any(CurrentState));
		self.assertEqual(1, len([call for call in self.testlistener.notifyChange.call_args_list
				if isinstance(call[0][0], CurrentState)]))
		
	def  testFinalActionRequest(self):
		this=self
		#FIXME double mock??
		#self.state.getNextActor=Mock(return_value=self.PARTY1ID)
		def __nextstate(pid:PartyId, act:Action):
			if isinstance(act, EndNegotiation):
				return this.finalstate

		self.state.withAction=Mock(side_effect=__nextstate)
		# when(finalstate.getAgreements()).thenReturn(Mock(Agreements));

		self.saop._nextTurn() # ensure we send YourTurn to party1.
		self.saop._actionRequest(self.conn1, Mock(EndNegotiation))

		#verify(state, times(0)).with(any(ProtocolException));
		self.assertEqual([], [call for call in self.state.WithException.call_args_list
					if isinstance(call[0][0], ProtocolException)	])
		#verify(state, times(1)).with(eq(PARTY1ID), any(EndNegotiation));
		self.assertEqual(1, len([call for call in self.state.WithAction.call_args_list\
					if isinstance(call[0][1], EndNegotiation)]))
		
		# verify broadcast
		#erify(conn1, times(1)).send(isA(Finished));
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list
			if isinstance(call[0][0], Finished)]))

		#verify(conn2, times(1)).send(isA(Finished));
		self.assertEqual(1, len([call for call in self.conn2.send.call_args_list
			if isinstance(call[0][0], Finished)]))

		#verify(testlistener, times(1)).notifyChange(any(CurrentState));
		self.assertEqual(1, len([call for call in self.testlistener.notifyChange.call_args_list
			if isinstance(call[0][0], CurrentState)]))

		#verify(conn1, times(1)).send(isA(YourTurn));
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list
			if isinstance(call[0][0], YourTurn)]))
		#verify(conn2, times(0)).send(isA(YourTurn));
		self.assertEqual( [] , [call for call in self.conn2.send.call_args_list
			if isinstance(call[0][0], YourTurn)])

	def testStart(self):
		self.saop.start(self.factory)

	def testActionFailNextYourturn(self):
		this=self
		def __throwExc(inf:Inform):
			if isinstance(inf, YourTurn):
				raise ConnectionError("fail sending yourturn")
		self.conn1.send=Mock(side_effect=__throwExc)
		# CHECK is the state really final after an exception?
		self.state.WithException=Mock(return_value=this.finalstate)
		# when(state.getAgreements()).thenReturn(Mock(Agreements));
		self.saop._actionRequest(self.conn1, Mock(Accept))

		
		#verify(state, times(1)).with(any(ProtocolException));
		self.assertEqual( 1, len([call for call in self.state.WithException.call_args_list
					if isinstance(call[0][0], ProtocolException)	]))
		#verify(testlistener, times(1)).notifyChange(any(CurrentState));
		self.assertEqual(1, len([call for call in self.testlistener.notifyChange.call_args_list
				if isinstance(call[0][0], CurrentState)]))

	def testActionNotTheTurn(self) :
		def __throwExc(inf:Inform):
			if isinstance(inf, YourTurn):
				raise ConnectionError("fail sending yourturn")
		self.conn1.send=Mock(side_effect=__throwExc)

		# when(failstate.getAgreements()).thenReturn(Mock(Agreements));
		# not turn of conn2.
		self.saop._actionRequest(self.conn2, Mock(EndNegotiation))

		#verify(state, times(1)).with(any(ProtocolException));
		self.assertEqual( 1, len([call for call in self.state.WithException.call_args_list
			if isinstance(call[0][0], ProtocolException)	]))
		#verify(testlistener, times(1)).notifyChange(any(CurrentState));
		self.assertEqual(1, len([call for call in self.testlistener.notifyChange.call_args_list
				if isinstance(call[0][0], CurrentState)]))


	def testActionInFinalState(self):
		saop = SAOP(self.finalstate, ReportToLogger("test"),
				self.connectionswithparties);
		# when(finalstate.getAgreements()).thenReturn(Mock(Agreements));

		saop._actionRequest(self.conn1, Mock(Offer))

		#verify(finalstate, times(0)).with(any(ProtocolException));
		self.assertEqual( [], [call for call in self.state.WithException.call_args_list
			if isinstance(call[0][0], ProtocolException)	])
		#verify(testlistener, times(0)).notifyChange(any());
		self.assertEqual([], self.testlistener.notifyChange.call_args_list)

	def testDescription(self):
		self.assertNotEquals(None,self.saop.getDescription())

	def testAddParticipant(self):
		self.assertRaises(ValueError, lambda:self.saop.addParticipant(None))
		
	def testDeadlineTimer(self):
		unconnectedstate = Mock(SAOPState)
		self.MockState(unconnectedstate, "unconnected state", False)
		saopempty = SAOP(unconnectedstate, ReportToLogger("test"),
				ProtocolToPartyConnections([]))
		saopempty.addListener(self.testlistener)

		saopempty.start(self.factory);
		# verify(testlistener, times(0)).notifyChange(any(CurrentState.class));
		self.assertEqual([], [call for call in self.testlistener.notifyChange.call_args_list
 			if isinstance(call[0][0], CurrentState)	])

		#verify(conn1, times(1)).send(isA(YourTurn.class));
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list
			if isinstance(call[0][0], YourTurn)]))
		time.sleep( (self.DEADLINE + SAOP._TIME_MARGIN + 100)/1000.)
		#verify(testlistener, times(1)).notifyChange(any(CurrentState.class));
		self.assertEqual(1, len([call for call in self.testlistener.notifyChange.call_args_list
			if isinstance(call[0][0], CurrentState)]))
		#verify(conn1, times(1)).send(isA(Finished.class));
		self.assertEqual(1, len([call for call in self.conn1.send.call_args_list
			if isinstance(call[0][0], Finished)]))


