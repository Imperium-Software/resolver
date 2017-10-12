import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
print(myPath)
sys.path.insert(0, myPath + '/../SATSolver')
from GA import GA
from unittest import TestCase
from individual import Individual
from bitarray import bitarray


class TestGA(TestCase):

    class FormulaReader:

        def __init__(self, filename):
            filename = os.path.join(os.path.dirname(__file__), filename)
            f = open(filename, "r")
            # Read all the lines from the file that aren't comments
            lines = [line.replace("\n", "") for line in f.readlines() if line[0] != "c" and line.strip() != ""]
            (self.numberOfVariables, self.numberOfClauses) = int(lines[0].split()[2]), int(lines[0].split()[3])
            self.formula = []

            # Go through the lines and create numberOfClauses clauses
            line = 1
            # for line in range(1, len(lines)):
            while line < len(lines):
                clause = []
                # We need a while loop as a clause may be split over many lines, but eventually ends with a 0
                end_of_clause = False
                while line < len(lines) and not end_of_clause:
                    # Split the line and append a list of all integers, excluding 0, to clause
                    clause.append(
                        [int(variable.strip()) for variable in lines[line].split() if int(variable.strip()) != 0])
                    # If this line ended with a 0, we reached the end of the clause
                    if int(lines[line].split()[-1].strip()) == 0:
                        end_of_clause = True
                        line += 1
                    # Otherwise continue reading this clause from the next line
                    else:
                        line += 1
                # clause is now a list of lists, so we need to flatten it and convert it to a list
                self.formula.append(tuple([item for sublist in clause for item in sublist]))
            f.close()

    def test_sat(self):
        ind = Individual(9)
        ind.data = bitarray("000100000")
        self.assertEqual(GA.sat(ind, [9, -5]), True)
        self.assertEqual(GA.sat(ind, [1, 3, 6]), False)
        ind.data = bitarray("111111111")
        self.assertEqual(GA.sat(ind, [-6, -4]), False)

    def test_evaluate(self):
        reader = self.FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = bitarray("111111111")
        ind.isCacheValid = False
        self.assertEqual(ga.evaluate(ind), 1)
        ind.data = bitarray("111111110")
        ind.isCacheValid = False
        self.assertEqual(ga.evaluate(ind), 2)
        ind.data = bitarray("111111110")
        ind.isCacheValid = False
        self.assertEqual(ga.evaluate(ind), 2)

    def test_evaluate_unsolvable(self):
        reader = self.FormulaReader("../examples/trivial3.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.isCacheValid = False
        self.assertTrue(ga.evaluate(ind) != 0, "Evaluate says unsolvable formula is solved.")

    def test_improvement(self):
        reader = self.FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = bitarray("000100000")
        self.assertEqual(ga.improvement(ind, 1), 1)
        self.assertEqual(ga.improvement(ind, 6), 1)
        ind.flip(6)
        self.assertEqual(ga.improvement(ind, 6), -1)

    def test_corrective_clause(self):
        # Read the trivial example and create a GA instance
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # Create two individuals for which we know what the outcome should be
        first_parent = Individual(9)
        first_parent.data = bitarray("000111000")
        second_parent = Individual(9)
        second_parent.data = bitarray("001110000")
        # Perform crossover to get the child
        child = ga.corrective_clause(first_parent, second_parent)
        # Assert that crossover was correctly performed
        self.assertEqual(child.get(1), 0)
        self.assertEqual(child.get(2), 0)
        self.assertEqual(child.get(4), 1)
        self.assertEqual(child.get(5), 1)
        self.assertEqual(child.get(7), 0)
        self.assertEqual(child.get(8), 0)
        self.assertEqual(child.get(9), 0)

    def test_corrective_clause_with_truth_maintenance(self):
        # Read the trivial example and create a GA instance
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # Create two individuals for which we know what the outcome should be
        first_parent = Individual(9)
        first_parent.data = bitarray("000111000")
        second_parent = Individual(9)
        second_parent.data = bitarray("001110000")
        # Perform crossover to get the child
        child = ga.corrective_clause_with_truth_maintenance(first_parent, second_parent)
        # Force the truth maintenance code to run by setting bits 3 and 6 to zero
        # Assert that crossover was correctly performed
        self.assertEqual(child.get(1), 0)
        self.assertEqual(child.get(2), 0)
        # self.assertEqual(child.get(3), 1) # 3 should be set to 1
        self.assertEqual(child.get(4), 1)
        self.assertEqual(child.get(5), 1)
        self.assertEqual(child.get(7), 0)
        self.assertEqual(child.get(8), 0)
        self.assertEqual(child.get(9), 0)

    def test_fluerent_and_ferland(self):
        # Read the trivial example and create a GA instance
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # Create two individuals for which we know what the outcome should be
        first_parent = Individual(9)
        first_parent.data = bitarray("001101011")
        second_parent = Individual(9)
        second_parent.data = bitarray("001110111")
        # Perform crossover to get the child
        child = ga.fluerent_and_ferland(first_parent, second_parent)
        # Assert that crossover was correctly performed
        self.assertEqual(child.get(1), 0)
        self.assertEqual(child.get(2), 0)
        self.assertEqual(child.get(3), 1)
        self.assertEqual(child.get(4), 1)
        self.assertEqual(child.get(6), 0)
        self.assertEqual(child.get(8), 1)
        self.assertEqual(child.get(9), 1)

    def test_standard_tabu_choose(self):
        # TEST 1 - All positions are tabu and best is the same as the individual........................................
        # An instance of the GA class which will be used to test the standard_tabu_choose function
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # The tabu list is set to the size which was received as parameter i.e. [5]
        ga_implementation.tabu = ga_implementation.tabu[:ga_implementation.tabu_list_length]
        # Every single position is tabu
        for index in range(1, 10, 1):
            ga_implementation.tabu.append(index)

        # Creating an individual that will represent the best individual during a tabu search procedure
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = bitarray("000100000")
        ga_implementation.best = ind

        # Creating an individual that will represent another individual for which we want to find best flip for
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = bitarray("000100000")
        # A test
        self.assertEqual(ga_implementation.standard_tabu_choose(ind)[1], [1, 2, 4, 6])
        # .............................................................................................................

        # TEST 2 - All positions are tabu and best individual is guaranteed to be better................................

        file_reader = self.FormulaReader("../examples/trivial2.cnf")
        ga_implementation = GA(file_reader.formula, 1, 3, 5, 5, 5, 5)
        ga_implementation.tabu = ga_implementation.tabu[:ga_implementation.tabu_list_length]

        for index in range(1, 4, 1):
            ga_implementation.tabu.append(index)

        ind = Individual(3)
        ind.data = bitarray("111")
        ga_implementation.best = ind

        ind = Individual(3)
        ind.data = bitarray("000")
        self.assertEqual(ga_implementation.standard_tabu_choose(ind)[1], [1, 2, 3])
        # .............................................................................................................

    def test_standard_tabu(self):
        # # # Test 1 - Satisfying assignment Passed - Nothing to intensify..................................................
        # # # An instance of the GA class which will be used to test the standard_tabu function
        # #
        # file_reader = self.FormulaReader("../examples/trivial.cnf")
        # ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # # Creating an individual that will represent the individual we want to intensify using tabu search
        # ind = Individual(9)
        # # Individual is assigned values for variables to overwrite the random initialisation
        # ind.data = BitVector(bitlist=[0, 0, 0, 0, 0, 1, 1, 1, 1])
        # # Test whether if a satisfying assignment is passed, then that assignment should be returned as best
        # ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        # self.assertEqual(list(ind.data), list(BitVector(bitlist=[0, 0, 0, 0, 0, 1, 1, 1, 1])))
        # # # .............................................................................................................
        # # # Test 2 - Max Number of Flips is Zero..........................................................................
        # file_reader = self.FormulaReader("../examples/trivial.cnf")
        # ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5, max_flip=0)
        # ind = Individual(9)
        # ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        # ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        # self.assertEqual(list(ind.data), list(BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])))
        # # # .............................................................................................................
        # # # Test 3 - No diversification..................................................................................
        # file_reader = self.FormulaReader("../examples/trivial.cnf")
        # ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5, is_diversification=False)
        # ind = Individual(9)
        # ind.data = bitarray(1, 1, 1, 1, 1, 1, 1, 1, 1])
        # ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        # if (list(ind.data) == list(bitarray(1, 1, 1, 0, 1, 1, 1, 1, 1])) or
        #         list(ind.data) == list(bitarray(1, 1, 1, 1, 1, 0, 1, 1, 1]))):
        #     self.assertEqual(1, 1)
        # else:
        #     self.assertEqual(1, 0)
        #
        # # # .............................................................................................................
        # # # Test 4 - No diversification - complex..................................................................................
        # file_reader = self.FormulaReader("../examples/trivial.cnf")
        # ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5, is_diversification=False)
        # ind = Individual(9)
        # ind.data = BitVector(bitlist=[0, 0, 0, 1, 1, 0, 0, 0, 0])
        # ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        # if ind.fitness == 0:
        #     self.assertEqual(1, 1)
        # else:
        #     self.assertEqual(1, 0)
        # # .............................................................................................................
        # # Test 5 - Real non diversification.....................................................................................
        # file_reader = self.FormulaReader("../examples/par16-4-c.cnf")
        # ga_implementation = GA(file_reader.formula, 1292, 324, 10, 5, 5, 5, max_flip=20)
        # ind = Individual(324)
        # val1 = ga_implementation.evaluate(ind)
        # ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        # val2 = ga_implementation.evaluate(ind)
        # if val2 < val1:
        #     self.assertEqual(1, 1)
        # else:
        #     self.assertEqual(1, 0)
        # ..................................................................................................
        # .............................................................................................................
        # Test 6 - Diversification.....................................................................................
        from pympler.tracker import SummaryTracker
        tracker = SummaryTracker()

        try:
            file_reader = self.FormulaReader("../examples/par16-4-c.cnf")
            ga_implementation = GA(file_reader.formula, 1292, 324, 10, 5, 5, 5, max_flip=50, is_diversification=True)
            ind = Individual(324)
            val1 = ga_implementation.evaluate(ind)
            ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
            val2 = ga_implementation.evaluate(ind)
            if val2 < val1:
                self.assertEqual(1, 1)
            else:
                self.assertEqual(1, 0)
        finally:
            tracker.print_diff()
        # .............................................................................................................

    def test_choose_rvcf(self):

        # An instance of the GA class which will be used to test the standard_tabu_choose function
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # Creating an individual that will represent the best individual during a tabu search procedure
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = bitarray("000000000")
        # A test
        self.assertEqual(ga_implementation.choose_rvcf(ind)[1], [6])

        file_reader = self.FormulaReader("../examples/trivial2.cnf")
        ga_implementation = GA(file_reader.formula, 1, 3, 5, 5, 5, 5)
        ind.data = bitarray("000")
        self.assertEqual(ga_implementation.choose_rvcf(ind)[1], [1, 2, 3])

    def test_weight(self):

        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        ind = Individual(9)
        ind.data = bitarray("000000000")
        self.assertEqual(ga_implementation.weight(ind, 4), 1.5)
        ind.data = bitarray("111111111")
        self.assertEqual(ga_implementation.weight(ind, 4), 1)
        ind.data = bitarray("111010101")
        self.assertEqual(ga_implementation.weight(ind, 4), 2)

    def test_degree(self):
        ind = Individual(9)
        ind.data = bitarray("100100000")
        self.assertEqual(GA.degree(ind, [9, -5]), 1)
        self.assertEqual(GA.degree(ind, [1, 3, 6]), 1)
        ind.data = bitarray("000000110")
        self.assertEqual(GA.degree(ind, [7, 8, -3]), 3)

    def test_tabu_with_diversification(self):
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        ga_implementation.tabu = [0, 0, 0, 0, 5]
        ind = Individual(9)
        ind.data = bitarray("111111111")
        ga_implementation.tabu_with_diversification(ind)

        self.assertEqual(1, 1)

    def test_check_flip(self):
        file_reader = self.FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        forbidden_flips = {}
        ind = Individual(9)
        ind.data = bitarray("111111111")
        ga_implementation.check_flip(ind, ga_implementation.formula[4], forbidden_flips)
        self.assertEqual(ind.data, bitarray("111110111"))

    def test_select(self):
        self.assertEqual(1, 1)

    def test_create_population(self):
        self.assertEqual(1, 1)

    def test_is_satisfied(self):
        reader = self.FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = bitarray("000000000")
        ind.isCacheValid = False
        ga.population = [ind for _ in range(100)]

        # There should not be a satisfiable assignment.
        self.assertIsNone(ga.is_satisfied())

        ga.population[0].data = bitarray("111011111")
        ga.population[0].isCacheValid = False

        # Population now has one satisfying assignment.
        self.assertIsNotNone(ga.is_satisfied())

    def test_replace(self):
        self.assertEqual(1, 1)

    def test_gasat(self):
        self.assertEqual(1, 1)
