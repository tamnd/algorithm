# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/even-tarjan-vertex-connectivity/. The authors are listed in prov/NX705H.jsonl.

from collections import deque


def _neighbours(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    nb: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:  # loops play no part; parallel edges collapse in the sets
            nb[u].add(v)
            nb[v].add(u)
    return nb


class SplitGraph:
    """The split digraph of an undirected graph, with unit capacities.

    The vertex w becomes w_in = 2w and w_out = 2w + 1 with the arc w_in -> w_out, and
    the edge {a, b} becomes the arcs a_out -> b_in and b_out -> a_in. Every arc has
    capacity 1, so a flow of value f from s_out to t_in is a set of f paths from s to t
    with pairwise disjoint inner vertices. Building it costs O(n + m).
    """

    def __init__(self, nb: list[set[int]]) -> None:
        self.n = len(nb)
        self.head: list[list[int]] = [[] for _ in range(2 * self.n)]
        self.to: list[int] = []
        self.res: list[int] = []
        for w in range(self.n):  # @line L9
            self._arc(2 * w, 2 * w + 1)
            for x in sorted(nb[w]):
                self._arc(2 * w + 1, 2 * x)

    def _arc(self, a: int, b: int) -> None:
        self.head[a].append(len(self.to))
        self.to.append(b)
        self.res.append(1)
        self.head[b].append(len(self.to))
        self.to.append(a)
        self.res.append(0)

    def flow(self, s: int, t: int, cap: int) -> int:
        """min(cap, the most s-t paths with pairwise disjoint inner vertices).

        Precondition: s != t are not adjacent. Each augmenting path is found by
        breadth-first search, so the time is O(min(cap, n) (n + m)). The residual
        capacities are restored before the return.
        """
        head, to, res = self.head, self.to, self.res
        source, sink = 2 * s + 1, 2 * t
        used: list[int] = []
        f = 0  # @line L10
        while f < cap:  # @line L11
            prev = {source: -2}
            queue = deque([source])
            while queue and sink not in prev:
                a = queue.popleft()
                for e in head[a]:
                    b = to[e]
                    if res[e] and b not in prev:
                        prev[b] = e
                        queue.append(b)
            if sink not in prev:
                break
            b = sink  # @line L12
            while b != source:
                e = prev[b]
                res[e] -= 1
                res[e ^ 1] += 1
                used.append(e)
                b = to[e ^ 1]
            f += 1
        for e in used:
            res[e] += 1
            res[e ^ 1] -= 1
        return f  # @line L13


def local_connectivity(nb: list[set[int]], s: int, t: int, cap: int) -> int:
    """min(cap, kappa(s, t)) for non-adjacent s != t; builds the split graph first."""
    return SplitGraph(nb).flow(s, t, cap)


def vertex_connectivity(n: int, edges: list[tuple[int, int]]) -> int:
    """The vertex connectivity kappa(G) of an undirected graph on 0 .. n-1.

    Precondition: n >= 1. Parallel edges and loops are allowed and ignored. kappa is
    the least size of a vertex cut, or n - 1 if G is complete. The vertices are taken
    in the order 0 .. n-1. At most (kappa + 1) n local flows run, each stopped at the
    current bound k <= n - 1, so the time is O((kappa + 1) n^2 (n + m)) in the worst
    case; Dinic's algorithm in place of plain augmenting paths gives
    O((kappa + 1) n^(3/2) m).
    """
    nb = _neighbours(n, edges)
    split = SplitGraph(nb)
    k = n - 1  # @line L1
    i = 0  # @line L2
    # The page counts vertices from 1, so its test i <= k becomes i + 1 <= k here.
    while i + 1 <= k:  # @line L3
        for j in range(i + 1, n):  # @line L4
            if j not in nb[i]:  # @line L5
                k = min(k, split.flow(i, j, k))  # @line L6
        i += 1  # @line L7
    return k  # @line L8
