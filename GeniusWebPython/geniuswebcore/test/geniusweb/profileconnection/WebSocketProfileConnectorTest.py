import logging
from pathlib import Path  # type:ignore
import threading
from time import sleep
from typing import Optional
import unittest
from unittest.mock import Mock

from tudelft_utilities_logging.Reporter import Reporter
from uri.uri import URI

from geniusweb.profileconnection.FileProfileConnector import FileProfileConnector
from geniusweb.profileconnection.Session import Session
from geniusweb.profileconnection.WebSocketContainer import WebSocketContainer, \
    DefaultWebSocketContainer
from geniusweb.profileconnection.WebsocketProfileConnector import WebsocketProfileConnector
from test.geniusweb.profileconnection.ProfileServerStub import ProfileServerStub


class DummyReporter(Reporter):
    def log(self, level:int, msg:str, thrown:BaseException=None):
        print(msg)



class WebSocketProfileConnectorTest(unittest.TestCase):
    
    profiletext = Path("test/resources/japantrip1.json").read_text("utf-8")
    reporter=DummyReporter()

    def t1estConnect(self):
        session=Mock(Session)
        # this session does nothing, we manipulate it ourselves.
        
        #mock websocket
        wsContainer = Mock(WebSocketContainer)
        wsContainer.connectToServer.return_value=session

        profint= WebsocketProfileConnector("ws://blabla", self.reporter, wsContainer )
        
        def pumpevents():
            profint.onOpen(session)
            sleep(1)
            profint.onMessage(self.profiletext)
            print ("Message was sent")

        threading.Thread(target=pumpevents).start()
        profint.close()
        
        
        self.assertEqual("japantrip1", profint.getProfile().getName())
        print("Received profile succesfully!")

    def t1estConnectTimeout(self):
        session=Mock(Session)       
        #mock websocket
        wsContainer = Mock(WebSocketContainer)
        wsContainer.connectToServer.return_value=session

        profint= WebsocketProfileConnector("ws://blabla", self.reporter, wsContainer )
        
        # since we don't pump events, this should timeout.
        self.assertRaises(IOError, lambda:profint.getProfile())
        profint.close()
        
        
    def testWithRealProfilesServer(self):
        '''
        TO RUN THIS, ENSURE YOU HAVE A RUNNING PROFILESSERVER ON LOCALHOST
        '''
        server=ProfileServerStub()
        server.start()
        try:
            profint= WebsocketProfileConnector(URI("ws://localhost:8080/profilesserver/websocket/get/party/party1"), self.reporter, DefaultWebSocketContainer() )
            sleep(1)
            profile=profint.getProfile()
            self.assertTrue(profile)
            profint.close()
        finally:
            server.stop()
        