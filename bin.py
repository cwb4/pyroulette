""" bin: something that will be picked at random
by the roulette

"""

class Bin:
    """ A collection of outcomes """
    def __init__(self, *outcomes):
        self.outcomes = frozenset(outcomes)

    def add(self, outcome):
        """ Add an outcome to this bin

        """
        self.outcomes |= set([outcome])

    def __str__(self):
        pass
