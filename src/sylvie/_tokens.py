"""This modules contains classes for token handling.

class TokenType(Enum): is an enum representing valid tokens.

class Token : a dataclass representing a token with it's value and type.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Union


class TokenType(Enum):
    """Enum representing valid tokens."""

    PLUS = "+"
    MINUS = "-"
    DIV = "/"
    MULTIPLY = "*"
    NUMBER = "REAL_CONST"
    RPAREN = ")"
    LPAREN = "("
    EOF = "EOF"


@dataclass
class Token:
    """Dataclass representing a token with it's type and value."""

    type: TokenType
    value: Union[int, float, str]
