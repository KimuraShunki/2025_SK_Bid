from decimal import Decimal
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.profile.utilityspace.DiscreteValueSetUtilities import DiscreteValueSetUtilities
from geniusweb.profile.utilityspace.NumberValueSetUtilities import NumberValueSetUtilities
from geniusweb.profile.utilityspace.ValueSetUtilities import ValueSetUtilities


class NumberValSetUtilsTest(unittest.TestCase):
    pyson=ObjectMapper()
    N0=Decimal("0")
    N04=Decimal("0.4")
    N05=Decimal("0.5")
    N065=Decimal("0.65") 
    N09=Decimal("0.9")
    N1=Decimal("1")
    
    salaryutils = NumberValueSetUtilities(Decimal(1000),N04, Decimal(3000),N09)
    salaryutils1 = NumberValueSetUtilities(Decimal(1000),N04, Decimal("3000"),N09)
    salaryutils2 = NumberValueSetUtilities(Decimal(1100),N04, Decimal("3000"),N09)
    salaryutils3 = NumberValueSetUtilities(Decimal(1000),N05, Decimal("3000"),N09)
    salaryjson:dict={"NumberValueSetUtilities":{ 'highUtility': 0.9,  'highValue': 3000, 
                                                'lowUtility': 0.4, 'lowValue': 1000}} 
    
    def testGetUtility(self):   
        self.assertEqual(self.N04, self.salaryutils.getUtility(NumberValue(Decimal(1000))))        
        self.assertEqual(self.N065, self.salaryutils.getUtility(NumberValue(Decimal(2000))))        
        self.assertEqual(self.N09, self.salaryutils.getUtility(NumberValue(Decimal(3000))))        
        self.assertEqual(self.N0, self.salaryutils.getUtility(Decimal(12)))
        
        
    def testSerialize(self):
        print(self.pyson.toJson(self.salaryutils))
        self.assertEqual(self.salaryjson, self.pyson.toJson(self.salaryutils))
        
    def testDeserialize(self):
        self.assertEqual(self.salaryutils, self.pyson.parse(self.salaryjson, ValueSetUtilities))
    
    def testRepr(self):
        self.assertEqual("NumberValueSetUtilities[1000->0.4,3000->0.9]", repr(self.salaryutils))
        
    def testEqual(self):
        self.assertEqual(self.salaryutils, self.salaryutils1)
        self.assertNotEqual(self.salaryutils, self.salaryutils2)
        self.assertNotEqual(self.salaryutils, self.salaryutils3)
        self.assertEqual(hash(self.salaryutils), hash(self.salaryutils1))
        self.assertNotEqual(hash(self.salaryutils), hash(self.salaryutils2))
        self.assertNotEqual(hash(self.salaryutils), hash(self.salaryutils3))
        