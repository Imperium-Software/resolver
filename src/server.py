"""
    Module: server
    Description: defines a tcp server through which simple push and pull
                 operation are possible.
"""
import socket
import sys
import time  # TODO Remove this when testing is moved to the testing framework.
from threading import Thread
from threading import Lock


class ClientThread(Thread):
    """ Defines a client thread that will facilitate communication between client and server. """

    def __init__(self, conn, thread_id, server_thread):
        Thread.__init__(self)
        self.conn = conn
        self.open = True
        self.thread_id = thread_id
        self.read_thread = None
        self.server_thread = server_thread

    def run(self):
        """ Creates a thread that will read data sent by the client and pass it to the server thread for processing. """

        self.read_thread = Thread(self.recv_from_client(), self)

    def recv_from_client(self):
        """ Reads data sent by the client and pass it to the DSL
        interpreter(or whatever the correct term for it is). """

        try:
            while self.open:
                msg_chunk = ""
                total_msg = ""
                while msg_chunk == "" or msg_chunk[-1] != '#':
                    msg_chunk = self.conn.recv(1024).strip().decode("utf-8").strip()
                    if msg_chunk == "":
                        self.kill()
                    total_msg += msg_chunk
                self.server_thread.process_message_from_client(msg_chunk)
        except socket.error:
            return

    def send_to_client(self, msg):
        """ Sends a msg to the client """

        self.conn.sendall(msg.encode())

    def kill(self):
        """ Closes the connection with client. """

        print(BColors.FAIL + '[-]' + BColors.ENDC + ' Client disconnected: ' + '{0}'.format(self.conn.getpeername()[0])
              + ':{0}'.format(self.conn.getpeername()[1]))
        self.server_thread.remove_thread(self.thread_id)
        self.conn.close()


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SATServer(Thread):

    """ Defines a SAT server. The server listens for new incoming connections and creates a new thread for each new
    connection. A higher module can request this server to broadcast data to all connected clients or send data to a
    single client. Clients can also send requests which will then be passed to a higher module."""

    def __init__(self, host, port):
        super(SATServer, self).__init__()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((host, port))
            self.socket.listen(5)
            print("Server listening on port: " + str(port))
        except socket.error:
            print('Failed to create socket')
            sys.exit()
        self.thread_id_iter = 1
        self.lock = Lock()
        self.threads = []

    def run(self):
        """ Listens for new connections and creates a ClientThread when a client connects and appends it to the threads
        array. """

        try:
            while True:
                client_connection, address = self.socket.accept()
                while not self.lock.acquire():
                    self.lock.acquire()
                try:
                    new_thread = ClientThread(client_connection, self.thread_id_iter, self)
                    self.thread_id_iter += 1
                    new_thread.start()
                    self.threads.append(new_thread)
                finally:
                    self.lock.release()
                print(BColors.OKGREEN + '[+]' + BColors.ENDC + ' Client connected: {0}'.format(address[0]) +
                      ':{0}'.format(address[1]))
        except ConnectionAbortedError:
            return

    def push_to_all(self, msg):
        """ Broadcasts a message to all connected clients. """

        for thread in self.threads:
            if thread:
                thread.send_to_client(msg)

    def push_to_one(self, thread_id, msg):
        """ Sends a message to a single client provided the thread's id on which the connection to the client
        is open. """

        while not self.lock.acquire():
            self.lock.acquire()
        try:
            index = 0
            while (self.threads[index].thread_id != thread_id) and (index < len(self.threads)):
                index += 1
            if (index < len(self.threads)) and (self.threads[index]):
                self.threads[index].send_to_client(msg)
        finally:
            self.lock.release()

    def process_message_from_client(self, msg):
        """ Passes a message to the DSL interpreter(or whatever the correct term for it is) to be interpreted."""

        # TODO When DSL interpreter is done this function should call it.
        print("From 'process_message_from_client': " + msg)

    def get_port(self):
        """ Returns the port on which the server is running on. """

        return self.socket.getsockname()[1]

    def remove_thread(self, thread_id):
        """ Sets a thread given its thread_id in the threads array to None to mark it as closed."""
        while not self.lock.acquire():
            self.lock.acquire()
        try:
            index = 0
            while (self.threads[index].thread_id != thread_id) and (index < len(self.threads)):
                index += 1
            if (index < len(self.threads)) and (self.threads[index]):
                self.threads[index] = None
        finally:
            self.lock.release()

    def close(self):
        """ Terminates server operation. """

        self.socket.close()
        for i in range(0, len(self.threads)-1):
            self.threads[i].kill()
        print("Server closed.")


# Stand-alone server code, for testing purposes:
def main():

    """ Main function for module SATServer """
    server_thread = SATServer("localhost", 55555)
    server_thread.start()
    sent = False
    while not sent:
        if len(server_thread.threads) == 2 and not sent:
            server_thread.push_to_all("Hello you two!")
            server_thread.push_to_one(1, "Hello number 1")
            server_thread.push_to_one(2, "Hello number 2")
            sent = True
            time.sleep(2)
            server_thread.threads[1].kill()
            time.sleep(2)
            server_thread.push_to_all("Hello you two!")
            server_thread.close()

if __name__ == "__main__":
    main()
