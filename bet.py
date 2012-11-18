class Bet:
    def __init__(self, amount, outcome):
        self.bet_amount = amount
        self.outcome = outcome

    def win_amount(self):
        """ Return amout won """
        return self.outcome.win_amount(self.bet_amount)

    def lose_amout(self):
        """ Return amount lost """
        return self.bet_amount

    def __str__(self):
        return "%d on %s" % (self.bet_amount, self.outcome.name)
