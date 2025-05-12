from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.profile.utilityspace.DiscreteValueSetUtilities import DiscreteValueSetUtilities
from geniusweb.profile.utilityspace.ValueSetUtilities import ValueSetUtilities


class DiscreteValSetUtilsTest(unittest.TestCase):
    pyson=ObjectMapper()
    N0=Decimal("0")
    N1=Decimal("1")
    N05=Decimal("0.5")
    N07=Decimal("0.7")
    high=DiscreteValue("high")
    low=DiscreteValue("low")
    medium=DiscreteValue("medium")
    
    carreerutils = DiscreteValueSetUtilities({high:N1,low:N0,medium:N05})
    carreerutils1 = DiscreteValueSetUtilities({high:N1,low:N0,medium:N05})
    carreerutils2 = DiscreteValueSetUtilities({high:N1,low:N0,medium:N07})

    carreerjson = {"DiscreteValueSetUtilities":{ "valueUtilities":{ "high":1, "medium":0.5, "low":0}}}
    def testGetUtility(self):   
        self.assertEqual(self.N05, self.carreerutils.getUtility(self.medium))        
        self.assertEqual(self.N0, self.carreerutils.getUtility(DiscreteValue("nonexisting")))
        
    def testSerialize(self):
        print(self.pyson.toJson(self.carreerutils))
        self.assertEqual(self.carreerjson, self.pyson.toJson(self.carreerutils))
        
    def testDeserialize(self):
        self.assertEqual(self.carreerutils, self.pyson.parse(self.carreerjson, ValueSetUtilities))


    def testRepr(self):
        self.assertEqual('DiscreteValueSetUtilities{"high"=1, "low"=0, "medium"=0.5}', repr(self.carreerutils))
        
    def testEqual(self):
        self.assertEqual(self.carreerutils, self.carreerutils1)
        self.assertNotEqual(self.carreerutils, self.carreerutils2)
        self.assertEqual(hash(self.carreerutils), hash(self.carreerutils1))
        self.assertNotEqual(hash(self.carreerutils), hash(self.carreerutils2))
        