"""This module parses the lexed tokens and evaluates the expression.

    Example:
        calc >> --7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

    Grammar:
        sub_expr  : mul ((PLUS | MINUS) mul)*
        mul       : term ((MUL | DIV) term))*
        term      : (PLUS | MINUS)* factor
        factor    : NUMBER | LPAREN sub_expr RPAREN
"""

from typing import Union

from sylvie.interpreter.syntax_directed.lexer import Lexer
from sylvie.interpreter.tokens import TokenType


class Parser:
    def __init__(self, text: str) -> None:
        """Parses tokens and evaluates the expression formed."""
        self.tokens = Lexer(text).get_tokens()
        self.column = 0
        self.advance()

    def advance(self) -> None:
        """Move to next token and increase column count."""
        try:
            self.current_token = next(self.tokens)
            self.column += 1
        except StopIteration:
            pass

    @staticmethod
    def error(msg: str) -> None:
        raise SyntaxError(msg)

    def eat(self, expected_token: TokenType) -> None:
        """Validated current token and advance to next token.

        Checks if current token is the the token we expect to be present,
        if not then raise SyntaxError.
        """
        if self.current_token.type == expected_token:
            self.advance()
        else:
            self.error(
                "Unexpected character '{}' at column {}, expected '{}'".format(
                    self.current_token.value, self.column, expected_token.value
                )
            )

    def factor(self) -> Union[int, float]:
        """factor : NUMBER | LPAREN sub_expr RPAREN"""
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return token.value

        # if is not NUMBER then has to be parenthesis
        self.eat(TokenType.LPAREN)
        result = self.sub_expr()
        self.eat(TokenType.RPAREN)
        return result

    def term(self) -> Union[int, float]:
        """term : (MINUS | PLUS)* factor"""
        minus_count = 0
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif self.current_token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                minus_count += 1

        result = self.factor()
        return (0 - result) if minus_count % 2 else result

    def mul(self):
        """mul : term ((MUL | DIV) term)*"""
        result = self.term()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIV):
            if self.current_token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                result *= self.term()
            elif self.current_token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                try:
                    result /= self.term()
                except ZeroDivisionError:
                    print("Oh! Its beyond my limit")
                    raise
        return result

    def sub_expr(self) -> Union[int, float]:
        """sub_expr: mul ((PLUS | MINUS) mul)*"""
        result = self.mul()

        while self.current_token.type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.mul()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.mul()
        return result

    def expr(self):
        """Parsed arithmetic expression."""
        result = self.sub_expr()
        if self.current_token.type != TokenType.EOF:
            self.error(
                "Unexpected character '{}' at column {}".format(
                    self.current_token.value, self.column
                )
            )
        return result
