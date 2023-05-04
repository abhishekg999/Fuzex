class Reader:
    def __init__(self, expr) -> None:
        self.expr = expr
        self._length = len(self.expr)
        self.i = 0

    def __len__(self):
        return self._length

    def EOF(self):
        if self.i >= self._length:
            return True
        return False

    def consume(self):
        self.i += 1
        return self.i - 1, self.expr[self.i - 1]

    def peek(self):
        return self.i - 1, self.expr[self.i]
