""" ---------------------------------------------------------------------- """

# Importing the time module for getting the current time. 

import time

""" ---------------------------------------------------------------------- """

# Createing custom errors class's.

# Defining the SeedingError for cases where the program fails to -
# - extract seed from current time.

class SeedingError(Exception):

    def __init__(self):
        self.msg = "Generator was never seeded, contact developer!"

    def __str__(self):
        return self.msg

# Defining the OrderError for cases where the user has cause starting int greater -
# - than the ending int.

class OrderError(Exception):

    def __init__(self):
        self.msg = "Starting int most be smaller than ending int!"

    def __str__(self):
        return self.msg

# Defining the ValueError for cases where the user has cause the same value -
# - for both starting and ending int's.

class ValueError(Exception):

    def __init__(self):
        self.msg = "Starting int can't be the same as ending int!"

    def __str__(self):
        return self.msg

""" ---------------------------------------------------------------------- """

#*** Important note: The & | and ^ operators are "and" "or" and "xor" respectively. ***#

# Creating mersenne twister class.
# (mersenne twister is the algorithm used for generating random numbers)

class MT(object):

    """ ---------------------------------------------------------------------- """

    # Defining the update function for generating seed from current time.
    # And from that seed generating first 623 random seeds.

    def update(self):
        
        # Generating seed from current time by using the time.time() function.

        x = str(time.time())
        dot = False
        seed = ""

        for i in range(len(x)):

            if dot:
                seed = seed + x[i]

            if x[i] == '.':
                dot = True

        seed = int(seed)
        dot = False

        self.index -= 1
        self.MT[0] = seed

        # Generating 623 following seeds from the original seed.

        for i in range(1, self.n):
            self.MT[i] = int(self.d & (self.f*(self.MT[i-1]^(self.MT[i-1]>>(self.w-2)))) + i)

    """ ---------------------------------------------------------------------- """

    # Initializing the the MT object and mathematical variables.

    def __init__(self):

        # Defining the mathematical variables.

        self.f = 1812433253
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0X9908B0DF
        self.u = 11
        self.d = 0xFFFFFFFF
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.index = self.n + 1
        self.LM = (1 << self.r) - 1 
        self.UM = 1 << self.r
        
        # Allocating memory for list with legnth of 624. 

        self.MT = [0]*self.n

        # Using the update function.

        self.update()

    """ ---------------------------------------------------------------------- """

    # Defining the randint function for generating random number. 

    def randint(self):

        # Checking the index value and if index equal to 624 we use the "twist" function.
        # Checking the index value and if index equal to 625 we raise an error (second "if").

        if self.index >= self.n:
            if self.index > self.n:
                raise SeedingError()
            self.twist()
        
        # Assigning seed value to the generated number.

        number = self.MT[self.index]

        # Performing mathematical operations on the generated number.

        number = number ^ ((number >> self.u) & self.d)
        number = number ^ ((number << self.s) & self.b)
        number = number ^ ((number << self.t) & self.c)
        number = number ^ (number >> self.l)

        # raising the index value by one.
 
        self.index += 1

        # Returning the generated number.
        
        return int(self.d & number)

    """ ---------------------------------------------------------------------- """

    # Defining the twist function for generating new seeds.

    def twist(self):

        # Generating 624 new seeds.

        for i in range(self.n):

            x = (self.MT[i] & self.UM) + (self.MT[(i+1) % self.n] & self.LM)
            xA = x >> 1

            if (x % 2) != 0:
                xA = xA ^ self.a

            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA

        # Setting the index value to 0

        self.index = 0

    """ ---------------------------------------------------------------------- """

    # Defining the randrange function for generating "n" random numbers in specific range.

    def randrange(self, a, b, n):

        # Checking for errors.

        if a == b: 
            raise ValueError()
        
        if a > b:
            raise OrderError()
        
        # Defining the distance / range size between the starting and ending int's.
        # Creating the results list.

        dis = b - a 
        results = []

        # Generating "n" random numbers.
        # Dividing them by max value for 32 bits int, from that geting random values -
        # - from 0 - 1.
        # Multiplying the values by the required range size, from that geting random - 
        # - values spreading from 0 to the required range size value.
        # And lastly adding the starting int value for adjusting to the required range.

        for i in range(n):
            x = (self.randint() / self.d)*dis + a
            results.append(x)

        # Returning the results list. 
        return results

""" ---------------------------------------------------------------------- """