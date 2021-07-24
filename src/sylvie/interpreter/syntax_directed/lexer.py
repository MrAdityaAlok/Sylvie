from typing import Any, Generator, Union
from sylvie.interpreter.tokens import Token, TokenType

MINUS = "-"
PLUS = "+"
DIV = "/"
MULTIPLY = "*"
DECIMAL = "."
LPAREN = "("
RPAREN = ")"


class Lexer:
    def __init__(self, text) -> None:
        """Convert input text into a stream of tokens."""
        self.text = iter(text)
        self.advance()

    def advance(self) -> None:
        try:
            self.current_char: Union[str, Any] = next(self.text)
        except StopIteration:
            self.current_char = None

    @staticmethod
    def error(msg: str):
        raise ValueError(f"ValueError: {msg}")

    def get_tokens(self) -> Generator:
        while self.current_char:
            if self.current_char.isspace():
                self.advance()
                continue
            if self.current_char.isdigit() or self.current_char == DECIMAL:
                yield self.scan_digits()
                continue
            if self.current_char == LPAREN:
                yield Token(TokenType.LPAREN)
            elif self.current_char == RPAREN:
                yield Token(TokenType.RPAREN)
            elif self.current_char == PLUS:
                yield Token(TokenType.PLUS)
            elif self.current_char == MINUS:
                yield Token(TokenType.MINUS)
            elif self.current_char == DIV:
                yield Token(TokenType.DIV)
            elif self.current_char == MULTIPLY:
                yield Token(TokenType.MULTIPLY)
            else:
                self.error(f"invalid character '{self.current_char}'")

            self.advance()

        yield Token(TokenType.EOF)

    def scan_digits(self) -> Token:
        decimal_count = 0
        num: str = ""

        while self.current_char and (
            self.current_char.isdigit() or self.current_char == DECIMAL
        ):
            if self.current_char == DECIMAL:
                decimal_count += 1
            if decimal_count > 1:
                self.error("more than one decimal in single number")

            num += self.current_char
            self.advance()

        if num.startswith(DECIMAL):
            num = "0" + num
        elif num.endswith(DECIMAL):
            num += "0"

        return Token(TokenType.NUMBER, float(num) if decimal_count else int(num))
