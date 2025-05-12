import unittest

from geniusweb.profileconnection.FileProfileConnector import FileProfileConnector


class FileProfileConnectorTest(unittest.TestCase):
    def testLoad(self):
        profint= FileProfileConnector("test/resources/japantrip1.json")
        self.assertEqual("japantrip1", profint.getProfile().getName())
