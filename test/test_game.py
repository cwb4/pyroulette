from player import Passenger57
from table import Table
from wheel import Wheel
from game import RouletteGame
from builder import BinBuilder
from non_random import NonRandom


def test_roulette_game():
    rng = NonRandom([0, 2])
    wheel = Wheel(rng=rng)
    builder = BinBuilder()
    builder.build_bins(wheel)
    table = Table()

    player = Passenger57(table)
    player.stake = 20
    game = RouletteGame(wheel, table)
    game.cycle(player)
    assert player.loss == [10]
    assert player.wins == list()
    game.cycle(player)
    assert player.loss == [10]
    assert player.wins == [10]
