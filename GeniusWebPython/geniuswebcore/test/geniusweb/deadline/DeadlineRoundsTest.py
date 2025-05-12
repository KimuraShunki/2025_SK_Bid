
from datetime import datetime
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.deadline.Deadline import Deadline
from geniusweb.deadline.DeadlineRounds import DeadlineRounds


class DeadlineRoundsTest(unittest.TestCase):
    pyson=ObjectMapper()
    deadline = DeadlineRounds(10,1999)
    deadline1 = DeadlineRounds(10,1999)
    deadline2 = DeadlineRounds(10,4328)
    deadline3 = DeadlineRounds(9,1999)
    deadlinejson = {"DeadlineRounds":{'rounds':10, "durationms":1999}}

    def testDeserialization(self):
        self.assertEqual(self.deadline, self.pyson.parse(self.deadlinejson, Deadline))

    def testSerialization(self):
        print(self.pyson.toJson(self.deadline))
        self.assertEqual(self.deadlinejson, self.pyson.toJson(self.deadline))
    
    def testRepr(self):
        self.assertEqual("DeadlineRounds[10,1999]", repr(self.deadline))
        
    def testEqual(self):
        self.assertEqual(self.deadline, self.deadline1)
        self.assertNotEqual(self.deadline, self.deadline2)
        self.assertNotEqual(self.deadline, self.deadline3)
        self.assertEqual(hash(self.deadline), hash(self.deadline1))
        self.assertNotEqual(hash(self.deadline), hash(self.deadline2))
        self.assertNotEqual(hash(self.deadline), hash(self.deadline3))
        
    def testGetDuration(self):
        self.assertEqual(1999, self.deadline.getDuration())