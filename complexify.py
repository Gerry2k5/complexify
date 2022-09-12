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

    # Symbols which should not be used as replace, to avoid
    # characters which may be difficult to use on console sessions
    # as well as minimising the risk of causing SQL errors on broken systems
    #
    # However, if the original string includes any of these characters,
    # they will not be removed
    unsafe_symbols = [chr(c) for c in [32, 34, 39, 92, 96, 124]]
    safe_symbols = list(set(symbols) - set(unsafe_symbols))

    char_classes = [lcase_letters, ucase_letters, numbers, symbols]
    char_classes_safe = [lcase_letters, ucase_letters, numbers, safe_symbols]

    class_count = len(char_classes)
    class_indexes = range(class_count)

    default_count = 1
    default_ignore_chars = " "
    default_base_string = ""
    # Collect stdin only if something has been passed (to prevent blocking)
    if not sys.stdin.isatty():
        default_base_string = "".join(sys.stdin.readlines()).rstrip("\n")

    parser = argparse.ArgumentParser(description="""Modify a string to ensure
        that it contains at least a minimum number of characters of each class
        (uppercase, lowercase, numbers and symbols)""")
    parser.add_argument(
        "base_string",
        nargs="?",
        default=default_base_string,
        help="String to be complexified"
    )
    parser.add_argument(
        "-?",
        action="help"
    )
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=default_count,
        help="""Number of characters of each class which should be included
        in the output (Defaults to 1)"""
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

    # TODO: It may be possible to convert this check to an argparse Action
    min_length = class_count * args.count
    if len(args.base_string) < min_length:
        print("Base String must be at least {} characters".format(min_length))
        exit(1)

    unclassed_chars = [
        args.base_string[i]
        for i in range(len(args.base_string))
    ]
    print("Unclassed", unclassed_chars)

    for i in class_indexes:
        classed_keys = classify(unclassed_chars, char_classes)
        print("Classed: ", classed_keys)

        print("i: ", i)
        chars_needed = args.count - len(classed_keys[i])
        print("Chars needed", chars_needed)
        if  chars_needed > 0:
            valid_keys = flatten_list([
                discard(classed_keys[j], args.count)
                for j in class_indexes
            ])
            print("Valid Keys", valid_keys)

            valid_values = char_classes_safe[i]
            print("Valid Values: ", valid_values)

            replace = random_dict(valid_keys, valid_values, chars_needed)
            print("Replacements: ", replace)

            for key in replace:
                unclassed_chars[key] = replace[key]
            print("New Unclassed: ", unclassed_chars)

    final_string = "".join(unclassed_chars)
    print("Final String: ", final_string)


def classify(chars_in, classes_in):
    """
    Classify characters in string based on supplied character lists

    Parameters:
    chars_in:           List of characters to be classified
    classes_in:         Character class lists encompassed in a list

    Returns:
    List containing lists of the position of characters on the original list
    separated into the given classes
    """

    classes_out = []

    for c in classes_in:
        class_out = [
            i
            for i in range(len(chars_in))
            if chars_in[i] in c
        ]
        classes_out.append(class_out)

    return classes_out


def discard(entries_in, count):
    """
    Discard up to 'count' entries from a list

    Parameters:
    entries_in:             List containing original entries
    count:                  Number of entries to be discarded

    Returns:
    List with up to 'count' entries discarded.
    If 'count' is greater than the size of entries_in, an empty list
    will be returned
    """
    entries_out = {}
    if len(entries_in) > count:
        entries_out = entries_in[:]

        for i in range(count):
            entries_out.remove(random.choice(entries_out))

    return entries_out


def flatten_list(lists_in):
    """
    Flatten multiple lists into a single list

    Parameters:
    lists_in:               List containing zero or more lists

    Returns:
    A sorted list of the entries in all contained lists
    """
    list_out = []
    for list in range(len(lists_in)):
        list_out.extend(lists_in[list])

    list_out.sort()
    return list_out


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
