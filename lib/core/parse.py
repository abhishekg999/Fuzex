# Parser for Fuzex expressions. An Fuzex expression can represent any
# finite regular language, using notation similar to regular expressions.
# Instead of recognizing regular expressions, Fuzex expressions generate
# all strings of a finite language specified by an expression.

from .lexer import Lexer
from .definitions import (
    CLOSE_BRACK,
    CLOSE_CURL,
    CLOSE_PAREN,
    Char,
    CountQuantifier,
    DynamicChar,
    Expression,
    Join,
    OPEN_BRACK,
    OPEN_CURL,
    OPEN_PAREN,
    OPTIONAL,
    OptionalQuantifier,
    Or,
    Quantifier,
    RANGE_QUANTIFIER_CHARACTERS,
    RangeQuantifier,
    SingleQuantifier,
    Statement,
    VAR_DECLAR,
    Variable,
)


class ParserException(Exception):
    pass


class Parser:
    """
    Parser for Fuzex expressions. An Fuzex expression can represent any
    finite regular language, using notation similar to regular expressions.
    Instead of recognizing regular expressions, Fuzex expressions generate
    all strings of a finite language specified by an expression.
    """

    def __init__(self, expr: str) -> None:
        self.Lexer = Lexer(expr)

    def parse(self) -> Expression:
        return self._parse_expression()

    def _parse_expression(self) -> Expression:
        expression = Expression()
        while not self.Lexer.EOF():
            statement = self._parse_statement()
            expression.push(statement)

        return expression

    def _parse_statement(self) -> Statement:
        """
        Depending on the statement.
        """
        value = None
        quantifier = None
        i, c = self.Lexer.peek()

        if isinstance(c, Char):
            value = self._parse_char()

        elif c == OPEN_PAREN:
            value = self._parse_join()

        elif c == VAR_DECLAR:
            value = self._parse_variable()

        elif c == OPEN_BRACK:
            value = self._parse_dynamic_char()
        else:
            raise ParserException(f"Unexpected character at index {i}, got {c}.")

        if self.Lexer.EOF():
            quantifier = SingleQuantifier()
            return Statement(value, quantifier)

        i, c = self.Lexer.peek()
        if c == OPEN_CURL or c == OPTIONAL:
            quantifier = self._parse_quantifier()
        else:
            quantifier = SingleQuantifier()

        return Statement(value, quantifier)

    def _parse_char(self) -> Char:
        i, c = self.Lexer.consume()
        value = ""
        if not isinstance(c, Char):
            raise ParserException("how tf")

        return c

    def _parse_dynamic_char(self) -> DynamicChar:
        i, c = self.Lexer.consume()
        value = ""
        if c != OPEN_BRACK:
            raise ParserException("how tf")

        while not self.Lexer.EOF():
            i, c = self.Lexer.peek()
            if c == CLOSE_BRACK:
                self.Lexer.consume()
                break
            elif isinstance(c, Char):
                i, c = self.Lexer.consume()
                value += c.value
            else:
                raise ParserException(
                    f"Unexpected character in class expression, got {c} at index {i}"
                )

        else:
            raise ParserException("Invalid class expression, closing ] not found.")

        return DynamicChar(value)

    def _parse_quantifier(self) -> Quantifier:
        """
        Parses starting from { until } or ?.
        RangeQuantifier can only have numbers
        and 0 or 1 commas.
        """
        quantifier = None
        i, c = self.Lexer.peek()
        if c == OPEN_CURL:
            quantifier = self._parse_range_quantifier()
        else:
            quantifier = OptionalQuantifier()
            self.Lexer.consume()

        return quantifier

    def _parse_range_quantifier(self):
        value = ""
        i, c = self.Lexer.consume()
        if c != OPEN_CURL:
            raise ParserException("how tf")

        while not self.Lexer.EOF():
            i, c = self.Lexer.peek()
            if c == CLOSE_CURL:
                self.Lexer.consume()
                break
            elif isinstance(c, Char) and c.value in RANGE_QUANTIFIER_CHARACTERS:
                i, c = self.Lexer.consume()
                value += c.value
            else:
                raise ParserException(
                    f"Unexpected character in range quantifier, got {c} at index {i}"
                )
        else:
            raise ParserException("Invalid range expression, closing } not found.")

        comma_count = value.count(",")
        if comma_count == 0:
            return CountQuantifier(int(value))

        if comma_count == 1:
            range = value.split(",")
            if range[0] and range[1]:
                return RangeQuantifier(int(range[0]), int(range[1]) + 1)

            elif not range[0] and range[1]:
                return RangeQuantifier(0, int(range[1]) + 1)

            elif range[0] and not range[1]:
                raise RangeQuantifier.RangeException(
                    "Fuzex does not support infinite range."
                )

            else:
                raise RangeQuantifier.RangeException(f"Unspecified range at {i}")
        else:
            raise RangeQuantifier.RangeException(f"Invalid range expression at {i}")

    def _parse_join_expression(self) -> Expression:
        expression = Expression()
        while not self.Lexer.EOF():
            i, c = self.Lexer.peek()
            if c == CLOSE_PAREN:
                self.Lexer.consume()
                break
            statement = self._parse_statement()
            expression.push(statement)
        else:
            raise ParserException("Invalid Join expression, closing ) not found.")

        return expression

    def _parse_join(self) -> Join:
        """
        Join parses starting from ( until ).
        A join can contain an expression
        """

        i, c = self.Lexer.consume()
        if c != OPEN_PAREN:
            raise ParserException("how did this happen")

        expression = self._parse_join_expression()

        return Join(expression)

    def _parse_variable_name(self):
        return Char("var") # TODO: implement actual variables?

    def _parse_variable(self) -> Variable:
        i, c = self.Lexer.consume()
        if c != VAR_DECLAR:
            raise ParserException("how did this happen")

        if self.Lexer.EOF():
            raise ParserException(
                "Unexpected EOF after $, expected variable declaration."
            )

        variable = self._parse_variable_name()
        return variable

    def _parse_or(self) -> Or:
        """
        Or parses an empty Or object. It must follow a Statement
        and come before a statement. Takes previous statement as
        argument.

        Returns Or containing prev, and next statement
        """
        pass

