import numpy as np


def ingest_p08(fname):
    with open (fname, "r") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    data = np.array([[ord(c) for c in line] for line in lines], dtype=np.uint8)

    freqs = set(data.flat) - set([np.uint8(ord("."))])
    freqs = {freq: list(zip(*np.where(data == freq))) for freq in freqs}

    return data, freqs


def _inbounds(loc, shape):
    ny, nx = shape
    return (loc[0] >= 0 and loc[0] < ny and
            loc[1] >= 0 and loc[1] < nx)


def p08a(data, freqs):
    antinodes = set()
    for freq, locs in freqs.items():
        for locidx0 in range(len(locs)):
            for locidx1 in range(locidx0 + 1, len(locs)):
                loc0 = locs[locidx0]
                loc1 = locs[locidx1]
                yoffs = loc1[0] - loc0[0]
                xoffs = loc1[1] - loc0[1]
                for antinode in ((loc0[0] - yoffs, loc0[1] - xoffs),
                                 (loc1[0] + yoffs, loc1[1] + xoffs)):
                    antinodes.add(antinode)
    antinodes = [antinode for antinode in antinodes if _inbounds(antinode, data.shape)]

    return len(antinodes)


def p08b(data, freqs):
    antinodes = set()
    for freq, locs in freqs.items():
        for locidx0 in range(len(locs)):
            for locidx1 in range(locidx0 + 1, len(locs)):
                loc0 = locs[locidx0]
                loc1 = locs[locidx1]
                yoffs = loc1[0] - loc0[0]
                xoffs = loc1[1] - loc0[1]
                # To get all antinodes, reduce offsets by their greatest common divisor
                divisor = np.gcd(yoffs, xoffs)
                yoffs //= divisor
                xoffs //= divisor
                antinode = loc0
                while _inbounds(antinode, data.shape):
                    antinodes.add(antinode)
                    antinode = (antinode[0] - yoffs, antinode[1] - xoffs)
                antinode = loc0
                while _inbounds(antinode, data.shape):
                    antinodes.add(antinode)
                    antinode = (antinode[0] + yoffs, antinode[1] + xoffs)

    return len(antinodes)


if __name__ == "__main__":
    data, freqs = ingest_p08("data/input_p08.txt")

    print("Part 1: {}".format(p08a(data, freqs)))
    print("Part 2: {}".format(p08b(data, freqs)))
