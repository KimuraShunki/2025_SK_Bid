from decimal import Decimal
import json
import unittest

from pyson.ObjectMapper import ObjectMapper

from geniusweb.issuevalue.Bid import Bid
from geniusweb.issuevalue.DiscreteValue import DiscreteValue
from geniusweb.issuevalue.DiscreteValueSet import DiscreteValueSet
from geniusweb.issuevalue.Domain import Domain
from geniusweb.issuevalue.NumberValue import NumberValue


class DomainTest (unittest.TestCase) :
    maxDiff=None

    pyson=ObjectMapper()
    
    # test value as in java GeniusWeb
    jobsstring = '{"name":"jobs",' \
        + '"issuesValues":{' \
        + '"lease car":{"values":["yes","no"]},' \
        + '"permanent contract":{"values":["yes","no"]},' \
        + '"career development opportunities":{"values":["low","medium","high"]},'  \
        + '"fte":{"values":["0.6","0.8","1.0"]},' \
        + '"salary":{"values":["2000","2500","3000","3500","4000"]},' \
        + '"work from home":{"values":["0","1","2"]}}}' 
    jobsjson = json.loads(jobsstring)
    yesno = DiscreteValueSet([DiscreteValue("yes"), DiscreteValue("no")])
    leasecarvals = yesno
    permcontractvals = yesno
    carreervals=DiscreteValueSet([DiscreteValue("low"),DiscreteValue("medium"),DiscreteValue("high")])
    ftevals=DiscreteValueSet([DiscreteValue("0.6"),DiscreteValue("0.8"),DiscreteValue("1.0")])
    salaryvals=DiscreteValueSet([DiscreteValue("2000"),DiscreteValue("2500"),DiscreteValue("3000"),DiscreteValue("3500"),DiscreteValue("4000")])
    workfromhomevals=DiscreteValueSet([DiscreteValue("0"),DiscreteValue("1"),DiscreteValue("2")])
    
    jobs = Domain("jobs", {"lease car":leasecarvals, "permanent contract":permcontractvals, \
            "career development opportunities":carreervals, "fte":ftevals, \
            "salary": salaryvals, "work from home": workfromhomevals  })
    jobs1 = Domain("jobs", {"lease car":leasecarvals, "permanent contract":permcontractvals, \
            "career development opportunities":carreervals, "fte":ftevals, \
            "salary": salaryvals, "work from home": workfromhomevals  })

    jobs2 = Domain("jobs2", {"lease car":leasecarvals, "permanent contract":permcontractvals, \
            "career development opportunities":carreervals, "fte":ftevals, \
            "salary": salaryvals, "work from home": workfromhomevals  })

    jobs3 = Domain("jobs", {"Lcar":leasecarvals, "permanent contract":permcontractvals, \
            "career development opportunities":carreervals, "fte":ftevals, \
            "salary": salaryvals, "work from home": workfromhomevals  })

    def testSerialize(self):
        print(str(self.pyson.toJson(self.jobs)))
        self.assertEqual(self.jobsjson,self.pyson.toJson(self.jobs))
        
    def testDeserializeJobs(self):
        self.assertEqual(self.jobs, self.pyson.parse(self.jobsjson, Domain))
    
    def testInit(self):
        self.assertRaises(ValueError, lambda: Domain("name",None))
        self.assertRaises(ValueError, lambda: Domain(None,{"issue"}))
        self.assertRaises(ValueError, lambda: Domain("_invalid_name",{"issue"}))
        self.assertRaises(ValueError, lambda: Domain("name",{}))
        
    def testIsFitting(self):
        self.assertEqual(None,self.jobs.isFitting(Bid({"lease car":DiscreteValue("no")})))
        self.assertTrue("refers to non-domain issue" in self.jobs.isFitting(Bid({"no such issue":DiscreteValue("no")})))
        self.assertNotEqual(None,self.jobs.isFitting(Bid({"lease car":NumberValue(Decimal(1))})))
        self.assertTrue('illegal value' in self.jobs.isFitting(Bid({"lease car":DiscreteValue("maybe")})))
     
    def testIsComplete(self):
        self.assertEqual(None,self.jobs.isComplete(Bid({"lease car":DiscreteValue("no"),
                                                        "permanent contract":DiscreteValue("yes"),
                                                        "career development opportunities":DiscreteValue("high"),
                                                        "fte":DiscreteValue("1.0"),
                                                        "salary":DiscreteValue("3000"),
                                                        "work from home":DiscreteValue("1")
                                                        })))
        self.assertTrue("do not match issues in domain" in self.jobs.isComplete(Bid({"lease car":DiscreteValue("no"),
                                                        "permanent contract":DiscreteValue("yes"),
                                                        "work from home":DiscreteValue("1")
                                                        })))
        
    def testGetValues(self):
        self.assertEqual(self.jobs.getValues("lease car"),self.yesno)
        
    def testgetIssues(self):
        self.assertEqual(self.jobs.getIssues(),{'permanent contract', 'fte', 'lease car', 'career development opportunities', 'salary', 'work from home'})
               
    def testgetName(self):
        self.assertEqual(self.jobs.getName(),"jobs")

    def testRepr(self):
        self.assertEqual("Domain[jobs,{'lease car': DiscreteValueSet[\"yes\", \"no\"], 'permanent contract': DiscreteValueSet[\"yes\", \"no\"], 'career development opportunities': DiscreteValueSet[\"low\", \"medium\", \"high\"], 'fte': DiscreteValueSet[\"0.6\", \"0.8\", \"1.0\"], 'salary': DiscreteValueSet[\"2000\", \"2500\", \"3000\", \"3500\", \"4000\"], 'work from home': DiscreteValueSet[\"0\", \"1\", \"2\"]}]"\
                         ,repr(self.jobs))
        
    def testEqual(self):
        self.assertEqual(self.jobs, self.jobs1)
        self.assertNotEqual(self.jobs, self.jobs2)
        self.assertNotEqual(self.jobs, self.jobs3)
        self.assertNotEqual(self.jobs2, self.jobs3)
        self.assertEqual(hash(self.jobs), hash(self.jobs1))
        self.assertNotEqual(hash(self.jobs), hash(self.jobs2))
        