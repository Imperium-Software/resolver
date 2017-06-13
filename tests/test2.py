from bitarray import bitarray, bits2bytes
import os
import math
import random
import timing
bv = bitarray()
print("Start Initialisation Tests")


timing.start()
for i in range(51):
    bv.frombytes(os.urandom(50))
timing.log("Random Initialisation with n = 50", 50.0)

timing.start()
for i in range(51):
    bv.frombytes(os.urandom(10000))
timing.log("Random Initialisation with n = 10,000", 50.0)

timing.start()
for i in range(51):
    bv.frombytes(os.urandom(250000))
timing.log("Random Initialisation with n = 250,000", 50.0)

timing.start()
for i in range(51):
    bv.frombytes(os.urandom(1000000))
timing.log("Random Initialisation with n = 1,000,000", 50.0)

"""
Start Initialisation Tests
======================================================================
0:00:00.000007 - Random Initialisation with n = 50
======================================================================

======================================================================
0:00:00.000643 - Random Initialisation with n = 10,000
======================================================================

======================================================================
0:00:00.015690 - Random Initialisation with n = 250,000
======================================================================

======================================================================
0:00:00.065976 - Random Initialisation with n = 1,000,000
======================================================================
"""

# print("Start Random Access Tests")
#
# bv = bv.gen_random_bits(50)
# timing.start()
# for i in range(51):
#     bv[random.randrange(50)]
# timing.log("Random Access with n = 50", 50.0)
#
# bv = bv.gen_random_bits(10000)
# timing.start()
# for i in range(51):
#     bv[random.randrange(10000)]
# timing.log("Random Access with n = 10,000", 50.0)
#
# bv = bv.gen_random_bits(250000)
# timing.start()
# for i in range(51):
#     bv[random.randrange(250000)]
# timing.log("Random Access with n = 250,000", 50.0)
#
# bv = bv.gen_random_bits(1000000)
# timing.start()
# for i in range(51):
#     bv[random.randrange(1000000)]
# timing.log("Random Access with n = 1,000,000", 50.0)

"""
Start Random Access Tests
======================================================================
0:00:00.000006 - Random Access with n = 50
======================================================================

======================================================================
0:00:00.000005 - Random Access with n = 10,000
======================================================================

======================================================================
0:00:00.000005 - Random Access with n = 250,000
======================================================================

======================================================================
0:00:00.000006 - Random Access with n = 1,000,000
======================================================================
"""