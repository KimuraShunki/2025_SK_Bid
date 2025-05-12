import unittest
from pyson.ObjectMapper import ObjectMapper
from geniusweb.bidspace.Interval import Interval
from decimal import Decimal
from geniusweb.profile.utilityspace.LinearAdditiveUtilitySpace import LinearAdditiveUtilitySpace
import json
from geniusweb.profile.Profile import Profile
from geniusweb.bidspace.BidsWithUtility import BidsWithUtility
from random import randrange
from geniusweb.bidspace.AllBidsList import AllBidsList
import time
from pathlib import Path

class BidsWithUtilityTest(unittest.TestCase):
	jackson = ObjectMapper()
	utilityGoal = Interval(Decimal("0.50"), Decimal("0.51"))
	accuracy = 5
	
	
	parameters=[
		[ "test/resources/jobs/jobs1.json", 11 ],
		[ "test/resources/7issues/7issues1.json", 260000 ],
		[ "test/resources/9issues/9issues1.json", 25000000 ] 
	]
	
	def testAll(self):
		''' 
		runs all the tests. Python has no standard 'parameterized' mechanism
		so we have to do it ourselves.
		'''
		for [filename, expectedsize] in self.parameters:
			self.filename=filename
			self.expectedSize= expectedsize
			with self.subTest("test"+self.filename):
				self.before()
				self.simple()
			with self.subTest("testMaxUtil"+self.filename):
				self.before()
				self.MaxUtil()
			with self.subTest("benchmark"+self.filename):
				self.before()
				self.benchmark()

	def before(self):
		print("Running from file " + self.filename)
		file = Path(self.filename).read_text("utf-8")
		self.profile = self.jackson.parse(json.loads(file), Profile)

			

	def simple(self):
		'''
		Test if the values are within acceptable range from the goal.
		'''
		list = BidsWithUtility.create(self.profile, self.accuracy).getBids(self.utilityGoal);
		#check not all but only 10000 random bids as list may be way too large
		#to test them all. Testing 1 billion bids may take 15 minutes or so on
		#quad core i7 @2.4GHz.....
		#also notice that we may be checking only part of the list if
		#the size of the list would become bigger than maxint.
		for n in range(10000):
			bid = list.get(randrange(list.size()))
			self.assertTrue(self.utilityGoal.contains(
				round(self.profile.getUtility(bid),self.accuracy-1)),
				"bid "+str(bid)+" is not in range "+str(self.utilityGoal))
						
		self.assertTrue(list.size()>= self.expectedSize)

	def MaxUtil(self) :
		bidswithutil = BidsWithUtility.create(self.profile)
		#notice, this is the *rounded* max util
		maxutil = bidswithutil.getRange().getMax()
		goal = Interval(maxutil - Decimal("0.00001"), maxutil)

		bidsnearmax = bidswithutil.getBids(goal)
		self.assertTrue(bidsnearmax.size() != 0)

		foundmax = Decimal(0)
		for bid in bidsnearmax :
			util = self.profile.getUtility(bid)
			if util>foundmax:
				foundmax = util;
		#found maximum may be slightly lower or higher because we rounded
		#all weighted utilities.
		self.assertTrue(abs(foundmax - maxutil) < 0.0001)

	def benchmark(self):
		print("\nBenchmarking " + self.profile.getName());
		domainsize = AllBidsList(self.profile.getDomain()).size()

		start = round(time.time()*1000)
		body = BidsWithUtility.create(self.profile, self.accuracy)
		list = body.getBids(self.utilityGoal)
		end = round(time.time()*1000)
		print("run time: " + str((end - start) / 1000.) + "s");
		print("Total size of bidspace:" + str(domainsize))
		print("Result size: " + str(list.size()))
