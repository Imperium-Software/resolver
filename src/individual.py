"""
    Module: Individual
    Description: Defines classes related to the creation and manipulation of
    and Individual for use in the genetic algorithm.
"""

from BitVector import BitVector
from bitarray import bitarray


class Individual:

    """ Encapsulates an Individual in the GA. """

    BIT_VECTOR = 0
    BIT_ARRAY = 1

    def __init__(self, length=0, method=None, defined=False, value=None):

        """ Creates a bit string of a certain length, using a certain underlying
        implementation.  """

        self.length = length

        if method not in [0, 1]:
            self.method = Individual.BIT_VECTOR
        else:
            self.method = method

        if self.method == Individual.BIT_VECTOR:
            self.data = BitVector(size=length)
            self.data = self.data.gen_random_bits(length)
            self.defined = BitVector(size=length)
            
            if defined:
                self.defined = None
            else:
                self.defined.reset(0)

            if value is not None:
                self.data = BitVector(bitlist = value)

        elif self.method == Individual.BIT_ARRAY:
            self.defined = bitarray(length)
            self.data = bitarray(length)

            if defined:
                self.defined = None
            else:
                self.defined.setall(False)

            if value is not None:
                self.data = [bool(x) for x in value]

    def __str__(self):

        """ Creates a consistent string method across implementations. """

        if self.method == Individual.BIT_VECTOR:
            return str(self.data)
        elif self.method == Individual.BIT_ARRAY:
            return self.data.to01()
        return ""

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

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.data[b] = v
        elif self.method == Individual.BIT_ARRAY:
            self.data[b] = bool(v)

    def flip(self, b):

        """ Flips the bit at position b. """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.data[b] ^= 1
        elif self.method == Individual.BIT_ARRAY:
            self.data[b] = not self.data[b]

    def set_defined(self, b):

        """ Sets """

        b -= 1
        if b >= self.length or b < 0:
            return

        if self.method == Individual.BIT_VECTOR:
            self.defined[b] = 1
        elif self.method == Individual.BIT_ARRAY:
            self.defined[b] = not self.data[b]

    def allocate(self, first, second):

        """ Allocates uniformly from either first or second parent. """

        for i in range(self.length):
            self.set_defined(i)


class Factory:

    """ A factory class for creating individuals in bulk. """

    @staticmethod
    def create(length, method, amount):

        """ Creates an array of individuals. """

        array = [Individual(length, method, fa) for _ in range(amount)]
        return array,

# TESTS

if __name__ == "__main__":
    ind = Individual(9, Individual.BIT_VECTOR)
    num_fail = 0
    print()
    for x in range(2):
        if x == 0:
            print("Testing implementation : BitVector")
            ind.data = BitVector(bitlist=[0, 1, 1, 0, 1, 0, 1, 0, 0])
            ind.method = Individual.BIT_VECTOR
        else:
            print("Testing implementation : bitarray")
            ind.data = bitarray("011010100")
            ind.method = Individual.BIT_ARRAY
        print("With data: " + str(ind))
        print("  Testing get")

        if ind.get(5) == 1:
            print("    get(5) == 1 => pass")
        else:
            print("    get(5) == 1 => fail")
            num_fail += 1

        if ind.get(8) == 0:
            print("    get(8) == 0 => pass")
        else:
            print("    get(8) == 0 => fail")
            num_fail += 1

        if ind.get(10) is None:
            print("    get(10) == None => pass")
        else:
            print("    get(10) == None => fail")
            num_fail += 1
        print()
        print("  Testing set")
        ind.set(2, 1)
        if ind.get(2) == 1:
            print("    set(2,1) => pass")
        else:
            print("    set(2,1) => fail")
            num_fail += 1

        ind.set(7, 0) == 0
        if ind.get(7) == 0:
            print("    set(7,0) => pass")
        else:
            print("    set(7,0) => fail")
            num_fail += 1

        ind.set(6, 1)
        if ind.get(6) == 1:
            print("    set(6,1) => pass")
        else:
            print("    set(6,1) => fail")
            num_fail += 1

        print()
        print("  Testing flip")
        ind.flip(1)
        if ind.get(1) == 1:
            print("    flip(1) => pass")
        else:
            print("    flip(1) => fail")
            num_fail += 1

        ind.flip(8)
        if ind.get(8) == 1:
            print("    flip(8) => pass")
        else:
            print("    flip(8) => fail")
            num_fail += 1

        ind.flip(4)
        if ind.get(4) == 1:
            print("    flip(4) => pass")
        else:
            print("    flip(4) => fail")
            num_fail += 1
        print()
    print("----------------------")
    if num_fail == 0:
        print("Passed all tests.")
    else:
        print(str(num_fail) + " tests failed.")
