from outcome import Outcome
from bet import Bet

import abc

class Player(metaclass=abc.ABCMeta):
    def __init__(self, table):
        self.stake = 0
        self.rounds_to_go = 0
        self.table = table

    @abc.abstractmethod
    def playing(self):
        pass

    def place_bets(self):
        pass

    def win(self, bet):
        self.stake += bet.win_amount()
        # bet amount was deduced from the stake,
        # when the bet was created, so we need to put it back
        self.stake += bet.bet_amount

    def loose(self, bet):
        # Nothing to do: amount was
        # already deduced from the stake when the bet was created
        pass


class Martingale(Player):
    outcome = Outcome("Black", 1)
    def __init__(self, table):
        super().__init__(table)
        self.stake = 0
        self.loss_count = 0
        self.bet_multiple = 1

    def place_bets(self):
        amount = self.bet_multiple
        self.stake -= amount
        bet = Bet(amount, self.outcome)
        self.table.place_bet(bet)

    def win(self, bet):
        super().win(bet)
        self.loss_count = 0
        self.bet_multiple = 1

    def loose(self, bet):
        super().loose(bet)
        self.loss_count += 1
        self.bet_multiple *= 2

    def playing(self):
        return self.stake >= self.bet_multiple

class Passenger57(Player):
    """ A Player that always bet on 'Black'

    """
    outcome = Outcome("Black", 1)
    bet_amount = 10
    def __init__(self, table):
        super().__init__(table)
        self.wins = list()
        self.loss = list()

    def playing(self):
        return self.stake >= self.bet_amount

    def place_bets(self):
        """ Make only one bet: 10 on black, and
        place it on the table

        """
        bet = Bet(self.bet_amount, self.outcome)
        self.stake -= self.bet_amount
        self.table.place_bet(bet)

    def win(self, bet):
        super().win(bet)
        self.wins.append(bet.win_amount())

    def loose(self, bet):
        super().loose(bet)
        self.loss.append(bet.bet_amount)
