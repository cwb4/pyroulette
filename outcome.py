""" Outcome: a name, and the odds that are paid

"""

class Outcome:
    """ A single outcome on which a bet can be placed:
    1, 36
    Red, 3
    Low, 4

    """
    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def win_amount(self, amount):
        """ What the player gets whe this Outcome occurs
        and he has bet the given amount

        """
        return self.odds * amount

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "%s (odds:%i:1)" % (self.name, self.odds)

    def __repr__(self):
        return '<Outcome "%s" %i:1>' % (self.name, self.odds)

    def __hash__(self):
        return hash(self.name)
