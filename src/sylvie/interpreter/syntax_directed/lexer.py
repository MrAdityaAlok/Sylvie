"""This module is the lexical analyzer (also known as scanner or tokenizer).

This is responsible for converting input text into a stream (here generator) of
tokens.
"""

from typing import Any, Generator, Union

from sylvie.interpreter.tokens import Token, TokenType


class Lexer:
    def __init__(self, text) -> None:
        """Converts input text into a stream of tokens."""
        self.text = iter(text)
        self.advance()

    def advance(self) -> None:
        """Move to next character."""
        try:
            self.current_char: Union[str, Any] = next(self.text)
        except StopIteration:
            self.current_char = "EOF" if self.current_char != "EOF" else None

    @staticmethod
    def error(msg: str):
        raise ValueError(f"ValueError: {msg}")

    def get_tokens(self) -> Generator:
        """Get tokens generated by the lexer.

        :returns : Generator
        """
        while self.current_char:
            if self.current_char.isspace():
                self.advance()

            if self.current_char.isdigit() or self.current_char == ".":
                yield self.scan_digits()

            try:
                # get enum member by value, e.g.
                # TokenType('(') --> TokenType.LPAREN
                token_type = TokenType(self.current_char)
            except ValueError:  # TODO: define lexing exception
                # if self.current_char not member of TokenType
                self.error(f"Invalid character '{self.current_char}'")
            else:
                token = Token(token_type, token_type.value)

            self.advance()
            yield token

    def scan_digits(self) -> Token:
        """Scans a continuous text of real constants."""
        decimal_count = 0
        num: str = ""

        while self.current_char and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            if self.current_char == ".":
                decimal_count += 1
            if decimal_count > 1:
                self.error("More than one decimal in single number")

            num += self.current_char
            self.advance()

        if num.startswith("."):
            num = "0" + num
        elif num.endswith("."):
            num += "0"

        return (
            Token(TokenType.NUMBER, float(num))
            if decimal_count > 0
            else Token(TokenType.NUMBER, int(num))
        )
