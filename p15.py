import numpy as np


S, E, N, W = range(4)

def ingest_p15(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    decoder = {"v": S,
               ">": E,
               "^": N,
               "<": W,
               }

    parse_map = True
    maplist = []
    instructions = []
    for line in lines:
        if not line:
            parse_map = False
            continue
        if parse_map:
            maplist.append([ord(c) for c in line])
        else:
            instructions.extend([decoder[c] for c in line])

    maparr = np.array(maplist)
    y_start, x_start = np.nonzero(maparr == ord("@"))
    start_pos = (y_start[0], x_start[0])
    maparr[start_pos] = ord(".")

    return maparr, instructions, start_pos


def _move(pos, drx):
    out = list(pos)
    out[drx % 2] += int((-1)**(drx // 2))
    return tuple(out)


def _widen(maparr, start_pos):
    ny, nx = maparr.shape
    out = np.empty((ny, nx * 2), dtype=maparr.dtype)
    for i in range(nx):
        out[:, i * 2] = np.where(maparr[:, i] == ord("O"), ord("["), maparr[:, i])
        out[:, i * 2 + 1] = np.where(maparr[:, i] == ord("O"), ord("]"), maparr[:, i])

    start_pos = (start_pos[0], 2 * start_pos[1])

    return out, start_pos


def p15a(maparr, instructions, start_pos):
    pos = tuple(start_pos)
    for drx in instructions:
        newpos = _move(pos, drx)
        stones = []
        while maparr[newpos] == ord("O"):
            dst = _move(newpos, drx)
            stones.append((newpos, dst))
            newpos = dst
        if maparr[newpos] == ord("#"):
            continue
        else:
            # We can move. First move the stones, then the player
            while stones:
                src, dst = stones.pop()
                maparr[dst] = maparr[src]
                maparr[src] = ord(".")
            pos = _move(pos, drx)

    # Now we are done moving. Figure out the GPS coordinates
    ybox, xbox = np.nonzero(maparr == ord("O"))
    gps = 100 * ybox + xbox

    return gps.sum()


def p15b(maparr, instructions, start_pos):
    stone_vals = (ord("["), ord("]"))
    pos = tuple(start_pos)
    for drx in instructions:
        needs_clear = [_move(pos, drx)]
        stones = []
        blocked = False
        while needs_clear:
            nc = needs_clear.pop(0)
            if maparr[nc] == ord("#"):
                blocked = True
                break
            if maparr[nc] in stone_vals:
                otherhalf = _move(nc, E if maparr[nc] == ord("[") else W)
                nc_dst = _move(nc, drx)
                otherhalf_dst = _move(otherhalf, drx)
                if not nc_dst == otherhalf and nc_dst not in needs_clear:
                    needs_clear.append(nc_dst)
                if otherhalf_dst not in needs_clear:
                    needs_clear.append(otherhalf_dst)
                stone_to_move = set([(nc, nc_dst), (otherhalf, otherhalf_dst)])
                if stone_to_move not in stones:
                    stones.append(stone_to_move)
        if blocked:
            continue
        else:
            # We can move. First move the stones, then the player
            while stones:
                (src0, dst0), (src1, dst1) = stones.pop()
                stonevals = maparr[src0], maparr[src1]
                maparr[src0] = ord(".")
                maparr[src1] = ord(".")
                maparr[dst0] = stonevals[0]
                maparr[dst1] = stonevals[1]
            pos = _move(pos, drx)

    # Now we are done moving. Figure out the GPS coordinates
    ybox, xbox = np.nonzero(maparr == ord("["))
    gps = 100 * ybox + xbox

    return gps.sum()


if __name__ == "__main__":
    maparr, instructions, start_pos = ingest_p15("data/input_p15.txt")

    print("Part 1: {}".format(p15a(maparr, instructions, start_pos)))

    maparr, instructions, start_pos = ingest_p15("data/input_p15.txt")
    maparr, start_pos = _widen(maparr, start_pos)

    print("Part 2: {}".format(p15b(maparr, instructions, start_pos)))
