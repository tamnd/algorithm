# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direction-optimizing-bfs/. The authors are listed in prov/HZS2BB.jsonl.

"""Direction-optimizing BFS (Beamer, Asanovic and Patterson), simulated in synchronous PRAM steps.

Each round is a top-down step (frontier vertices claim their unvisited
neighbours, concurrent writes follow the CRCW arbitrary rule) or a bottom-up
step (each unvisited vertex scans its in-neighbours in order and stops at the
first one in the frontier). The choice follows the heuristic of the paper with
the parameters alpha and beta.

Precondition: adj is a list of out-adjacency lists over 0 .. n - 1 with no
parallel edges, 0 <= s < n, alpha > 0 and beta > 0. radj, if given, is the
list of in-adjacency lists (for an undirected graph it equals adj).
Cost: each top-down round costs O(|F| + m_f) work and O(log n) span. Each
bottom-up round costs O(n + edges examined) work and O(log n + longest scan)
span. Over all rounds the work is O((n + m) D) in the worst case.
"""

import random


class Cost:
    """Counters for work, span, rounds, and the edges examined."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0
        self.examined = 0
        self.modes: list[str] = []


def log2_ceil(k: int) -> int:
    """The number of tree levels that a scan or pack over k items needs."""
    return max(1, (k - 1).bit_length()) if k > 1 else 1


def transpose(adj: list[list[int]]) -> list[list[int]]:
    """The in-adjacency lists."""
    radj: list[list[int]] = [[] for _ in adj]
    for u, nbrs in enumerate(adj):
        for v in nbrs:
            radj[v].append(u)
    return radj


def top_down_step(adj, frontier, dist, parent, rng, c) -> list[int]:
    """Lines L14 to L16: the round of parallel BFS, with an arbitrary concurrent write."""
    inf = float("inf")
    k = sum(len(adj[u]) for u in frontier)
    claims: dict[int, list[int]] = {}
    for u in frontier:  # @line L14
        for v in adj[u]:
            if parent[v] is None:  # @line L15
                claims.setdefault(v, []).append(u)
    for v, writers in claims.items():
        parent[v] = rng.choice(writers)  # an arbitrary writer wins
    nxt = [v for u in frontier for v in adj[u] if parent[v] == u and dist[v] == inf]  # @line L16
    c.examined += k
    c.work += len(frontier) + 3 * k + len(nxt)
    c.span += 2 * log2_ceil(k + 1) + 4
    return nxt


def bottom_up_step(radj, frontier, dist, parent, c) -> list[int]:
    """Lines L17 to L21: each unvisited vertex looks for a parent in the frontier."""
    n = len(radj)
    inf = float("inf")
    in_f = [False] * n  # @line L17
    for u in frontier:
        in_f[u] = True
    marked = [False] * n
    longest = 0
    examined = 0
    for v in range(n):  # @line L18
        if dist[v] != inf:
            continue
        scanned = 0
        for u in radj[v]:  # @line L19
            scanned += 1
            if in_f[u]:  # @line L20
                parent[v] = u
                marked[v] = True
                break
        examined += scanned
        longest = max(longest, scanned)
    nxt = [v for v in range(n) if marked[v]]  # @line L21
    c.examined += examined
    c.work += 2 * n + len(frontier) + examined
    c.span += longest + 2 * log2_ceil(n + 1) + 2
    return nxt


def direction_optimizing_bfs(
    adj: list[list[int]],
    s: int,
    alpha: float = 14.0,
    beta: float = 24.0,
    radj: list[list[int]] | None = None,
    rng: random.Random | None = None,
    cost: Cost | None = None,
    force: str | None = None,
) -> tuple[list[float], list[int | None]]:
    """Return (dist, parent) of a BFS from s. force may be "top-down" or "bottom-up" to fix the mode."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    radj = radj if radj is not None else transpose(adj)
    n = len(adj)
    inf = float("inf")
    dist: list[float] = [inf] * n  # @line L1
    parent: list[int | None] = [None] * n
    dist[s], parent[s] = 0, s  # @line L2
    frontier, d, mode, n_prev = [s], 0, "top-down", 0
    m_u = sum(len(radj[v]) for v in range(n)) - len(radj[s])  # in-edges of the unvisited vertices
    c.work += 2 * n
    c.span += log2_ceil(n + 1) + 1
    while frontier:  # @line L3
        d += 1  # @line L4
        c.rounds += 1
        m_f = sum(len(adj[u]) for u in frontier)  # @line L5
        c.work += len(frontier)
        c.span += log2_ceil(len(frontier) + 1)
        if mode == "top-down" and m_f > m_u / alpha and len(frontier) > n_prev:  # @line L6
            mode = "bottom-up"
        elif mode == "bottom-up" and len(frontier) < n / beta and len(frontier) < n_prev:  # @line L7
            mode = "top-down"
        if force is not None:
            mode = force
        n_prev = len(frontier)  # @line L8
        c.modes.append(mode)
        if mode == "top-down":  # @line L9
            nxt = top_down_step(adj, frontier, dist, parent, rng, c)
        else:  # @line L10
            nxt = bottom_up_step(radj, frontier, dist, parent, c)
        for v in nxt:  # @line L11
            dist[v] = d
        m_u -= sum(len(radj[v]) for v in nxt)
        c.work += 2 * len(nxt)
        c.span += log2_ceil(len(nxt) + 1) + 1
        frontier = nxt  # @line L12
    return dist, parent  # @line L13
