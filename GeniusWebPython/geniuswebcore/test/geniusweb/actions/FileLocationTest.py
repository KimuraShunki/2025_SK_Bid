import unittest
from uuid import UUID

from pyson.ObjectMapper import ObjectMapper

from geniusweb.actions.FileLocation import FileLocation


class FileLocationTest (unittest.TestCase) :
	pyson=ObjectMapper()
	uuidstr='d5a4718a-4cc8-41d7-a988-2e2fda9154aa'
	fileloc = FileLocation(UUID(uuidstr))

	def testSerialize(self):
		
		loc=FileLocation()
		locstr = str(loc.getName())
		
		print(str(self.pyson.toJson(loc)))
		self.assertEqual(locstr, self.pyson.toJson(loc))
		self.assertEqual( self.uuidstr, self.pyson.toJson(self.fileloc))
		
	def testDeserialize(self):
		loc=FileLocation()
		locstr = str(loc.getName())
		
		self.assertEqual(loc, self.pyson.parse(locstr, FileLocation))
		
		self.assertEqual( self.fileloc, self.pyson.parse(self.uuidstr, FileLocation))

	def testTryWrite(self):
		path=self.fileloc.getFile()
		print(str(path))
		f=open(path,"w")
		f.write("test data")
		f.close()
		