import re
import numpy as np


COSTS = [3, 1]

def ingest_p13(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    lines = [line for line in lines if line]

    # Parse
    outputs = [[], [], []]
    patterns = [
        r"Button A: X([+-]?\d+), Y([+-]?\d+)",
        r"Button B: X([+-]?\d+), Y([+-]?\d+)",
        r"Prize: X=([+-]?\d+), Y=([+-]?\d+)",
    ]
    for iline, line in enumerate(lines):
        iout = iline % 3
        m = re.match(patterns[iout], line)
        outputs[iout].append((int(m[1]), int(m[2])))
    a, b, prize = outputs

    return np.array(a), np.array(b), np.array(prize)


def p13a(avecs, bvecs, prizes):
    abmats = np.moveaxis([avecs, bvecs], 0, -1)
    n_possible = 0
    total_cost = 0
    for ab, prize in zip(abmats, prizes):
        # TODO: Handle singular AB matrices if they come up
        abdet = ab[0, 0] * ab[1, 1] - ab[0, 1] * ab[1, 0]
        abinv = np.array([[ab[1, 1], -ab[0, 1]], [-ab[1, 0], ab[0, 0]]])
        soln = abinv.dot(prize) // abdet
        if np.all(ab.dot(soln) == prize):
            n_possible += 1
            total_cost += np.dot(COSTS, np.round(soln).astype(int))

    return n_possible, total_cost


def p13b(avecs, bvecs, prizes):
    return p13a(avecs, bvecs, prizes + 10000000000000)


if __name__ == "__main__":
    a, b, prize = ingest_p13("data/input_p13.txt")

    print("Part 1: {}".format(p13a(a, b, prize)))
    print("Part 2: {}".format(p13b(a, b, prize)))
