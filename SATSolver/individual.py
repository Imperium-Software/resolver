"""
    Module: Individual
    Description: Defines classes related to the creation and manipulation of
    an Individual for use in the genetic algorithm.
"""

from BitVector import BitVector
from bitarray import bitarray
import random


class Individual:
    """ Encapsulates an Individual in the GA. """

    BIT_VECTOR = 0
    BIT_ARRAY = 1

    def __init__(self, length=0, method=None, parents=None, value=None):

        """ Creates a bit string of a certain length, using a certain underlying
        implementation.

        :param parents: A 2-tuple of the parents to initialise this child from

        """

        self.length = length
        self.fitness = 0
        self.isCacheValid = False

        if method not in [0, 1]:
            self.method = Individual.BIT_VECTOR
        else:
            self.method = method

        if self.method == Individual.BIT_VECTOR:

            if value is not None:
                self.data = BitVector(bitlist=value)
            elif parents is not None:
                self.data = BitVector(size=length)
                x, y = parents
                for i in range(1, x.length + 1):
                    # If the parents have the same value the bit stays the same, otherwise it is random
                    val = x.get(i)
                    if val == y.get(i):
                        self.set(i, val)
                    else:
                        self.set(i, 0 if random.random() < 0.5 else 1)
            else:
                self.data = BitVector(size=length)
                self.data = self.data.gen_random_bits(length)

        elif self.method == Individual.BIT_ARRAY:

            if value is not None:
                self.data = bitarray([bool(_) for _ in value])
            elif parents is not None:
                self.data = bitarray(length)
                x, y = parents
                for i in range(1, x.length + 1):
                    # If the parents have the same value the bit stays the same, otherwise it is random
                    val = x.get(i)
                    if val == y.get(i):
                        self.set(i, val)
                    else:
                        self.set(i, 0 if random.random() < 0.5 else 1)
            else:
                self.data = bitarray(length)

        for i in range(1, length+1):
            if bool(random.getrandbits(1)):
                self.flip(i)

    def __str__(self):

        """ Creates a consistent string method across implementations. """

        if self.method == Individual.BIT_VECTOR:
            return str(self.data)
        elif self.method == Individual.BIT_ARRAY:
            return self.data.to01()
        return ""

    def __call__(self, b):
        return self.get(b)

    def get(self, b):

        """ Returns the value at position b, that is either 1 or 0. """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            return self.data[b]
        elif self.method == Individual.BIT_ARRAY:
            return int(self.data[b])

    def set(self, b, v):

        """ Sets the bit at position b to value v. """

        self.isCacheValid = False
        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.data[b] = v
        elif self.method == Individual.BIT_ARRAY:
            self.data[b] = bool(v)

    def flip(self, b):

        """ Flips the bit at position b. """

        self.isCacheValid = False
        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.data[b] ^= 1
        elif self.method == Individual.BIT_ARRAY:
            self.data[b] = not self.data[b]


class Factory:
    """ A factory class for creating individuals in bulk. """

    @staticmethod
    def create(length, amount, method=None):
        """ Creates an array of individuals. """

        array = [Individual(length, method) for _ in range(amount)]
        return array
