from outcome import Outcome
from bet import Bet

import abc
import sys
import random

class Player(metaclass=abc.ABCMeta):
    def __init__(self, table):
        self.stake = 10
        self.rounds_to_go = 250
        self.table = table
        self._can_play = True
        self._done_playing = False

    def set_duration(self, duration):
        """ Set the maximum number of rounds
        for this player

        """
        self.rounds_to_go = duration

    def set_stake(self, initial_stake):
        """ Set the initial stake of the player

        """
        self.stake = initial_stake

    def playing(self):
        """ Should return False when the player is done playing
        (Called by Game.cycle)

        """
        return self._can_play and \
               not self._done_playing and \
               self.wants_to_play()

    def wants_to_play(self):
        """ Overlood this if you want to stop playing
        before you can no longer play

        """
        return True

    @abc.abstractmethod
    def next_bet(self):
        """ Return the next bet the player wants to make

        """
        pass

    def on_win(self, _ununsed_bet):
        """ What to do next when the player wins.
        Update strategy to choose next bet

        """
        pass

    def on_loose(self, _ununsed_bet):
        """ What to do next when the player looses.
        Update strategy to choose next bet

        """
        pass

    def winners(self, outcomes):
        """ Called by Game every round.
        This lets the player update its next bet even when not playing

        """
        pass

    def place_bets(self):
        """ Calls the next_bet() method on the
        player

        If we can't afford the bet or the bet is over
        the table limit, set self._playing to false
        so that the game knows we are done

        """
        self.check_done_playing()
        self.rounds_to_go -= 1
        if self._done_playing:
            return
        bet = self.next_bet()
        if not bet:
            return
        self.check_can_play(bet)
        if not self._can_play:
            return
        self.stake -= bet.bet_amount
        self.table.place_bet(bet)

    def check_done_playing(self):
        """ Compute self._done_playing. Called at each place_bets
        call

        """
        if self.rounds_to_go <= 0:
            self._done_playing = True

    def check_can_play(self, bet):
        """ Compute self._can_play. Called at whenever a bet
        is about to be mad

        """
        if bet.bet_amount > self.stake:
            self._can_play = False
        if bet.bet_amount >= self.table.max_limit:
            self._can_play = False

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
    def __init__(self, table):
        super().__init__(table)
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


class SevenReds(Martingale):
    """ A specialization of Martingale.
    Waits for 7 red in a row to start betting

    """
    def __init__(self, table):
        super().__init__(table)
        self.red_count = 7

    def winners(self, outcomes):
        """ Overrid Player.winners """
        red_outcome = self.table.wheel.get_outcome("Red")
        if red_outcome in outcomes:
            self.red_count -= 1
        else:
            self.red_count = 7

    def next_bet(self):
        """ Implements Player.next_bet """
        if self.red_count <= 0:
            black = self.table.wheel.get_outcome("Black")
            return Bet(self.bet_amount, black)

class Passenger57(Player):
    """ A Player that always bet on 'Black'

    """
    bet_amount = 10

    def __init__(self, table):
        super().__init__(table)
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

class RandomPlayer(Player):
    """ A player that plays randomly

    """
    def __init__(self, table, rng=None):
        super().__init__(table)
        if rng is None:
            rng = random.Random()
        self.rng = rng
        all_outcomes = set()
        for bin in self.table.wheel.bins:
            for outcome in bin.outcomes:
                all_outcomes.add(outcome)
        self.outcomes_pool = list(all_outcomes)
        self.bet_amount = 1

    def next_bet(self):
        """ Make a random bet by choosing a random outcome from
        all the possible outcomes

        """
        outcome = self.rng.choice(self.outcomes_pool)
        bet = Bet(self.bet_amount, outcome)
        return bet

class Player1236(Player):
    """ A player with a state machine

    State       Bet   On Win      On Loss
    -------------------------------------
    No Wins     1     One Win     No Wins
    One Win     3     Two Wins    No Wins
    Two Wins    2     Three Wins  No Wins
    Three Wins  6     No Wins     No Wins
    """
    def __init__(self, table):
        from player1236 import NoWinState
        super().__init__(table)
        self.outcome = self.table.wheel.get_outcome("Black")
        self.state = NoWinState(self)

    def next_bet(self):
        """ Implements Player.next_bet """
        bet = self.state.current_bet()
        return bet

    def on_win(self, _):
        """ Implements Player.on_win """
        self.state = self.state.next_won()

    def on_loose(self, _):
        """ Implements Player.on_win """
        self.state = self.state.next_lost()



def create_player(player_class_name, table, stake, duration):
    """ Create a new player given a class

    """
    player_class = getattr(sys.modules[__name__], player_class_name)
    player = player_class(table)
    player.set_duration(duration)
    player.set_stake(stake)
    return player
