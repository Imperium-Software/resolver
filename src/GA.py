"""
    Module: GA
    Description: Defines the genetic algorithm and all the core functionality of it, including crossover and Tabu search
"""

from src.individual import Individual
from decimal import Decimal
import random
import copy


class GA:
    def __init__(self, filename, tabu_list_length, max_false, rec, k, max_generations=1000, population_size=100,
                 sub_population_size=15, crossover_operator=0, max_flip=10000, is_rvcf=True,
                 is_diversification=True, method=None):

        f = open(filename, "r")
        # Read all the lines from the file that aren't comments
        lines = [line.replace("\n", "") for line in f.readlines() if line[0] != "c" and line.strip() != ""]
        (self.numberOfVariables, self.numberOfClauses) = int(lines[0].split()[2]), int(lines[0].split()[3])
        self.formula = []

        # Creating member variables for each of the parameters
        self.max_generations = max_generations
        self.population_size = population_size
        self.sub_population_size = sub_population_size
        self.crossover_operator = crossover_operator
        self.tabu_list_length = tabu_list_length
        self.max_flip = max_flip
        self.is_rvcf = is_rvcf
        self.is_diversification = is_diversification
        self.max_false = max_false
        self.rec = rec
        self.k = k
        self.method = method

        # Initialize tabu, population and the sub_population to empty lists
        self.tabu = []
        self.population = []
        self.sub_population = []

        # Used in tabu search to determine best configuration/move
        self.best = None

        # Go through the lines and create numberOfClauses clauses
        line = 1
        # for line in range(1, len(lines)):
        while line < len(lines):
            clause = []
            # We need a while loop as a clause may be split over many lines, but eventually ends with a 0
            end_of_clause = False
            while line < len(lines) and not end_of_clause:
                # Split the line and append a list of all integers, excluding 0, to clause
                clause.append([int(variable.strip()) for variable in lines[line].split() if int(variable.strip()) != 0])
                # If this line ended with a 0, we reached the end of the clause
                if int(lines[line].split()[-1].strip()) == 0:
                    end_of_clause = True
                    line += 1
                # Otherwise continue reading this clause from the next line
                else:
                    line += 1
            # clause is now a list of lists, so we need to flatten it and convert it to a list
            self.formula.append(tuple([item for sublist in clause for item in sublist]))
        self.false_counts = [0 for _ in range(len(self.formula))]

        f.close()
        self.gasat()

    @staticmethod
    def sat(individual, clause):
        """
        sat (X,c) - by literature
        Indicates whether the clause c is true or false for the individual X i.e. satisfied or not by the assignment
        corresponding to X.
        :param individual: Individual class (Implemented by Regan) representing a particular assignment of truth values
        to variables.
        :param clause: Python tuple of integers - should be the same tuple as in the DIMACS format.
        :return: returns a boolean value indicating whether the assignment represented by the individual satisfies the
        clause.
        """

        # Iterate over atoms in the clause
        for atom in clause:
            # IF the atom is not negated
            if atom > 0:
                if individual.get(atom):
                    # The clause is satisfiable on seeing the first true atom
                    return True
            # IF the atom is negated
            else:
                if individual.get(abs(atom)) == 0:
                    # The clause is satisfiable on seeing the first false atom due to it being a negation
                    return True
        # Clause is unsatisfiable - no true atoms
        return False

    @staticmethod
    def sat_crossover(individual, clause):
        """
        sat (X,c) - by literature
        Indicates whether the clause c is true or false for the individual X i.e. satisfied or not by the assignment
        corresponding to X - Particular to crossovers as it takes into account whether there are undefined variables
        used in the clause - if so, the clause is not satisfied.
        :param individual: Individual class (Implemented by Regan) representing a particular assignment of truth values
        to variables.
        :param clause: Python tuple of integers - should be the same tuple as in the DIMACS format.
        :return: returns a boolean value indicating whether the assignment represented by the individual satisfies the
        clause.
        """

        # Iterate over atoms in the clause
        for atom in clause:
            # IF the atom is not negated
            if atom > 0:
                # The Clause is unsatisfiable on seeing an undefined variable.
                if individual.get_defined(atom) is False:
                    return False
                if individual.get(atom):
                    # The clause is satisfiable on seeing the first true atom
                    return True
            # IF the atom is negated
            else:
                # The Clause is unsatisfiable on seeing an undefined variable.
                if individual.get_defined(abs(atom)) is False:
                    return False
                if individual.get(abs(atom)) == 0:
                    # The clause is satisfiable on seeing the first false atom due to it being a negation
                    return True
        # Clause is unsatisfiable - no true atoms
        return False

    def evaluate(self, individual):
        """
        The fitness of individual with respect to the formula.
        :param individual: Individual class (Implemented by Regan) representing a particular assignment of truth values
        to variables.
        :return: the number of clauses of F which are not satisfied by X.
        """

        # Keeps count of unsatisfied clauses
        num_unsatisfied_clauses = 0

        # Iterate over clauses in the formula
        for clause in self.formula:

            # If a clause is unsatisfied increase the unsatisfied counter
            if not self.sat(individual, clause):
                num_unsatisfied_clauses = num_unsatisfied_clauses + 1

        return num_unsatisfied_clauses

    def improvement(self, individual, index):
        """
        The function computes the improvement (difference in unsatisfiable clauses) obtained by the flip of the ith
        variable of the individual.
        :param individual: Individual class (Implemented by Regan) representing a particular assignment of truth values
        to variables.
        :param index: index of a bit (starts at 1 - as per clause numbering in DIMACS format).
        :return: computed improvement value.
        """

        # index is not boundary tested - assuming this is done before a call to this function.

        # Determine fitness of individual before alterations
        original_individual_fitness = self.evaluate(individual)

        new_individual = copy.deepcopy(individual)
        # Flips the bit at the specified index
        new_individual.flip(index)

        # Calculates improvement in fitness
        return original_individual_fitness - self.evaluate(new_individual)

    def corrective_clause(self, x, y):
        """
        Performs the corrective clause cross-over.

        :param x: The first parent parameter.
        :param y: The second parent parameter.
        :return: The generated individual z
        """

        z = Individual(self.numberOfVariables, self.method, False)
        for clause in self.formula:
            best_pos = 0
            best_improvement = 0
            if not self.sat(x, clause) and not self.sat(y, clause) and not self.sat_crossover(z, clause):
                for i in range(len(clause)):
                    current_improvement = self.improvement(x, i) + self.improvement(y, i)
                    if current_improvement >= best_improvement:
                        best_improvement = current_improvement
                        best_pos = i
                z.set(best_pos, x.get(best_pos))
                z.set_defined(best_pos, x.get(best_pos))
                z.flip(best_pos)
                z.allocate(x, y)
        return z

    def corrective_clause_with_truth_maintenance(self, x, y):
        """
        Performs the CCTM cross-over operator.

        :param x: The first parent parameter.
        :param y: The second parent parameter.
        :return: The generated individual z
        """

        z = Individual(self.numberOfVariables, self.method, False)
        for clause in self.formula:
            best_pos = 0
            maximum_improvement = self.improvement(x, 0) + self.improvement(y, 0)
            if not self.sat(x, clause) and not self.sat(y, clause) and not self.sat_crossover(z, clause):
                for i in range(len(clause)):
                    current_improvement = self.improvement(x, i) + self.improvement(y, i)
                    if current_improvement >= maximum_improvement:
                        maximum_improvement = current_improvement
                        best_pos = i
                z.set(best_pos, x.get(best_pos))
                z.set_defined(best_pos, x.get(best_pos))
                z.flip(best_pos)

        # Truth maintenance - See section 4.2 of the paper
        for clause in self.formula:
            best_pos = -1
            minimum_improvement = self.numberOfClauses + 1
            if self.sat(x, clause) and self.sat(y, clause) and not self.sat_crossover(z, clause):
                for i in range(len(clause)):
                    if x.get(i) == 1 or y.get(i) == 1:
                        current_improvement = self.improvement(x, i) + self.improvement(y, i)
                        z_new = copy.deepcopy(z)
                        z_new.set(best_pos, 1)
                        z_new.set_defined(best_pos, 1)
                        if current_improvement < minimum_improvement and self.sat_crossover(z_new, clause):
                            minimum_improvement = current_improvement
                            best_pos = i
                if not best_pos == -1:
                    z.set(best_pos, 1)
                    z.set_defined(best_pos, 1)
        z.allocate(x, y)
        return z

    def standard_tabu_choose(self, assignment):
        """
        Choose function for the Tabu search. The best move (flips of value of an assignment) is chosen i.e.
        it is the best gain in flip and if it is not a tabu configuration.
        :param assignment: A particular individual (assignment of atoms).
        :return: A position (index) in the assignment due to which maximum gain is obtained.
        """

        # A list to maintain the position(s) where the gain (by flip) is the best. 
        positions = []
        # The current overall best gain observed. Initially, it is set to a large negative value.
        best_sigma = Decimal('-Infinity')
        # Iterate through each of the positions (atoms) of the individual.
        for position in assignment:
            # A copy of the original individual is made and the particular position of the copy is flipped.
            temp = copy.deepcopy(assignment)
            temp.flip(position)
            # If the move is not in the tabu list and the number of unsatisfied clauses in the copy is
            # better (lower) than that of the best_assignment, then we can consider this move as a possibility.
            if (position not in self.tabu) or (self.evaluate(temp) < self.evaluate(self.best)):
                # Calculate the gain in the fitness function.
                gain = self.improvement(assignment, position)
                # If a new best gain is found (greater than the previous best), then we empty the list
                # as the list should not include positions of the previous best gain.
                # The list will currently only include the position of the current move.
                if gain > best_sigma:
                    positions = []
                    best_sigma = gain
                    positions.append(position)
                # If the gain calculated is equal to the best gain calculated so far, we simply append the position.     
                elif gain == best_sigma:
                    positions.append(position)
            # This will only fire in the case that the we have not yet managed to find neither an individual who wasn't
            # in the tabu list nor one with a better evaluation in each iteration of the for loop above.
            elif best_sigma == Decimal('-Infinity'):
                positions.append(position)
        # Return a position that is randomly selected in those which have the maximum sigma 
        # i.e. out of those elements in the positions list.
        return random.choice(positions)    
    
    def standard_tabu(self, individual_in, choose_function):
        """
        Performs the standard Tabu algorithm.

        :param individual_in: An individual
        :param choose_function: A function object
        :return: An individual that conforms to the Tabu restrictions.
        """

        self.tabu = self.tabu[:self.tabu_list_length]
        self.best = individual_in
        num_flips = 0
        while not (self.evaluate(self.best) == 0 or num_flips > self.max_flip):
            # index = self.choose(individual_in)
            index = choose_function(individual_in)
            individual_temp = copy.deepcopy(individual_in)
            individual_temp.flip(index)
            if self.evaluate(individual_temp) < self.evaluate(self.best):
                self.best = individual_temp
            num_flips += 1

            if self.tabu:
                self.tabu.pop()
            self.tabu = [index] + self.tabu
        return self.best

    def choose_rvcf(self, individual_in):
        """

        :param individual_in:
        :return:
        """

        improvements = [self.improvement(individual_in, i) for i in range(1, individual_in.length + 1)]
        improvements = [(max(improvements), improvements.index(max(improvements)) + 1)]
        if len(improvements) == 1:
            return improvements[0][1]
        weights = [self.weight(individual_in, j) for j in improvements]
        return random.choice(weights)

    def weight(self, individual, index):
        """
        Calculates the weight of an individual in respects to some index.

        :param individual:
        :param index:
        :return: The weight value.
        """

        c_ones = [clause for clause in self.formula if (index in clause) and (individual.get(index) == 1)]
        c_zeros = [clause for clause in self.formula if (index in clause) and (individual.get(index) == 0)]

        return sum(self.degree(individual, c) for c in c_ones) / len(c_ones) + sum(self.degree(individual, c)
                                                                                   for c in c_zeros) / len(c_zeros)

    @staticmethod
    def degree(individual, clause):
        """
        Calculates the number of true atoms that appear in some clause, for some individual.

        :param individual: The individual for whom the True/False values will be obtained.
        :param clause: The clause to be tested.
        :return: A numerical value representing the degree.
        """

        l = [literal for literal in clause if individual.get(abs(literal)) == 1]
        return len(l)

    def tabu_with_diversification(self, individual):
        """
        Performs Tabu Search with measures to avoid "stumble clauses".

        :param individual:
        :return:
        """

        false_clauses = [self.formula[i] for i in range(len(self.formula)) if self.false_counts[i] >= self.max_false]
        individual_temp = copy.deepcopy(individual)
        forbidden_flips = {}
        for clause in false_clauses:
            self.check_flip(individual_temp, clause, forbidden_flips)
            for _ in range(self.rec):
                non_false_clauses = [self.formula[i] for i in range(len(self.formula))
                                     if self.sat(individual_temp, clause) and not self.sat(individual, clause)]
                for nested_clause in non_false_clauses:
                    self.check_flip(individual_temp, nested_clause, forbidden_flips)
        return individual_temp

    def check_flip(self, individual, clause, iteration_dict):
        """

        :param individual:
        :param clause: The clause
        :param iteration_dict:
        :return: Whether
        """

        temp_clause = [c for c in clause if c not in iteration_dict.keys()]
        try:
            index = max(temp_clause, key=lambda c: self.improvement(individual, c))[0]
        except ValueError as e:
            raise e
        pos = temp_clause[index]

        # Check if pos has been flipped before
        # flips this one stubborn bit and refuse to flip it back before k flips.
        if pos in iteration_dict.keys():
            # Check if pos has been flipped k times and remove it if it has
            # or increment it if it hasn't
            if iteration_dict[pos] < self.k:
                iteration_dict[pos] = iteration_dict[pos] + 1
                individual.flip(pos)
            else:
                del iteration_dict[pos]
        else:
            # Otherwise add pos to the dictionary with an initial count of 1
            iteration_dict[pos] = 1
            individual.flip(pos)

    def fluerent_and_ferland(self, x, y):
        """
        Performs the Fluerent & Ferland cross-over operator.

        :param x: The first parent parameter.
        :param y: The second parent parameter.
        :return: The generated individual z.
        """

        z = Individual(self.numberOfVariables, self.method, False)
        for clause in self.formula:
            if self.sat(x, clause) and not self.sat(y, clause):
                for i in range(len(clause)):
                    z.set(i, x(i))
                    z.set_defined(i, 1)
            elif not self.sat(x, clause) and self.sat(y, clause):
                for i in range(len(clause)):
                    z.set(i, y(i))
                    z.set_defined(i, 1)
        z.allocate(x, y)
        return z

    def select(self):
        """
        Selects two parents from a sub-population.
        :return: Two individuals child_x and child_y
        """

        self.population.sort(key=self.evaluate)
        self.sub_population = self.population[0:self.sub_population_size]
        child_x = random.choice(self.sub_population)
        child_y = random.choice(self.sub_population)
        while child_x == child_y:
            child_x = random.choice(self.sub_population)
        return child_x, child_y

    def create_population(self):
        """
        Creates a population of individuals (possible assignments of values to variables) of a specific size specified
        as a parameter to the genetic algorithm.
        :return: void (no return value)
        """

        individual_counter = 0
        while individual_counter < self.population_size:
            self.population.append(Individual(self.numberOfVariables))
            individual_counter = individual_counter + 1

        return

    def is_satisfied(self):
        """
        Determines whether or not there is a satisfying assignment.
        :return: An individual (assignment) or None.
        """
        for individual in self.population:
            if self.evaluate(individual) == 0:
                return individual
        return None

    def replace(self, child):
        """
        Replace the weakest individual in the sub-population (most number of unsatisfied clauses) with the newborn
        child. If the child is worse than the weakest individual, then no replacement is done.
        :return: void (NONE)
        """

        weakest_individual = max(self.sub_population, key=self.evaluate)
        if not self.evaluate(weakest_individual) > self.evaluate(child):
            self.population.remove(weakest_individual)
            self.population.append(child)

        return

    def gasat(self):
        """
        The GASAT algorithm
        :return:
        """

        # The GASAT Algorithm
        # -------------------------------------------------------------------------------------------------------------
        # A population of individuals is initialised
        self.create_population()

        # Counts the current number of iterations completed
        generation_counter = 0

        # An individual that satisfies the formula or None
        satisfied_individual = None

        # While no individual in the population satisfies the formula and while we have not reached the maximum
        # generation threshold
        while satisfied_individual is None and generation_counter < self.max_generations:
            # A sub-population of possible parents is selected and two individuals are randomly selected as parents
            parents = self.select()

            # A child is produced through reproduction - the method of reproduction is determined by the operator
            # parameter
            child = None
            if self.crossover_operator == 0:
                child = self.corrective_clause(parents[0], parents[1])
            elif self.crossover_operator == 1:
                child = self.corrective_clause_with_truth_maintenance(parents[0], parents[1])
            elif self.crossover_operator == 2:
                child = self.fluerent_and_ferland(parents[0], parents[1])

            # TODO: Complete Tabu Search
            if not self.is_rvcf:
                child = self.standard_tabu(child, self.standard_tabu_choose)
                if self.is_diversification:
                    child = self.tabu_with_diversification(child)
            else:
                child = self.standard_tabu(child, self.choose_rvcf)
                if self.is_diversification:
                    child = self.tabu_with_diversification(child)

            # TODO: Insertion Condition of the child
            self.replace(child)

            # Determine whether any individual that satisfies the formula appeared in the current generation
            satisfied_individual = self.is_satisfied()
            # Increase the generation
            generation_counter = generation_counter + 1

        # Return a satisfying assignment if there exists one
        if satisfied_individual is not None:
            return satisfied_individual
        else:
            # Sort the population by fitness value
            self.population.sort(key=self.evaluate)
            # The first individual in the sorted population has the lowest number of unsatisfied clauses - best
            # assignment found
            return self.population[0]

        # -------------------------------------------------------------------------------------------------------------

# Old Tests
# if __name__ == "__main__":
#     # TESTS
#     num_fail = 0
#     print("Testing SAT instance : f1000")
#     test_individual = GA("../examples/f1000.cnf")
#     if len(test_individual.formula) == test_individual.numberOfClauses:
#         print("    len(formula) == numberOfClauses => pass")
#     else:
#         print("    len(formula) == numberOfClauses => fail")
#         num_fail += 1
#     if test_individual.formula[0] == (119, 325, -401):
#         print("    formula[0] == (119, 325, -401) => pass")
#     else:
#         print("    formula[0] == (119, 325, -401) => fail")
#         num_fail += 1
#     if test_individual.formula[-1] == (-839, -494, 718):
#         print("    formula[-1] == (-839, -494, 718) => pass")
#     else:
#         print("    formula[-1] == (-839, -494, 718) => fail")
#         num_fail += 1
#
#     print()
#     print("Testing SAT instance : f2000")
#     test_individual = GA("../examples/f2000.cnf")
#     if len(test_individual.formula) == test_individual.numberOfClauses:
#         print("    len(formula) == numberOfClauses => pass")
#     else:
#         print("    len(formula) == numberOfClauses => fail")
#         num_fail += 1
#     if test_individual.formula[0] == (1295, 1303, -1372):
#         print("    formula[0] == (1295, 1303, -1372) => pass")
#     else:
#         print("    formula[0] == (1295, 1303, -1372) => fail")
#         num_fail += 1
#     if test_individual.formula[-1] == (1952, -450, 952):
#         print("    formula[-1] == (1952, -450, 952) => pass")
#     else:
#         print("    formula[-1] == (1952, -450, 952) => fail")
#         num_fail += 1
#
#     print()
#     print("Testing SAT instance : par16-4-c")
#     test_individual = GA("../examples/par16-4-c.cnf")
#     if len(test_individual.formula) == test_individual.numberOfClauses:
#         print("    len(formula) == numberOfClauses => pass")
#     else:
#         print("    len(formula) == numberOfClauses => fail")
#         num_fail += 1
#     if test_individual.formula[0] == (-2, 1):
#         print("    formula[0] == (-2, 1) => pass")
#     else:
#         print("    formula[0] == (-2, 1) => fail")
#         num_fail += 1
#     if test_individual.formula[-1] == (132, 324, -140):
#         print("    formula[-1] == (132, 324, -140) => pass")
#     else:
#         print("    formula[-1] == (132, 324, -140) => fail")
#         num_fail += 1
#
#     print()
#     print("Testing SAT instance : par32-5")
#     test_individual = GA("../examples/par32-5.cnf")
#     if len(test_individual.formula) == test_individual.numberOfClauses:
#         print("    len(formula) == numberOfClauses => pass")
#     else:
#         print("    len(formula) == numberOfClauses => fail")
#         num_fail += 1
#     if test_individual.formula[0] == (-1,):
#         print("    formula[0] == (-1,) => pass")
#     else:
#         print("    formula[0] == (-1,) => fail")
#         num_fail += 1
#     if test_individual.formula[-1] == (-3176,):
#         print("    formula[-1] == (-3176,) => pass")
#     else:
#         print("    formula[-1] == (-3176,) => fail")
#         num_fail += 1
#
#     print()
#     print("Testing SAT instance : par32-5-c")
#     test_individual = GA("../examples/par32-5-c.cnf")
#     if len(test_individual.formula) == test_individual.numberOfClauses:
#         print("    len(formula) == numberOfClauses => pass")
#     else:
#         print("    len(formula) == numberOfClauses => fail")
#         num_fail += 1
#     if test_individual.formula[0] == (-2, 1):
#         print("    formula[0] == (-2, 1) => pass")
#     else:
#         print("    formula[0] == (-2, 1) => fail")
#         num_fail += 1
#     if test_individual.formula[-1] == (450, -408, 1339):
#         print("    formula[-1] == (450, -408, 1339) => pass")
#     else:
#         print("    formula[-1] == (450, -408, 1339) => fail")
#         num_fail += 1
#
#     print("----------------------")
#     if num_fail == 0:
#         print("Passed all tests.")
#     else:
#         print(str(num_fail) + " tests failed.")