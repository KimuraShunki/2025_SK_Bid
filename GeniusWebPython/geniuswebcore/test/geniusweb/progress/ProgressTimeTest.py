from datetime import datetime
import json
from typing import List
import unittest

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.progress.Progress import Progress
from geniusweb.progress.ProgressTime import ProgressTime


class ProgressTimeTest (unittest.TestCase, GeneralTests[Progress]):
	# we set T0 quite high because Python has trouble handling small datetime
	T0 = 100000
	TIMEZERO = datetime.fromtimestamp(T0 / 1000)
	TESTTIME = 10  # milliseconds!
	progress1 = ProgressTime(TESTTIME, TIMEZERO)
	progress1a = ProgressTime(TESTTIME, TIMEZERO)
	progress2 = ProgressTime(200, TIMEZERO)

	jackson = ObjectMapper()
	progressstring = "{\"ProgressTime\":{\"duration\":10,\"start\":100000}}"

	start = 1234
	pr = ProgressTime(TESTTIME, datetime.fromtimestamp(start / 1000))

	def getGeneralTestData(self) -> List[List[Progress]]:
		return [[self.progress1, self.progress1a], [self.progress2]]
	
	def getGeneralTestStrings(self) -> List[str]:
		return ["ProgressTime\\[100000.*10ms\\]",
				"ProgressTime\\[100000.*200ms\\]"]

	def testInit(self):
		self.assertEqual(0, self.progress1.get(0))

	def testAdvancingTime(self):
		for n in range(0, self.TESTTIME):
			self.assertEqual(float(n) / self.TESTTIME,
					self.progress1.get(self.T0 + n))

	def testAdvanceWhenDeadlineReached(self):
		progress = ProgressTime(self.TESTTIME, self.TIMEZERO)
		self.assertEqual(1, self.progress1.get(self.T0 + self.TESTTIME));

	def testSerialize(self):
		actual = self.jackson.toJson(self.progress1)
		print(actual)
		self.assertEqual(json.loads(self.progressstring), actual)

	def testDeserialize(self):
		newprog = self.jackson.parse(json.loads(self.progressstring), 	ProgressTime)
		# we can't directly compare with progress since that's a hacked
		# object...
		self.assertEqual(self.TESTTIME, newprog.getDuration())
		self.assertEqual(self.T0, 1000 * newprog.getStart().timestamp())

	def pastDeadlinetest(self):
		self.assertTrue(self.pr.isPastDeadline(self.start + self.TESTTIME + 1))
		self.assertFalse(self.pr.isPastDeadline(self.start + self.TESTTIME - 1))

	def terminationTimetest(self):
		self.assertEqual(self.start + self.TESTTIME, self.pr.getTerminationTime().getTime())

	def gettest(self):
		self.assertEqual(0, self.pr.get(self.start))
		self.assertEqual(1, self.pr.get(self.start + self.TESTTIME));
		self.assertEqual(0.5, self.pr.get(self.start + self.TESTTIME / 2));
		self.assertEqual(0, self.pr.get(self.start - 10))
		self.assertEqual(1, self.pr.get(self.start + self.TESTTIME + 10))
