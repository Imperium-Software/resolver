"""
    Module: individual
    Description: Defines classes related to the creation and manipulation of
    and individual for use in the genetic algorithm.
"""

from BitVector import BitVector
from bitarray import bitarray

class individual:

    """ Encapsulates an individual in the GA. """

    BIT_VECTOR = 0
    BIT_ARRAY = 1

    def __init__(self, length=0, method=None):

        """ Creates a bit string of a certain length, using a certain underlying
        implementation.  """

        self.length = length

        if method not in [0, 1]:
            self.method = individual.BIT_VECTOR
        else:
            self.method = method

        if self.method == individual.BIT_VECTOR:
            self.data = BitVector(size=length)
            self.data = self.data.gen_random_bits(length)
        elif self.method == individual.BIT_ARRAY:
            self.data = bitarray(length)

    def __str__(self):

        """ Creates a consistent string method across implementations. """

        if self.method == individual.BIT_VECTOR:
            return str(self.data)
        elif self.method == individual.BIT_ARRAY:
            return self.data.to01()
        return ""

    def get(self, b):

        """ Returns the value at position b, that is either 1 or 0. """

        if b >= self.length:
            return

        if self.method == individual.BIT_VECTOR:
            return self.data[b]
        elif self.method == individual.BIT_ARRAY:
            return int(self.data[b])

    def set(self, b, v):

        """ Sets the bit at position b to value v. """

        if b >= self.length:
            return

        if self.method == individual.BIT_VECTOR:
            self.data[b] = v
        elif self.method == individual.BIT_ARRAY:
            self.data[b] = bool(v)

    def flip(self, b):

        """ Flips the bit at position b. """

        if b >= self.length:
            print("nope!")
            return

        if self.method == individual.BIT_VECTOR:
            self.data[b] = self.data[b] ^ 1
        elif self.method == individual.BIT_ARRAY:
            self.data[b] = not self.data[b]


class factory:

    """ A factory class for creating individuals in bulk. """

    def create(self, length, method, amount):

        """ Creates an array of individuals. """

        array = [individual(length, method) for x in range(amount)]
        return array

# TESTS

if __name__ == "__main__":
    ind = individual(9, individual.BIT_VECTOR)
    num_fail = 0
    print()
    for x in range(2):
        if x == 0:
            print("Testing implementation : BitVector")
            ind.data = BitVector(bitlist = [0,1,1,0,1,0,1,0,0])
            ind.method = individual.BIT_VECTOR
        else:
            print("Testing implementation : bitarray")
            ind.data = bitarray("011010100")
            ind.method = individual.BIT_ARRAY


        print("With data: " + str(ind))
        print("  Testing get")

        if ind.get(4) == 1:
            print("    get(4) == 1 => pass")
        else:
            print("    get(4) == 1 => fail")
            num_fail+=1

        if ind.get(7) == 0:
            print("    get(7) == 0 => pass")
        else:
            print("    get(7) == 0 => fail")
            num_fail+=1

        if ind.get(9) == None:
            print("    get(9) == None => pass")
        else:
            print("    get(9) == None => fail")
            num_fail+=1

        print()
        print("  Testing set")

        ind.set(2,1)
        if ind.get(2) == 1:
            print("    set(2,1) => pass")
        else:
            print("    set(2,1) => fail")
            num_fail+=1

        ind.set(6,0) == 0
        if ind.get(7) == 0:
            print("    set(6,0) => pass")
        else:
            print("    set(6,1) => fail")
            num_fail+=1

        ind.set(5,1)
        if ind.get(5) == 1:
            print("    set(5,1) => pass")
        else:
            print("    set(5,1) => fail")
            num_fail+=1

        print()
        print("  Testing flip")
        ind.flip(0)
        if ind.get(0) == 1:
            print("    flip(0) => pass")
        else:
            print("    flip(0) => fail")
            num_fail+=1

        ind.flip(7)
        if ind.get(7) == 1:
            print("    flip(7) => pass")
        else:
            print("    flip(7) => fail")
            num_fail+=1

        ind.flip(3)
        if ind.get(3) == 1:
            print("    flip(3) => pass")
        else:
            print("    flip(3) => fail")
            num_fail+=1
        print()

    print("----------------------")
    if num_fail == 0:
        print("Passed all tests.")
    else:
        print(str(num_fail) + " tests failed.")
