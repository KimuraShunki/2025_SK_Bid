import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.inform.Inform import Inform
from geniusweb.inform.YourTurn import YourTurn


class YourTurnTest(unittest.TestCase):

    pyson=ObjectMapper()
    yourturn = YourTurn()
    yourturnjson:dict= {'YourTurn': {}}
    

    def testSerializeDeserialize(self):
        
        print(str(self.pyson.toJson(self.yourturn)))
        self.assertEqual(self.yourturnjson, self.pyson.toJson(self.yourturn))
        
    def testDeserialize(self):
        self.assertEqual(self.yourturn, self.pyson.parse(self.yourturnjson, Inform))
    
    def testrepr(self):
        self.assertEqual(repr(self.yourturn),"YourTurn")