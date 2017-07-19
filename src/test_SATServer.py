from unittest import TestCase

import time

from server import SATServer
from threading import Thread
import socket

import sys

class TestSATServer(TestCase):

    def test_push_to_all(self):
        # Test Message
        msg = "Test Message#"

        # Server with two clients connected
        server_thread = SATServer("localhost", 55555)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        client2 = TesterClient()
        client2.start()
        while len(server_thread.threads) < 2:
            pass
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        client2_response = None
        while client2_response is None:
            client2_response = client2.received
        self.assertEqual(msg, client1_response, "Client one did not receive the correct message.")
        self.assertEqual(msg, client2_response, "Client two did not receive the correct message.")

        # Clients disconnected test send message
        server_thread.push_to_all(msg)

        # New client connects
        client3 = TesterClient()
        client3.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_all(msg)
        client3_response = None
        while client3_response is None:
            client3_response = client3.received
        self.assertEqual(msg, client3_response, "Client three did not receive the correct message.")

        server_thread.close()

        # Server with one client connected
        server_thread = SATServer("localhost", 55555)
        server_thread.start()
        client1 = TesterClient()
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        msg = "Test Message#"
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg, client1_response, "The client did not receive the correct message.")
        server_thread.close()

        # Server with no clients
        server_thread = SATServer("localhost", 55555)
        server_thread.start()
        msg = "Test Message#"
        server_thread.push_to_all(msg)
        server_thread.close()

        pass

    def test_push_to_one(self):
        self.fail()

    def test_process_message_from_client(self):
        self.fail()

    def test_get_port(self):
        self.fail()

    def test_remove_thread(self):
        self.fail()

    def test_close(self):
        self.fail()

class TesterClient(Thread):

    def __init__(self, msg=None):
        Thread.__init__(self)
        self.msg = msg
        self.received = None

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 55555)
        sock.connect(server_address)
        try:
            if self.msg is None:
                total_msg = ""
                msg_chunk = ""
                while msg_chunk == "" or msg_chunk[-1] != '#':
                    msg_chunk = sock.recv(1024).strip().decode("utf-8").strip()
                    total_msg += msg_chunk
                self.received = total_msg
            else:
                sock.sendall(self.msg)
        finally:
            sock.close()
