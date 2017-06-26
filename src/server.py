"""
    Module: server
    Description: defines a tcp server through which simple push and pull
                 operation are possible.
"""
import socket
from threading import Thread
from threading import Lock
import time


class ClientThread(Thread):
    """ Defines a client thread that will facilitate communication between client and server. """

    def __init__(self, ip, port, conn, thread_id):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.open = True
        self.thread_id = thread_id
        self.read_thread = None
        print("New client connected on: " + ip + ":" + str(port))

    def run(self):
        """ Creates a thread that will read data sent by the client and pass it to the DSL
        interpreter(or whatever the correct term for it is). """

        self.read_thread = Thread(self.recv_from_client(), self)

    def recv_from_client(self):
        """ Reads data sent by the client and pass it to the DSL
        interpreter(or whatever the correct term for it is). """

        while self.open:
            msg_chunk = ""
            total_msg = ""
            while msg_chunk == "" or msg_chunk[-1] != '#':
                msg_chunk = self.conn.recv(1024).strip().decode("utf-8").strip()
                total_msg += msg_chunk
            print(msg_chunk)

    def send_to_client(self, msg):
        """ Sends a msg to the client """
        self.conn.sendall(msg.encode())

    def kill(self):
        """ Closes the connection with the client. """
        self.read_thread.join()
        self.conn.close()


class SATServer(Thread):

    """ Defines a SAT server. The server listens for new incoming connections and creates a new thread for each new
    connection. A higher module can request this server to broadcast data to all connected clients or send data to a
    single client. Clients can also send requests which will then be passed to a higher module."""

    def __init__(self, host, port):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = None
        self.thread_id_iter = 1
        self.lock = Lock()
        self.threads = []
        self.listen()

    def listen(self):
        """ Listens for new connections and creates a thread when a client connects. """

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print("Server listening on port: " + str(self.port))
        while True:
            (client_connection, (ip, port)) = self.socket.accept()
            while not self.lock.acquire():
                self.lock.acquire()
            try:
                new_thread = ClientThread(ip, port, client_connection, self.thread_id_iter)
                self.thread_id_iter += 1
                new_thread.start()
                self.threads.append(new_thread)
            finally:
                self.lock.release()
            self.push_to_one(1, "Hello 1")

    def push_to_all(self, msg):
        """ Broadcasts a message to all connected clients. """

        for thread in self.threads:
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
            if index < len(self.threads):
                self.threads[index].send_to_client(msg)
        finally:
            self.lock.release()

    def get_port(self):
        """ Returns the port on which the server is running on. """

        return self.socket.getsockname()[1]

    def close(self):
        """ Terminates server operation. """

        self.socket.close()


# Stand-alone server code, for testing purposes:
def main():

    """ Main function for module SATServer """

    server_thread = SATServer("localhost", 55555)
    #time.sleep(15)
    print("Done Spleeping")
    server_thread.push('Hello World!')

if __name__ == "__main__":
    main()
