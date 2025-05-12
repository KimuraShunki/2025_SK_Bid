from decimal import Decimal
from typing import Collection, List, Dict
import unittest

from tudelft.utilities.immutablelist.Range import Range

from geniusweb.bidspace.AllBidsList import AllBidsList
from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.NumberValueSet import NumberValueSet
from geniusweb.issuevalue.ValueSet import ValueSet


class AllBidsListTest(unittest.TestCase):
    I1V2 = DiscreteValue("i1v2")
    I1V1 = DiscreteValue("i1v1")
    I2V1 = NumberValue(Decimal("2.00"))
    I2V2 = NumberValue(Decimal("2.45"))
    
    I2V3 = NumberValue(Decimal("2.90"))
    DOMAINNAME = "testdomain"
    
    ISSUE1 = "issue1"
    ISSUE2 = "issue2"
    issues:Dict[str, ValueSet]  = {}
     
     
    discretevalues1:List[DiscreteValue]  = [I1V1, I1V2]
    values1 = DiscreteValueSet(discretevalues1)
    
    issues[ISSUE1]= values1
    
    values2 = NumberValueSet(Range(Decimal("2"), Decimal("3"), Decimal("0.45")))
    issues[ISSUE2]=values2
    
    domain = Domain(DOMAINNAME, issues)
    allBidsList = AllBidsList(domain)

    print(str(allBidsList))

    def testListElements(self):
        self.assertEqual(6, self.allBidsList.size())
        allbids = [bid for bid in self.allBidsList]
        self.assertTrue(Bid({self.ISSUE1:self.I1V1, self.ISSUE2:self.I2V1}) in allbids)
        self.assertTrue(Bid({self.ISSUE1:self.I1V1, self.ISSUE2:self.I2V2}) in allbids)
        self.assertTrue(Bid({self.ISSUE1:self.I1V1, self.ISSUE2:self.I2V3}) in allbids)
        self.assertTrue(Bid({self.ISSUE1:self.I1V2, self.ISSUE2:self.I2V1}) in allbids)
        self.assertTrue(Bid({self.ISSUE1:self.I1V2, self.ISSUE2:self.I2V1}) in allbids)
        self.assertTrue(Bid({self.ISSUE1:self.I1V2, self.ISSUE2:self.I2V3}) in allbids)

