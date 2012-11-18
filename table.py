from wheel import create_wheel
from bet import InvalidBet

class Table:
    """ A Table contains a Wheel, so that player
    can ask the Wheel for the possible outcomes

    """
    def __init__(self, wheel, min_limit=1, max_limit=1000):
        self.max_limit = max_limit
        self.min_limit = min_limit
        self.wheel = wheel
        self.bets = list()

    def is_valid(self, bet):
        """ A bet is valid if the total bets are lower that
        the max limit, and it is higher than the min limit

        """
        cur_total = 0
        for cur_bet in self:
            cur_total += cur_bet.bet_amount
        too_high = cur_total + bet.bet_amount >= self.max_limit
        too_low = bet.bet_amount < self.min_limit
        return not too_low and not too_high

    def place_bet(self, bet):
        """ Check that the bet is valid (should be true
        unless there's a bug in the Player class,
        and add the bet to the list of the bets

        """
        if not self.is_valid(bet):
            raise InvalidBet()
        self.bets.append(bet)

    def __iter__(self):
        self._it = iter(self.bets)
        return self

    def __next__(self):
        return next(self._it)

def create_table():
    wheel = create_wheel()
    table = Table(wheel)
    return table
