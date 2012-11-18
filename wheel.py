"""

"""

import random

from bin import Bin

class Wheel:
    """ A collection of bins and a random generator

    """
    def __init__(self, rng=None):
        self.bins = tuple(Bin() for i in range(38))
        if rng is None:
            rng = random.Random()
        self.rng = rng
        # A map name -> Outcome
        self.all_outcomes = dict()

    def add_outcome(self, number, outcome):
        """ Add the given outcome to the given number

        """
        self.all_outcomes[outcome.name] = outcome
        self.bins[number].add(outcome)

    def get_outcome(self, name):
        return self.all_outcomes[name]

    def next(self):
        """ Return the next bin

        """
        return self.rng.choice(self.bins)

    def get_bin(self, bin):
        """ Get the given bin

        """
        return self.bins[bin]


