import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
print(myPath)
sys.path.insert(0, myPath + '/../SATSolver')

from unittest import TestCase
from SATSolver.individual import Individual
from BitVector import BitVector
from bitarray import bitarray


class TestIndividual(TestCase):
    """
    Testing class for Individual.
    """

    def test_get(self):
        ind = Individual(9)
        ind.data = bitarray("011010100")
        self.assertEqual(ind.get(5), 1)
        self.assertEqual(ind.get(1), 0)
        self.assertEqual(ind.get(10), None)

    def test_set(self):
        ind = Individual(9)
        ind.data = bitarray("011010100")
        ind.set(2, 1)
        self.assertEqual(ind.get(2), 1)
        ind.set(7, 0)
        self.assertEqual(ind.get(7), 0)
        ind.set(6, 1)
        self.assertEqual(ind.get(6), 1)

    def test_flip(self):
        ind = Individual(9)
        ind.data = bitarray("011010100")
        ind.flip(1)
        self.assertEqual(ind.get(1), 1)
        ind.flip(8)
        self.assertEqual(ind.get(8), 1)
        ind.flip(4)
        self.assertEqual(ind.get(4), 1)

