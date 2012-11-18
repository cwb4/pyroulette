from bet import InvalidBet

class Table:
    max_limit = 1000
    min_limit = 1

    def __init__(self):
        self.bets = list()

    def is_valid(self, bet):
        cur_total = 0
        for cur_bet in self:
            cur_total += cur_bet.bet_amount
        too_high = cur_total + bet.bet_amount >= self.max_limit
        too_low = bet.bet_amount < self.min_limit
        return not too_low and not too_high

    def place_bet(self, bet):
        if not self.is_valid(bet):
            raise InvalidBet()
        self.bets.append(bet)

    def __iter__(self):
        self._it = iter(self.bets)
        return self

    def __next__(self):
        return next(self._it)

