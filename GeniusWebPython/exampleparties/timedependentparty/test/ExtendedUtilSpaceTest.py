import unittest
from pyson.ObjectMapper import ObjectMapper
from decimal import Decimal
from geniusweb.profile.utilityspace.LinearAdditive import LinearAdditive
import json
from pathlib import Path
from geniusweb.profile.utilityspace.LinearAdditiveUtilitySpace import LinearAdditiveUtilitySpace
from timedependentparty.ExtendedUtilSpace import ExtendedUtilSpace

class ExtendedUtilSpaceTest(unittest.TestCase):
	jackson = ObjectMapper()
	SMALL = Decimal("0.0001")


	parameters=[
		["test/resources/jobs/jobs1.json", Decimal(0.02) ],
		[ "test/resources/7issues/7issues1.json", Decimal(0.0055) ],
		["test/resources/9issues/9issues1.json", Decimal(0.0013) ] 
	]
	
	def testAll(self):
		''' 
		runs all the tests. Python has no standard 'parameterized' mechanism
		so we have to do it ourselves.
		'''
		for [filename, expectedtolerance] in self.parameters:
			self.filename=filename
			self.expectedTolerance= expectedtolerance
			with self.subTest("testsmokeTest"+self.filename):
				self.before()
				self.smoke()
			with self.subTest("testTolerance"+self.filename):
				self.before()
				self.Tolerance()



	def before(self) :
		file = Path(self.filename).read_text("utf-8")
		profile=self.jackson.parse(json.loads(file), LinearAdditiveUtilitySpace)
		self.space=ExtendedUtilSpace(profile)
		print("self.space="+str(self.space))

	def smoke(self): 
		pass
	
	def Tolerance(self):
		self.assertTrue(abs(self.space._computeTolerance()-self.expectedTolerance) < self.SMALL)
