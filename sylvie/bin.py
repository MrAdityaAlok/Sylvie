"""This module contains functioncs to run Sylvie from command line."""

from sylvie.interpreter.parser import Parser


def cmd():
    """Starts Sylvie's REPL."""
    parser = Parser()
    try:
        while True:
            try:
                text = input("Sylvie >> ")
                print(parser.parse(text))
            except (ValueError, SyntaxError, ZeroDivisionError) as err:
                print("Error :", err)
    except (EOFError, KeyboardInterrupt):
        print("Exiting as requested.")
