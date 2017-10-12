"""
    Module: Individual
    Description: Defines classes related to the creation and manipulation of
    an Individual for use in the genetic algorithm.
"""

from bitarray import bitarray
import random


class Individual:
    """ Encapsulates an Individual in the GA. """

    def __init__(self, length=0, defined=False, value=None):

        """ Creates a bit string of a certain length, using a certain underlying
        implementation.  """

        self.length = length
        self.fitness = 0
        self.isCacheValid = False
        self.defined = bitarray(length)
        self.data = bitarray(length)

        if defined:
            self.defined = None
        else:
            self.defined.setall(False)

        if value is not None:
            self.data = [bool(X) for X in value]

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

    def set_defined(self, b):

        """ Sets a certain bit b as defined. """

        b -= 1
        if b >= self.length or b < 0:
            return
        self.defined[b] = not self.data[b]

    def get_defined(self, b):

        """ Gets whether a certain bit is defined or not (boolean) """

        b -= 1
        if b >= self.length or b < 0:
            return
        return self.defined[b]

    def allocate(self, first, second):

        """ Allocates uniformly from either first or second parent. """

        for i in range(self.length):
            # i is inconsistently indexed in comparison to other places get_defined and set are called thus 1
            # must be added
            index = i + 1
            if not self.get_defined(index):
                if bool(random.getrandbits(1)):
                    self.set(index, first.get(index))
                else:
                    self.set(index, second.get(index))
                self.set_defined(index)


class Factory:
    """ A factory class for creating individuals in bulk. """

    @staticmethod
    def create(length, amount):
        """ Creates an array of individuals. """

        array = [Individual(length, True) for _ in range(amount)]
        return array
