"""
    Module: Server DSL Interpreter
    Description: defines a interpreter that can decode requests sent by the client and encode data that needs to be sent to the client.
"""
import json


def decode(data):
    """
    This function decodes a JSON string then determines which command should be exected and calls the corresponding
    function. The SATServer module will call this function to execute request sent by a client.
    :param data: The JSON string that needs to be decoded and executed.
    :return: Will return either `None` if no errors occurred and the command was successfully executed or a string
    explaining the error that occurred.
    """

    def solve(json_data):
        """
        Helper method that will try execute the `SOLVE` command.
        :param json_data: The JSON object 'SOLVE'
        :return: Will return either `None` if no errors occurred and the command was successfully executed or a string
        explaining the error that occurred.
        """
        required_parameters = ["filename", "tabu_list_length", "max_false", "rec", "k"]
        optional_parameters = ["max_generations", "population_size", "sub_population_size", "crossover_operator",
                               "max_flip", "is_rvcf", "is_diversification", "method"]
        if set(required_parameters).issubset(list(json_data["SOLVE"].keys())):
            if set(list(json_data["SOLVE"].keys())).issubset(set(required_parameters+optional_parameters)):
                # TODO Call solving module.
                return None

            else:
                return "Unexpected arguments found: " + ', '.join(set(list(json_data["SOLVE"].keys()))
                                                                  - set(required_parameters+optional_parameters))
        else:
            return "Missing required arguments: " + ', '.join(set(required_parameters)
                                                              - set(list(json_data["SOLVE"].keys())))

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
        command = json.loads(data)
    except json.JSONDecodeError as e:
        return "JSON could not be decoded: " + str(e)

    # Execute the command if it is a supported command. If it is not supported return a error message.
    if list(command.keys())[0] in ["SOLVE", "POLL"]:
        options = {
            "SOLVE": solve,
            "POLL": poll
            }
        return options[list(command.keys())[0]](command)
    else:
        return "Unsupported command: " + str(list(command.keys())[0])


def encode():
    pass

print(decode("""{
"SOLV" : {
    "tabu_list_length": "test",
    "max_false": "test",
    "rec": "test",
    "k": "test",
    "max_flip": "test"
    }
}"""))


