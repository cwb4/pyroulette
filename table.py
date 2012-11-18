from bet import InvalidBet

class Table:
    limit = 1000
    def __init__(self):
        self.bets = list()

    def is_valid(self, bet):
        cur_total = 0
        for cur_bet in self:
            cur_total += cur_bet.bet_amount
        return cur_total + bet.bet_amount <= self.limit

    def place_bet(self, bet):
        if not self.is_valid(bet):
            raise InvalidBet()
        self.bets.append(bet)

    def __iter__(self):
        self._it = iter(self.bets)
        return self

    def __next__(self):
        return next(self._it)

