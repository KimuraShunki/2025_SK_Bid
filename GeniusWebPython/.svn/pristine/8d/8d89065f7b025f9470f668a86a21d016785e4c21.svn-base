import json
from pathlib import Path
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.bidspace.pareto.GenericPareto import GenericPareto
from geniusweb.bidspace.pareto.ParetoLinearAdditive import ParetoLinearAdditive
from geniusweb.profile.Profile import Profile


class ParetoE2Etest (unittest.TestCase):
	'''
	Test pareto functionality with some real profiles in an e2e test
	'''
	jackson = ObjectMapper()

	data = \
		[\
				[ "test/resources/jobs/jobs1.json", \
						"test/resources/jobs/jobs2.json", 18 ], \
				[ "test/resources/7issues/7issues1.json", \
						"test/resources/7issues/7issues2.json", 557 ]\
		]
	
	def testAll(self):
		''' 
		runs all the tests. Python has no standard 'parameterized' mechanism
		so we have to do it ourselves.
		'''
		for [profile1, profile2, expectedNr] in self.data:
			self.path1 = profile1
			self.path2 = profile2
			self.expectedNrPoints = expectedNr
			with self.subTest("checkGeneric " + self.path1 + "," + self.path2):
				self.checkGenerciPareto()

	def checkGenerciPareto(self):
		file1 = Path(self.path1).read_text("utf-8")
		profile1 = self.jackson.parse(json.loads(file1), Profile)
		
		file2 = Path(self.path2).read_text("utf-8")
		profile2 = self.jackson.parse(json.loads(file2), Profile)

		profiles = [profile1, profile2]
		linaddpareto = ParetoLinearAdditive(profiles)
		print("linaddpareto result" + str(linaddpareto))
		self.assertEqual(self.expectedNrPoints, len(linaddpareto.getPoints()))

		if self.expectedNrPoints < 40:
			generalpareto = GenericPareto(profiles)
			self.assertEqual(generalpareto.getPoints(), linaddpareto.getPoints())
			print("generalpareto result" + str(generalpareto))
		else:
			print("Skippedn generalpareto - expected too slow")
