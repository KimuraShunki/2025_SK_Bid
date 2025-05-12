from queue import Empty
import unittest

from geniusweb.PriorityQueue import PriorityQueue


class A:
    def __init__(self, x):
        self.x=x
    def get(self):
        return self.x
    def __repr__(self):
        return str(self.x)
    def __hash__(self):
        return hash(self.x)
    def __eq__(self,other):
        return self.x==other.x 


class PriorityQueueTest(unittest.TestCase):
    
    def setUp(self):
        self.q=PriorityQueue[int]( lambda x,y: x.get() < y.get())

    def testSmoke(self):
        PriorityQueue(lambda:False)
        
    def testPush1(self):
        self.assertEqual(0, self.q.qsize())
        self.assertTrue(self.q.empty())
        self.q.put(A(1))
        self.assertEqual(1, self.q.qsize())
        self.assertFalse(self.q.empty())
        
        self.assertEqual(A(1), self.q.get( block=False)) 
        self.assertEqual(0, self.q.qsize())
        self.assertTrue(self.q.empty())

        self.assertRaises(Empty, lambda:self.q.get(block=False))
        
    def testPushDuplicates(self):
        self.q.put(A(1))
        self.q.put(A(1))
        self.assertEqual(2, self.q.qsize())
        
        self.assertEqual(A(1), self.q.get(block=False)) 
        self.assertEqual(A(1), self.q.get(block=False)) 
        self.assertTrue( self.q.empty())
 
    def testProperSorted(self):
        self.q.put(A(2))
        self.q.put(A(3))
        self.q.put(A(1))
        self.assertEqual(A(1), self.q.get(block=False)) 
        self.assertEqual(A(2), self.q.get(block=False)) 
        self.assertEqual(A(3), self.q.get(block=False)) 
        
    def testReverseSort(self):
        q1=PriorityQueue( lambda x,y: x.get() > y.get())
        q1.put(A(2))
        q1.put(A(3))
        q1.put(A(1))
        self.assertEqual(A(3), q1.get(block=False)) 
        self.assertEqual(A(2), q1.get(block=False)) 
        self.assertEqual(A(1), q1.get(block=False)) 

    def testContains(self):
        self.q.put(A(2))
        self.q.put(A(3))
        self.q.put(A(1))
        self.assertTrue(A(1) in self.q)