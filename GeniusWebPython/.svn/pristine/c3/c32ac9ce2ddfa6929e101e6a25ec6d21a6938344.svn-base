import json
from typing import List, Dict
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Agreements import Agreements
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.session.mopac.PartyStates import PartyStates


class PartyStatesTest (unittest.TestCase, GeneralTests[PartyStates]):
	jackson = ObjectMapper()

	party1 = PartyId("party1")
	party2 = PartyId("party2")
	party3 = PartyId("party3")

	powers:Dict[PartyId, int]  = {}
	serialized = "{\"notYetActed\":[\"party2\",\"party1\",\"party3\"],\"actions\":[],\"agreements\":{},\"walkedAway\":[],\"exceptions\":{},\"powers\":{\"party2\":3,\"party1\":2,\"party3\":3}}";


	powers[party1]= 2
	powers[party2]=3
	states2 = PartyStates(powers)
	powers[party3]= 3
	states1 = PartyStates(powers)
	states1a = PartyStates(powers)

	def getGeneralTestData(self)->List[List[PartyStates]] :
		return [[self.states1, self.states1a],
				[self.states2]]

	def getGeneralTestStrings(self)->List[str] :
		return [
				"PartyStates.*\\[party., party., party.\\],\\[\\],Agreements\\{\\},\\[\\],\\{\\}.*",
				"PartyStates.*\\[party., party.\\],\\[\\],Agreements\\{\\},\\[\\],\\{\\}.*"]

	def testBasics(self):
		self.assertEqual(self.powers.keys(), self.states1.getNegotiatingParties())
		self.assertEqual(self.powers.keys(), self.states1.getNotYetActed());
		self.assertEqual(0, len(self.states1.getExceptions()))

	def  testException(self):
		newstates = self.states1\
			.WithException(ProtocolException("bla", self.party1))
		self.assertEqual(Agreements(), newstates.getAgreements())
		self.assertEqual(self.powers.keys(), self.states1.getNegotiatingParties())
		self.assertEqual(set([self.party2, self.party3]),
				newstates.getNotYetActed())

	def testFinish(self):
		newstates = self.states1.finish()
		self.assertEqual(Agreements(), newstates.getAgreements())
		self.assertEqual(self.powers.keys(), self.states1.getNegotiatingParties())
		self.assertEqual(set(), newstates.getNotYetActed())

	def testDeserialize(self):
		obj = self.jackson.parse(json.loads(self.serialized), PartyStates)
		print(obj)
		self.assertEqual(self.states1, obj)

	def testSerialize(self):
		jsonobj = self.jackson.toJson(self.states1)
		print(jsonobj);
		jsonloads=json.loads(self.serialized)
		# BRUTE HACK workaround set ordering
		jsonloads['notYetActed']=jsonobj['notYetActed']
		self.assertEqual(jsonloads, jsonobj)

	def testWalkAway(self):
		walkawaystate = self.states1.WithWalkAway(self.party2)
		self.assertEqual(set([self.party1, self.party3]),
				walkawaystate.getNotYetActed())
		self.assertEqual([self.party2], walkawaystate.getWalkedAway())
