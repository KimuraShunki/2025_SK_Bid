import io
import sys
import time
import unittest

from tudelft.utilities.listener.Listener import Listener

from geniusweb.inform.Inform import Inform
from geniusweb.inform.Settings import Settings
from geniusweb.inform.YourTurn import YourTurn
from geniusweb.partystdio.StdInOutConnectionEnd import StdInOutConnectionEnd


class SimpleListener(Listener[Inform]):
	def __init__(self):
		self.received=[]
		
	def notifyChange(self, info: Inform):
		self.received.append(info) 
	

class StdInOutTest(unittest.TestCase):
	def testSmoke(self):
		StdInOutConnectionEnd()
		
	
	#disabled, hangs for now.
	def testRun(self):
		print("TESTING STDINOUT")
		data=bytes('{"Settings": {"id": "party1", "profile": "profile:1", "protocol": "protocol:1", "progress": {"ProgressTime": {"duration": 1000, "start": 12345000}}, "parameters": {"params": {}}}}', 'utf-8')
		data2=bytes('{"YourTurn": {}}', 'utf-8')
		fname="test.bin"
		
		listener=SimpleListener()
		
		with open(fname, "wb") as f:
			f.write(len(data).to_bytes(4,'little'))
			f.write(data)
			
			f.write(len(data2).to_bytes(4,'little'))
			f.write(data2)


		std=sys.stdin
		sys.stdin = open(fname,'r') 
		StdInOutConnectionEnd().run(listener)
		#sys.stderr.write("test")
		sys.stdin=std
		self.assertTrue( isinstance(listener.received[0], Settings))
		self.assertTrue( isinstance(listener.received[1], YourTurn))
		
def printsize(buf):
	print("args="+str(buf))
	time.sleep(0.1)
	buf.write('82128')
	