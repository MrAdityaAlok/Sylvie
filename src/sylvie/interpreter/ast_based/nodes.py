from sylvie.interpreter.tokens import Token
from dataclasses import dataclass, field
from sylvie.interpreter.ast_based.ast import AST
from typing import Union


@dataclass
class BinOp(AST):
    right_child: Token
    op: Token
    left_child: Token


@dataclass
class Num(AST):
    token: Token
    value: Union[int,float] = field(init=False)

    def __post_init__(self):
        self.value = self.token.value
