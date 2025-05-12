import traceback
import unittest

from geniusweb.actions.PartyId import PartyId
from geniusweb.protocol.ProtocolException import ProtocolException


class ProtocolExceptionTest(unittest.TestCase):
    def testConstructor(self):
        party = PartyId("test")
        try:
            x=1/0
        except Exception as e:
            err = ProtocolException("div by zero", party,  e)
            
        print(err) # BUG ? FEATURE? this does NOT show the cause nor the stacktrace... 
        self.assertTrue(err)
        self.assertTrue(err.__cause__)

    def testNullParty(self):
        ProtocolException("test",None, None)
        
