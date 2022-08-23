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
symbols_donotuse = [32, 34, 39, 92, 96, 124]
char_symbols = list(set(char_symbols) - set(symbols_donotuse))


def main():
    default_char_count = 3
    default_ignore_chars = " "
    default_basestring = ""
    # Collect stdin only if something has been passed (to prevent blocking)
    if not sys.stdin.isatty():
        default_basestring = "".join(sys.stdin.readlines()).rstrip("\n")

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
        "-i", "--ignore",
        nargs="?",
        const="",
        default=default_ignore_chars,
        help="characters to ignore (Defaults to '" + default_ignore_chars + "')"
    )
    args = parser.parse_args()
    print(args)

    # TODO: It may be possible to convert this check to an argparse Action
    if len(args.basestring) < 4:
        print("Base String must be at least 4 characters")
        exit(1)

    string_dict = classify(args.basestring)


def classify(base_string):
    # Build dicts containing incidences of each character class in string
    # with the index of that character in the string as the key to the dict
    for index in range(len(base_string)):
        print("{} {}".format(index, base_string[index]))


if __name__ == "__main__":
    main()
