from player import Martingale
from wheel import create_wheel
from non_random import NonRandom
from game import RouletteGame
from table import Table

def test_martingale_lucky():
    # black, red, red,red, black, black
    rng = NonRandom([2, 5, 9, 12, 11, 10])
    wheel = create_wheel(rng=rng)
    table = Table(wheel)

    player = Martingale(table, stake=100)
    game = RouletteGame(wheel, table)
    # win
    game.cycle(player)
    assert player.stake == 101
    game.cycle(player)
    # loose, bet 1
    assert player.stake == 100
    game.cycle(player)
    # loose, bet 2
    assert player.stake == 98
    game.cycle(player)
    # loose, bet 4
    assert player.stake == 94
    game.cycle(player)
    # win, gain 8, will bet 1
    assert player.stake == 102
    game.cycle(player)
    # win, gain 2, will bet 1
    assert player.stake == 103

def test_martingale_unlucky():
    # Always red
    rng = NonRandom([1] * 4)
    wheel = create_wheel(rng=rng)
    table = Table(wheel)

    player = Martingale(table, stake=8)
    game = RouletteGame(wheel, table)

    for i in range(4):
        game.cycle(player)

    assert player.stake > 0
    assert player.playing() is False
