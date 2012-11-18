from outcome import Outcome
from builder import BinBuilder
from wheel import Wheel

def test_straight_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_straight_bets(wheel)
    assert wheel.get_bin(0).outcomes == frozenset([Outcome("0", 35)])
    assert wheel.get_bin(37).outcomes == frozenset([Outcome("00", 35)])
    assert wheel.get_bin(3).outcomes == frozenset([Outcome("3", 35)])

def test_split_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_split_bets(wheel)
    assert wheel.get_bin(1).outcomes == frozenset([
        Outcome("1, 2", 17),
        Outcome("1, 4", 17)
    ])
    assert wheel.get_bin(20).outcomes == frozenset([
        Outcome("17, 20", 17),
        Outcome("19, 20", 17),
        Outcome("20, 21", 17),
        Outcome("20, 23", 17),
    ])
    assert wheel.get_bin(18).outcomes == frozenset([
        Outcome("15, 18", 17),
        Outcome("17, 18", 17),
        Outcome("18, 21", 17),
    ])

def test_streets_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_streets_bets(wheel)
    assert wheel.get_bin(1).outcomes == frozenset([Outcome("1, 2, 3", 17)])
    assert wheel.get_bin(2).outcomes == frozenset([Outcome("1, 2, 3", 17)])
    assert wheel.get_bin(3).outcomes == frozenset([Outcome("1, 2, 3", 17)])

def test_corner_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_corner_bets(wheel)
    assert wheel.get_bin(1).outcomes == frozenset([Outcome("1, 2, 4, 5", 8)])
    assert wheel.get_bin(4).outcomes == frozenset([
        Outcome("1, 2, 4, 5", 8),
        Outcome("4, 5, 7, 8", 8),
        ])
    assert wheel.get_bin(7).outcomes == frozenset([
        Outcome("4, 5, 7, 8", 8),
        Outcome("7, 8, 10, 11", 8),
        ])
    assert wheel.get_bin(8).outcomes == frozenset([
        Outcome("4, 5, 7, 8", 8),
        Outcome("5, 6, 8, 9", 8),
        Outcome("7, 8, 10, 11", 8),
        Outcome("8, 9, 11, 12", 8),
        ])

def test_line_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_line_bets(wheel)
    assert wheel.get_bin(1).outcomes == frozenset([
        Outcome("1, 2, 3, 4, 5, 6", 5)
    ])
    assert wheel.get_bin(4).outcomes == frozenset([
        Outcome("1, 2, 3, 4, 5, 6", 5),
        Outcome("4, 5, 6, 7, 8, 9", 5)
    ])

def test_dozen_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_dozen_bets(wheel)
    assert wheel.get_bin(1).outcomes == frozenset([
        Outcome("Dozen 1", 2)
    ])
    assert wheel.get_bin(13).outcomes == frozenset([
        Outcome("Dozen 2", 2)
    ])
    assert wheel.get_bin(36).outcomes == frozenset([
        Outcome("Dozen 3", 2)
    ])

def test_column_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_column_bets(wheel)
    assert wheel.get_bin(1).outcomes  == frozenset([Outcome("Column 1", 2)])
    assert wheel.get_bin(28).outcomes == frozenset([Outcome("Column 1", 2)])
    assert wheel.get_bin(27).outcomes == frozenset([Outcome("Column 3", 2)])

def test_even_money_bets():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.gen_even_money_bets(wheel)
    assert wheel.get_bin(1).outcomes == frozenset([
        Outcome("Low", 1),
        Outcome("Odd", 1),
        Outcome("Red", 1),
    ])
    assert wheel.get_bin(24).outcomes == frozenset([
        Outcome("High", 1),
        Outcome("Even", 1),
        Outcome("Black", 1),
    ])

def test_build():
    bin_builder = BinBuilder()
    wheel = Wheel()
    bin_builder.build_bins(wheel)
    wheel.get_bin(13).outcomes == frozenset([
        Outcome("13", 35),
        Outcome("10, 13", 17),
        Outcome("13, 14", 17),
        Outcome("13, 16", 17),
        Outcome("13, 14, 15", 11),
        Outcome("10, 11, 13, 14", 8),
        Outcome("13, 14, 16, 17", 8),
        Outcome("10, 11, 12, 13, 14, 15", 5),
        Outcome("13, 14, 15, 16, 17, 18", 5),
        Outcome("Dozen 1", 2),
        Outcome("Column 1", 1),
        Outcome("Low", 1),
        Outcome("Odd", 1),
        Outcome("Black", 1),
    ])



