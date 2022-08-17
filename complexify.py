#!/usr/bin/env python3

import argparse

def main():
    default_char_count = 3
    default_ignore_chars = " "

    parser = argparse.ArgumentParser(description="Replace characters in a string to make it more complex")
    parser.add_argument(
        "basestring",
        help="Base String to be complexified"
    )
    parser.add_argument(
            "numchars",
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
