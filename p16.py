from heapq import heapify, heappush, heappop
import numpy as np

from p10 import Node
from p15 import _move


S, E, N, W = range(4)

def ingest_p16(fname):
    with open(fname, "r") as f:
        lines = [line.strip() for line in f.readlines()]

    data = np.array([[ord(c) for c in line] for line in lines])

    start = tuple(np.argwhere(data == ord("S"))[0])
    end = tuple(np.argwhere(data == ord("E"))[0])

    data[start] = ord(".")
    data[end] = ord(".")

    return data, start, end


def _make_graph(data, cost_go=1, cost_turn=1000):
    graph = {}
    ny, nx = data.shape
    for iy in range(ny):
        for ix in range(nx):
            if data[iy, ix] == ord("#"):
                continue
            # Four nodes per valid position
            for drx in range(4):
                whither = [(iy, ix, (drx + 1) % 4, cost_turn),
                           (iy, ix, (drx + 3) % 4, cost_turn)]
                newpos = _move((iy, ix), drx)
                if data[newpos] == ord("."):
                    whither.append(newpos + (drx, cost_go))
                graph[(iy, ix, drx)] = Node((iy, ix, drx), whither=whither)

    return graph


def p16a(graph, start, end, drx_start=E):
    pq = [(0,) + start + (drx_start,)]
    while pq:
        totalcost, iy, ix, drx = heappop(pq)
        node = graph[(iy, ix, drx)]
        #print(node.idx, node.value)
        if (iy, ix) == end:
            return totalcost
        if node.visited[0]:
            continue
        node.visit(0)
        for iynew, ixnew, drxnew, cost in node.whither:
            heappush(pq, (totalcost + cost, iynew, ixnew, drxnew))


def p16b(graph, start, end, drx_start=E):
    pq = [(0, 0, 0, 0) + start + (drx_start,)]
    while pq:
        totalcost, iyold, ixold, drxold, iy, ix, drx = heappop(pq)
        node = graph[(iy, ix, drx)]
        if node.value is not None and totalcost > node.value:
            continue
        node.value = totalcost
        node.whence.append((iyold, ixold, drxold))
        for iynew, ixnew, drxnew, cost in node.whither:
            newtotalcost = totalcost + cost
            heappush(pq, (newtotalcost, iy, ix, drx, iynew, ixnew, drxnew))

    # Now search the graph backward starting from end
    # and using "whence"
    paths = set([start])
    pq = [end + (idrx,) for idrx in range(4)]
    while pq:
        iy, ix, drx = pq.pop(0)
        node = graph[(iy, ix, drx)]
        if node.idx[:2] == start:
            continue
        node.whence = set(node.whence)
        for iynew, ixnew, drxnew in node.whence:
            paths.add((iy, ix))
            pq.append((iynew, ixnew, drxnew))

    return len(paths)


if __name__ == "__main__":
    data, start, end = ingest_p16("data/input_p16.txt")
    graph = _make_graph(data)

    print("Part 1: {}".format(p16a(graph, start, end)))
    print("Part 2: {}".format(p16b(graph, start, end)))
