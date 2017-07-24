
from src.GA import GA
from BitVector import BitVector
from unittest import TestCase
from src.individual import Individual


class TestGA(TestCase):
    def test_sat(self):
        ga = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(ga.sat(ind, ga.formula[0]), 1)

        ind.data = BitVector(bitlist=[0, 0, 0, 0, 1, 0, 0, 0, 0])
        self.assertEqual(ga.sat(ind, ga.formula[0]), 0)

        ind.data = BitVector(bitlist=[1, 0, 1, 0, 1, 1, 0, 0, 0])
        self.assertEqual(ga.sat(ind, ga.formula[1]), 1)

        ind.data = BitVector(bitlist=[1, 0, 1, 0, 1, 1, 0, 0, 0])
        self.assertEqual(ga.sat(ind, ga.formula[2]), 1)

        ind.data = BitVector(bitlist=[1, 0, 1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(ga.sat(ind, ga.formula[2]), 0)

        # TODO: More sub-tests

    def test_sat_crossover(self):
        self.fail()

    def test_evaluate(self):
        self.fail()

    def test_improvement(self):
        ga = GA("../examples/trivial.cnf", 10, 5, 5, 5)
        ind = Individual(9)
        ind.data = BitVector(bitlist=[0, 0, 0, 1, 0, 0, 0, 0, 0])
        self.assertEqual(ga.improvement(ind, 1), 1)

        # TODO: More sub-tests

    def test_corrective_clause(self):
        self.fail()

    def test_corrective_clause_with_truth_maintenance(self):
        self.fail()

    def test_standard_tabu_choose(self):
        self.fail()

    def test_standard_tabu(self):
        self.fail()

    def test_choose_rvcf(self):
        self.fail()

    def test_weight(self):
        self.fail()

    def test_degree(self):
        self.fail()

    def test_tabu_with_diversification(self):
        self.fail()

    def test_check_flip(self):
        self.fail()

    def test_fluerent_and_ferland(self):
        self.fail()

    def test_select(self):
        self.fail()

    def test_create_population(self):
        self.fail()

    def test_is_satisfied(self):
        self.fail()

    def test_replace(self):
        self.fail()

    def test_gasat(self):
        self.fail()
