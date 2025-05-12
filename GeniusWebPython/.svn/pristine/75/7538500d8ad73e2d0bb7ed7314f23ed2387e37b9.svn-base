from collections import OrderedDict
from decimal import Decimal
import json
from pathlib import Path
from typing import List, Dict
import unittest
from unittest.mock import Mock

from pyson.ObjectMapper import ObjectMapper
from unitpy.GeneralTests import GeneralTests

from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.Value import Value
from geniusweb.issuevalue.ValueSet import ValueSet
from geniusweb.profile.Profile import Profile
from geniusweb.profile.utilityspace.DiscreteValueSetUtilities import DiscreteValueSetUtilities
from geniusweb.profile.utilityspace.LinearAdditiveUtilitySpace import LinearAdditiveUtilitySpace
from geniusweb.profile.utilityspace.UtilitySpace import UtilitySpace
from geniusweb.profile.utilityspace.ValueSetUtilities import ValueSetUtilities


class LinearAdditiveTest(unittest.TestCase, GeneralTests[LinearAdditiveUtilitySpace]):
    NAME = "test"
    I1V1UTIL = Decimal("0.3")
    I1V2UTIL = Decimal("0.2")
    I2V1UTIL = Decimal("0.6")
    I2V2UTIL = Decimal("0.8")
    WEIGHT1 = Decimal("0.4")
    WEIGHT2 = Decimal("0.6")
    ISS1 = "issue1"
    ISS2 = "issue2"
    ISS3 = "issue3"
    i1v1 = DiscreteValue("issue1value1")
    i1v2 = DiscreteValue("issue1value2")
    i2v1 = DiscreteValue("issue2value1")
    i2v2 = DiscreteValue("issue2value2")
    i3v1 = DiscreteValue("issue3value1")
    i3v2 = DiscreteValue("issue3value2")

    pyson = ObjectMapper()

    WEIGHT1a = Decimal("0.3")
    WEIGHT2a = Decimal("0.7")
 
    values:Dict[str, ValueSet] =  OrderedDict()
    values[ISS1]=DiscreteValueSet([i1v1, i1v2])
    smalldomain = Domain(NAME, values)
    values[ISS2]= DiscreteValueSet([i2v1, i2v2])
    domain = Domain(NAME, values)

    # build utilspace for string and equals testing.
    utils:Dict[str, ValueSetUtilities] =  OrderedDict()
    valueUtils =  OrderedDict()
    valueUtils[i2v2]= I2V2UTIL
    valueUtils[i2v1]= I2V1UTIL
    value2Utils = DiscreteValueSetUtilities(valueUtils)
    utils[ISS2]= value2Utils
    valueUtils =  OrderedDict()
    valueUtils[i1v1]= I1V1UTIL
    valueUtils[i1v2]= I1V2UTIL
    value1Utils = DiscreteValueSetUtilities(valueUtils)
    utils[ISS1]= value1Utils

    # build utilspaceb, mix up the utilities a bit.
    utilsb:Dict[str, ValueSetUtilities] =  OrderedDict()
    valueUtils =  OrderedDict()
    valueUtils[i2v2] =I1V2UTIL
    valueUtils[i2v1]= I1V1UTIL
    value2UtilsB = DiscreteValueSetUtilities(valueUtils)
    utilsb[ISS2]= value2UtilsB
    valueUtils =  OrderedDict()
    valueUtils[i1v1]= I2V1UTIL
    valueUtils[i1v2]= I2V2UTIL
    value1UtilsB = DiscreteValueSetUtilities(valueUtils)
    utilsb[ISS1] =value1UtilsB

    # weight map
    weights =  OrderedDict()
    weights[ISS2]= WEIGHT2
    weights[ISS1]= WEIGHT1

    # weight map 2
    weightsb =  OrderedDict()
    weightsb[ISS2]= WEIGHT2a
    weightsb[ISS1]= WEIGHT1a

    # bid with lowest utility
    issuevalues:Dict[str, Value] = OrderedDict()
    issuevalues[ISS2]= i2v1
    issuevalues[ISS1]=i1v2
    reservationBid = Bid(issuevalues)

    issuevalues =  OrderedDict()
    issuevalues[ISS2]= i2v1
    issuevalues[ISS1]= i1v1
    reservationBid2 = Bid(issuevalues)

    # make the utilspaces
    utilspace1 = LinearAdditiveUtilitySpace(domain, NAME, utils,
            weights, reservationBid)
    utilspace1a = LinearAdditiveUtilitySpace(domain, NAME, utils,
            weights, reservationBid);

    utilspace2a = LinearAdditiveUtilitySpace(domain, NAME, utils,
            weightsb, reservationBid);
    utilspace2b =  LinearAdditiveUtilitySpace(domain, NAME, utilsb,
            weights, reservationBid);
    utilspace3 = LinearAdditiveUtilitySpace(domain, NAME, utilsb,
            weights, reservationBid2);


    #Override
    def getGeneralTestData(self)->List[List[LinearAdditiveUtilitySpace]] :
        return [ [self.utilspace1, self.utilspace1a], [self.utilspace2a], 
                [self.utilspace2b], [self.utilspace3]]

    #Override
    def getGeneralTestStrings(self)-> List[str] :
        return [
            "LinearAdditive\\[\\{issue2=DiscreteValueSetUtilities\\{\"issue2value2\"=0.8, \"issue2value1\"=0.6\\}, issue1=DiscreteValueSetUtilities\\{\"issue1value1\"=0.3, \"issue1value2\"=0.2\\}\\},\\{issue2=0.6, issue1=0.4\\},Bid\\{issue2=\"issue2value1\", issue1=\"issue1value2\"\\}\\]",
            "LinearAdditive\\[\\{issue2=DiscreteValueSetUtilities\\{\"issue2value2\"=0.8, \"issue2value1\"=0.6\\}, issue1=DiscreteValueSetUtilities\\{\"issue1value1\"=0.3, \"issue1value2\"=0.2\\}\\},\\{issue2=0.7, issue1=0.3\\},Bid\\{issue2=\"issue2value1\", issue1=\"issue1value2\"\\}\\]",
            "LinearAdditive\\[\\{issue2=DiscreteValueSetUtilities\\{\"issue2value2\"=0.2, \"issue2value1\"=0.3\\}, issue1=DiscreteValueSetUtilities\\{\"issue1value1\"=0.6, \"issue1value2\"=0.8\\}\\},\\{issue2=0.6, issue1=0.4\\},Bid\\{issue2=\"issue2value1\", issue1=\"issue1value2\"\\}\\]",
            "LinearAdditive\\[\\{issue2=DiscreteValueSetUtilities\\{\"issue2value2\"=0.2, \"issue2value1\"=0.3\\}, issue1=DiscreteValueSetUtilities\\{\"issue1value1\"=0.6, \"issue1value2\"=0.8\\}\\},\\{issue2=0.6, issue1=0.4\\},Bid\\{issue2=\"issue2value1\", issue1=\"issue1value1\"\\}\\]"            
        ]


    def testConstructorNullIssues(self):
        self.assertRaises(ValueError, lambda:LinearAdditiveUtilitySpace(self.domain, self.NAME, None, None,self.reservationBid))

    def testConstructorNullDomain(self):
        self.assertRaises(ValueError, lambda:LinearAdditiveUtilitySpace(None, self.NAME, self.utils, self.weights,
                self.reservationBid))

    # Empty profile is not allowed since the weights then don't sum up to 1
    def testConstructorEmpty(self): 
        self.assertRaises(ValueError, lambda:LinearAdditiveUtilitySpace(self.domain, self.NAME, {}, self.weights,
                self.reservationBid))

    def testConstructorOneIssue(self):
        utilset = {}
        weightset = {}
        utilset[self.ISS1]= self.value1Utils
        weightset[self.ISS1]=Decimal(1)
        LinearAdditiveUtilitySpace(self.smalldomain, self.NAME, utilset, weightset,
                None)

    # Empty profile is not allowed since the weights then don't sum up to 1
    def testConstructoroneIssueWrongWeight(self):
        utilset = {}
        weightset = {}
        utilset[self.ISS1]= self.value1Utils
        weightset[self.ISS1]=self.WEIGHT1
        self.assertRaises(ValueError, lambda:LinearAdditiveUtilitySpace(self.smalldomain, self.NAME, utilset, weightset,
                self.reservationBid))

    # Try creating a domain and check isFitting
    #@Test
    def testCheckCoversDomain(self):
        utilset = {}
        weightset = {}

        utilset[self.ISS1]=self.value1Utils
        weightset[self.ISS1]=Decimal(1)
        space = LinearAdditiveUtilitySpace(
                self.smalldomain, self.NAME, utilset, weightset, None)

    
    # Try creating a domain and check isFitting but there is more issues in our
    # map than in the actual domain
    def testCheckCoversWrongDomain(self):
        utilset = {}
        weightset = {}

        utilset[self.ISS1]=self.value1Utils
        weightset[self.ISS1]= Decimal(1)
        self.assertRaises(ValueError,  lambda:LinearAdditiveUtilitySpace(
                self.domain, self.NAME, utilset, weightset, self.reservationBid))

    # Empty profile is not allowed since the weights then don't sum up to 1
    def testUtility(self):
        space = LinearAdditiveUtilitySpace(
                self.domain, self.NAME, self.utils, self.weights, self.reservationBid)

        bid = Mock()
        issues = [self.ISS1]
        bid.getIssues = Mock(return_value = issues)
        bid.getValue = Mock(return_value = self.i1v1)
        self.assertEqual(self.WEIGHT1 * self.I1V1UTIL, space.getUtility(bid))

    def testPreferred(self) :
        issuevalues = {}
        issuevalues[self.ISS1]=self.i1v1
        issuevalues[self.ISS2]=self.i2v2
        bid1 = Bid(issuevalues)
        issuevalues1 = {}
        issuevalues1[self.ISS1]= self.i1v2
        issuevalues1[self.ISS2]= self.i2v1
        bid2 = Bid(issuevalues1)
        self.assertTrue(self.utilspace1.isPreferredOrEqual(bid1, bid2))
        self.assertTrue(self.utilspace1.isPreferredOrEqual(bid1, bid1))
        self.assertTrue(self.utilspace1.isPreferredOrEqual(bid2, bid2))
        self.assertFalse(self.utilspace1.isPreferredOrEqual(bid2, bid1))
        self.assertFalse(self.utilspace1.isPreferredOrEqual(Bid({}), bid1))

    def testPartialBidUtilityTest(self):
        space = LinearAdditiveUtilitySpace(
                self.domain, self.NAME, self.utils, self.weights, self.reservationBid)
        issuevalues = {}
        issuevalues[self.ISS1]= self.i1v1
        bid = Bid(issuevalues)
        self.assertEqual(self.WEIGHT1* self.I1V1UTIL, space.getUtility(bid))

    def testLoadFullWithJson(self) :
        serialized = Path("test/resources/party1.json").read_text("utf-8")
        jsonobj=json.loads(serialized)
        space = self.pyson.parse(jsonobj, Profile)

    def testLoadFullWithJsonNumber(self) :
        serialized = Path("test/resources/japantrip1.json").read_text("utf-8")
        jsonobj=json.loads(serialized)
        profile:Profile = self.pyson.parse(jsonobj, Profile)


    def testResBidWithNonsenseIssue(self) :
        resBid = Bid({"nonsense": self.i1v1})
        self.assertRaises(ValueError, 
            lambda:LinearAdditiveUtilitySpace(self.domain, self.NAME, self.utils, self.weights, resBid))

    def testResBidWithWrongValueType(self):
        resBid = Bid({self.ISS1: NumberValue(Decimal(0))})
        self.assertRaises(ValueError, lambda:LinearAdditiveUtilitySpace(self.domain, self.NAME, self.utils, self.weights, resBid))

    def testResBidWithNonsenseValue(self):
        resBid =  Bid({self.ISS1: DiscreteValue("nonsense")})
        self.assertRaises(ValueError, lambda:LinearAdditiveUtilitySpace(self.domain, self.NAME, self.utils, self.weights, resBid))

