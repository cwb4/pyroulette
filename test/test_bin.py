from bin import Bin
from outcome import Outcome

def test_bin_has_outcomes():
    outcome_0 = Outcome("0", 35)
    outcome_5 = Outcome("Five", 6)
    outcome_00 = Outcome("00", 35)
    bin_0 = Bin()
    bin_0.add(outcome_0)
    bin_0.add(outcome_5)
    bin_00 = Bin()
    bin_00.add(outcome_00)
    bin_00.add(outcome_5)
    assert bin_0.outcomes == frozenset([outcome_0, outcome_5])
    assert bin_00.outcomes == frozenset([outcome_00, outcome_5])
