import time
import unittest

from uri.uri import URI

from geniusweb.references.PartyRef import PartyRef
from geniusweb.simplerunner.ClassPathConnectionFactory import ClassPathConnectionFactory, \
	ConnectionPair


class ClassPathConnectionFactoryTest(unittest.TestCase):
	factory=ClassPathConnectionFactory()
	PARTYREF = PartyRef(URI("pythonpath:test.testparty.TestParty.TestParty"))


	def testWrongURI(self): 
		self.assertRaises(ValueError, 
				lambda:self.factory.connect(PartyRef(URI("http://blabla"))))


	def testNullPath(self):
		# bad because classpath should not start with //
		self.assertRaises(ValueError, lambda:self.factory.connect(PartyRef(URI(
			"pythonpath://some.class.path"))))

	def testUnknownParty(self):
		self.assertRaises(ValueError, lambda:self.factory.connect(PartyRef(URI(
			"pythonpath:blabla.bla"))))

	def testParty(self) :
		conn = self.factory.connect(self.PARTYREF)
		self.assertIsNotNone(conn)
		conn.close()

	def testConnectionPairProtocolClosesNormally(self):
		cpair = ConnectionPair(self.PARTYREF);
		self.assertEquals(2, len(cpair.getOpenConnections()))
		cpair.getProtocolToPartyConn().close()
		time.sleep(0.1)
		self.assertEqual(0, len(cpair.getOpenConnections()))
			
	def testConnectionPairProtocolClosesWithExc(self):
		cpair = ConnectionPair(self.PARTYREF)
		self.assertEqual(2, len(cpair.getOpenConnections()))
		cpair.getProtocolToPartyConn().setError(ValueError("test"))
		time.sleep(0.1)
		self.assertEqual(0, len(cpair.getOpenConnections()))

	def testConnectionPairPartyClosesNormally(self):
		cpair = ConnectionPair(self.PARTYREF)
		self.assertEqual(2, len(cpair.getOpenConnections()))
		cpair._getPartyToProtocolConn().close()
		time.sleep(0.1)

		self.assertEqual(0, len(cpair.getOpenConnections()))

	def testConnectionPairPartyClosesWithExc(self):
		cpair = ConnectionPair(self.PARTYREF)
		self.assertEqual(2, len(cpair.getOpenConnections()))
		cpair._getPartyToProtocolConn().setError(ValueError("test"))
		time.sleep(0.1)
		self.assertEqual(0, len(cpair.getOpenConnections()))
			