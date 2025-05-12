from typing import List
import unittest
from unittest.mock import Mock

from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.PartyId import PartyId
from geniusweb.protocol.partyconnection.ProtocolToPartyConn import ProtocolToPartyConn
from geniusweb.protocol.partyconnection.ProtocolToPartyConnections import ProtocolToPartyConnections


class ConnectionWithPartiesTest (unittest.TestCase, GeneralTests[ProtocolToPartyConnections]):
	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")

	con1 = Mock(ProtocolToPartyConn)
	con2 = Mock(ProtocolToPartyConn)
	con3 = Mock(ProtocolToPartyConn)

	conns1 = ProtocolToPartyConnections([con1, con2])
	conns1a = ProtocolToPartyConnections([con1, con2])
	conns2 = ProtocolToPartyConnections([con1, con3])
	conns3 = ProtocolToPartyConnections([con2, con1])
	conns4 = ProtocolToPartyConnections([con2, con1, con3])
	conns5 = ProtocolToPartyConnections([con2, con1, con3, con1])

	con1.__repr__=Mock(return_value="con1") #type:ignore
	con2.__repr__=Mock(return_value="con2") #type:ignore
	con3.__repr__=Mock(return_value="con3")  #type:ignore
	
	con1.getParty=Mock(return_value=party1)
	con2.getParty=Mock(return_value=party2)
	con3.getParty=Mock(return_value=party3)


	def getGeneralTestData(self)->List[List[ProtocolToPartyConnections]] :
		return [[self.conns1, self.conns1a],[self.conns2], [self.conns3],
				[self.conns4]]

	def getGeneralTestStrings(self) -> List[str] : 
		return ["ConnectionWithParties\\[con1, con2\\]",
				"ConnectionWithParties\\[con1, con3\\]",
				"ConnectionWithParties\\[con2, con1\\]",
				"ConnectionWithParties\\[con2, con1, con3\\]"]

	def testGet(self):
		self.assertEqual(self.con1, self.conns1.getConn(0))
		self.assertEqual(self.con3, self.conns4.getConn(2))

	def testGetParty(self):
		self.assertEquals(self.con1, self.conns1.get(self.party1))
		self.assertEquals(self.con1, self.conns4.get(self.party1))
		self.assertEquals(self.con2, self.conns1.get(self.party2))
		self.assertEquals(self.con2, self.conns3.get(self.party2))
		self.assertEquals(self.con2, self.conns4.get(self.party2))
	
	def testGetUnknownParty(self) :
		self.assertEqual(None, self.conns2.get(self.party2))

	def testSize(self):
		self.assertEqual(2, self.conns1.size())
		self.assertEquals(2, self.conns2.size())
		self.assertEquals(2, self.conns3.size())
		self.assertEquals(3, self.conns4.size())

	def testWithParty(self) :
		conns = self.conns3.With(self.con3)
		self.assertEqual(2, self.conns3.size())
		self.assertEqual(3, conns.size())
		self.assertEqual(self.conns4, conns)

	def testWithExistingParty(self):
		self.conns4.With(self.con1);
		# no throw, default this is ok, it should be the protocol testing this.
	
	def testAllUnique(self):
		self.assertTrue(self.conns4.allunique());
		self.assertFalse(self.conns5.allunique());

