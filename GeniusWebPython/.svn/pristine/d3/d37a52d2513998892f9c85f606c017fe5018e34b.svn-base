from fileinput import filename
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from tudelft_utilities_logging.ReportToLogger import ReportToLogger

from geniusweb.protocol.NegoSettings import NegoSettings
from geniusweb.simplerunner.ClassPathConnectionFactory import ClassPathConnectionFactory
from geniusweb.simplerunner.NegoRunner import NegoRunner
from geniusweb.simplerunner.Runner import Runner


class SessionRunnerE2ETest(unittest.TestCase):
	'''
	E2E test doing a full real run of a session with real agents and protocol.
	NOTICE This will exercise a full system to errors here may point far outside
	this module.
	'''
	TEST_RUNTIME = 5000
	jackson = ObjectMapper()
	logger = Mock(ReportToLogger("test"))
	filename:str
	runner:Runner

	params = ["test/resources/settings.json",
# 				 "test/resources/settings2.json" ,          PARTIALORDERING NOT YET
 				 "test/resources/settingsbadprofile.json",
# 				 "test/resources/shaoptoursettings.json",   ALLPERMUTATIONSETTINGS NOT YET
 				 "test/resources/mopac.json"
# 				 "test/resources/tournament.json"			ALLPERMUTATIONSETTINGS NOT YET
				 ]
	
	def testAll(self):
		''' 
		runs all the tests. Python has no standard 'parameterized' mechanism
		so we have to do it ourselves.
		'''
		for filename in self.params:
			self.filename = filename
			with self.subTest("before " + self.filename):
				self.before()
			with self.subTest("runMain" + self.filename):
				self.runTestMainFunction()

	def before(self):
		print("Running from file " + self.filename)
		serialized = Path(self.filename).read_text("utf-8")
		settings = self.jackson.parse(json.loads(serialized), NegoSettings)
		self.runner = Runner(settings, ClassPathConnectionFactory(),
				self.logger, self.TEST_RUNTIME)
			
	def runTestMainFunction(self):
		NegoRunner.main([self.filename])

	def runTest(self):
		self.runner.run()
		print("Final state:\n" + str(self.runner.getProtocol().getState()))
		self.assertTrue(self.runner.isProperlyStopped())
		# check no warnings and more severe
		self.asssertEqual([], self.logger.log.call_args_list)
