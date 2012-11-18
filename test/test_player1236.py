from table import create_table
from non_random import NonRandom
from game import create_game
from player1236 import *
from player import Player1236


def test_player_state():
    table = create_table()
    player = Player1236(table)
    s = NoWinState(player)
    assert s.current_bet().bet_amount == 1
    s = s.next_won()
    assert s.current_bet().bet_amount == 3
    s = s.next_won()
    assert s.current_bet().bet_amount == 2
    s = s.next_won()
    assert s.current_bet().bet_amount == 6
    s = s.next_won()
    assert s.current_bet().bet_amount == 1
    s = s.next_lost()
    assert s.current_bet().bet_amount == 1
    s = s.next_won()
    assert s.current_bet().bet_amount == 3
    s = s.next_lost()
    assert s.current_bet().bet_amount == 1

def test_player1236():
    """ Helper functiosn for testing Player1236

    """

    data = [
        ([1, 1, 1, 1], 16),
        ([1, 1, 1, 2], 18),
        ([1, 1, 2, 1], 16),
        ([1, 1, 2, 2], 22),
        ([1, 2, 1, 1], 16),
        ([1, 2, 1, 2], 18),
        ([1, 2, 2, 1], 21),
        ([1, 2, 2, 2], 25),
        ([2, 1, 1, 1], 16),
        ([2, 1, 1, 2], 18),
        ([2, 1, 2, 1], 16),
        ([2, 1, 2, 2], 22),
        ([2, 2, 1, 1], 21),
        ([2, 2, 1, 2], 23),
        ([2, 2, 2, 1], 20),
        ([2, 2, 2, 2], 32),
    ]
    for (sequence, expected_stake) in data:
        rng = NonRandom(sequence)
        game = create_game(rng=rng)
        player= Player1236(game.table)
        player.set_stake(20)
        for i in range(len(sequence)):
            game.cycle(player)
        assert player.stake == expected_stake
