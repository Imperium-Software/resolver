import sys
from optparse import OptionParser
from server import SATServer
    
default_port = 55555
default_host = "localhost"


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
class SATController():

    def __init__(self):
        pass


def main(argv):
    """
        The main method of the program. It is responsible for:
         - Managing the server and request handler
         - Spawning the GA instance
         - Starts the interface or parses command-line arguments
        And finally returns the exit code
    """

    controller = singleton(SATController)()

    if len(argv) == 0:
        # Start the interface
        server_thread = SATServer(default_host, default_port)
        server_thread.start()
    else:
        parser = OptionParser()
        parser.add_option("-p", "--port", dest="port", help="Port number on which the server should run.",
                          metavar="<port>")
        parser.add_option("-f", "--file", dest="file", help="File that will be opened", metavar="<filename>")
        (options, args) = parser.parse_args()
        options = vars(options)
        if options["port"] is not None:
            # Port has been specified start server
            server_thread = SATServer(default_host, default_port)
            server_thread.start()
        else:
            print("Server not wanted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))