from wheel import create_wheel
from table import Table

class RouletteGame:
    """ Manage the game of Roulette.
    Notify players to place bets, spin the wheel, and resolve bets

    """
    def __init__(self, wheel, table):
        self.wheel = wheel
        self.table = table

    def cycle(self, player):
        """ Player places the bets, and either win or loose

        """
        if player.playing():
            player.place_bets()
        bin = self.wheel.next()
        player.winners(bin.outcomes)
        if not player.playing():
            return
        for bet in self.table:
            if bet.outcome in bin.outcomes:
                player.win(bet)
            else:
                player.loose(bet)
            self.table.bets.remove(bet)

def create_game(rng=None):
    """ Create a new gam """
    wheel = create_wheel(rng=rng)
    table = Table(wheel)
    game = RouletteGame(wheel, table)
    return game
