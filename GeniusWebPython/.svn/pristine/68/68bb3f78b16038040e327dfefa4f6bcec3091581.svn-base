
from datetime import datetime
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.deadline.Deadline import Deadline
from geniusweb.deadline.DeadlineTime import DeadlineTime


class DeadlineTimeTest(unittest.TestCase):
    pyson=ObjectMapper()
    deadline = DeadlineTime(1999)
    deadline1 = DeadlineTime(1999)
    deadline2 = DeadlineTime(4328)
    deadlinejson = {"DeadlineTime":{"durationms":1999}}

    def testDeserialization(self):
        self.assertEqual(self.deadline, self.pyson.parse(self.deadlinejson, Deadline))

    def testSerialization(self):
        print(self.pyson.toJson(self.deadline))
        self.assertEqual(self.deadlinejson, self.pyson.toJson(self.deadline))
    
    def testRepr(self):
        self.assertEqual("DeadlineTime[1999]", repr(self.deadline))
        
    def testEqual(self):
        self.assertEqual(self.deadline, self.deadline1)
        self.assertNotEqual(self.deadline, self.deadline2)
        self.assertEqual(hash(self.deadline), hash(self.deadline1))
        self.assertNotEqual(hash(self.deadline), hash(self.deadline2))
        
    def testGetDuration(self):
        self.assertEqual(1999, self.deadline.getDuration())