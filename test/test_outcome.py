from outcome import Outcome
def test_equality():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 2)
    o3 = Outcome("Low", 4)
    assert o1 == o2
    assert o1 != o3

def test_same_hash():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 2)
    assert hash(o1) == hash(o2)

