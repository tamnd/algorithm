# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stoer-wagner/. The authors are listed in prov/M60CT8.jsonl.


def stoer_wagner(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, set[int]]:
    """Global minimum cut of an undirected graph by the Stoer-Wagner algorithm.

    Vertices are 0 .. n-1 with n >= 2, and edges (u, v, w) are undirected with
    weight w >= 0, an integer or a real number. Parallel edges add up and
    self-loops are ignored. Returns (value, S), where S is a nonempty proper
    subset of the vertices whose cut has the least total weight. This is the
    adjacency-matrix version, O(n^3) time and O(n^2) space.
    """
    if n < 2:
        raise ValueError("need at least two vertices")
    w = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        if c < 0:
            raise ValueError("weights must be nonnegative")
        if u != v:
            w[u][v] += c
            w[v][u] += c
    group = [{v} for v in range(n)]  # @line L1
    alive = list(range(n))
    best, best_set = None, set()
    while len(alive) > 1:  # @line L2
        s, t, cut = minimum_cut_phase(w, alive)  # @line L3
        if best is None or cut < best:  # @line L4
            best, best_set = cut, set(group[t])
        group[s] |= group[t]  # @line L5
        for v in alive:
            w[s][v] += w[t][v]
            w[v][s] = w[s][v]
        w[s][s] = 0
        alive.remove(t)
    return best, best_set  # @line L6


def minimum_cut_phase(w: list[list[float]], alive: list[int]) -> tuple[int, int, float]:
    """One maximum adjacency ordering of the alive vertices.

    Returns (s, t, cut): the last two vertices of the ordering and the weight
    of the edges between t and all other alive vertices, which is a minimum
    s-t cut of the current graph.
    """
    start = alive[0]  # @line L7
    key = {v: w[start][v] for v in alive if v != start}
    order = [start]
    last_key = 0
    while key:  # @line L8
        z = max(key, key=lambda v: key[v])  # @line L9
        last_key = key.pop(z)
        order.append(z)
        for v in key:  # @line L10
            key[v] += w[z][v]
    return order[-2], order[-1], last_key  # @line L11
