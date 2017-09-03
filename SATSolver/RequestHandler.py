"""
    Module: Server Request Handler
    Description: Defines a c
"""
import json
import threading
from SATController import SingletonMixin
from SATSolver.main import SATController


class RequestHandlerError(Exception):
    """This error should be raised when there was a error interpreting a message."""


def decode(data, server, client_id):
    """
    This function decodes a JSON string then determines which command should be exected and calls the corresponding
    function. The SATServer module will call this function to execute request sent by a client.
    :param data: The JSON string that needs to be decoded and executed.
    :param server: A reference to the SATServer to which the client is connected.
    :param client_id: The ID of the thread on which the client is connected. It helps identify the client who sent the
    original message.
    :return: Will return either `None` if no errors occurred and the command was successfully executed or a string
    explaining the error that occurred.
    """

    def solve(json_data):
        """
        Helper method that will try execute the `SOLVE` command.
        :param json_data: The JSON object 'SOLVE'
        """

        required_parameters = ["raw_input", "tabu_list_length", "max_false", "rec", "k"]
        optional_parameters = ["max_generations", "population_size", "sub_population_size", "crossover_operator",
                               "max_flip", "is_rvcf", "is_diversification", "method"]
        if set(required_parameters).issubset(list(json_data["SOLVE"].keys())):
            if set(list(json_data["SOLVE"].keys())).issubset(set(required_parameters + optional_parameters)):
                controller = SATController.instance()
                if controller.has_ga_instance():
                    raise RequestHandlerError("This server is already solving. No `SOLVE` requests can be handled "
                                              "until it has completed.")
                else:
                    raw_formula_array = json_data["SOLVE"]["raw_input"]

                    json_data["SOLVE"]["formula"], json_data["SOLVE"]["number_of_variables"], json_data["SOLVE"][
                        "number_of_clauses"] = controller.parse_formula(raw_formula_array, False)
                    del json_data["SOLVE"]["raw_input"]
                    controller.create_ga(json_data["SOLVE"])
                    controller.ga_thread = threading.Thread(target=controller.start_ga())
                    controller.ga_thread.start()
            else:
                raise RequestHandlerError("Unexpected arguments found for SOLVE command: " + ', '.join(set(list(
                    json_data["SOLVE"].keys())) - set(required_parameters + optional_parameters)))
        else:
            raise RequestHandlerError("Missing required arguments for SOLVE command: " + ', '.join(
                set(required_parameters) - set(list(json_data["SOLVE"].keys()))))

    def poll(json_data):
        """
        Helper method that will execute the `POLL` command.
        :param json_data: The JSON object 'POLL'
        :return: Will return either `None` if no errors occurred and the command was successfully executed or a string
        explaining the error that occurred.
        """
        print("Poll called")
        pass

    def stop():
        controller = SATController.instance()
        if controller.GA is not None:
            controller.ga_thread.terminate()
            controller.GA = None
        else:
            raise RequestHandlerError("Server has nothing to stop.")

    # Try and decode the JSON string. Return error message if the decoding failed.
    try:
        try:
            # print("Request handler got this juicy data " + str(data[:data.index('#')]))
            command = json.loads(data[:data.index('#')])
        except json.JSONDecodeError as e:
            raise RequestHandlerError("JSON could not be decoded: " + str(e))

        # Execute the command if it is a supported command. If it is not supported return a error message.
        if list(command.keys())[0] in ["SOLVE", "POLL"]:
            options = {
                "SOLVE": solve,
                "POLL": poll,
                "STOP": stop
            }
            options[list(command.keys())[0]](command)
        else:
            raise RequestHandlerError("Unsupported command: " + str(list(command.keys())[0]))
    except RequestHandlerError as e:
        error_response = encode("ERROR", [e])
        server.push_to_one(client_id, error_response)
    except Exception as e:
        error_response = encode("ERROR", ["A fatal error occurred: " + str(e)])
        server.push_to_one(client_id, error_response)


def encode(message_type, data):

    def error(data_arr):
        return '{"RESPONSE":{"ERROR":"' + str(data_arr[0]) + '"}}#'

    def report_progress(data_arr):
        response = {
            "RESPONSE": {
                "PROGRESS": {
                    "GENERATION": data_arr[0],
                    "TIME_STARTED": data_arr[1],
                    "BEST_INDIVIDUAL_FITNESS": data_arr[2],
                    "BEST_INDIVIDUAL": data_arr[3],
                    "CURRENT_CHILD_FITNESS": data_arr[4],
                    "CURRENT_CHILD": data_arr[5],
                    "NUM_VARIABLES": data_arr[6],
                    "NUM_CLAUSES": data_arr[7]
                }
            }
        }
        return json.dumps(response) + '#'

    def finished(data_arr):
        response = {
            "RESPONSE": {
                "FINISHED": {
                    "SUCCESSFUL": data_arr[0],
                    "FITNESS": data_arr[1],
                    "GENERATION": data_arr[2],
                    "TIME_STARTED": data_arr[3],
                    "TIME_FINISHED": data_arr[4]
                }
            }
        }
        return json.dumps(response) + '#'

    options = {
        "ERROR": error,
        "PROGRESS": report_progress,
        "FINISHED": finished
    }
    return options[message_type](data)
