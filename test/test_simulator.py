from simulator import Simulator
from wheel import create_wheel
from non_random import NonRandom
from player import Passenger57
from game import RouletteGame
from table import Table

def create_simulator():
    rng = NonRandom(
        [
        # 2 blacks, 2 red
        2, 6, 5, 7,
        # 4 blacks
        2, 6, 4, 8,
        # 4 red
        27, 30, 32, 34,
        ]
    )
    wheel = create_wheel(rng=rng)
    table = Table(wheel)
    game = RouletteGame(wheel, table)
    simulator = Simulator(game, "Passenger57",
                          init_duration=4, samples=3,
                          init_stake=10)
    return simulator

def test_session():
    simulator = create_simulator()
    stakes = simulator.session()
    assert stakes == [10, 20, 30, 20, 10]
    stakes = simulator.session()
    assert stakes == [10, 20, 30, 40, 50]
    stakes = simulator.session()
    assert stakes == [10, 0]

def test_gather():
    simulator = create_simulator()
    simulator.gather()
    assert simulator.durations == [5, 5, 2]
    assert simulator.maxima == [30, 50, 10]

