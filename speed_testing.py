#!/usr/bin/env python3

import timeit

REPS = 10000
LIST_SIZE = 100000

def main():
    list_testing()

def list_testing():
    listonly = timeit.Timer("list(range(LIST_SIZE))", globals=globals())
    withcomp = timeit.Timer("[x for x in range(LIST_SIZE)]", globals=globals())

    print("With list() function took {} seconds".format(listonly.timeit(REPS)))
    print("With list comprehensions took {} seconds".format(withcomp.timeit(REPS)))
    # Conclusion is that list() function is almost twice as fast in this case

if __name__ == "__main__":
    main()
