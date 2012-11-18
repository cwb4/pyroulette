class NonRandom:
    def __init__(self, values):
        self.values = values
        self._index = 0

    def choice(self, sequence):
        rand = self.values[self._index]
        self._index += 1
        return sequence[rand]
