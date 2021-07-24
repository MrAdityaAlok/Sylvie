from typing import Union
from sylvie.interpreter.syntax_directed.lexer import Lexer
from sylvie.interpreter.tokens import TokenType


class Parser:
    def __init__(self, text: str) -> None:
        """Parse tokens and evaluate expression."""
        self.tokens = Lexer(text).get_tokens()
        self.advance()

    def advance(self) -> None:
        try:
            self.current_token = next(self.tokens)
            # print("advance called :", self.current_token)
        except StopIteration:
            pass
            # self.current_token = Token(TokenType.EOF)

    @staticmethod
    def error() -> None:
        raise SyntaxError("SyntaxError: invalid syntax")

    def eat(self, expected_token: TokenType) -> None:
        if self.current_token.type == expected_token:
            self.advance()
        else:
            self.error()

    def factor(self) -> Union[int, float]:
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return token.value

        # if is not NUMBER then has to be parenthesis
        self.eat(TokenType.LPAREN)
        result = self.expr()
        self.eat(TokenType.RPAREN)
        return result

    def term(self) -> Union[int, float]:
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

    def expr(self) -> Union[int, float]:
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
        if self.current_token.type != TokenType.EOF:
            self.error()
        return result
