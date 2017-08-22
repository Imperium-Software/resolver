from unittest import TestCase
from server import SATServer
from threading import Thread
from time import sleep
import socket


class TestSATServer(TestCase):

    class TesterClient(Thread):

        def __init__(self, port=55555, msg=None, wait=False):
            Thread.__init__(self)
            self.msg = msg
            self.received = None
            self.wait = wait
            self.port = port

        def run(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_address = ("localhost", self.port)
            sock.connect(server_address)
            try:
                if self.msg is None:
                    total_msg = ""
                    msg_chunk = ""
                    if self.wait:
                        sleep(0.1)
                    while msg_chunk == "" or msg_chunk[-1] != '#':
                        msg_chunk = sock.recv(1024).strip().decode("utf-8").strip()
                        if msg_chunk == "":
                            break
                        total_msg += msg_chunk
                    self.received = total_msg
                else:
                    sock.sendall(self.msg.encode())
                    if self.wait:
                        total_msg = ""
                        msg_chunk = ""
                        while msg_chunk == "" or msg_chunk[-1] != '#':
                            sock.sendall(self.msg.encode())
                            msg_chunk = sock.recv(1024).strip().decode("utf-8").strip()
                            if msg_chunk == "":
                                break
                            total_msg += msg_chunk
                        self.received = total_msg
            finally:
                sock.close()

    def test_push_to_all(self):
        # Test Message
        msg = "Test Message#"

        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = self.TesterClient(port=55555, wait=True)
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg, client1_response, "Client one did not receive the correct message.")

        # Clients disconnected test send message
        server_thread.push_to_all(msg)

        server_thread.close()

        # Server with one client connected
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        client1 = self.TesterClient(port=55555, wait=True)
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_all(msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg, client1_response, "The client did not receive the correct message.")
        server_thread.close()

        # Server with no clients
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        server_thread.push_to_all(msg)
        server_thread.close()

    def test_push_to_one(self):
        # Test Messages
        msg = "Test Message#"
        msg1 = "Test Message1#"
        msg2 = "Test Message2#"
        msg3 = "Test Message3#"

        # Server with two clients connected
        server_thread = SATServer("localhost", 55559, None)
        server_thread.start()
        client1 = self.TesterClient(port=55559, wait=True)
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_one(1, msg1)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg1, client1_response, "Client one did not receive the correct message.")

        # Send message to client which does not exist.
        server_thread.push_to_one(3, msg)
        server_thread.close()

        # Server with one client connected
        server_thread = SATServer("localhost", 55560, None)
        server_thread.start()
        client1 = self.TesterClient(port=55560, wait=True)
        client1.start()
        while len(server_thread.threads) < 1:
            pass
        server_thread.push_to_one(1, msg)
        client1_response = None
        while client1_response is None:
            client1_response = client1.received
        self.assertEqual(msg, client1_response, "The client did not receive the correct message.")
        server_thread.close()

    def test_address_in_use_exception(self):
        server_thread = SATServer("localhost", 55555, None)
        server_thread.start()
        another_server_thread = SATServer("localhost", 55555, None)
        another_server_thread.close()
        server_thread.close()

    def test_process_message_from_client(self):
        # Test message
        msg = "Test Message#"
        msg_from_client = None
        # Function to get the message sent by the client

        def get_message_from_client(msg_to_process, server, client_id):
            nonlocal msg_from_client
            msg_from_client = msg_to_process
            return None

        server_thread = SATServer("localhost", 55558, get_message_from_client)
        server_thread.start()
        client1 = self.TesterClient(55558, msg)
        client1.start()
        while msg_from_client is None:
            pass
        self.assertEqual(msg, msg_from_client[:-1], "The message sent by the client does not match the message "
                                                    "received by the server.")
        get_message_from_client(None, None, None)
        server_thread.close()

    def test_get_port(self):
        server_thread = SATServer("localhost", 55556, None)
        server_thread.start()
        self.assertEqual(55556, server_thread.get_port(), "The get_port() function did not return the correct port "
                                                          "number")
        server_thread.close()

    def test_close(self):
        server_thread = SATServer("localhost", 55557, None)
        server_thread.start()
        client1 = self.TesterClient(port=55557, wait=True)
        client1.start()
        client2 = self.TesterClient(port=55557, wait=True)
        client2.start()
        client3 = self.TesterClient(port=55557, wait=True)
        client3.start()
        while len(server_thread.threads) < 3:
            pass
        server_thread.close()
