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

    char_classes = [lcase_letters, ucase_letters, numbers, symbols]

    # Symbols which should not be used as replacements, to avoid
    # characters which may be difficult to use on console sessions
    # as well as minimising the risk of causing SQL errors on broken systems
    #
    # However, if the original string includes any of these characters,
    # they will not be removed
    sym_donotuse = [chr(c) for c in [32, 34, 39, 92, 96, 124]]
    valid_symbols = list(set(symbols) - set(sym_donotuse))

    default_count = 1
    default_ignore_chars = " "
    default_basestring = ""
    # Collect stdin only if something has been passed (to prevent blocking)
    if not sys.stdin.isatty():
        default_basestring = "".join(sys.stdin.readlines()).rstrip("\n")

    parser = argparse.ArgumentParser(description="""Modify a string to ensure
        that it contains at least a minimum number of characters of each class
        (uppercase, lowercase, numbers and symbols)""")
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
        "-c", "--count",
        type=int,
        default=default_count,
        help="""Number of characters of each of the 4 classes which should
        be included in the output (Defaults to 1)"""
    )
    parser.add_argument(
        "-i", "--ignore",
        nargs="?",
        const="",
        default=default_ignore_chars,
        help="Characters which should not be replaced (Defaults to '"
            +default_ignore_chars + "')"
    )
    args = parser.parse_args()
    print(args)

    # TODO: It may be possible to convert this check to an argparse Action
    min_length = len(char_classes) * args.count
    if len(args.basestring) < min_length:
        print("Base String must be at least {} characters".format(min_length))
        exit(1)





    char_dict = classify(args.basestring, char_classes)
    print(char_dict)



    # Determine how many characters of each class are present
    class_sizes = [len(c) for c in char_dict]
    print(class_sizes)

    # NOTE: valid_replacement_symbols =
    new_lcase = random_dict(list(char_dict[0]), numbers, args.count)
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


def random_dict(keys_in, values_in, count):
    """
    Generate a dict of (up to) 'count'/'keys_in' entries (whichever is lower)
    from supplied lists of keys and values.

    Parameters:
    keys_in:                List containing allowed keys
    values_in:              List containing allowed values
    count:                  Maximum number of entries to be returned

    Returns:
    Dict containing up to 'count' entries, with keys from the 'keys_in' list
    and values from the 'values_in' list.

    Each key can only appear once, but the values may appear more than once.

    Note that the returned dict will never be larger than 'keys_in', even
    if 'count' is greater.

    Also, the items in the returned dict may be in a different order than
    those in 'keys_in' (Only relevant if count is greater than 1).
    """
    dict_out = {}
    valid_keys = keys_in[:]
    sane_count = min(count, len(valid_keys))

    for i in range(sane_count):
        rand_key = random.choice(valid_keys)
        dict_out[rand_key] = random.choice(values_in)
        valid_keys.remove(rand_key)

    return (dict_out)


if __name__ == "__main__":
    main()
