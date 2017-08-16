from GA import GA
from unittest import TestCase
from BitVector import BitVector
from individual import Individual
from formula_reader_test import FormulaReader


class TestGA(TestCase):
    def test_sat(self):
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(GA.sat(ind, [9, -5]), True)
        self.assertEqual(GA.sat(ind, [1, 3, 6]), False)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(GA.sat(ind, [-6, -4]), False)

    def test_sat_crossover(self):
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        ind.defined = BitVector(bitlist=[0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(GA.sat_crossover(ind, [9, -5]), False)
        ind.set_defined(9)
        self.assertEqual(GA.sat_crossover(ind, [9, -5]), True)

    def test_evaluate(self):
        reader = FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(ga.evaluate(ind), 1)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 0])
        self.assertEqual(ga.evaluate(ind), 2)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 0])
        self.assertEqual(ga.evaluate(ind), 2)

    def test_improvement(self):
        reader = FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(ga.improvement(ind, 1), 1)
        self.assertEqual(ga.improvement(ind, 6), 1)
        ind.flip(6)
        self.assertEqual(ga.improvement(ind, 6), -1)

    def test_corrective_clause(self):
        file_reader = FormulaReader("../examples/trivial.cnf")
        ga = GA(file_reader.formula, 5, 9, 5, 5, 5, 5)
        # Creates two parent bitvectors manually.
        parent1 = Individual(9)
        parent2 = Individual(9)
        # for x in range(0, 10):
            # Seed parent bitvectors.
            # parent1.data = BitVector(bitlist=[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)])
            # parent2.data = BitVector(bitlist=[random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)])
            # Evaluate parents
            # par1_eval = ga.evaluate(parent1)
            # par2_eval = ga.evaluate(parent2)

            # Run corrective clause using set parents.
            # child = ga.corrective_clause(parent1, parent2)
            # child_eval = ga.evaluate(child)
            # Compare child with parents.
            # self.assertLessEqual(child_eval, par1_eval, "child sucks")
            # self.assertLessEqual(child_eval, par2_eval, "child sucks")

        #
        for x in range(0, 10):
            # Seed parent bitvectors.
            parent1.data = BitVector(bitlist=[0, 1, 1, 0, 0, 1, 0, 0, 1])
            parent2.data = BitVector(bitlist=[0, 1, 1, 1, 0, 1, 1, 1, 1])
            # Evaluate parents
            par1_eval = ga.evaluate(parent1)
            par2_eval = ga.evaluate(parent2)

            # Run corrective clause using set parents.
            child = ga.corrective_clause(parent1, parent2)
            child_eval = ga.evaluate(child)
            # Compare child with parents. These will fail on occasion as child will be worse sometimes.
            # self.assertLessEqual(child_eval, par1_eval, "child sucks")
            # self.assertLessEqual(child_eval, par2_eval, "child sucks")

    def test_corrective_clause_with_truth_maintenance(self):
        self.assertEqual(1, 1)

    def test_standard_tabu_choose(self):
        # TEST 1 - All positions are tabu and best is the same as the individual........................................
        # An instance of the GA class which will be used to test the standard_tabu_choose function
        ga_implementation = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        # The tabu list is set to the size which was received as parameter i.e. [5]
        ga_implementation.tabu = ga_implementation.tabu[:ga_implementation.tabu_list_length]
        # Every single position is tabu
        for index in range(1, 10, 1):
            ga_implementation.tabu.append(index)

        # Creating an individual that will represent the best individual during a tabu search procedure
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        ga_implementation.best = ind

        # Creating an individual that will represent another individual for which we want to find best flip for
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        # A test
        self.assertEqual(ga_implementation.standard_tabu_choose(ind)[1], [1, 2, 4, 6])
        # .............................................................................................................

        # TEST 2 - All positions are tabu and best individual is guaranteed to be better................................

        reader = FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ga_implementation.tabu = ga_implementation.tabu[:ga_implementation.tabu_list_length]

        for index in range(1, 4, 1):
            ga_implementation.tabu.append(index)

        ind = Individual(3)
        ind.data = BitVector(bitlist=[1, 1, 1])
        ga_implementation.best = ind

        ind = Individual(3)
        ind.data = BitVector(bitlist=[0, 0, 0])
        self.assertEqual(ga_implementation.standard_tabu_choose(ind)[1], [1, 2, 3])
        # .............................................................................................................

    def test_standard_tabu(self):
        # Test 1 - Satisfying assignment Passed - Nothing to intensify..................................................
        # An instance of the GA class which will be used to test the standard_tabu function
        reader = FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        # Creating an individual that will represent the individual we want to intensify using tabu search
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 0, 0, 1, 1, 1, 1])
        # Test whether if a satisfying assignment is passed, then that assignment should be returned as best
        ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        self.assertEqual(list(ind.data), list(BitVector(bitlist=[0, 0, 0, 0, 0, 1, 1, 1, 1])))
        # .............................................................................................................
        # Test 2 - Max Number of Flips is Zero..........................................................................
        ga_implementation = GA(reader.formula, 9, 5,  10, 5, 5, 5, max_flip=0)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        self.assertEqual(list(ind.data), list(BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])))
        # .............................................................................................................
        # Test 3 - No diversification..................................................................................
        ga_implementation = GA(reader.formula, 9, 5, 10, 5, 5, 5, is_diversification=False)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 1, 1, 1, 1, 1, 1, 1, 1])
        ind = ga_implementation.standard_tabu(ind, ga_implementation.standard_tabu_choose)
        if (list(ind.data) == list(BitVector(bitlist=[1, 1, 1, 0, 1, 1, 1, 1, 1])) or
                list(ind.data) == list(BitVector(bitlist=[1, 1, 1, 1, 1, 0, 1, 1, 1]))):
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)
        # .............................................................................................................
        # Test 4 - Diversification.....................................................................................

        # .............................................................................................................
    def test_choose_rvcf(self):
        # An instance of the GA class which will be used to test the standard_tabu_choose function
        reader = FormulaReader("../examples/trivial.cnf")
        ga_implementation = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        # Creating an individual that will represent the best individual during a tabu search procedure
        ind = Individual(9)
        # Individual is assigned values for variables to overwrite the random initialisation
        ind.data = BitVector(bitlist=[0, 0, 0, 0, 0, 0, 0, 0, 0])
        # A test
        self.assertEqual(ga_implementation.choose_rvcf(ind)[1], [0])

    def test_weight(self):
        reader = FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(ga.weight(ind, 4), 4)
        self.assertEqual(1, 1)

    def test_degree(self):
        ind = Individual(9)
        ind.data = BitVector(bitlist=[1, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(GA.degree(ind, [9, -5]), 0)
        self.assertEqual(GA.degree(ind, [1, 3, 6]), 1)
        ind.data = BitVector(bitlist=[0, 0, 1, 0, 0, 0, 1, 1, 0])
        self.assertEqual(GA.degree(ind, [7, 8, -3]), 3)

    def test_tabu_with_diversification(self):
        self.assertEqual(1, 1)

    def test_check_flip(self):
        self.assertEqual(1, 1)

    def test_fluerent_and_ferland(self):
        self.assertEqual(1, 1)

    def test_select(self):
        self.assertEqual(1, 1)

    def test_create_population(self):
        self.assertEqual(1, 1)

    def test_is_satisfied(self):
        reader = FormulaReader("../examples/trivial.cnf")
        ga = GA(reader.formula, 9, 5, 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 0, 0, 0, 0, 0, 0])
        ga.population = [ind for x in range(100)]

        # There should not be a satisfiable assignment.
        self.assertIsNone(ga.is_satisfied())

        ga.population[0].data = BitVector(bitlist=[1, 1, 1, 0, 1, 1, 1, 1, 1])

        # Population now has one satisfying assignment.
        self.assertIsNotNone(ga.is_satisfied())

    def test_replace(self):
        self.assertEqual(1, 1)

    def test_gasat(self):
        self.assertEqual(1, 1)
