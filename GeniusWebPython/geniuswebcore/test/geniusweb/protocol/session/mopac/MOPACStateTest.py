from datetime import datetime
import json
from typing import List
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.actions.Action import Action
from geniusweb.actions.PartyId import PartyId
from geniusweb.progress.Progress import Progress
from geniusweb.progress.ProgressTime import ProgressTime
from geniusweb.protocol.ProtocolException import ProtocolException
from geniusweb.protocol.session.TeamInfo import TeamInfo
from geniusweb.protocol.session.mopac.MOPACSettings import MOPACSettings
from geniusweb.protocol.session.mopac.MOPACState import MOPACState
from geniusweb.protocol.session.mopac.PartyStates import PartyStates
from geniusweb.protocol.session.mopac.phase.OfferPhase import OfferPhase
from geniusweb.protocol.session.mopac.phase.Phase import PHASE_MAXTIME, Phase, \
	PHASE_MINTIME
from geniusweb.references.Parameters import Parameters
from geniusweb.references.PartyWithParameters import PartyWithParameters
from geniusweb.references.PartyWithProfile import PartyWithProfile
from geniusweb.references.ProfileRef import ProfileRef
from geniusweb.voting.votingevaluators.LargestAgreement import LargestAgreement


class MOPACStateTest (unittest.TestCase, GeneralTests[MOPACState]):
	maxDiff=None
	
	NOW = datetime.fromtimestamp(1001/1000.)

	jackson = ObjectMapper()

	settings = Mock(MOPACSettings)

	state = MOPACState(None,[],None, settings, {})

	PARTY1 = PartyId("party1");
	PARTY2 =  PartyId("party2")
	PARTY3 =  PartyId("party3")


	# copy from MopacSettingsTest. We need settings here but don't want to mock
	# this large structure.
	mopacsettingstr = "{\"MOPACSettings\":{\"participants\":[{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party1\",\"parameters\":{}},\"profile\":\"http://profile1\"}]}},{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party2\",\"parameters\":{}},\"profile\":\"http://profile2\"}]}}],\"deadline\":{\"DeadlineTime\":{\"durationms\":100}},\"votingevaluator\":{\"LargestAgreement\":{}}}}";
	# create real objects for the GeneralTests and for serialization tests
	progress1 = ProgressTime(100, NOW)
	progress2 = ProgressTime(200, NOW)

	
	serialized = "{\"MOPACState\":{\"phase\":{\"OfferPhase\":{\"partyStates\":{\"powers\":{},\"notYetActed\":[],\"actions\":[],\"agreements\":{},\"walkedAway\":[],\"exceptions\":{}},\"deadline\":100,\"evaluator\":{\"LargestAgreement\":{}}}},\"actions\":[],\"progress\":{\"ProgressTime\":{\"duration\":100,\"start\":1001}},\"settings\":{\"MOPACSettings\":{\"participants\":[{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party1\",\"parameters\":{}},\"profile\":\"http://profile1\"}]}},{\"TeamInfo\":{\"parties\":[{\"party\":{\"partyref\":\"http://party2\",\"parameters\":{}},\"profile\":\"http://profile2\"}]}}],\"deadline\":{\"DeadlineTime\":{\"durationms\":100}},\"votingevaluator\":{\"LargestAgreement\":{}}}},\"partyprofiles\":{}}}"

	def setUp(self):
		self.partyparams1 = Mock(PartyWithParameters)
		self.profile1 = PartyWithProfile(self.partyparams1,Mock(ProfileRef))
		self.partyStates = PartyStates({})
		self.phase1 = OfferPhase(self.partyStates, 100, LargestAgreement())
		self.phase2 = OfferPhase(self.partyStates, 200, LargestAgreement())
		self.params1 = Parameters().With("power", 2);
		self.partyparams1.getParameters=Mock(return_value=self.params1)

		realsettings = self.jackson.parse(json.loads(self.mopacsettingstr),	MOPACSettings)
		party = Mock(TeamInfo)
		pwithp = Mock(PartyWithParameters)
		pwithp.getParameters=Mock(return_value= Parameters())
		party.getParties=Mock(
			return_value=[PartyWithProfile(pwithp, Mock(ProfileRef))])
		party.getSize=Mock(return_value=1)
		realsettings2 = realsettings.With(party)

		self.state1 = MOPACState(self.phase1, [], self.progress1, realsettings, {})
		self.state1a = MOPACState(self.phase1, [], self.progress1, realsettings, {})
		self.state2 = MOPACState(self.phase2, [], self.progress1, realsettings, {})
		self.state3 = MOPACState(self.phase1, [Mock(Action)],
				self.progress1, realsettings, {})
		self.state4 = MOPACState(self.phase1, [], self.progress2,realsettings, {})
		self.state5 = MOPACState(self.phase1, [], self.progress1,
				realsettings2, {})
		self.state6 = MOPACState(self.phase1, [], self.progress1,
				realsettings,
				{self.PARTY1: Mock(PartyWithProfile)})


	def getGeneralTestData(self)-> List[List[MOPACState]] :
		return [[self.state1, self.state1a],
				[self.state2], [self.state3],
				[self.state4], [self.state5],
				[self.state6]]

	def getGeneralTestStrings(self)-> List[str]:
		return [
				"MOPACState.*OfferPhase.*PartyStates.*,MOPACSettings.*PartyWithProfile.*ProgressTime.*",
				"MOPACState.*OfferPhase.*PartyStates.*,MOPACSettings.*PartyWithProfile.*ProgressTime.*",
				"MOPACState.*OfferPhase.*PartyStates.*,MOPACSettings.*PartyWithProfile.*ProgressTime.*",
				"MOPACState.*OfferPhase.*PartyStates.*,MOPACSettings.*PartyWithProfile.*ProgressTime.*",
				"MOPACState.*OfferPhase.*PartyStates.*,MOPACSettings.*PartyWithProfile.*ProgressTime.*",
				"MOPACState.*OfferPhase.*PartyStates.*,MOPACSettings.*PartyWithProfile.*ProgressTime.*"]

	def testsmokeTest(self):
		pass

	def testaddProfilesBeforeInit(self):
		st = self.state.With(self.PARTY1, self.profile1)
		self.assertTrue(self.PARTY1 in st.getPartyProfiles())

	def testInit(self):
		# no parties were added, should throw? Go to final mode?
		# Notice that it's possible to create settings with 0 participants,
		# because this is needed for Tournament mechanism.
		state1 = self.state.initPhase(ProgressTime(100,datetime.fromtimestamp(0)),
				1)
		self.assertEqual(0, len(state1.getActions()))
		self.assertEqual(0, len(state1.getAgreements().getMap()))
		self.assertEqual(0, len(state1.getPartyProfiles()))
		phase1 = state1.getPhase()
		self.assertTrue(isinstance(phase1,OfferPhase))
		offer1 = phase1
		self.assertEqual(PartyStates({}), offer1.getPartyStates())
	
	def testgetAgreementsTest(self):
		st = self.state.initPhase(ProgressTime(100, datetime.fromtimestamp(0)), 1)
		self.assertEqual(0, len(st.getAgreements().getMap()))

	def testDeserialize(self):
		obj = self.jackson.parse(json.loads(self.serialized), MOPACState)
		print(obj)
		self.assertEqual(self.state1, obj)

	def testSerialize(self):
		jsonobj = self.jackson.toJson(self.state1)
		print(jsonobj)
		self.assertEqual(json.loads(self.serialized), jsonobj)

	def testNewPhasePossible(self):
		phase = Mock(Phase)
		actions = []
		progress = Mock(Progress)
		progress.getTerminationTime=Mock(return_value=
				datetime.fromtimestamp(PHASE_MAXTIME/1000.)) # plenty for new phase
		def checkargs(*args, **kwargs):
			if args[0]==10 + PHASE_MINTIME:
				return False
			raise ValueError("unexpected arg");
			
				
		progress.isPastDeadline.side_effect=checkargs

		partyprofiles = {}
		s1 = MOPACState(phase, actions, progress, self.settings,
				partyprofiles)

		states = Mock(PartyStates)
		phase.getPartyStates=Mock(return_value=states)
		states.getNegotiatingParties=Mock(return_value=	
						set([self.PARTY1, self.PARTY2]))
		self.assertTrue(s1.isNewPhasePossible(10))

	def testNewPhasePossibleOnly1Party(self):
		phase = Mock(Phase)
		actions = []
		progress = Mock(Progress)
		progress.getTerminationTime=Mock(
				return_value=datetime.fromtimestamp(PHASE_MAXTIME/1000.)) 
				# plenty for new phase
				
		def checkargs(*args, **kwargs):
			if args[0]==10 + PHASE_MINTIME:
				return False
			raise ValueError("unexpected arg");
			
				
		progress.isPastDeadline.side_effect=checkargs
		
		partyprofiles = {}
		s1 = MOPACState(phase, actions, progress, self.settings,
				partyprofiles)

		states = Mock(PartyStates)
		phase.getPartyStates=Mock(return_value=states)
		states.getNegotiatingParties=Mock(return_value=
				set([self.PARTY1]))
		self.assertFalse(s1.isNewPhasePossible(10))

	def testNewPhasePossibleNotEnoughTime(self):
		phase = Mock(Phase)
		actions = []
		progress = Mock(Progress)
		progress.getTerminationTime=Mock(
				return_value=datetime.fromtimestamp((PHASE_MINTIME - 10)/1000.))
		partyprofiles = {}
		s1 = MOPACState(phase, actions, progress, self.settings,
				partyprofiles)

		states = Mock(PartyStates)
		phase.getPartyStates=Mock(return_value=states)
		states.getNegotiatingParties=Mock(return_value=
				set([self.PARTY1]))
		self.assertFalse(s1.isNewPhasePossible(10))

	def testnextPhaseTest(self):
		NOW = 102;
		phase = Mock(Phase)
		actions = []
		progress = Mock(Progress)
		progress.getTerminationTime=Mock(return_value=
				datetime.fromtimestamp(PHASE_MAXTIME/1000.))
		partyprofiles = {}
		s1 = MOPACState(phase, actions, progress, self.settings,
				partyprofiles)

		# PhaseB is the next phase, with remaining time
		phaseB = Mock(Phase)
		
		def checkargs(*args, **kwargs):
			if args[0]==NOW and args[1]==PHASE_MAXTIME-NOW:
				return phaseB
			raise ValueError("unexpected args")
		
		phase.next.side_effect=checkargs
		
		s2 = s1.nextPhase(NOW)
		self.assertEquals(phaseB, s2.getPhase())

	def testexceptionTest(self):
		phase = Mock(Phase)
		actions = []
		progress = Mock(Progress)
		
		partyprofiles = {}
		s1 = MOPACState(phase, actions, progress, self.settings,
				partyprofiles)

		exphase = Mock(Phase); # supposed phase that contains the exception
		
		def checkargs(*args, **kwargs):
			if isinstance(args[0], ProtocolException):
				return exphase
			raise ValueError("expected ProtocolException") 
			
		phase.WithException.side_effect=checkargs

		errstate = s1.WithException(ProtocolException("test", self.PARTY1))
		self.assertEqual(exphase, errstate.getPhase())
		self.assertEqual(progress, errstate.getProgress())
