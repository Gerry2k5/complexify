#!/usr/bin/env python3

import argparse
import random
import sys

def main():
    # Define character classes using ASCII codes
    lcase_letters = [chr(c) for c in range(97, 123)]
    ucase_letters = [chr(c) for c in range(65, 91)]
    numbers = [chr(c) for c in range(48, 58)]
    symbols = [chr(c) for c in range(32, 48)]
    symbols.extend([chr(c) for c in range(58, 65)])
    symbols.extend([chr(c) for c in range(91, 97)])
    symbols.extend([chr(c) for c in range(123, 127)])

    # Symbols which should not be used as replacements, to avoid
    # characters which may be difficult to use on console sessions
    # as well as minimising the risk of causing SQL errors on broken systems
    #
    # However, if the original string includes any of these characters,
    # they will not be removed
    sym_donotuse = [chr(c) for c in [32, 34, 39, 92, 96, 124]]
    valid_symbols = list(set(symbols) - set(sym_donotuse))

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

    # Determine how many characters of each class are present
    class_sizes = [len(c) for c in char_dict]
    print(class_sizes)

    # NOTE: valid_replacement_symbols =
    new_lcase = replace_chars(char_dict[0], symbols, 1)
    print(new_lcase)


def classify(string_in, classes_in):
    """
    Classify characters in string based on supplied character lists

    Parameters:
    string_in:          String to be classified
    classes_in:         Character class lists encompassed in a list

    Returns:
    List of dicts containing classified characters with their position
    in the original string as the key to each dict entry
    """

    classes_out = []

    for c in classes_in:
        class_out = {
            i: string_in[i]
            for i in range(len(string_in))
            if string_in[i] in c
        }
        classes_out.append(class_out)

    return classes_out


def replace_chars(chars_in, replacements, count):
    """
    Replace 'count' values in a dict with random characters from a supplied
    list of replacements

    Parameters:
    chars_in:               Dict containing original keys/values
    replacements:           List containing possible replacements
    count:                  Maximum number of characters to be replaced

    Returns:
    Dict containing the same keys as 'chars_in' but up to 'count' values
    replaced from the 'replacements' list.
    Note that the returned dict will be the same size as 'chars_in', even
    if 'count' is greater
    """
    chars_out = chars_in.copy()
    valid_keys = set(chars_in.keys())
    sane_count = min(count, len(chars_in))

    for i in range(sane_count):
        rand_key = random.choice(tuple(valid_keys))
        chars_out[rand_key] = random.choice(replacements)
        valid_keys.remove(rand_key)

    return (chars_out)


if __name__ == "__main__":
    main()
