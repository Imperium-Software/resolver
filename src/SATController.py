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
class SATController:

    def __init__(self):
        self.GA = None
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
        parser.add_option("-p", "--port", dest="port", type="int", help="Port number on which the server should run.",
                          metavar="<port>")
        parser.add_option("-f", "--file", dest="file", type="string", help="The CNF source.", metavar="<filename>")
        parser.add_option("--tabu-list-length", dest="tabu_list_length", type="int", help="", metavar="<tabu list length>")
        parser.add_option("--max-false", dest="max_false", type="int", help="", metavar="<max false>")
        parser.add_option("--rec", dest="rec", type="int", help="", metavar="<rec>")
        parser.add_option("-k", dest="k", type="int", help="", metavar="<k>")
        parser.add_option("--max-generations", dest="max_generations", type="int", help="", metavar="<max generations>")
        parser.add_option("--population-size", dest="population_size", type="int", help="", metavar="<population size>")
        parser.add_option("--sub-population-size", dest="sub_population_size", type="int", help="", metavar="<sub population size>")
        parser.add_option("--crossover-operator", dest="crossover_operator", type="string", help="", metavar="<crossover operator>")
        parser.add_option("--max-flip", dest="max-flip", type="int", help="", metavar="<max flip>")
        parser.add_option("--rvcf", dest="is_rcvf", type="string", help="")
        parser.add_option("--diversification", dest="is_diversification", type="string", help="")
        parser.add_option("--method", dest="method", type="string", help="", metavar="<method>")

        (options, args) = parser.parse_args()
        options = vars(options)
        if options["port"] is not None:
            # Port has been specified start server
            server_thread = SATServer(default_host, options["port"])
            server_thread.start()
        else:
            print("Server not wanted")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))