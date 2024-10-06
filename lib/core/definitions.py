"""
SPECIAL_CHARACTERS:
[   - start of character group
]   - end of character group

{   - start of repetition count
}   - end of repitition count

,   - separate digits inside repition count
?   - 0 or 1 occurance, follows literal or character group

$   - specify variable, must immediately be followed by ( 
(   - if followed by $ start of specify variable
)   - if followed by $ end of specify variable

(   - start of joined statement group
)   - end of joined statement group

\   - escape token used to escape Special Characters   

Grammar:

------------------- BASE DEFINITIONS -------------------
END: \n
SPECIAL_CHARACTER: 
    | [
    | ]
    | {
    | }
    | ?
    | $
    | (
    | )
    | |

INPUT_NAME_CHARACTER:
    | ALPHABET
    | NUMBER
    | UNDERSCORE

NON_SPECIAL_CHARACTER: 
# All characters that are not special characters

ESCAPED_CHARACTER:
    | '\' SPECIAL_CHARACTER

token:
    | NON_SPECIAL_CHARACTER
    | ESCAPED_CHARACTER
    
------------------- MAIN EXPRESSION -------------------

expression: statement+ 
statement:
    | char
    | dynamic_char
    | join
    | variable

quantified_stmt:
    | variable_value quantifier

quantifier:
    | ?
    | range_quantifier

range_quantifier:
    | {NUMBER+}             # repeat n times                 
    | {NUMBER+,NUMBER+}     # repeat from n to m times
    | {,NUMBER+}            # repeat from 0 to m times

static_stmt:
    | NON_SPECIAL_CHARACTERS+
    | variable

variable:
    | $(variable_name)

variable_name:
    | INPUT_NAME_CHARACTER+

"""

from math import prod


ESCAPE_CHARACTER = "\\"
SPECIAL_CHARACTERS = r"[]{}()?$()|"
INPUT_NAME_CHARACTER = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789_"
RANGE_QUANTIFIER_CHARACTERS = r"0123456789,"

OPEN_PAREN = "("
CLOSE_PAREN = ")"

OPEN_BRACK = "["
CLOSE_BRACK = "]"


OPEN_CURL = "{"
CLOSE_CURL = "}"

OPTIONAL = "?"
VAR_DECLAR = "$"

DYNAMIC_RANGE_SPECIFIER = "-"


class Char:
    def __init__(self, value="") -> None:
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def size(self):
        return 1

    def generate(self):
        yield self.value


class DynamicChar:
    class RangeException(Exception):
        pass

    def _get_range(self, i, j):
        if ord(j) < ord(i):
            raise self.RangeException()
        return [chr(x) for x in range(ord(i), ord(j) + 1)]

    def __init__(self, expr="") -> None:
        self.expr = expr
        chars = list(expr)
        if len(chars) <= 2:
            # self.value = list(set(chars))
            self.value = sorted(list(set(chars)))
            return

        i = 1
        to_extend = []
        while i < len(chars) - 1:
            if chars[i] == DYNAMIC_RANGE_SPECIFIER:
                prev = chars[i - 1]
                next = chars[i + 1]
                del chars[i - 1 : i + 2]
                i -= 2
                to_extend += self._get_range(prev, next)
            i += 1

        chars += to_extend
        # self.value = list(set(chars))
        self.value = sorted(list(set(chars)))

    def __repr__(self):
        return f'DynamicChar("{self.expr}")'

    def size(self):
        return len(self.value)

    def generate(self):
        for c in self.value:
            yield c


class Variable:
    def __init__(self, value="") -> None:
        self.value = value

    def evaluate(self, value):
        pass


class Join:
    """
    A join contains an Expression.
    """

    def __init__(self, expression) -> None:
        self.expression = expression

    def __repr__(self) -> str:
        return self.expression.__repr__()

    def size(self):
        return self.expression.size()

    def generate(self):
        yield from self.expression.generate()


class Or:
    """
    A Or contains two statements. It will generate values from each
    statements independently.
    """

    def __init__(self, st_a, st_b) -> None:
        self.value = [st_a, st_b]

    def __repr__(self):
        return f"Or({self.value})"

    def size(self):
        return self.value[0].size() + self.value[1].size()

    def generate(self):
        yield from self.value[0].generate()
        yield from self.value[1].generate()


class Expression:
    """
    Expression contains a list of statements.
    Each statement has a generate method that yields
    strings in the statement. Each statement additionally
    has a .size() property that yields the number of strings
    it generates. The size of an expression is the product
    of the sizes of its statements.
    """

    def __init__(self) -> None:
        self.statements = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.statements})"

    def generate(self):
        yield from self._generate(0)

    def _generate(self, n):
        if len(self.statements) == 0:
            yield ""
            return

        if n == len(self.statements) - 1:
            yield from self.statements[n].generate()
        else:
            for c in self.statements[n].generate():
                for r in self._generate(n + 1):
                    yield c + r

    def size(self):
        return prod(q.size() for q in self.statements)

    def push(self, item):
        """Push an item onto the expression's statement list"""
        self.statements.append(item)

    def pop(self):
        """Pop the last item off the expression's statement list"""
        return self.statements.pop()


class Statement:
    """
    A statement consists of a value and a quantifier,
    indicating how differing values the statement alone
    generates. The value can be a, DynamicString,
    a Variable, or a Join.
    """

    def __init__(self, value, quantifier) -> None:
        self.value = value
        self.quantifier = quantifier

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value},{self.quantifier})"

    def size(self):
        return sum(
            self.value.size() ** (self.quantifier.begin() + i)
            for i in range(self.quantifier.size())
        )

    def generate(self):
        for count in self.quantifier.generate():
            yield from self._generate(count)

    def _generate(self, n):
        if n == 0:
            yield ""
        elif n == 1:
            for val in self.value.generate():
                yield val
        else:
            for c in self.value.generate():
                for r in self._generate(n - 1):
                    yield c + r


class Quantifier:
    """
    A quantifier describes a starting count, and the number
    total values to generate. It then generates the value
    self.start times, to self.start + self.count times.
    """

    def __init__(self, start, count) -> None:
        self.start = start
        self.count = count

    def __repr__(self) -> str:
        return f"{{{self.start},{self.start+self.count-1}}}"

    def generate(self):
        for i in range(self.start, self.start + self.count):
            yield i

    def size(self):
        return self.count

    def begin(self):
        return self.start


class SingleQuantifier(Quantifier):
    def __init__(self) -> None:
        super().__init__(1, 1)


class OptionalQuantifier(Quantifier):
    def __init__(self) -> None:
        super().__init__(0, 2)


class CountQuantifier(Quantifier):
    def __init__(self, start) -> None:
        super().__init__(start, 1)


class RangeQuantifier(Quantifier):
    class RangeException(Exception):
        pass

    def __init__(self, start, end) -> None:
        if end <= start:
            raise RangeQuantifier.RangeException("Invalid range")
        super().__init__(start, end - start)


if __name__ == "__main__":
    q = DynamicChar("aa-zA-Z")
    print(q.value)
    assert q.size() == 26 * 2
