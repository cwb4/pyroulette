""" bin: something that will be picked at random
by the roulette

"""

class Bin:
    """ A collection of outcomes """
    def __init__(self, index_, *outcomes):
        self.index_ = index_
        self.outcomes = frozenset(outcomes)

    def add(self, outcome):
        """ Add an outcome to this bin

        """
        self.outcomes |= set([outcome])

    def __str__(self):
        if self.index_ == 37:
            return "00"
        else:
            return "%2i" % self.index_
