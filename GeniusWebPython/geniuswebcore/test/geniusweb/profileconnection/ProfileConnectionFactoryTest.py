from builtins import BaseException
import unittest

from tudelft_utilities_logging.Reporter import Reporter
from uri.uri import URI

from geniusweb.profileconnection.ProfileConnectionFactory import ProfileConnectionFactory


class DummyReporter(Reporter):
    def log(self, level:int, msg:str, thrown:BaseException=None):
        print(msg)

class FileProfileConnectorTest(unittest.TestCase):
    def testLoad(self):
        profint= ProfileConnectionFactory.create(URI("file:test/resources/japantrip1.json"), DummyReporter())
        self.assertEqual("japantrip1", profint.getProfile().getName())
