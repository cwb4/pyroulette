from player import Player
from bet import Bet

import abc


class PlayerState(metaclass=abc.ABCMeta):
    """ A Base classe for the Player1236 possible states

    """
    def __init__(self, player):
        self.player = player

    @abc.abstractmethod
    def current_bet(self):
        """ The current bet from the player preferred outcome

        """

    @abc.abstractmethod
    def next_won(self):
        """ Return the new PlayerState to use when the player won

        """

    # Not abstract because it's the same for every state
    def next_lost(self):
        """ Return the new PlayerState to use when the player lost

        """
        return NoWinState(self.player)

class NoWinState(PlayerState):
    """ No wins state """
    def current_bet(self):
        return Bet(1, self.player.outcome)

    def next_won(self):
        return OneWinState(self.player)

class OneWinState(PlayerState):
    """ One win state """
    def current_bet(self):
        return Bet(3, self.player.outcome)

    def next_won(self):
        return TwoWinsState(self.player)

class TwoWinsState(PlayerState):
    """ Two wins state """
    def current_bet(self):
        return Bet(2, self.player.outcome)

    def next_won(self):
        return ThreeWinsState(self.player)

class ThreeWinsState(PlayerState):
    """ Three wins state """
    def current_bet(self):
        return Bet(6, self.player.outcome)

    def next_won(self):
        return NoWinState(self.player)
