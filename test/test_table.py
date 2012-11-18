from wheel import create_wheel
from table import Table
from bet import Bet, InvalidBet
from outcome import Outcome

import pytest

def test_place_bet():
    wheel = create_wheel()
    table = Table(wheel)
    zerozero = Outcome("00", 35)
    zerozero_bet = Bet(900, zerozero)
    red_bet = Bet(60, Outcome("Red", 1))
    table.place_bet(zerozero_bet)
    table.place_bet(red_bet)
    assert [x.bet_amount for x in table] == [900, 60]
    with pytest.raises(InvalidBet):
        table.place_bet(red_bet)
