"""Sylvie is a mathematical interpreter. 
It takes mathematical expressions as text and then evaluate it.

Examples:
    From command line:

        Sylvie>> 4*8(93-2/4*3)-9
        -8.650273224043715

        Sylvie>> 8/4
        2.0

        Sylvie>> 5*5
        25
"""


if __name__ == "__main__":
    from sylvie.bin import cmd

    cmd()
