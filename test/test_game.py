from player import Passenger57
from table import Table
from wheel import create_wheel
from game import RouletteGame
from non_random import NonRandom


def test_roulette_game():
    rng = NonRandom([0, 2])
    wheel = create_wheel(rng)
    table = Table(wheel)

    player = Passenger57(table)
    player.stake = 20
    game = RouletteGame(wheel, table)
    game.cycle(player)
    assert player.loss == [10]
    assert player.wins == list()
    game.cycle(player)
    assert player.loss == [10]
    assert player.wins == [10]
