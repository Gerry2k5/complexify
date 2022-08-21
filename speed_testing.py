#!/usr/bin/env python3

import timeit

REPS = 10000000
LIST_SIZE = 100000

# ASCII codes for different character classes
char_symbols = list(range(33, 48))
char_symbols.extend(list(range(58, 65)))
char_symbols.extend(list(range(91, 97)))
char_symbols.extend(list(range(123, 127)))

sym_donotuse = [34, 39, 92, 96, 124]


def main():
#    list_create_testing()
    list_remove_testing()

def list_create_testing():
    list_only = timeit.Timer("list(range(LIST_SIZE))", globals=globals())
    with_comp = timeit.Timer("[x for x in range(LIST_SIZE)]", globals=globals())

    print("With list() function took {} seconds".format(list_only.timeit(REPS)))
    print("With list comprehensions took {} seconds".format(with_comp.timeit(REPS)))
    # Conclusion is that list() function is almost twice as fast in this case

def list_remove_testing():
    with_sets = timeit.Timer("list(set(char_symbols)-set(sym_donotuse))", globals=globals())
    with_comp = timeit.Timer("[x for x in char_symbols if x not in sym_donotuse]", globals=globals())

    print("With set() function took {} seconds".format(with_sets.timeit(REPS)))
    print("With list comprehension took {} seconds".format(with_comp.timeit(REPS)))
    # Conclusion is that set() function is very slightly faster in this case


if __name__ == "__main__":
    main()
