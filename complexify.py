#!/usr/bin/env python3

import argparse
import sys

def main():
    # Define character classes using ASCII codes
    lcase_letters = [chr(c) for c in range(97, 123)]
    ucase_letters = [chr(c) for c in range(65, 91)]
    numbers = [chr(c) for c in range(48, 58)]
    symbols = [chr(c) for c in range(33, 48)]
    symbols.extend([chr(c) for c in range(58, 65)])
    symbols.extend([chr(c) for c in range(91, 97)])
    symbols.extend([chr(c) for c in range(123, 127)])

    # Remove symbols which should not be used as replacements, to avoid
    # characters which may be difficult to use on console sessions
    # as well as minimising the risk of causing SQL errors on broken systems
    sym_donotuse = [chr(c) for c in [32, 34, 39, 92, 96, 124]]
    symbols = list(set(symbols) - set(sym_donotuse))

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

    char_classes = [lcase_letters, ucase_letters, numbers, symbols]
    char_dict = classify(args.basestring, char_classes)
    print(char_dict)



def classify(base_string, classes_in):
    """
    Classify characters in string based on supplied character lists

    Parameters:
    base_string:        String to be classified
    char_classes:       List of lists containing character lists

    Returns:
    List of dicts containing classified characters with their position
    in the original string as the key to each dict entry
    """

    classes_out = []

    for c in classes_in:
        class_out = {
            i: base_string[i]
            for i in range(len(base_string))
            if base_string[i] in c
        }
        classes_out.append(class_out)

    return classes_out


if __name__ == "__main__":
    main()
