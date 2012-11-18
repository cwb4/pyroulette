from player import Martingale, Passenger57, SevenReds, RandomPlayer
from wheel import create_wheel
from non_random import NonRandom
from game import RouletteGame, create_game
from table import Table

def test_martingale_lucky():
    # black, red, red,red, black, black
    rng = NonRandom([2, 5, 9, 12, 11, 10])
    game = create_game(rng=rng)

    player = Martingale(game.table)
    player.set_stake(100)
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

def test_martingale_loose_all():
    # Always red
    rng = NonRandom([1] * 4)
    game = create_game(rng=rng)

    player = Martingale(game.table)
    player.set_stake(8)

    for i in range(4):
        game.cycle(player)

    assert player.stake > 0
    assert player.playing() is False

def test_martingale_cant_make_huge_bets():
    # Always red
    rng = NonRandom([1] * 4)
    game = create_game(rng=rng)

    player = Martingale(game.table)
    player.set_stake(32)
    player.bet_amount = 4

    for i in range(4):
        game.cycle(player)

    assert player.playing() is False

def test_player_in_hurry():
    # Always black
    rng = NonRandom([2] * 4)
    game = create_game(rng=rng)
    player = Passenger57(game.table)
    player.set_duration(3)
    player.set_stake(10)

    for i in range(4):
        game.cycle(player)
    assert player.playing() is False
    assert player.stake == 40

def test_cautious_martingale():
    class CautiousMartingale(Martingale):
        def wants_to_play(self):
            return self.stake <= 102

    # Always black
    rng = NonRandom([2] * 4)
    game = create_game(rng=rng)
    player = CautiousMartingale(game.table)
    player.set_stake(100)

    for i in range(4):
        game.cycle(player)

    assert player.playing() is False
    assert player.stake == 103

def test_seven_red_waits():
    # 7 Reds, 1 Black, 2 Red
    rng = NonRandom([1] * 7 + [2] + [1] * 9)
    game = create_game(rng=rng)
    player = SevenReds(game.table)

    for i in range(9):
        game.cycle(player)

    # Bet 1 and gain 1
    assert player.stake == 11

    game.cycle(player)
    assert player.stake == 11

    # Finish the seven series:
    for i in range(5):
        game.cycle(player)

    # Re-bet 1, loose and  bet 2
    for i in range(2):
        game.cycle(player)

    assert player.stake == 8

def test_seven_red_double_when_loose():
    # 10 Reds, 1 Black
    rng = NonRandom([1] * 10 + [2])
    game = create_game(rng=rng)
    player = SevenReds(game.table)

    for i in range(7):
        game.cycle(player)
    assert player.stake == 10
    game.cycle(player)
    assert player.stake == 9
    game.cycle(player)
    assert player.stake == 7
    game.cycle(player)
    assert player.stake == 3

def test_seven_red_number_respect_duration():
    rng = NonRandom([2] * 10)
    game = create_game(rng=rng)
    player = SevenReds(game.table)
    player.set_duration(4)
    for i in range(7):
        game.cycle(player)
    assert player.playing() is False

class NonRandomOutcomeChoice:
    """ A non random choice generator

    """
    def __init__(self, wheel):
        self.wheel = wheel
        self.outcomes = list()
        self._index = 0

    def set_outcomes(self, outcomes):
        """ To be called before the fake random generator
        is used

        """
        self._index = 0
        self.outcomes = outcomes[:]

    def choice(self, _ununsed):
        """ Override random.choice """
        res = self.outcomes[self._index]
        self._index += 1
        return res

def test_random_player():
    wheel = create_wheel()
    rng = NonRandomOutcomeChoice(wheel)
    expected_outcomes = [wheel.get_outcome(n) for n in ["Black", "Low", "00"]]
    rng.set_outcomes(expected_outcomes)
    table = Table(wheel)
    random_player = RandomPlayer(table, rng=rng)
    bets = [random_player.next_bet() for i in range(3)]
    actual_outcomes = [b.outcome for b in bets]
    assert actual_outcomes == expected_outcomes
