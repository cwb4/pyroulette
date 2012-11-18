from outcome import Outcome
from bet import Bet

import abc

class Player(metaclass=abc.ABCMeta):
    def __init__(self, table, stake=10):
        self.stake = stake
        self.rounds_to_go = 0
        self.table = table
        self._playing = True

    def playing(self):
        """ Should return False when the player is done playing
        (Called by Game.cycle)

        """
        return self._playing

    @abc.abstractmethod
    def next_bet(self):
        """ Return the next bet the player wants to make

        """
        pass

    @abc.abstractmethod
    def on_win(self):
        """ What to do next when the player wins.
        Update strategy to choose next bet

        """
        pass

    @abc.abstractmethod
    def on_loose(self):
        """ What to do next when the player looses.
        Update strategy to choose next bet

        """
        pass

    def place_bets(self):
        """ Calls the next_bet() method on the
        player

        If we can't afford the bet or the bet is over
        the table limit, set self._playing to false
        so that the game knows we are done

        """
        bet = self.next_bet()
        if bet.bet_amount > self.stake:
            self._playing = False
            return
        if bet.bet_amount >= self.table.max_limit:
            self._playing = False
            return
        self.stake -= bet.bet_amount
        self.table.place_bet(bet)

    def win(self, bet):
        """ Called by Game.cycle when the player won
        the bet

        """
        self.stake += bet.win_amount()
        # bet amount was deduced from the stake,
        # when the bet was created, so we need to put it back
        self.stake += bet.bet_amount
        self.on_win(bet)

    def loose(self, bet):
        """ Called by Game.cycle when the player lost
        the bet

        """
        # Nothing to do: amount was
        # already deduced from the stake when the bet was created
        self.on_loose(bet)


class Martingale(Player):
    outcome = Outcome("Black", 1)
    def __init__(self, table, stake=10):
        super().__init__(table, stake=stake)
        self.loss_count = 0
        self.bet_amount = 1

    def next_bet(self):
        """ Implements Player.next_bet.

        Bet on Black with the correct bet amount
        """
        black = self.table.wheel.get_outcome("Black")
        return Bet(self.bet_amount, black)

    def on_win(self, _):
        """ Implemnts Player.on_win

        Reset strategy
        """
        self.loss_count = 0
        self.bet_amount = 1

    def on_loose(self, _):
        """ Implements Player.on_loose

        Double the next bet
        """
        self.loss_count += 1
        self.bet_amount *= 2

class Passenger57(Player):
    """ A Player that always bet on 'Black'

    """
    bet_amount = 10

    def __init__(self, table, stake=10):
        super().__init__(table, stake=stake)
        self.wins = list()
        self.losses = list()

    def next_bet(self):
        """ Make only one bet: 10 on black, and
        place it on the table

        """
        black = self.table.wheel.get_outcome("Black")
        return Bet(self.bet_amount, black)

    def on_win(self, bet):
        """ Implements Player.on_win(bet)
        Simply register the win for later checks by testing

        """
        self.wins.append(bet.win_amount())

    def on_loose(self, bet):
        """ Implements Player.on_loose(bet)
        Simply register the loss for later checks by testing

        """
        self.losses.append(bet.bet_amount)
