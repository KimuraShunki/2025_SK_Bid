import unittest
from geniusweb.utils import val, HASH, toStr


class utilsTest (unittest.TestCase):
    def testVal(self):
        a:Optional[int]=None
        self.assertRaises(ValueError, lambda:val(a))
        a=1
        self.assertEqual(1, val(a))
        
        
    def testToStr(self):
        self.assertEqual("{a=1}", toStr({'a':1}))
        self.assertEqual("{a=1}", toStr({'a':'1'}))
        self.assertEqual("[1, 2]", toStr([1,'2']))
        self.assertEqual("{a=[1, 2]}", toStr({'a':[1,'2']}))

    def testHASH(self):
        HASH([1,2,3])
        HASH((1,2,3))
        HASH({'a':1,'b':2})
        HASH(12)
        HASH('12')
        HASH(0.12)
        