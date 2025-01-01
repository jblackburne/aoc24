from math import log10
from collections import Counter


def _propagate(num):
    if num == 0:
        return [1]
    ndigits = int(log10(num)) + 1
    if ndigits % 2 == 1:
        return [num * 2024]
    else:
        lefthalf, righthalf = divmod(num, 10**(ndigits // 2))
        return [lefthalf, righthalf]


def p11a(data, stop_age=25):
    """Construct a tree in a breadth-first fashion. Once you get to nodes with
    an age of 25, stop and count. Node values are (age, number) pairs.
    """
    total = 0
    graph = [(0, x) for x in data]
    while graph:
        age, num = graph.pop(0)
        newnums = _propagate(num)
        if age == stop_age - 1:
            total += len(newnums)
        else:
            graph.extend([(age + 1, newnum) for newnum in newnums])

    return total


if __name__ == "__main__":
    with open("data/input_p11.txt", "r") as f:
        lines = f.readlines()
    data = [int(x) for x in lines[0].strip().split()]

    print("Part 1: {}".format(p11a(data)))
    print("Part 2: {}".format(p11a(data, stop_age=75)))
