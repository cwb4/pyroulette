from outcome import Outcome
import inspect

class BinBuilder:
    """ Create the outcomes for all the 38 bins on
    a roulette wheel

    """
    def __init__(self):
        pass

    def build_bins(self, wheel):
        members = inspect.getmembers(self)
        for (name, func) in members:
            if name.startswith("gen_"):
                func(wheel)

    def gen_straight_bets(self, wheel):
        for i in range(1, 37):
            outcome = Outcome(str(i), 35)
            wheel.add_outcome(i, outcome)
        wheel.add_outcome(0, Outcome("0", 35))
        wheel.add_outcome(37, Outcome("00", 35))

    def gen_split_bets(self, wheel):
        # Horizontal splits:
        for r in range(12):
            # First column number:
            n = 3 * r + 1
            # Column 1-2 split
            outcome = Outcome("%s, %s" % (n, n+1), 17)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n+1, outcome)
            # Second column number:
            n = 3 * r + 2
            # Column 2-3 split
            outcome = Outcome("%s, %s" % (n, n+1), 17)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n+1, outcome)
        # Vertical splits:
        for i in range(1, 33):
            outcome = Outcome("%s, %s" % (i, i+3), 17)
            wheel.add_outcome(i, outcome)
            wheel.add_outcome(i + 3, outcome)

    def gen_streets_bets(self, wheel):
        for r in range(12):
            n = 3 * r + 1
            outcome = Outcome("%i, %i, %i" % (n, (n + 1), (n + 2)), 11)
            wheel.add_outcome(n, outcome)
            wheel.add_outcome(n + 1, outcome)
            wheel.add_outcome(n + 2, outcome)

    def gen_corner_bets(self, wheel):
        def _gen_corner_bet(n):
            ns = (n, (n + 1), (n + 3), (n + 4))
            outcome = Outcome(", ".join([str(x) for x in ns]), 8)
            for bin in ns:
                wheel.add_outcome(bin, outcome)

        for r in range(11):
            # first column
            n = 3 * r + 1
            _gen_corner_bet(n)
            # second column
            n = 3 * r + 2
            _gen_corner_bet(n)

    def gen_line_bets(self, wheel):
        for r in range(10):
            line = list()
            for i in range(6):
                line.append(3 * r + 1 + i)
            outcome = Outcome(", ".join([str(x) for x in line]), 5)
            for bin in line:
                wheel.add_outcome(bin, outcome)

    def gen_dozen_bets(self, wheel):
        for d in range(3):
            outcome = Outcome("Dozen %i" % (d + 1), 2)
            for m in range(0, 12):
                wheel.add_outcome(12 * d + m + 1, outcome)

    def gen_column_bets(self, wheel):
        for c in range(3):
            outcome = Outcome("Column %i" % (c + 1), 2)
            for r in range(0, 12):
                wheel.add_outcome(3 * r + c + 1, outcome)

    def gen_even_money_bets(self, wheel):
        red   = Outcome("Red"   , 1)
        black = Outcome("Black" , 1)
        even  = Outcome("Even"  , 1)
        odd   = Outcome("Odd"   , 1)
        high  = Outcome("High"  , 1)
        low   = Outcome("Low"   , 1)
        for n in range(1, 37):
            if n < 19:
                wheel.add_outcome(n, low)
            else:
                wheel.add_outcome(n, high)
            if n % 2 == 0:
                wheel.add_outcome(n, even)
            else:
                wheel.add_outcome(n, odd)
            if n in [1, 3, 5, 7, 9,
                     12, 14, 16, 18,
                     19, 21, 23, 25,
                     30, 32, 34, 36]:
                wheel.add_outcome(n, red)
            else:
                wheel.add_outcome(n, black)
