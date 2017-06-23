"""
    Module: server
    Description: defines a tcp server through which simple push and pull
                 operation are possible.
"""
import socket

class SATServer():

    """ Defines a SAT server. """

    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("localhost", port))
        self.conn = None

    def accept(self):

        """ Initializes a connection  """

        self.socket.listen(1)
        conn = self.socket.accept()[0]
        self.conn = conn

    def pull(self):

        """ Retrieves messages from the stream. Assumes messages are terminated
        with a # """

        msg_chunk = ""
        total_msg = ""
        while msg_chunk == "" or msg_chunk[-1] != '#':
            msg_chunk = self.conn.recv(1024).strip().decode("utf-8").strip()
            total_msg += msg_chunk
        return total_msg

    def push(self, msg):

        """ Sends a certain message down the stream. """

        self.conn.send(str.encode(msg))

    def get_port(self):

        """ Returns the port on which the server is running on. """

        return self.socket.getsockname()[1]

    def close(self):

        """ Terminates server operation. """

        self.conn.close()
        self.socket.close()

# Stand-alone server code, for testing purposes:

def main():

    """ Main function for module SATServer """

    server = SATServer(0)
    print("Listening on " + str(server.get_port()))
    server.accept()
    while True:
        server.push("\nNEXT MESSAGE PLEASE:\n")
        server.pull()

if __name__ == "__main__":
    main()
