import logging
from threading import Thread
from time import sleep

from websocket_server import WebsocketServer  # type:ignore


def new_client(client, server):
    print("client connected!")
    with open('test/resources/jobs/jobs1.json') as f:
        text = f.read()
    server.send_message_to_all(text)

class ProfileServerStub(Thread):
    '''
    Run a fake profileserver for a simple test
    '''
    def run(self):
        self.server = WebsocketServer(host='127.0.0.1',port=8080,  
                loglevel=logging.INFO, key="key.pem", cert="cert.pem")
        self.server.set_fn_new_client(new_client)
        self.server.run_forever()

    def stop(self):
        self.server.shutdown()

if __name__ == '__main__':   
    server=ProfileServerStub()
    server.start()
    sleep(2)
    print("bla")
    server.stop()
    print("stopped")