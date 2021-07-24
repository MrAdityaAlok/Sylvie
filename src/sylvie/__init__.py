import importlib
import argparse


def evaluate(text: str, interpreter_type: str):
    parser = importlib.import_module(f"sylvie.interpreter.{interpreter_type}.parser")
    return parser.Parser(text).expr()


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
        help="Change interpreter used. Pass 0 (default) for syntax-directed or 1 for ast-based",
    )
    args = parser.parse_args()

    try:
        while True:
            text = input("calc >> ")
            try:
                print(
                    evaluate(
                        text,
                        interpreter_type=("syntax_directed", "ast_based")[
                            args.interpreter_type
                        ],
                    )
                )
            except Exception as err:
                print(err)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting as requested")
