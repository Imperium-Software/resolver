import sys
sys.path.insert(0, '../SATSolver/')
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
        controller.server_thread.terminate()