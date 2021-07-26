import argparse
import importlib


def main(script: str = "Sylvie"):
    parser = argparse.ArgumentParser(
        description="Mathematical interpreter",
        usage=f"{script} [-h] [-i INTERPRETER_TYPE]",
    )
    parser.add_argument(
        "-i",
        "--interpreter-type",
        default=0,
        type=int,
        help=(
            "Change interpreter used. Pass 0 (default) for syntax-directed or"
            " 1 for ast-based"
        ),
    )
    args = parser.parse_args()
    parser = importlib.import_module(
        "sylvie.interpreter."
        f"{('syntax_directed', 'ast_based')[args.interpreter_type]}.parser"
    )

    try:
        while True:
            text = input("calc >> ")
            try:
                print(parser.Parser(text).expr())
            except Exception as err:
                print(err)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting as requested")
