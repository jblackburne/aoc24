import numpy as np


S, E, N, W = range(4)

def ingest_p06(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    decoder = {".": 0,
               "#": 1,
               "v": 2,
               ">": 3,
               "^": 4,
               "<": 5,
               }
    data = np.array([[decoder[c] for c in line] for line in lines])
    idx_start = np.where(data > 1)
    idx_start = tuple([int(idx[0]) for idx in idx_start])
    direction = data[idx_start] - 2
    data[idx_start] = 0

    return data, idx_start, direction


def p06a(data, idx_start, direction):
    ny, nx = data.shape
    pos = list(idx_start)
    drx = direction
    visited = np.zeros_like(data, dtype=bool)
    while 1:
        visited[tuple(pos)] = True
        if (pos[0] == 0 or pos[0] == ny - 1 or
            pos[1] == 0 or pos[1] == nx - 1):
            break
        newpos = list(pos)
        newpos[drx % 2] += int((-1)**(drx // 2))
        while data[tuple(newpos)] == 1:
            # Turn right
            drx = (drx + 3) % 4
            newpos = list(pos)
            newpos[drx % 2] += int((-1)**(drx // 2))
        pos = newpos
    return visited.sum()


def p06b(data, idx_start, direction):
    """Brute force. Ugly and slow, but not enough to make me rewrite it."""
    ny, nx = data.shape
    total = 0
    for yobst in range(ny):
        for xobst in range(nx):
            if data[yobst, xobst] == 1 or (yobst, xobst) == idx_start:
                continue
            data2 = np.copy(data)
            data2[yobst, xobst] = 1
            pos = list(idx_start)
            drx = direction
            visited = np.zeros_like(data, dtype=np.uint8)
            is_loop = False
            while 1:
                if visited[tuple(pos)] & 1 << drx:
                    is_loop = True
                visited[tuple(pos)] |= 1 << drx
                if (is_loop or
                    pos[0] == 0 or pos[0] == ny - 1 or
                    pos[1] == 0 or pos[1] == nx - 1):
                    break
                newpos = list(pos)
                newpos[drx % 2] += int((-1)**(drx // 2))
                while data2[tuple(newpos)] == 1:
                    # Turn right
                    drx = (drx + 3) % 4
                    newpos = list(pos)
                    newpos[drx % 2] += int((-1)**(drx // 2))
                pos = newpos
            if is_loop:
                total += 1

    return total


if __name__ == "__main__":
    data, idx_start, direction = ingest_p06("data/input_p06.txt")

    print("Part 1: {}".format(p06a(data, idx_start, direction)))
    print("Part 2: {}".format(p06b(data, idx_start, direction)))
