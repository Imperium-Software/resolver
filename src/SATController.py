import sys
import getopt
from server import SATServer
    
default_port = 55555
default_host = "localhost"


def main(argv):
    """
        The main method of the program. It is responsible for:
         - Managing the server and request handler
         - Spawning the GA instance
         - Starts the interface or parses command-line arguments
        And finally returns the exit code
    """
    server_thread = SATServer(default_host, default_port)
    if len(argv) == 0:
        # Start the interface
        print("Starting Interface")
    else:
        try:
            opts, args = getopt.getopt(argv, '', [])
        except getopt.GetoptError:
            show_help()
            sys.exit(2)
        if any('port' in opt for opt in opts):
            # Run GA without server
            print("Without Server")
        else:
            # Run with server
            print("With Server")
            pass

        pass

        # Parse command-line args and start the server instance or start solving
        pass
    
def show_help():
    print("The command-line arguments are:")
    print("-o \t The file to output the (partially) satisfying assignment to")
    pass

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))