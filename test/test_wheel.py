from wheel import Wheel
from outcome import Outcome
from non_random import NonRandom


def test_run_the_wheel():
    nrg = NonRandom([0, 37])
    wheel = Wheel(nrg)
    outcome_0 = Outcome("0", 35)
    outcome_5 = Outcome("Five", 6)
    outcome_00 = Outcome("00", 35)

    wheel.add_outcome(0, outcome_0)
    wheel.add_outcome(0, outcome_5)
    wheel.add_outcome(37, outcome_00)
    wheel.add_outcome(37, outcome_5)

    bin = wheel.next()
    assert bin.outcomes == frozenset([outcome_0, outcome_5])

    bin = wheel.next()
    assert bin.outcomes == frozenset([outcome_00, outcome_5])


def test_get_outcome():
    wheel = Wheel()
    outcome_5 = Outcome("Five", 6)
    wheel.add_outcome(4, outcome_5)
    assert wheel.get_outcoume("Five") == outcome_5
