from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Union


@unique
class TokenType(IntEnum):
    PLUS = 1
    MINUS = 2
    DIV = 3
    MULTIPLY = 4
    NUMBER = 5
    RPAREN = 6
    LPAREN = 7
    EOF = 8


@dataclass
class Token:
    type: TokenType
    value: Union[int, float, None] = None

    def __repr__(self) -> str:
        """String representation of token object."""
        return f"{self.type.name}: {self.value if self.value else ''}"
