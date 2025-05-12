from collections import OrderedDict
import json
from typing import List, Dict
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests
from uri.uri import URI

from geniusweb.actions.PartyId import PartyId
from geniusweb.inform.Agreements import Agreements
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.Value import Value
from geniusweb.protocol.session.SessionResult import SessionResult
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyRef import PartyRef
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef


class SessionResultTest(unittest.TestCase,  GeneralTests[SessionResult]):
	jackson = ObjectMapper()
	error = ValueError("test");

	ISSUE1 = "issue1";
	jsonstring = "{\"participants\":{\"party2\":{\"party\":{\"partyref\":\"party2\",\"parameters\":{}},\"profile\":\"profile2\"},\"party1\":{\"party\":{\"partyref\":\"party1\",\"parameters\":{}},\"profile\":\"profile1\"}},\"agreements\":{\"party2\":{\"issuevalues\":{\"issue1\":\"a\"}},\"party1\":{\"issuevalues\":{\"issue1\":\"a\"}}},\"penalties\":{\"party2\":0.0,\"party1\":0.0},\"error\":null}";
	nopenalties:Dict[PartyId, float] = {}
	penalties:Dict[PartyId, float]  = {}

	PARTY1 = PartyId("party1")
	PARTY2 = PartyId("party2")
	PARTY3 = PartyId("party3")

	penalties[PARTY1]= 0.1
	penalties[PARTY2]= 0.2
	nopenalties[PARTY1]= 0.
	nopenalties[PARTY2]= 0.

	errorstring = "\"error\":{\"java.lang.RuntimeException\":"\
			+ json.dumps(jackson.toJson(error)) + "}"
	print(errorstring)

	party1 = PartyWithParameters(PartyRef(URI("party1")), Parameters())
	party2 = PartyWithParameters(PartyRef(URI("party2")), Parameters())

	partyprofile1 = PartyWithProfile(party1, ProfileRef(URI("profile1")))
	partyprofile2 = PartyWithProfile(party2, ProfileRef(URI("profile2")))

	issuevalues1:Dict[str, Value] = {}
	issuevalues1[ISSUE1]=DiscreteValue("a")
	bid1 = Bid(issuevalues1)
	agreement1 = Agreements().With(Agreements({PARTY1:bid1, PARTY2:bid1} ))

	# different order but that shouldn't matter
	issuevalues2:Dict[str, Value]  =OrderedDict()
	issuevalues2[ISSUE1]= DiscreteValue("b")
	bid2 = Bid(issuevalues2)
	agreement2 = Agreements().With(Agreements({ PARTY1:bid2, PARTY3:bid2} ))

	partiesmap:Dict[PartyId, PartyWithProfile] = OrderedDict()
	partiesmap[PARTY2]= partyprofile2
	partiesmap[PARTY1]= partyprofile1

	partiesmap2:Dict[PartyId, PartyWithProfile] = OrderedDict()
	partiesmap2[PARTY1]= partyprofile2
	partiesmap2[PARTY3]= partyprofile1

	result1 = SessionResult(partiesmap, agreement1, nopenalties, None) 
	result1a = SessionResult(partiesmap, agreement1, nopenalties, None)
	result2 = SessionResult(partiesmap, agreement2, nopenalties, None)
	result3 = SessionResult(partiesmap2, agreement1, nopenalties, None)
	result4 = SessionResult(partiesmap2, agreement1, penalties, None)

	# IGNORE ERROR for now, it fails somewhere deep in maven suddenly.
	# result4 = new SessionResult(Arrays.asList(partyprofile1,
	# partyprofile2), bid1, error);

	def getGeneralTestData(self) ->List[List[SessionResult]]: 
		return [[self.result1, self.result1a],
				[self.result2], [self.result3],
				[self.result4]]

	def  getGeneralTestStrings(self) -> List[str]:
		return [
				"SessionResult.*party2.*profile2.*,.*party1.*profile1.*Agreements.*Bid.*issue1=\"a\".*0\\.0.*0\\.0.*None.*",
				"SessionResult.*party2.*profile2.*,.*party1.*profile1.*Agreements.*Bid.*issue1=\"b\".*0\\.0.*0\\.0.*None.*",
				"SessionResult.*party1.*profile2.*,.*party3.*profile1.*Agreements.*Bid.*issue1=\"a\".*0\\.0.*0\\.0.*None.*",
				"SessionResult.*party1.*profile2.*,.*party3.*profile1.*Agreements.*Bid.*issue1=\"a\".*party1.*0\\.1.*party2.*0\\.2.*None.*"
				]

	def serializeTest(self) :
		print(self.jackson.toJson(self.result1))
		self.assertEqual(json.loads(self.jsonstring), self.jackson.toJson(self.result1))

	def deserializeTest(self):
		act = self.jackson.parse(json.loads(self.jsonstring), SessionResult)
		self.assertEqual(self.result1, act)

