import socket

class server():
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("localhost", port))

    def accept(self):
        self.socket.listen(1)
        conn,addr = self.socket.accept()
        self.conn = conn

    def pull(self):
        return "some messages"

    def push(self, msg):
        self.conn.send(str.encode(msg))

    def get_port(self):
        return self.socket.getsockname()[1]

    def close(self):
        self.conn.close()
        self.socket.shutdown(1)
        self.socket.close()

if __name__ == "__main__":
    s = server(0)
    while True:
        try:
            print("Listening on " + str(s.get_port()))
            s.accept()
            s.push("\nHello!\n")
            s.push("This is now an open stream.\n")
        except:
            s.close()
