import numpy as np

from p08 import _inbounds


VISIT_NVALS = 32

class Node:
    def __init__(self, node_idx, value=None, whence=(), whither=()):
        self.whence = list(whence)
        self.whither = list(whither)
        self.visited = [False for _ in range(VISIT_NVALS)]
        self.value = value
        self.idx = node_idx

    def visit(self, visit_idx=None):
        if visit_idx is None:
            self.visited = [True for _ in self.visited]
        else:
            self.visited[visit_idx] = True

    def unvisit(self, visit_idx=None):
        if visit_idx is None:
            self.visited = [False for _ in self.visited]
        else:
            self.visited[visit_idx] = False


def ingest_p10(fname):
    with open(fname, "r") as f:
        lines = f.readlines()

    data = np.array([[int(c) for c in line.strip()] for line in lines])

    return data


def _setup_graph_p10(data):
    # Set up the graph
    graph = []
    idx_start = []
    ny, nx = data.shape
    for j in range(ny):
        for i in range(nx):
            whence = []
            whither = []
            for neighbor in ((j, i - 1), (j, i + 1), (j - 1, i), (j + 1, i)):
                if _inbounds(neighbor, data.shape):
                    if data[neighbor] == data[j, i] + 1:
                        whither.append(neighbor[0] * nx + neighbor[1])
                    elif data[neighbor] == data[j, i] - 1:
                        whence.append(neighbor[0] * nx + neighbor[1])
            graph.append(Node(j * nx + i, value=data[j, i], whence=whence, whither=whither))
            if graph[-1].value == 0:
                idx_start.append(graph[-1].idx)

    return graph, idx_start


def p10a(data):
    # Set up the graph
    graph, idx_start = _setup_graph_p10(data)

    # Traverse using DFS from each start point and count reachable end points for each
    # Don't bother keeping track of visits, because the graph is acyclic
    END_VALUE = 9
    total = 0
    for istart in idx_start:
        inode = istart
        idx_end = set()
        to_visit = [inode]
        while to_visit:
            inode = to_visit.pop()
            if graph[inode].value == END_VALUE:
                idx_end.add(inode)
            else:
                to_visit.extend(graph[inode].whither)
        total += len(idx_end)

    return total


def p10b(data):
    """Haha, this is literally the problem I accidentally solved when trying to do part 1."""
    # Set up the graph
    graph, idx_start = _setup_graph_p10(data)

    # Traverse using DFS from each start point and count reachable end points for each
    # Don't bother keeping track of visits, because the graph is acyclic
    END_VALUE = 9
    total = 0
    for istart in idx_start:
        inode = istart
        idx_end = []
        to_visit = [inode]
        while to_visit:
            inode = to_visit.pop()
            if graph[inode].value == END_VALUE:
                idx_end.append(inode)
            else:
                to_visit.extend(graph[inode].whither)
        total += len(idx_end)

    return total


if __name__ == "__main__":
    data = ingest_p10("data/input_p10.txt")

    print("Part 1: {}".format(p10a(data)))
    print("Part 2: {}".format(p10b(data)))
