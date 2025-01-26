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
                graph[(iy, ix, drx)] = Node((iy, ix, drx), 0, whither=whither)

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
    for node in graph.values():
        node.visited = None
    pq = [(0,) + start + (drx_start,)]
    while pq:
        totalcost, iy, ix, drx = heappop(pq)
        node = graph[(iy, ix, drx)]
        if node.visited is None or totalcost < node.visited:
            node.visited = totalcost
        if totalcost > node.visited:
            if (iy, ix) == end:
                break
            else:
                continue
        if (iy, ix) == end:
            # construct path
            pass
        for iynew, ixnew, drxnew, cost in node.whither:
            heappush(pq, (totalcost + cost, iynew, ixnew, drxnew))


if __name__ == "__main__":
    data, start, end = ingest_p16("data/input_p16.txt")
    graph = _make_graph(data)

    print("Part 1: {}".format(p16a(graph, start, end)))
    print("Part 2: {}".format(p16b(graph, start, end)))
