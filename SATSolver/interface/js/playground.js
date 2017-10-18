function construct_request(cnf) {
    var request = {
        "SOLVE": {
            "raw_input": cnf["raw_input"],
            "tabu_list_length": 10,
            "max_false": 5,
            "rec": 5,
            "k": 5,
            "max_flip": 5,
            "population_size": 50,
            "sub_population_size": 5,
        }
    };
    return JSON.stringify(request) + '#';
}

function solve() {

}

function solve1() {
    solve({"raw_input":['p cnf 4 2', '4 1 -3 0', '4 2 -3 0']}, $('#problem1'));
}

