from collections import Counter
import numpy as np


def p01a(lista, listb):
    lista = sorted(lista)
    listb = sorted(listb)

    return np.sum(np.abs(np.array(lista) - np.array(listb)))


def p01b(lista, listb):
    counterb = Counter(listb)

    return np.sum([a * counterb[a] for a in lista])


if __name__ == "__main__":
    data = np.fromfile("data/input_p01.txt", sep=" ", dtype=int).reshape((-1, 2))

    print("Part 1: {}".format(p01a(data[:, 0], data[:, 1])))
    print("Part 2: {}".format(p01b(data[:, 0], data[:, 1])))
