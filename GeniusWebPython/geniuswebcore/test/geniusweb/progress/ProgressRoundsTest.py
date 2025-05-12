from datetime import datetime
import json
from typing import List
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb import progress
from geniusweb.deadline.DeadlineRounds import DeadlineRounds
from geniusweb.progress.Progress import Progress
from geniusweb.progress.ProgressRounds import ProgressRounds
from geniusweb.progress.ProgressTime import ProgressTime


class ProgressRoundsTest(unittest.TestCase, GeneralTests[Progress]): 
    deadline = Mock(DeadlineRounds)
    TESTROUNDS = 10
    TESTTIME = 10  # milliseconds!

    date = datetime.fromtimestamp(98765 / 1000)
    date0 = datetime.fromtimestamp(100000 / 1000)

    deadline1 = ProgressRounds(20, 0, date)
    deadline2 = ProgressRounds(20, 0, date)
    deadline3 = ProgressRounds(30, 0, date)
    deadline4 = ProgressTime(20, date0)
    deadline5 = ProgressTime(20, date)
    jackson = ObjectMapper()
    progressstring = "{\"ProgressRounds\":{\"duration\":10,\"currentRound\":0,\"endtime\":98765}}"

    start = 1234
    end = datetime.fromtimestamp((start + TESTTIME) / 1000)
    pr = ProgressRounds(TESTROUNDS, 4, end)

    def setUp(self):
        self.deadline.getRounds = Mock(return_value=self.TESTROUNDS)
        self.progress = ProgressRounds(self.deadline.getRounds(), 0, self.date)

    def getGeneralTestData(self) -> List[List[Progress]]:
        return [[self.deadline1, self.deadline2], [self.deadline3], [self.deadline4], [self.deadline5]]

    def getGeneralTestStrings(self) -> List[str]:
        return ["ProgressRounds\\[0.*20\\]",
                "ProgressRounds\\[0.*30\\]", "ProgressTime\\[100000.*20ms\\]",
                "ProgressTime\\[98765.*20ms\\]"]

    def testInit(self):
        self.assertEqual(0, self.progress.get(1))

    def testCurrentRound(self):
        self.assertEqual(0, self.progress.getCurrentRound())

    def testAdvance(self):
        p = self.progress
        n = 0;
        while n <= self.TESTROUNDS:
            self.assertEqual((float(n) / self.TESTROUNDS), p.get(1))
            n = n + 1
            p = p.advance()

    def testAdvanceWhenDeadlineReached(self):
        p = ProgressRounds(self.TESTROUNDS, 9, self.date)
        p = p.advance()
        self.assertEqual(1, p.get(1))

    def testSerialize(self):
        print(json.dumps(self.jackson.toJson(self.progress)))
        self.assertEqual(json.loads(self.progressstring), self.jackson.toJson(self.progress))

    def testDeserialize(self):
        self.assertEqual(self.progress,
                self.jackson.parse(json.loads(self.progressstring), Progress))

    def testIllegalArg1(self):
        self.assertRaises(ValueError, lambda:ProgressRounds(10, 11, self.date))

    def testIllegalArg2(self):
        self.assertRaises(ValueError, lambda:ProgressRounds(10, -1, self.date))

    def pastDeadlinetest(self):
        self.assertFalse(self.pr.isPastDeadline(self.start));
        self.assertTrue(self.pr.isPastDeadline(self.start + self.TESTTIME + 1))
        self.assertFalse(self.pr.isPastDeadline(self.start + self.TESTTIME - 1))
        self.assertTrue(ProgressRounds(self.TESTROUNDS, self.TESTROUNDS, self.end)
                .isPastDeadline(self.start + self.TESTTIME + 1))

    def terminationTimetest(self):
        self.assertEquals(self.start + self.TESTTIME, self.pr.getTerminationTime().getTime())

    def gettest(self):
        # time does not matter for rounds-based deadline
        self.assertEqual(0.4, self.pr.get(self.start));
        self.assertEqual(0.4, self.pr.get(self.start + self.TESTTIME + 1))
        self.assertEqual(0.4, self.pr.get(self.start + self.TESTTIME))
        self.assertEqual(0.4, self.pr.get(self.start + self.TESTTIME / 2))
        self.assertEqual(0.4, self.pr.get(self.start - 10))
        self.assertEqual(0.4, self.pr.get(self.start + self.TESTTIME + 10))

        self.assertEqual(0.1,
                ProgressRounds(self.TESTROUNDS, 1, self.end).get(self.start))
        self.assertEqual(1,
                ProgressRounds(self.TESTROUNDS, self.TESTROUNDS, self.end).get(self.start));

    def totalRoundstest(self):
        self.assertEqual(10, self.pr.getTotalRounds())
