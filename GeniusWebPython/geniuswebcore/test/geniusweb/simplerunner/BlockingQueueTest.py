from threading import Thread
import time
import unittest
from geniusweb.simplerunner.BlockingQueue import BlockingQueue


class BlockingQueueTest(unittest.TestCase):

    def testSimple(self):
        q = BlockingQueue[int](4)
        self.assertEqual(0, q.size())
        q.put(1)
        q.put(2)
        q.put(3)
        self.assertEqual(3, q.size())
        self.assertEqual(1, q.take())
        self.assertEqual(2, q.take())
        self.assertEqual(3, q.take())
        self.assertEqual(0, q.size())
        
    def testThreading(self):
        q = BlockingQueue[int](4)

        def pushnumbers():
            for n in range(4):
                time.sleep(1)
                q.put(n)
        
        t = Thread(target=pushnumbers)
        t.start()
        
        for n in range(4):
            val = q.take()
            print(val)
            self.assertEqual(n, val)
        
