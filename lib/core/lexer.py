import sys
from .reader import Reader
from .definitions import ESCAPE_CHARACTER, SPECIAL_CHARACTERS, Char

from . import DEBUG
_print = print
print = lambda *args, **kwargs: _print(*args, file=sys.stderr, **kwargs)


class LexerException(Exception):
    pass


class Lexer:
    def __init__(self, expr) -> None:
        self.expr = expr
        self.reader = Reader(expr)
        self._tokenStream = list(q for q in self.tokenize())
        self._length = len(self._tokenStream)
        self.i = 0

    def __len__(self):
        return self._length

    def tokenize(self):
        while not self.reader.EOF():
            i, c = self.reader.consume()
            if c == ESCAPE_CHARACTER and self.reader.EOF():
                raise LexerException("Recieved escape character at EOF")

            if c == ESCAPE_CHARACTER:
                i, c = self.reader.consume()
                yield Char(c)

            elif c not in SPECIAL_CHARACTERS:
                yield Char(c)

            elif c in SPECIAL_CHARACTERS:
                yield c

    def EOF(self):
        if DEBUG:
            print(f"[INFO] Checked EOF at index {self.i}.")

        if self.i >= self._length:
            return True
        return False

    def consume(self):
        self.i += 1
        if DEBUG:
            print(
                f"[INFO] Trying to consume {self._tokenStream[self.i-1]} at index {self.i-1}"
            )
        return self.i - 1, self._tokenStream[self.i - 1]

    def peek(self):
        if DEBUG:
            print(
                f"[INFO] Trying to peek {self._tokenStream[self.i]} at index {self.i}"
            )
        return self.i, self._tokenStream[self.i]

    def stream(self):
        for q in self._tokenStream:
            yield q
