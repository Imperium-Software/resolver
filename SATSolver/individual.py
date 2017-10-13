"""
    Module: Individual
    Description: Defines classes related to the creation and manipulation of
    an Individual for use in the genetic algorithm.
"""

from bitarray import bitarray
import random


class Individual:
    """ Encapsulates an Individual in the GA. """

    def __init__(self, length=0, value=None, parents=None):

        """ Creates a bit string of a certain length, using a certain underlying
        implementation.

        :param parents: A 2-tuple of the parents to initialise this child from

        """

        self.length = length
        self.fitness = 1
        self.isCacheValid = False
        self.data = bitarray(length)

        if parents is not None:
            for i in range(1, length+1):
                if (bool(random.getrandbits(1))):
                    self.set(i, parents[0].get(i))
                else:
                    self.set(i, parents[1].get(i))
        else:
            for i in range(1, length+1):
                if bool(random.getrandbits(1)):
                    self.flip(i)

    def __str__(self):

        """ Creates a consistent string method across implementations. """

        return self.data.to01()

    def __call__(self, b):
        return self.get(b)

    def get(self, b):

        """ Returns the value at position b, that is either 1 or 0. """

        b -= 1
        if b >= self.length or b < 0:
            return
        return int(self.data[b])

    def set(self, b, v):

        """ Sets the bit at position b to value v. """

        self.isCacheValid = False
        b -= 1
        if b >= self.length or b < 0:
            return
        self.data[b] = bool(v)

    def flip(self, b):

        """ Flips the bit at position b. """

        self.isCacheValid = False
        b -= 1
        if b >= self.length or b < 0:
            return
        self.data[b] = not self.data[b]


class Factory:
    """ A factory class for creating individuals in bulk. """

    @staticmethod
    def create(length, amount):
        """ Creates an array of individuals. """

        array = [Individual(length=length) for _ in range(amount)]
        return array
