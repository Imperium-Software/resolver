import sys
from SATController import SATController
from optparse import OptionParser
from server import SATServer
from GA import InputError


default_port = 55555
default_host = ""


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
        parser.add_option("-f", "--file", dest="file", type="string", help="The CNF source file in DIMACS format.",
                          metavar="<filename>")
        parser.add_option("--tabu-list-length", dest="tabu_list_length", type="int",
                          help="Length of tabu list - a fixed size FIFO queue.",
                          metavar="<tabu list length>")
        parser.add_option("--max-false", dest="max_false", type="int",
                          help='How many times a clause must be false to be considered a "stumble-clause".',
                          metavar="<max false>")
        parser.add_option("--rec", dest="rec", type="int",
                          help="The number of times false clauses induced "
                               "by a flip are forced to become true recursively.", metavar="<rec>")
        parser.add_option("-k", dest="k", type="int", help="How long an atom in a stumble-clause is prevented from "
                                                           "flipping.", metavar="<k>")
        parser.add_option("--max-generations", dest="max_generations", type="int",
                          help="The max number of iterations for the genetic algorithm.", metavar="<max generations>")
        parser.add_option("--population-size", dest="population_size", type="int",
                          help="The number of individuals in the population.", metavar="<population size>")
        parser.add_option("--sub-population-size", dest="sub_population_size", type="int",
                          help="The number of individuals to use in the selection process for parents.",
                          metavar="<sub population size>")
        parser.add_option("--crossover-operator", dest="crossover_operator", type="int",
                          help="0 - Corrective Clause; 1 - Corrective Clause with Truth Maintenance; "
                               "2 - Fluerent and Ferland.",
                          metavar="<crossover operator>")
        parser.add_option("--max-flip", dest="max_flip", type="int",
                          help="The maximum number of flips that can be performed during a tabu search procedure.",
                          metavar="<max flip>")
        parser.add_option("--rvcf", dest="is_rvcf", type="int",
                          help="Refinement of variable choice to flip - "
                               "using weight criterion to choose a better variable to flip - "
                               "0 for False; 1 for True.")
        parser.add_option("--diversification", dest="is_diversification", type="int",
                          help="A mechanism to help flip the last few stubborn false clauses -  "
                               "0 for False; 1 for True.")

        (options, args) = parser.parse_args()
        options = vars(options)
        if options["port"] is not None:
            # Port has been specified start server
            controller.server_thread = SATServer(default_host, options["port"], decode)
            controller.server_thread.start()
        f = open(options['file'], "r")
        formula, number_of_variables, number_of_clauses = controller.parse_formula(f.readlines())
        port_number = options['port']
        del options['port']
        del options['file']
        options['formula'] = formula
        options['number_of_variables'] = number_of_variables
        options['number_of_clauses'] = number_of_clauses
        try:
            controller.create_ga(options)
        except InputError as ie:
            print(ie)
            if port_number is not None:
                # Close Server
                pass
            return
        controller.start_ga()


if __name__ == '__main__':
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    sys.path.append(dir_path)
    sys.exit(main(sys.argv[1:]))
