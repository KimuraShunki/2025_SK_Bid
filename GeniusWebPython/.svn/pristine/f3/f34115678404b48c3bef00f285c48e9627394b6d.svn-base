from collections import OrderedDict
from decimal import Decimal
import json
from typing import List, Dict
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.Value import Value


class BidTest (unittest.TestCase,  GeneralTests[Bid]):

    asString1 = "{\"issuevalues\":{\"issue3\":901234567.89,\"issue2\":1,\"issue1\":\"b\"}}"
    ISSUE1 = "issue1"
    VALUE1:Value = DiscreteValue("value1")
    ISSUE2 = "issue2"
    VALUE2:Value  =  NumberValue(Decimal("10"))
    list:List[List[Bid]] = []

    issuevalues:Dict[str, Value]  = OrderedDict()
    issuevalues["issue3"]=  NumberValue(Decimal("901234567.89"))
    issuevalues[ISSUE2]= NumberValue(Decimal(1))
    issuevalues[ISSUE1]= DiscreteValue("b")
    bid = Bid(issuevalues);

    # different order but that shouldn't matter
    issuevalues1:Dict[str, Value]  = OrderedDict()
    issuevalues1["issue3"]= NumberValue(Decimal("901234567.89"))
    issuevalues1[ISSUE2]= NumberValue(Decimal(1))
    issuevalues1[ISSUE1]= DiscreteValue("b")
    bid1 = Bid(issuevalues1)

    issuevaluesb:Dict[str, Value] = OrderedDict()
    issuevaluesb[ISSUE2]= NumberValue(Decimal(1))
    issuevaluesb[ISSUE1]= DiscreteValue("b")
    bidb = Bid(issuevaluesb)

    # bidc and bidd have values swapped, so different issuevalues.
    issuevaluesc:Dict[str, Value]  = OrderedDict()
    issuevaluesc[ISSUE2]=VALUE2
    issuevaluesc[ISSUE1]= VALUE1
    bidc =  Bid(issuevaluesc)

    list.append([bid, bid1])
    list.append([bidb])
    list.append([bidc])
   
    def getGeneralTestData(self)->List[List[Bid]] :
        return self.list

    def getGeneralTestStrings(self)->List[str] : 
        return [
                "Bid\\{issue3=901234567.89, issue2=1, issue1=\"b\"\\}",
                "Bid\\{issue2=1, issue1=\"b\"\\}",
                "Bid\\{issue2=10, issue1=\"value1\"\\}"]


    def testNullConstructor(self):
        issuevalues = None;
        self.assertRaises(ValueError, lambda: Bid(issuevalues))
        
    def testUnkownIssue(self):
        self.assertEqual(None, self.bid.getValue("NotAnIssue")) 

    def testBidSimple(self):
        issuevalues = {}
        Bid(issuevalues) # no issues, no values should be ok

    def testBidNull(self):
        issuevalues = {}
        issuevalues[self.ISSUE1]=None
        self.assertRaises(ValueError, lambda:Bid(issuevalues)) # smokes

    def testbidOkIssueValue(self):
        issuevalues = OrderedDict()
        issuevalues[self.ISSUE1]=Mock(Value)
        Bid(issuevalues) # shouldn't smoke

    def testSerialize(self) :
        jackson = ObjectMapper()
        print(str(jackson.toJson(self.bid)))
        self.assertEqual(json.loads(self.asString1), jackson.toJson(self.bid))

    def testDeserialize(self) :
        jackson = ObjectMapper()
        read = jackson.parse(json.loads(self.asString1), Bid)
        self.assertEquals(self.bid, read)

    def testMerge(self):
        issuevalues = {}
        issuevalues[self.ISSUE1]= self.VALUE1
        partial1 = Bid(issuevalues)

        issuevalues = {}
        issuevalues[self.ISSUE2]= self.VALUE2
        partial2 = Bid(issuevalues)

        mergedbid = partial1.merge(partial2)
        self.assertEqual(self.bidc, mergedbid)

    def testMergeIssuesOverlap(self):
        issuevalues = {}
        issuevalues[self.ISSUE1]=self.VALUE1
        partial1 = Bid(issuevalues)

        issuevalues = {}
        issuevalues[self.ISSUE1]=self.VALUE2
        partial2 =  Bid(issuevalues)

        self.assertRaises(ValueError, lambda:partial1.merge(partial2))

    def testSmokeConstructor2(self):
        Bid({"issue": DiscreteValue("dss")})

    def testSmokeConstructor2b(self):
        Bid({"issue": NumberValue(Decimal("0.5"))})

    def testSmokeConstructor2Null1(self):
        self.assertRaises(ValueError, lambda:Bid({None: DiscreteValue("dss")}))

    def testSmokeConstructor2Null2(self):
        self.assertRaises(ValueError, lambda: Bid({"issue": None}))

