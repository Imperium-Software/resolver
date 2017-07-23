"""
    Module: Server Request Handler
    Description: Defines a c
"""
import json


class RequestHandlerError(Exception):
    """This error should be raised when there was a error interpreting a message."""


class RequestHandler:
    
    def __init__(self):
        pass

    @staticmethod
    def decode(data):
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
            :return:
            """
            required_parameters = ["filename", "tabu_list_length", "max_false", "rec", "k"]
            optional_parameters = ["max_generations", "population_size", "sub_population_size", "crossover_operator",
                                   "max_flip", "is_rvcf", "is_diversification", "method"]
            if set(required_parameters).issubset(list(json_data["SOLVE"].keys())):
                if set(list(json_data["SOLVE"].keys())).issubset(set(required_parameters+optional_parameters)):
                    # TODO Call solving module.
                    return None
    
                else:
                    raise RequestHandlerError("Unexpected arguments found for SOLVE command: " + ', '.join(set(list(
                        json_data["SOLVE"].keys())) - set(required_parameters+optional_parameters)))
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
    
        # Try and decode the JSON string. Return error message if the decoding failed.
        try:
            command = json.loads(data[:-1])
        except json.JSONDecodeError as e:
            raise RequestHandlerError("JSON could not be decoded: " + str(e))
    
        # Execute the command if it is a supported command. If it is not supported return a error message.
        if list(command.keys())[0] in ["SOLVE", "POLL"]:
            options = {
                "SOLVE": solve,
                "POLL": poll
                }
            options[list(command.keys())[0]](command)
        else:
            raise RequestHandlerError("Unsupported command: " + str(list(command.keys())[0]))

    def encode(self, message_type, message):
    
        def error(msg):
            return '{"RESPONSE":{"ERROR":"' + msg + '"}}#'
    
        options = {
            "ERROR": error
        }
        return options[message_type](message)