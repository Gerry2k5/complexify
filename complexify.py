#!/usr/bin/env python3

import argparse
import sys

# ASCII codes for different character classes
char_lcase = list(range(97, 123))
char_ucase = list(range(65, 91))
char_numbers = list(range(48, 58))
char_symbols = list(range(33, 48))
char_symbols.extend(list(range(58, 65)))
char_symbols.extend(list(range(91, 97)))
char_symbols.extend(list(range(123, 127)))

# Remove symbols which should not be used as replacements, to avoid
# characters which may be difficult to use on console sessions
# as well as minimising the risk of causing SQL errors on broken systems
sym_donotuse = [34, 39, 92, 96, 124]
char_symbols = list(set(char_symbols) - set(sym_donotuse))


def main():
    default_char_count = 3
    default_ignore_chars = " "
    default_basestring = ""
    # Collect stdin only if something has been passed (to prevent blocking)
    if not sys.stdin.isatty():
        default_basestring = sys.stdin.readlines()

    parser = argparse.ArgumentParser(description="Replace characters in a string to make it more complex")
    parser.add_argument(
        "basestring",
        nargs="?",
        default=default_basestring,
        help="Base String to be complexified"
    )
    parser.add_argument(
        "-?",
        action="help"
    )
    parser.add_argument(
        "-n", "--numchars",
        type=int,
        default=default_char_count,
        help="Number of characters to replace"
    )
    parser.add_argument(
        "-i", "--ignore",
        nargs="?",
        const="",
        default=default_ignore_chars,
        help="characters to ignore (Defaults to '" + default_ignore_chars + "')"
    )
    args = parser.parse_args()


if __name__ == "__main__":
    main()
