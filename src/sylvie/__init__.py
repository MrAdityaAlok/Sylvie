"""Sylvie: the maths interpreter.

It is a mathematical interpreter. It takes mathematical expressions
as text and then evaluate it.

Examples:
    As REPL:

        >> 4*8(93-2/4*3)-9
        -8.650273224043715

        >> 8/4
        2.0

        >> 5*5
        25

    As module:

        calc = Sylvie()
        print(calc.parse("4*8"))
"""

from typing import Union


class Sylvie:
    """Evaluates the given mathematical expressions.

    Attributes:
        interpreter_type: Optional; An integer value representing
            type of interpreter to be used.
    """

    def __init__(self, interpreter_type: int = 0) -> None:
        """Initializes Sylvie's interpreter type.

        Args:
            interpreter_type: Optional; An integer representing interpreter
                type to be used. 1 for abstract-syntax-tree based while
                0 for syntax-directed. (Default 0)
        """
        self.interpreter_type = interpreter_type

    @property
    def interpreter_type(self):
        """Returns interpreter type."""
        return self._interpreter_type

    @interpreter_type.setter
    def interpreter_type(self, value: int):
        """Set interpreter type.

        Args:
            value: 0 for syntax-directed interpreter or
                1 for abstract-syntax-tree based interpreter.
        """
        self._interpreter_type: int = value

    def parse(self, text: str) -> Union[int, float]:
        """Parses the given text as mathematical expressions.

        Args:
            text : mathematical expressions to be evaluated.

        Returns:
            Result of expressions as integer or float.
        """
        if self.interpreter_type == 0:
            from sylvie.syntax_directed.parser import Parser
        else:
            # from sylvie.ast_based.parser import Parser
            raise NotImplementedError(
                "Parser for ast based interpreter has not been implemented yet."
            )

        return Parser(text=text).expr()


def _main():  # skipcq: PY-D0003
    import argparse

    parser = argparse.ArgumentParser(description="Sylvie's math interpreter")
    parser.add_argument(
        "-i",
        "--interpreter-type",
        nargs=1,
        default=0,
        type=int,
        help=(
            "Change interpreter type."
            " Pass 1 for ast based or 0 (default) for syntax directed."
        ),
    )
    s = Sylvie(parser.parse_args().interpreter_type)

    def evaluate():  # skipcq: PY-D0003
        try:
            text = input(">> ")
            print(s.parse(text=text))
        except (ValueError, SyntaxError) as err:
            print("Error :", err)

    try:
        while True:
            evaluate()
    except EOFError:
        print("Exiting as requested.")


if __name__ == "__main__":
    _main()
