from decimal import Decimal
import json
from pathlib import Path
from typing import Dict
import unittest

from pyson.ObjectMapper import ObjectMapper
# from unitpy.GeneralTests import GeneralTests

from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue
from geniusweb.issuevalue.ValueSet import ValueSet
from geniusweb.profile.Profile import Profile
from geniusweb.profile.utilityspace.DiscreteValueSetUtilities import DiscreteValueSetUtilities
from geniusweb.profile.utilityspace.LinearAdditiveUtilitySpace import LinearAdditiveUtilitySpace
from geniusweb.profile.utilityspace.ValueSetUtilities import ValueSetUtilities


class LinearAdditiveTest(unittest.TestCase): #, GeneralTests[LinearAdditiveUtilitySpace]):
    pyson=ObjectMapper()

    yesno = DiscreteValueSet([DiscreteValue("yes"), DiscreteValue("no")])
    leasecarvals = yesno
    permcontractvals = yesno
    carreervals=DiscreteValueSet([DiscreteValue("low"),DiscreteValue("medium"),DiscreteValue("high")])
    ftevals=DiscreteValueSet([DiscreteValue("0.6"),DiscreteValue("0.8"),DiscreteValue("1.0")])
    salaryvals=DiscreteValueSet([DiscreteValue("2000"),DiscreteValue("2500"),
         DiscreteValue("3000"),DiscreteValue("3500"),DiscreteValue("4000")])
    workfromhomevals=DiscreteValueSet([DiscreteValue("0"),DiscreteValue("1"),DiscreteValue("2")])
     
    jobsdomain = Domain("jobs", {"lease car":leasecarvals, "permanent contract":permcontractvals, \
            "career development opportunities":carreervals, "fte":ftevals, \
            "salary": salaryvals, "work from home": workfromhomevals  })
    N0=Decimal("0")
    N1=Decimal("1")
    N025=Decimal("0.25")
    N03=Decimal("0.3")
    N05=Decimal("0.5")
    N075=Decimal("0.75")

    leasevarutils = DiscreteValueSetUtilities({DiscreteValue("no"):N0, DiscreteValue("yes"):N1})
    leasevarutils2 = DiscreteValueSetUtilities({DiscreteValue("no"):N0, DiscreteValue("yes"):N075})
    permcontrutils = DiscreteValueSetUtilities({DiscreteValue("no"):N0, DiscreteValue("yes"):N1})
    carreerutils = DiscreteValueSetUtilities({DiscreteValue("high"):N1,DiscreteValue("low"):N0,DiscreteValue("medium"):N05})
    fteutils = DiscreteValueSetUtilities({DiscreteValue("1.0"):N075,DiscreteValue("0.6"):N025,DiscreteValue("0.8"):N05})
    salaryutils = DiscreteValueSetUtilities({DiscreteValue("4000"):N1,DiscreteValue("2500"):N025,DiscreteValue("3500"):N075,
                     DiscreteValue("2000"):N0,DiscreteValue("3000"):N03})
    fromhomeutils = DiscreteValueSetUtilities({DiscreteValue("1"):N05,DiscreteValue("2"):Decimal("0.666666666666"),
                   DiscreteValue("0"):Decimal("0.333333333")})
    utils:Dict[str, ValueSetUtilities] = {'lease car': leasevarutils, 'permanent contract':permcontrutils,  'career development opportunities': carreerutils,
             'fte':fteutils, 'salary':salaryutils, 'work from home':fromhomeutils }
    utils2:Dict[str, ValueSetUtilities] = {'lease car': leasevarutils2, 'permanent contract':permcontrutils,  'career development opportunities': carreerutils,
             'fte':fteutils, 'salary':salaryutils, 'work from home':fromhomeutils }
    weights:Dict[str, Decimal] = {"lease car":Decimal("0.06"),"permanent contract":Decimal("0.16"),
            "career development opportunities":Decimal("0.04"),"fte":Decimal("0.32"),
            "salary":Decimal("0.24"),"work from home":Decimal("0.18")}
    weights2:Dict[str, Decimal] = {"lease car":Decimal("0.06"),"permanent contract":Decimal("0.16"),
            "career development opportunities":Decimal("0.05"),"fte":Decimal("0.31"),
            "salary":Decimal("0.24"),"work from home":Decimal("0.18")}

    jobs=LinearAdditiveUtilitySpace(jobsdomain, "jobs1",utils, weights )
    jobs1=LinearAdditiveUtilitySpace(jobsdomain, "jobs1",utils, weights )
    jobs2=LinearAdditiveUtilitySpace(jobsdomain, "jobs2",utils, weights )
    jobs3=LinearAdditiveUtilitySpace(jobsdomain, "jobs",utils2, weights )
    jobs4=LinearAdditiveUtilitySpace(jobsdomain, "jobs",utils, weights2 )

    # A real jobs profile from profiles server
    # "reservationBid":null was added because toJson will also add this (even though it's the default value)
    jobsstr = '{"LinearAdditiveUtilitySpace":{"issueUtilities":{'  \
        + '"lease car":{"DiscreteValueSetUtilities":{"valueUtilities":{"no":0,"yes":1}}},' \
        + '"permanent contract":{"DiscreteValueSetUtilities":{"valueUtilities":{"no":0,"yes":1}}},'  \
        + '"career development opportunities":{"DiscreteValueSetUtilities":{"valueUtilities":{"high":1,"low":0,"medium":0.5}}},' \
        + '"fte":{"DiscreteValueSetUtilities":{"valueUtilities":{"1.0":0.75,"0.6":0.25,"0.8":0.5}}},' \
        + '"salary":{"DiscreteValueSetUtilities":{"valueUtilities":{"4000":1,"2500":0.25,"3500":0.75,"2000":0,"3000":0.3}}},' \
        + '"work from home":{"DiscreteValueSetUtilities":{"valueUtilities":{"1":0.5,"2":0.666666666666,"0":0.333333333}}}},' \
        + '"issueWeights":{"lease car":0.06,"permanent contract":0.16,' \
        + '"career development opportunities":0.04,"fte":0.32,"salary":0.24,"work from home":0.18},' \
        + '"domain":{"name":"jobs","issuesValues":{"lease car":{"values":["yes","no"]},"permanent contract":{"values":["yes","no"]},"career development opportunities":{"values":["low","medium","high"]},"fte":{"values":["0.6","0.8","1.0"]},"salary":{"values":["2000","2500","3000","3500","4000"]},"work from home":{"values":["0","1","2"]}}},'\
        + '"name":"jobs1", "reservationBid":null}}'

    jobsjson = json.loads(jobsstr)

    partystr='{"LinearAdditiveUtilitySpace":{"domain":{"name":"party","issuesValues":{"Invitations":{"values":["Plain","Photo","Custom, Handmade","Custom, Printed"]},"Music":{"values":["MP3","DJ","Band"]},"Drinks":{"values":["Non-Alcoholic","Beer Only","Handmade Cocktails","Catering"]},"Cleanup":{"values":["Water and Soap","Specialized Materials","Special Equiment","Hired Help"]},"Food":{"values":["Chips and Nuts","Finger-Food","Handmade Food","Catering"]},"Location":{"values":["Party Tent","Your Dorm","Party Room","Ballroom"]}}},"name":"party1","issueUtilities":{"Invitations":{"DiscreteValueSetUtilities":{"valueUtilities":{"Plain":0.24,"Custom, Printed":0.48,"Photo":0.74,"Custom, Handmade":1}}},"Music":{"DiscreteValueSetUtilities":{"valueUtilities":{"DJ":0.99,"Band":0.35,"MP3":0.65}}},"Drinks":{"DiscreteValueSetUtilities":{"valueUtilities":{"Handmade Cocktails":0.672,"Non-Alcoholic":0.263,"Beer Only":0.98,"Catering":0.334}}},"Cleanup":{"DiscreteValueSetUtilities":{"valueUtilities":{"Special Equiment":0.32,"Water and Soap":0.65,"Specialized Materials":0.96,"Hired Help":0.31}}},"Food":{"DiscreteValueSetUtilities":{"valueUtilities":{"Finger-Food":0.52,"Handmade Food":0.51,"Catering":0.25,"Chips and Nuts":0.75}}},"Location":{"DiscreteValueSetUtilities":{"valueUtilities":{"Your Dorm":0.23,"Ballroom":0.77,"Party Room":0.99,"Party Tent":0.52}}}},"issueWeights":{"Invitations":0.05,"Music":0.19,"Drinks":0.28,"Cleanup":0.10,"Food":0.19,"Location":0.19},"reservationBid":null}}'
    partyjson = json.loads(partystr)
    
    def testSerialize(self):
        print(self.pyson.toJson(self.jobs))
        self.maxDiff=None
        self.assertEqual(self.jobsjson, self.pyson.toJson(self.jobs))
        
    def testDeserialize(self):
        self.assertEqual(self.jobs, self.pyson.parse(self.jobsjson, Profile))
        
    def testDeserializeJapanTrip(self):
        serialized = Path("test/resources/japantrip1.json").read_text("utf-8")
        jsonobj=json.loads(serialized)
        profile:Profile = self.pyson.parse(jsonobj, Profile);
        self.assertEquals("japantrip1", profile.getName())
        self.assertEquals("japantrip", profile.getDomain().getName())
        
    def testDeserializeParty1(self):
        print( str(self.pyson.parse(self.partyjson, Profile)))

    def testEquals(self):
        self.assertEqual(self.jobs,self.jobs1)
        self.assertEqual(hash(self.jobs),hash(self.jobs1))
        self.assertNotEqual(self.jobs,self.jobs2)
        self.assertNotEqual(hash(self.jobs),hash(self.jobs2))
        self.assertNotEqual(self.jobs,self.jobs3)
        self.assertNotEqual(hash(self.jobs),hash(self.jobs3))
        self.assertNotEqual(self.jobs,self.jobs4)
        self.assertNotEqual(hash(self.jobs),hash(self.jobs4))

        
    def testUtil(self):
        bid=Bid({"lease car":DiscreteValue("yes"), "permanent contract":DiscreteValue("yes"), \
                 "career development opportunities": DiscreteValue("low"), \
                "fte": DiscreteValue("0.8"), "salary":DiscreteValue("2500"), "work from home": DiscreteValue("1") });
        # 0.06 * 1 + 0.16 * 1 +  0.04 * 0 + 0.32 * 0.5 + 0.24 * 0.25 + 0.18 * 0.5 
        self.assertEqual(Decimal("0.53"), self.jobs.getUtility(bid))
