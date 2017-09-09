import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
print(myPath)
sys.path.insert(0, myPath + '/../SATSolver')

from unittest import TestCase
from individual import Individual
# TODO: Try from SATSolver.individual import Individual
from BitVector import BitVector
from bitarray import bitarray


class TestIndividual(TestCase):
    """
    Testing class for Individual.
    """

    def test_get(self):
        ind = Individual(9, Individual.BIT_VECTOR)

        # BitVector implementation

        ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
        ind.method = Individual.BIT_VECTOR
        self.assertEqual(ind.get(5), 1)
        self.assertEqual(ind.get(1), 0)
        self.assertEqual(ind.get(10), None)

        # bittarray implementation

        ind.data = bitarray("011010100")
        ind.method = Individual.BIT_ARRAY
        self.assertEqual(ind.get(5), 1)
        self.assertEqual(ind.get(1), 0)
        self.assertEqual(ind.get(10), None)

    def test_set(self):
        ind = Individual(9, Individual.BIT_VECTOR)

        ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
        ind.method = Individual.BIT_VECTOR
        ind.set(2, 1)
        self.assertEqual(ind.get(2), 1)
        ind.set(7, 0)
        self.assertEqual(ind.get(7), 0)
        ind.set(6, 1)
        self.assertEqual(ind.get(6), 1)

        # bittarray implementation

        ind.data = bitarray("011010100")
        ind.method = Individual.BIT_ARRAY
        ind.set(2, 1)
        self.assertEqual(ind.get(2), 1)
        ind.set(7, 0)
        self.assertEqual(ind.get(7), 0)
        ind.set(6, 1)
        self.assertEqual(ind.get(6), 1)

    def test_flip(self):
        ind = Individual(9, Individual.BIT_VECTOR)

        # BitVector implementation

        ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
        ind.method = Individual.BIT_VECTOR
        ind.flip(1)
        self.assertEqual(ind.get(1), 1)
        ind.flip(8)
        self.assertEqual(ind.get(8), 1)
        ind.flip(4)
        self.assertEqual(ind.get(4), 1)

        # bittarray implementation

        ind.data = bitarray("011010100")
        ind.method = Individual.BIT_ARRAY
        ind.flip(1)
        self.assertEqual(ind.get(1), 1)
        ind.flip(8)
        self.assertEqual(ind.get(8), 1)
        ind.flip(4)
        self.assertEqual(ind.get(4), 1)
