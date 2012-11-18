from outcome import Outcome
from bet import Bet

class Passenger57:
    """ A Player that always bet on 'Black'

    """
    def __init__(self, table):
        self.table = table
        self.black = Outcome("Black", 1)
        self.wins = list()
        self.loss = list()

    def place_bets(self):
        """ Make only one bet: 10 on black, and
        place it on the table

        """
        bet = Bet(10, self.black)
        self.table.place_bet(bet)

    def win(self, bet):
        self.wins.append(bet.win_amount())

    def loose(self, bet):
        self.loss.append(bet.bet_amount)

