import sys
from SATSolver.SATController import SATController
from optparse import OptionParser
from SATSolver.server import SATServer


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
    controller = SATController.instance()
    from RequestHandler import decode

    if len(argv) == 0:
        # Start the interface
        controller.server_thread = SATServer(default_host, default_port, decode)
        controller.server_thread.start()
        controller.server_thread.join()
        pass
    else:
        parser = OptionParser()
        parser.add_option("-p", "--port", dest="port", type="int", help="Port number on which the server should run.",
                          metavar="<port>")
        parser.add_option("-f", "--file", dest="file", type="string", help="The CNF source.", metavar="<filename>")
        parser.add_option("--tabu-list-length", dest="tabu_list_length", type="int", help="",
                          metavar="<tabu list length>")
        parser.add_option("--max-false", dest="max_false", type="int",
                          help='How many times a clause must be false to be considered a "stumble-clause".',
                          metavar="<max false>")
        parser.add_option("--rec", dest="rec", type="int", help="", metavar="<rec>")
        parser.add_option("-k", dest="k", type="int", help="How long an atom in a stumble-clause is prevented from "
                                                           "flipping.", metavar="<k>")
        parser.add_option("--max-generations", dest="max_generations", type="int", help="", metavar="<max generations>")
        parser.add_option("--population-size", dest="population_size", type="int", help="", metavar="<population size>")
        parser.add_option("--sub-population-size", dest="sub_population_size", type="int", help="",
                          metavar="<sub population size>")
        parser.add_option("--crossover-operator", dest="crossover_operator", type="int", help="",
                          metavar="<crossover operator>")
        parser.add_option("--max-flip", dest="max_flip", type="int", help="", metavar="<max flip>")
        parser.add_option("--rvcf", dest="is_rvcf", type="string", help="")
        parser.add_option("--diversification", dest="is_diversification", type="string", help="")

        (options, args) = parser.parse_args()
        options = vars(options)
        if options["port"] is not None:
            # Port has been specified start server
            controller.server_thread = SATServer(default_host, options["port"], decode)
            controller.server_thread.start()
        f = open(options['file'], "r")
        formula, number_of_variables, number_of_clauses = controller.parse_formula(f.readlines())
        del options['port']
        del options['file']
        options['formula'] = formula
        options['number_of_variables'] = number_of_variables
        options['number_of_clauses'] = number_of_clauses
        controller.create_ga(options)
        controller.start_ga()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
