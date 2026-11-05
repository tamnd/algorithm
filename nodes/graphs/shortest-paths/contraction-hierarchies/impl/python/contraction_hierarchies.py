# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contraction-hierarchies/. The authors are listed in prov/K2PFVE.jsonl.

import heapq
import math

INF = math.inf


class CH:
    """A contraction hierarchy: ranks, upward and downward edges, shortcut middles."""

    def __init__(self, n: int) -> None:
        self.rank = [0] * n
        self.up: list[list[tuple[int, float]]] = [[] for _ in range(n)]
        self.down: list[list[tuple[int, float]]] = [[] for _ in range(n)]
        self.mid: dict[tuple[int, int], int | None] = {}
        self.shortcuts = 0


def _witness(out, u: int, x: int, skip: int, limit: float) -> bool:
    """True if the remaining graph without skip has a u-x path of weight <= limit."""
    d = {u: 0}
    heap = [(0, u)]
    while heap:
        du, a = heapq.heappop(heap)
        if du > limit:
            return False
        if du > d[a]:
            continue
        if a == x:
            return True
        for b, (w, _) in out[a].items():
            if b != skip and du + w < d.get(b, INF):
                d[b] = du + w
                heapq.heappush(heap, (d[b], b))
    return False


def _needed(out, inn, v: int) -> list[tuple[int, int, float]]:
    """The shortcuts that contracting v would add: (u, x, weight)."""
    res = []
    for u, (wu, _) in inn[v].items():
        for x, (wx, _) in out[v].items():  # @line L2
            if u != x and not _witness(out, u, x, v, wu + wx):  # @line L3
                res.append((u, x, wu + wx))
    return res


def ch_preprocess(
    adj: list[list[tuple[int, float]]], order: list[int] | None = None
) -> CH:
    """Build a contraction hierarchy of the directed graph adj.

    The graph has the vertices 0 .. n-1; adj[u] lists the edges (v, w) out of u.
    Precondition: every weight is nonnegative (a ValueError is raised otherwise).
    If order is given, vertices are contracted in that order; otherwise by the
    edge-difference heuristic with lazy updates. Witness searches are exact.
    """
    n = len(adj)
    out: list[dict[int, tuple[float, int | None]]] = [{} for _ in range(n)]
    inn: list[dict[int, tuple[float, int | None]]] = [{} for _ in range(n)]
    for u in range(n):
        for v, w in adj[u]:
            if w < 0:
                raise ValueError("contraction hierarchies need nonnegative weights")
            if u != v and w < out[u].get(v, (INF, None))[0]:
                out[u][v] = (w, None)
                inn[v][u] = (w, None)
    ch = CH(n)

    def priority(v: int) -> int:
        return len(_needed(out, inn, v)) - len(out[v]) - len(inn[v])

    if order is None:
        heap = [(priority(v), v) for v in range(n)]
        heapq.heapify(heap)
        seq = []
        done = [False] * n
        while heap:
            p, v = heapq.heappop(heap)
            if done[v]:
                continue
            q = priority(v)
            if heap and q > heap[0][0]:
                heapq.heappush(heap, (q, v))
                continue
            done[v] = True
            seq.append(v)
            _contract(ch, out, inn, v, len(seq) - 1)
        return ch
    for i, v in enumerate(order):  # @line L1
        _contract(ch, out, inn, v, i)
    return ch


def _contract(ch: CH, out, inn, v: int, r: int) -> None:
    ch.rank[v] = r
    for u, x, w in _needed(out, inn, v):
        if w < out[u].get(x, (INF, None))[0]:
            out[u][x] = (w, v)  # @line L4
            inn[x][u] = (w, v)
            ch.shortcuts += 1
    for x, (w, m) in out[v].items():  # @line L5
        ch.up[v].append((x, w))
        ch.mid[(v, x)] = m
        del inn[x][v]
    for u, (w, m) in inn[v].items():
        ch.down[v].append((u, w))
        ch.mid[(u, v)] = m
        del out[u][v]
    out[v].clear()
    inn[v].clear()


def _unpack(ch: CH, u: int, v: int, acc: list[int]) -> None:
    m = ch.mid[(u, v)]
    if m is None:
        acc.append(v)
    else:
        _unpack(ch, u, m, acc)
        _unpack(ch, m, v, acc)


def ch_query(ch: CH, s: int, t: int) -> tuple[float, list[int] | None]:
    """Return (dist, path) from s to t, or (math.inf, None) if t is unreachable."""
    if s == t:
        return 0, [s]
    n = len(ch.rank)
    dist = [[INF] * n, [INF] * n]
    pred: list[list[int | None]] = [[None] * n, [None] * n]
    done = [[False] * n, [False] * n]
    graph = [ch.up, ch.down]
    dist[0][s] = 0  # @line L6
    dist[1][t] = 0
    heaps = [[(0, s)], [(0, t)]]
    mu, meet = INF, None
    while True:
        side = min((0, 1), key=lambda i: heaps[i][0][0] if heaps[i] else INF)
        if not heaps[side] or heaps[side][0][0] >= mu:  # @line L7
            break
        du, u = heapq.heappop(heaps[side])
        if done[side][u]:
            continue
        done[side][u] = True
        if du + dist[1 - side][u] < mu:  # @line L8
            mu, meet = du + dist[1 - side][u], u
        for v, w in graph[side][u]:
            if du + w < dist[side][v]:
                dist[side][v] = du + w
                pred[side][v] = u
                heapq.heappush(heaps[side], (dist[side][v], v))
    if meet is None:  # @line L9
        return INF, None
    fwd = [meet]
    while fwd[-1] != s:
        fwd.append(pred[0][fwd[-1]])
    fwd.reverse()
    bwd = [meet]
    while bwd[-1] != t:
        bwd.append(pred[1][bwd[-1]])
    up_path = fwd + bwd[1:]
    path = [s]
    for a, b in zip(up_path, up_path[1:]):
        _unpack(ch, a, b, path)  # @line L10
    return mu, path
