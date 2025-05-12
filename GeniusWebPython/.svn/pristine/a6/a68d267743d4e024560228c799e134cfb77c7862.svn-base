import time
import unittest

from geniusweb.partystdio.PartyStdIo import PartyStdIo
from test.geniusweb.partystdio.EmptyParty import EmptyParty


class PartyStdIoTest(unittest.TestCase):
        
        
     
    def testCapabilities(self):
        channel = PartyStdIo(EmptyParty)
        channel.capabilities()
        # we really should check what is printed to stdout now...
        
        
    def testDescription(self):
        channel = PartyStdIo(EmptyParty)
        channel.description()
        # we really should check what is printed to stdout now...
    
    '''
    Test if the pipe to the party correctly converts incoming test
    strings to objects
    '''
        #FIXME
#     def testPipe(self):
#         channel = PartyStdIo(EmptyParty)
#         r,w = os.pipe()
#         inpipe = os.fdopen(r)
#         outpipe=os.fdopen(w,  'w')    
# 
#         thread = threading.Thread(target=lambda:channel.run(connend=inpipe))                   
#         thread.start()
#         time.sleep(0.5)
#         outpipe.write('nonsense')
#         thread.join(0.5)
#         os.close(inpipe)
#         os.close(outpipe)
#         self.assertFalse(thread.isAlive())
        