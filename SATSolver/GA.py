"""
    Module: GA
    Description: Defines the genetic algorithm and all the core functionality of it, including crossover and Tabu search
"""

import copy
import random
import operator
from decimal import Decimal
from SATSolver.individual import Individual, Factory


class GAStop(Exception):
    """This exception should be raised when GA should stop"""


class GA:
    def __init__(self, formula, number_of_clauses, number_of_variables, tabu_list_length, max_false, rec, k,
                 max_generations=1000, population_size=100, sub_population_size=15, crossover_operator=0,
                 max_flip=10000, is_rvcf=False, is_diversification=False, method=None):

        self.formula = formula
        self.numberOfClauses = int(number_of_clauses)
        self.numberOfVariables = int(number_of_variables)
        # Creating member variables for each of the parameters
        self.max_generations = int(max_generations)
        # TODO: Test for minimum possible size. It is at least 2
        self.population_size = int(population_size)
        # TODO: Set sub-population size default to some percentage - May NOT be smaller than 2 because of crossover
        self.sub_population_size = int(sub_population_size)

        # Alias one of the crossover operators as a method called crossover_operator
        if crossover_operator == 0:
            self.crossover_operator = self.corrective_clause
        elif crossover_operator == 1:
            self.crossover_operator = self.corrective_clause_with_truth_maintenance
        else:
            self.crossover_operator = self.fluerent_and_ferland

        # TODO: Check that length is not greater than the population length
        self.tabu_list_length = int(tabu_list_length)
        self.max_flip = int(max_flip)
        self.is_rvcf = bool(is_rvcf)
        self.is_diversification = bool(is_diversification)
        self.max_false = int(max_false)
        self.rec = int(rec)
        self.k = int(k)
        self.method = method
        self._observers = set()
        self._generation_counter = None
        # TODO: Remove these 2 attributes. Best individual is always population[0]
        self.best_individual_fitness = None
        self.best_individual = None
        self.current_child_fitness = None
        self.current_child = None

        self.stop = False

        # Initialize tabu, population and the sub_population to empty lists
        self.tabu = []
        self.population = []
        self.sub_population = []

        # Used in tabu search to determine best configuration/move
        self.best = None

        self.false_counts = [0 for _ in self.formula]

    @staticmethod
    def sat(individual, clause):
        """
        sat (X,c) - by literature
        Indicates whether the clause c is true or false for the individual X i.e. satisfied or not by the assignment
        corresponding to X.
        :param individual: Individual class representing a particular assignment of truth values
        to variables.
        :param clause: Python tuple of integers - should be the same tuple as in the DIMACS format.
        :return: returns a boolean value indicating whether the assignment represented by the individual satisfies the
        clause.
        """

        # Iterate over atoms in the clause
        for atom in clause:
            if (atom > 0 and individual.get(atom)) or (atom <= 0 and individual.get(abs(atom)) == 0):
                return True
        return False

    # @staticmethod
    # def sat_crossover(individual, clause):
    #     """
    #     sat (X,c) - by literature
    #     Indicates whether the clause c is true or false for the individual X i.e. satisfied or not by the assignment
    #     corresponding to X - Particular to crossovers as it takes into account whether there are undefined variables
    #     used in the clause - if so, the clause is not satisfied.
    #     to variables.
    #     :param clause: Python tuple of integers - should be the same tuple as in the DIMACS format.
    #     :return: returns a boolean value indicating whether the assignment represented by the individual satisfies the
    #     clause.
    #     """
    #
    #     # Iterate over atoms in the clause
    #     for atom in clause:
    #         # IF the atom is not negated
    #         if atom > 0:
    #             # The Clause is unsatisfiable on seeing an undefined variable.
    #             if individual.get_defined(atom) is False:
    #                 return False
    #             if individual.get(atom):
    #                 # The clause is satisfiable on seeing the first true atom
    #                 return True
    #         # IF the atom is negated
    #         else:
    #             # The Clause is unsatisfiable on seeing an undefined variable.
    #             if individual.get_defined(abs(atom)) is False:
    #                 return False
    #             if individual.get(abs(atom)) == 0:
    #                 # The clause is satisfiable on seeing the first false atom due to it being a negation
    #                 return True
    #     # Clause is unsatisfiable - no true atoms
    #     return False

    def evaluate(self, individual):
        """
        The fitness of individual with respect to the formula.
        :param individual: Individual class (Implemented by Regan) representing a particular assignment of truth values
        to variables.
        :return: the number of clauses of F which are not satisfied by X.
        """

        if self.stop:
            raise GAStop("GA needs to be stopped.")

        if individual.isCacheValid:
            return individual.fitness

        individual.isCacheValid = True

        # Keeps count of unsatisfied clauses
        num_unsatisfied_clauses = 0

        # Iterate over clauses in the formula
        for clause in self.formula:

            # If a clause is unsatisfied increase the unsatisfied counter
            if not self.sat(individual, clause):
                num_unsatisfied_clauses = num_unsatisfied_clauses + 1

        individual.fitness = num_unsatisfied_clauses
        return num_unsatisfied_clauses

    def improvement(self, individual, index):
        """
        The function computes the improvement (difference in unsatisfiable clauses) obtained by the flip of the ith
        variable of the individual.
        :param individual: Individual class (Implemented by Regan) representing a particular assignment of truth values
        to variables.
        :param index: index of a bit (starts at 1 - as per clause numbering in DIMACS format). Boundary checking is
        not performed
        :return: computed improvement value.
        """

        new_individual = copy.deepcopy(individual)
        # Flip the bit at the specified index
        new_individual.flip(abs(index))

        # Calculate improvement in fitness
        return individual.fitness - self.evaluate(new_individual)

    def corrective_clause(self, x, y):
        """
        Performs the corrective clause cross-over.

        :param x: The first parent parameter.
        :param y: The second parent parameter.
        :return: The generated individual z
        """

        z = Individual(self.numberOfVariables, self.method, parents=(x, y))
        clauses = [i for i in range(self.numberOfClauses) if
                   not self.sat(x, self.formula[i]) and not self.sat(y, self.formula[i])]
        for index in clauses:
            clause = self.formula[index]
            best_pos = 0
            best_improvement = 0
            for i in range(len(clause)):
                # Find best index to flip in current clause. Absolute value of index must be used
                current_improvement = self.improvement(x, abs(clause[i])) + self.improvement(y, abs(clause[i]))
                if current_improvement >= best_improvement:
                    best_improvement = current_improvement
                    best_pos = abs(clause[i])
            if best_pos != 0:
                # TODO: Check if we could perhaps use 1 - x.get(best_pos) to avoid the flip
                z.set(best_pos, x.get(best_pos))
                z.flip(best_pos)
        return z
        # for clause in self.formula:
        #     best_pos = 0
        #     best_improvement = 0
        #     if not self.sat(x, clause) and not self.sat(y, clause):
        #         for i in range(len(clause)):
        #             # Find best index to flip in current clause. Absolute value of index must be used
        #             current_improvement = self.improvement(x, abs(clause[i])) + self.improvement(y, abs(clause[i]))
        #             if current_improvement >= best_improvement:
        #                 best_improvement = current_improvement
        #                 best_pos = abs(clause[i])
        #         if best_improvement != 0:
        #             z.set(best_pos, x.get(best_pos))
        #             z.flip(best_pos)
        # return z

    def corrective_clause_with_truth_maintenance(self, x, y):
        """
        Performs the CCTM cross-over operator.

        :param x: The first parent parameter.
        :param y: The second parent parameter.
        :return: The generated individual z
        """

        z = Individual(self.numberOfVariables, self.method, parents=(x, y))
        for clause in self.formula:
            best_pos = 0
            maximum_improvement = 0
            if not self.sat(x, clause) and not self.sat(y, clause):
                for i in range(len(clause)):
                    current_improvement = self.improvement(x, abs(clause[i])) + self.improvement(y, abs(clause[i]))
                    if current_improvement >= maximum_improvement:
                        maximum_improvement = current_improvement
                        best_pos = abs(clause[i])
                if maximum_improvement != 0:
                    z.set(best_pos, x.get(best_pos))
                    z.flip(best_pos)

        # Truth maintenance - See section 4.2 of the paper
        for clause in self.formula:
            best_pos = -1
            minimum_improvement = self.numberOfClauses + 1
            if self.sat(x, clause) and self.sat(y, clause) and not self.sat(z, clause):
                for i in range(len(clause)):
                    if x.get(abs(clause[i])) == 1 or y.get(abs(clause[i])) == 1:
                        current_improvement = self.improvement(x, abs(clause[i])) + self.improvement(y, abs(clause[i]))
                        z_new = copy.deepcopy(z)
                        z_new.set(abs(clause[i]), 1)
                        if current_improvement < minimum_improvement and self.sat(z_new, clause):
                            minimum_improvement = current_improvement
                            best_pos = abs(clause[i])
                if not best_pos == -1:
                    z.set(best_pos, 1)
        return z

    def fluerent_and_ferland(self, x, y):
        """
        Performs the Fluerent & Ferland crossover operator.

        :param x: The first parent parameter.
        :param y: The second parent parameter.
        :return: The generated individual z.
        """

        z = Individual(self.numberOfVariables, self.method, parents=(x, y))
        for clause in self.formula:
            if self.sat(x, clause) and not self.sat(y, clause):
                for i in range(len(clause)):
                    z.set(abs(clause[i]), x(abs(clause[i])))
            elif not self.sat(x, clause) and self.sat(y, clause):
                for i in range(len(clause)):
                    z.set(abs(clause[i]), y(abs(clause[i])))
        return z

    def standard_tabu_choose(self, assignment):
        """
        Choose function for the Tabu search. The best move (flips of value of an assignment) is chosen i.e.
        it is the best gain in flip and if it is not a tabu configuration.
        :param assignment: A particular individual (assignment of atoms).
        :return: A position (index) in the assignment due to which maximum gain is obtained and the array of positions
        from which it was randomly chosen.
        """
        # TODO: We can use one temp and just do flips on that - Might be faster than all these deep copies
        # A list to maintain the position(s) where the gain (by flip) is the best. 
        positions = []
        # The current overall best gain observed. Initially, it is set to a large negative value.
        best_sigma = Decimal('-Infinity')
        # Iterate through each of the positions (atoms) of the individual.
        for position in range(1, len(assignment.data) + 1):
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
        # Also return the positions list for the purposes of testing
        return random.choice(positions), positions

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
        while (self.evaluate(self.best) != 0) and (self.max_flip > num_flips):
            # index = self.choose(individual_in)
            index = choose_function(individual_in)
            individual_temp = copy.deepcopy(individual_in)
            if not index[0] in self.tabu:
                individual_temp.flip(index[0])
                if self.evaluate(individual_temp) < self.evaluate(self.best):
                    self.best = individual_temp
                num_flips += 1
                individual_in = individual_temp
            if self.is_diversification:
                self.tabu_with_diversification(individual_in)
        return self.best

    def choose_rvcf(self, individual_in):
        """

        :param individual_in:
        :return:
        """

        positions = []
        best_sigma = Decimal('-Infinity')
        for position in range(1, len(individual_in.data) + 1):
            gain = self.improvement(individual_in, position)
            if gain > best_sigma:
                positions = []
                best_sigma = gain
                positions.append(position)
            elif gain == best_sigma:
                positions.append(position)

        best_sigma = Decimal('-Infinity')
        max_weights = []
        for j in positions:
            weight = self.weight(individual_in, j)
            if weight > best_sigma:
                max_weights = []
                best_sigma = weight
                max_weights.append(j)
            elif weight == best_sigma:
                max_weights.append(j)

        return random.choice(max_weights), max_weights

    def weight(self, individual, index):
        """
        Calculates the weight of an individual in respects to some index.

        :param individual:
        :param index:
        :return: The weight value.
        """

        c_ones = [clause for clause in self.formula if (index in clause or -index in clause) and
                  (individual.get(index) == 1)]
        c_zeros = [clause for clause in self.formula if (index in clause or -index in clause) and
                   (individual.get(index) == 0)]

        length_c_ones = len(c_ones)
        length_c_zeros = len(c_zeros)

        sum_ones = sum(self.degree(individual, c) for c in c_ones)
        sum_zeros = sum(self.degree(individual, c) for c in c_zeros)

        # To cater for the case where the length is 0
        ratio_ones = 0
        ratio_zeros = 0
        if length_c_ones > 0:
            ratio_ones = sum_ones / length_c_ones

        if length_c_zeros > 0:
            ratio_zeros = sum_zeros / length_c_zeros

        return ratio_ones + ratio_zeros

    @staticmethod
    def degree(individual, clause):
        """
        Calculates the number of true atoms that appear in some clause, for some individual.

        :param individual: The individual for whom the True/False values will be obtained.
        :param clause: The clause to be tested.
        :return: A numerical value representing the degree.
        """

        list_of_literals = []
        for literal in clause:
            if literal > 0:
                if individual.get(literal) == 1:
                    list_of_literals.append(literal)
            else:
                if individual.get(abs(literal)) == 0:
                    list_of_literals.append(literal)

        return len(list_of_literals)

    def tabu_with_diversification(self, individual):
        """
        Performs Tabu Search with measures to avoid "stumble clauses".

        :param individual:
        :return:
        """

        false_clauses = []

        for i in range(len(self.formula)):
            if not self.sat(individual, self.formula[i]):
                self.false_counts[i] += 1
                if self.false_counts[i] == self.max_false:
                    false_clauses.append(self.formula[i])
                    self.false_counts[i] = 0

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
            value = max(temp_clause, key=lambda c: self.improvement(individual, c))
        except ValueError as e:
            raise e
        pos = abs(value)

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

    def select(self):
        """
        Selects two parents from a sub-population.
        :return: Two individuals child_x and child_y
        """
        self.sub_population = self.population[0:self.sub_population_size]
        child_x, child_y = random.sample(self.sub_population, 2)
        return child_x, child_y

    def create_population(self):
        """
        Creates a population of individuals (possible assignments of values to variables) of a specific size specified
        as a parameter to the genetic algorithm.
        :return: void (no return value)
        """

        self.population = Factory.create(self.numberOfVariables, self.population_size)
        # Initial sort of the population. This also calls evaluate and therefore every individual has a stored
        # fitness value
        self.population.sort(key=self.evaluate)
        return

    def is_satisfied(self):
        """
        Determines whether or not there is a satisfying assignment.
        :return: An individual (assignment) or None.
        """
        # TODO: Change this check only the first individual in the population
        # for individual in self.population:
        #     if self.evaluate(individual) == 0:
        #         return individual
        # return None
        if self.population[0].fitness == 0:
            return True
        else:
            return False

    def replace(self, child):
        """
        Replace the weakest individual in the sub-population (most number of unsatisfied clauses) with the newborn
        child. If the child is worse than the weakest individual, then no replacement is done.
        :return: void (NONE)
        """
        # Change this to get rid of the sort - Do an insertion sort
        self.population.sort(key=operator.attrgetter("fitness"))
        self.best_individual_fitness = self.population[0].fitness
        self.best_individual = self.population[0]
        if self.population[0].fitness > child.fitness:
            # self.population.remove(self.population[len(self.population)-1])
            # self.population.append(child)
            self.population[-1] = child

        # if self.sub_population[-1].fitness > child.fitness:
        #     return
        # self.population[-1] = child
        # # Python's timsort makes this efficient as the population is almost already sorted. Use the saved fitness of
        # # each individual instead of calling evaluate. For more on timsort, see:
        # # http://svn.python.org/projects/python/trunk/Objects/listsort.txt
        # self.population.sort(key=operator.attrgetter("fitness"))
        # self.best_individual_fitness = self.population[0].fitness
        # self.best_individual = self.population[0]
        # return

    def gasat(self):
        """
        The GASAT algorithm
        :return:
        """

        # The GASAT Algorithm
        # -------------------------------------------------------------------------------------------------------------
        # A population of individuals is initialised. The population is ordered by fitness
        self.create_population()

        # Counts the current number of iterations completed
        self.generation_counter = 0

        # While no individual in the population satisfies the formula and while we have not reached the maximum
        # generation threshold
        while self._generation_counter < self.max_generations and not self.is_satisfied():
            # A sub-population of possible parents is selected and two individuals are randomly selected as parents
            parents = self.select()

            # A child is produced through reproduction - the method of reproduction is determined by the operator
            # parameter
            child = self.crossover_operator(parents[0], parents[1])
            # elif self.crossover_operator == 1:
            #     child = self.corrective_clause_with_truth_maintenance(parents[0], parents[1])
            # elif self.crossover_operator == 2:
            #     child = self.fluerent_and_ferland(parents[0], parents[1])

            if not self.is_rvcf:
                child = self.standard_tabu(child, self.standard_tabu_choose)
            else:
                child = self.standard_tabu(child, self.choose_rvcf)

            # TODO: Current_child_fitness is redundant as we can just use current_child.fitness instead
            self.current_child_fitness = child.fitness
            self.current_child = child
            self.replace(child)

            # Increase the generation
            self.generation_counter += 1

        return self.population[0]

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)

    def detach(self, observer):
        observer._subject = None
        self._observers.discard(observer)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._generation_counter)

    @property
    def generation_counter(self):
        return self._generation_counter

    @generation_counter.setter
    def generation_counter(self, arg):
        self._generation_counter = arg
        self._notify()
