from wheel import Wheel
from outcome import Outcome

class NonRandom:
    def __init__(self):
        self.value = None

    def set_seed(self, seed):
        self.value = seed

    def choice(self, sequence):
        assert self.value is not None, "set_seed was not called"
        assert len(sequence) > self.value
        return sequence[self.value]

def test_run_the_wheel():
    nrg = NonRandom()
    nrg.set_seed(0) # We will always return the first element
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

    wheel.rng.set_seed(37)
    bin = wheel.next()
    assert bin.outcomes == frozenset([outcome_00, outcome_5])
