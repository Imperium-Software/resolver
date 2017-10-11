import sys
sys.path.insert(0, '../SATSolver/')
import socket
from unittest import TestCase
from multiprocessing import Process
from SATController import  SATController
from server import SATServer
from RequestHandler import decode

class IntegrationTests(TestCase):

    def test_request_chain(self):
        controller = SATController.instance()
        controller.server_thread = Process(target=SATServer, args=('localhost', 3000, decode))
        controller.server_thread.start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 3000))
        sock.close()

        controller.server_thread.terminate()
        self.assertEqual(1, 1)