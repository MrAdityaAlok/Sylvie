"""This module allows using package from command line.

This allows `python -m sylvie` command as well as `python sylvie`
to start REPL.
"""

try:
    from sylvie import _main
except ImportError:
    import sys
    from pathlib import Path

    # if it was run from directory other than src/ then directory
    # src/ would not be present in sys.path, from where imports start.
    # Thus, add src/ to sys.path and remove current file directory(i.e sylvie/).
    # when __file__ is not defined then use parent of '.' (Path.cwd())
    # Note: it would still not work if current directory is not sylvie/.
    # There is nothing I could think of to solve this issue.
    #
    # Although it's highly unlikley for __file__ to be not defined.
    script_dir = Path(globals().get("__file__", "./_")).absolute().parent

    # sys.path may contain a trailing '/' depending on the the command used
    # to invoke.
    # For example:
    # - when using `python sylvie`, sys.path will not contain trailing '/'
    #   in search path of this file.
    #
    # - but when `python sylvie/` is used, it will contain trailing '/'
    try:
        sys.path.remove(str(script_dir))
    except ValueError:
        sys.path.remove(f"{script_dir}/")

    # insert parent of script_dir (sylvie/), i.e src/ to sys.path
    sys.path.insert(0, str(script_dir.parent))

    from sylvie import _main

_main()
