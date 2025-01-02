from math import log10
from collections import Counter
from itertools import chain
from functools import lru_cache


def _collect(nums):
    hist = Counter(nums)
    return list(hist.items())


def _consolidate(collected):
    hist = {}
    for num, mult in collected:
        priormult = hist.get(num, 0)
        hist[num] = mult + priormult
    return list(hist.items())


@lru_cache(maxsize=None)
def _propagate(num, nblinks=1, collect=True):
    if nblinks <= 0:
        raise ValueError("nblinks must be 1 or greater")

    # Base case
    if nblinks == 1:
        if num == 0:
            newnums = [1]
        else:
            ndigits = int(log10(num)) + 1
            if ndigits % 2 == 1:
                newnums = [num * 2024]
            else:
                lefthalf, righthalf = divmod(num, 10**(ndigits // 2))
                newnums = [lefthalf, righthalf]
        if collect:
            newnums = _collect(newnums)
        return newnums

    # Recursive case
    # Must use collect=True
    if not collect:
        raise ValueError("Must use collect=True unless nblinks is 1")
    half, rem = divmod(nblinks, 2)
    if rem:
        newnums = _propagate(num, nblinks=1)
    else:
        newnums = [(num, 1)]
    newnums = _consolidate(chain(*[[(n, mult * m) for n, m in _propagate(num, nblinks=half)]
                                   for num, mult in newnums]))
    newnums = _consolidate(chain(*[[(n, mult * m) for n, m in _propagate(num, nblinks=half)]
                                   for num, mult in newnums]))

    return newnums


def p11a(data, stop_age=25):
    """Construct a tree in a breadth-first fashion. Once you get to nodes with
    an age of 25, stop and count. Node values are (age, number) pairs.
    """
    total = 0
    graph = [(0, x) for x in data]
    while graph:
        age, num = graph.pop(0)
        newnums = _propagate(num, collect=False)
        if age == stop_age - 1:
            total += len(newnums)
        else:
            graph.extend([(age + 1, newnum) for newnum in newnums])

    return total


def p11b(data, stop_age=75):
    total = 0
    for num in data:
        for num, mult in _propagate(num, nblinks=stop_age):
            total += mult

    return total


if __name__ == "__main__":
    with open("data/input_p11.txt", "r") as f:
        lines = f.readlines()
    data = [int(x) for x in lines[0].strip().split()]

    # Use the faster part 2 approach (recursion + memoization) for both
    print("Part 1: {}".format(p11b(data, stop_age=25)))
    print("Part 2: {}".format(p11b(data)))
