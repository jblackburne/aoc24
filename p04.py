import numpy as np


XMAS = np.array([ord(c) for c in "XMAS"]).reshape((-1, 1))


def ingest_p04(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    data = np.array([[ord(c) for c in line] for line in lines])

    # Pad the data with zeros to avoid spurious wraparound words
    data = np.pad(data, 1)

    return data


def p04a(data):
    "Use strides in a 1-D array. Strides should be 1, and -1 for east and west, etc."
    ny, nx = data.shape
    strides = (1, -1, nx, -nx, nx + 1, nx - 1, -nx + 1, -nx - 1)
    data = data.flatten()

    n_matches = 0
    for stride in strides:
        datax4 = np.array([np.roll(data, stride * i) for i in range(4)])
        n_matches += np.sum(np.all(datax4 == XMAS, axis=0))

    return n_matches


def p04b(data):
    total = 0
    ctr = (data == ord("A"))[1:-1, 1:-1]
    for ms in (list("MMSS"), list("MSSM"), list("SSMM"), list("SMMS")):
        total += np.logical_and.reduce([
            ctr,
            data[2:, 2:] == ord(ms[0]),
            data[:-2, 2:] == ord(ms[1]),
            data[:-2, :-2] == ord(ms[2]),
            data[2:, :-2] == ord(ms[3]),
        ], axis=0).sum()

    return total


if __name__ == "__main__":
    data = ingest_p04("data/input_p04.txt")

    print("Part 1: {}".format(p04a(data)))
    print("Part 2: {}".format(p04b(data)))
