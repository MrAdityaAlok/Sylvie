"""This module is used when executing this package directly
with python -m sylvie.

Python calls this module automaticaly after __init__.py
when used as stated above.
"""

from sylvie import main

main(script="python -m sylvie")
