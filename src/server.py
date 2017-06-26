"""
    Module: server
    Description: defines a tcp server through which simple push and pull
                 operation are possible.
"""
import asyncore
import socket
import select
from threading import Thread
from threading import Lock
import time


class ClientThread(Thread):
    """ Defines a actual TCP server that will do actual communication."""

    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.open = True
        print("New client connected on: " + ip + ":" + str(port))

    def run(self):
        Thread(self.recv_from_client(), self)

    def recv_from_client(self):
        while self.open:
            msg_chunk = ""
            total_msg = ""
            while msg_chunk == "" or msg_chunk[-1] != '#':
                msg_chunk = self.conn.recv(1024).strip().decode("utf-8").strip()
                total_msg += msg_chunk
            print(msg_chunk)

    def send_to_client(self):
        print('Someone is trying to send something :D')

class SATServer():

    """ Defines a SAT server. The server listens for new incoming connections and creates a new thread for each new
    connection. A higher module can request this server to broadcast data to all connected clients. Clients can also
    send requests which will then be passed to a higher module."""

    def __init__(self, port, host):
        self.host = host
        self.port = port
        self.lock = Lock()
        self.threads = []
        self.socket.listen(0)



    def listen(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((self.host, self.port))
        print("Server listening on port: " + str(self.port))
        while True:
            (client_connection, (ip, port)) = listen_socket.accept()
            new_thread = ClientThread(ip, port, client_connection)
            new_thread.start()
            self.lock.acquire()
            try:
                self.threads.append(new_thread)
            finally:
                self.lock.release()



    def push(self, msg):
        """ Sends a certain message down the stream. """
        for thread in self.threads:
            thread.send_to_client(msg)

    #
    # def get_port(self):
    #     """ Returns the port on which the server is running on. """
    #
    #     return self.socket.getsockname()[1]
    #
    # def close(self):
    #     """ Terminates server operation. """
    #
    #     self.conn.close()
    #     self.socket.close()

# Stand-alone server code, for testing purposes:
def main():

    """ Main function for module SATServer """

    server = SATServer(55555)
    asyncore.loop()
    time.sleep(15)
    print("Done Spleeping")
    server.push('Hello World!')

if __name__ == "__main__":
    main()