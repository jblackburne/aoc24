import re

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import ArtistAnimation


def ingest_p14(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    # Parse
    pos = []
    vel = []
    pattern = r"p=([+-]?\d+),([+-]?\d+) v=([+-]?\d+),([+-]?\d+)"
    for iline, line in enumerate(lines):
        m = re.match(pattern, line)
        pos.append((int(m[1]), int(m[2])))
        vel.append((int(m[3]), int(m[4])))

    return np.array(pos), np.array(vel)


def p14a(pos, vel, deltat=100, shape=(101, 103)):
    endpos = np.mod(pos + vel * deltat, shape)

    n_quad = [
        np.sum((endpos[:, 0] < shape[0] // 2) & (endpos[:, 1] < shape[1] // 2)),
        np.sum((endpos[:, 0] < shape[0] // 2) & (endpos[:, 1] > shape[1] // 2)),
        np.sum((endpos[:, 0] > shape[0] // 2) & (endpos[:, 1] < shape[1] // 2)),
        np.sum((endpos[:, 0] > shape[0] // 2) & (endpos[:, 1] > shape[1] // 2)),
    ]

    return np.prod(n_quad)


def p14b(pos, vel, shape=(101, 103)):
    "This was stupid and frustrating and I did not like it."
    pos0 = pos.copy()
    fig, ax = plt.subplots()
    a = np.zeros(shape[::-1])
    imgs = []
    for i in range(30, 10403, 103):
        pos = np.mod(pos0 + i * vel, shape)
        a[...] = 0
        for p in pos:
            a[p[1], p[0]] += 1
        img = plt.imshow(a)
        fnum = ax.text(0, 0, "{:03d}".format(i))
        imgs.append([img, fnum])
    anim = ArtistAnimation(fig, imgs, repeat_delay=1000)
    plt.show()


if __name__ == "__main__":
    pos, vel = ingest_p14("data/input_p14.txt")

    print("Part 1: {}".format(p14a(pos, vel)))
    #p14b(pos, vel)
