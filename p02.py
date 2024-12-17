import numpy as np


def ingest_p02(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
    lines = [l.strip() for l in lines]

    return [[int(x) for x in line.split()] for line in lines]

def is_safe(dr):
    return (np.all((dr > 0) & (dr < 4)) or
            np.all((dr < 0) & (dr > -4)))

def p02a(reports):
    n_safe = 0
    n_unsafe = 0
    for report in reports:
        dr = np.diff(report)
        if is_safe(dr):
            n_safe += 1
        else:
            n_unsafe += 1

    return n_safe, n_unsafe

def p02b(reports):
    safe = np.zeros(len(reports), dtype=bool)
    for ireport, report in enumerate(reports):
        dr = np.diff(report)
        if is_safe(dr):
            safe[ireport] = True
            continue
        for idx in range(0, len(report)):
            dr = np.diff(np.delete(report, idx))
            if is_safe(dr):
                safe[ireport] = True
                break
        if safe[ireport]:
            continue
    n_safe = np.sum(safe)

    return n_safe, len(reports) - n_safe

if __name__ == "__main__":
    reports = ingest_p02("data/input_p02.txt")

    n_safe, n_unsafe = p02a(reports)
    print("Part 1: {}".format(n_safe))

    n_safe, n_unsafe = p02b(reports)
    print("Part 2: {}".format(n_safe))
