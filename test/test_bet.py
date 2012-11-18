from bet import Bet
from outcome import Outcome

def test_win_loose():
    zerozero = Outcome("00", 35)
    bet = Bet(10, zerozero)
    assert bet.win_amount() == 350
