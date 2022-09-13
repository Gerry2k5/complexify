#!/usr/bin/env python3

import os
import sys


def main():
#    if not os.isatty(sys.stdin.fileno()):
#        input_string = sys.stdin.readlines()

    if sys.stdin.isatty():
        print("TTY")
    else:
        print("NoTTY")

    print(vars())

if __name__ == "__main__":
    main()
