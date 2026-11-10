# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-backward-scc/. The authors are listed in prov/5T2WQ4.jsonl.

"""Forward-backward (FW-BW) strongly connected components, simulated level by level.

A part of the graph is first trimmed: vertices with no in-edge or no out-edge
inside the part are their own SCC. Then a random pivot is chosen, the sets F
(reachable from the pivot) and B (reaching the pivot) are found by parallel
BFS inside the part, F and B meet in the SCC of the pivot, and the three other
pieces F - B, B - F and the rest are handled in parallel at the next level.
The recursion is run with an explicit list of parts per level.

Precondition: edges is a list of pairs (u, v) with 0 <= u, v < n, meaning the
arc u -> v. Self-loops and parallel arcs are allowed.
Cost: the parts of one level are disjoint and arcs between parts are never
followed, so a level costs O(n + m) work; the total work is O((n + m) d) for
recursion depth d. The span of a level is the largest number of trim rounds
and BFS rounds in one part, times O(log n).
"""

import math
import random
from collections.abc import Callable


class Cost:
    """Counters for work, span, recursion depth and the number of parts handled."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.depth = 0
        self.parts = 0


def _bfs(src: int, adj: list[list[int]], part: list[int], pid: int, c: Cost) -> tuple[set[int], int]:
    """Vertices reachable from src inside part pid, and the number of BFS rounds."""
    seen = {src}
    frontier = [src]
    rounds = 0
    while frontier:
        rounds += 1
        nxt = []
        for u in frontier:
            for v in adj[u]:
                c.work += 1
                if part[v] == pid and v not in seen:
                    seen.add(v)
                    nxt.append(v)
        frontier = nxt
    return seen, rounds


def fw_bw_scc(
    n: int,
    edges: list[tuple[int, int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    trim: bool = True,
    pick: Callable[[list[int]], int] | None = None,
) -> list[int]:
    """Return comp with comp[u] == comp[v] exactly when u and v are in the same SCC."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 2)))
    out: list[list[int]] = [[] for _ in range(n)]
    inn: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        out[u].append(v)
        inn[v].append(u)
    comp = [-1] * n
    part = [0] * n  # the part a live vertex belongs to; -1 once its SCC is known
    count = 0
    level = [list(range(n))] if n else []
    pid = 0
    while level:
        c.depth += 1
        level_span = 0
        nxt: list[list[int]] = []
        for vs in level:  # all parts of a level run in parallel
            c.parts += 1
            pid += 1
            for v in vs:
                part[v] = pid
            c.work += len(vs)
            rounds = 0
            if trim:  # @line L1 (trim: a vertex with no in-arc or no out-arc in the part is an SCC)
                indeg = {v: sum(1 for u in inn[v] if u != v and part[u] == pid) for v in vs}
                outdeg = {v: sum(1 for u in out[v] if u != v and part[u] == pid) for v in vs}
                c.work += sum(len(inn[v]) + len(out[v]) for v in vs)
                zero = [v for v in vs if indeg[v] == 0 or outdeg[v] == 0]
                while zero:
                    rounds += 1
                    for v in zero:
                        part[v] = -1
                        comp[v] = count
                        count += 1
                    cand = set()
                    for v in zero:
                        for u in out[v]:
                            if part[u] == pid:
                                indeg[u] -= 1
                                cand.add(u)
                        for u in inn[v]:
                            if part[u] == pid:
                                outdeg[u] -= 1
                                cand.add(u)
                        c.work += 1 + len(out[v]) + len(inn[v])
                    zero = sorted(u for u in cand if indeg[u] == 0 or outdeg[u] == 0)
                vs = [v for v in vs if part[v] == pid]
            if not vs:  # @line L2
                level_span = max(level_span, rounds)
                continue
            p = pick(vs) if pick is not None else rng.choice(vs)  # @line L3
            f, rf = _bfs(p, out, part, pid, c)  # @line L4
            b, rb = _bfs(p, inn, part, pid, c)  # @line L5
            for v in f & b:  # @line L6 (the SCC of the pivot)
                part[v] = -1
                comp[v] = count
            count += 1
            pieces: list[list[int]] = [[], [], []]
            for v in vs:  # @line L7 (F - B, B - F and the rest, all at the next level)
                if part[v] == pid:
                    pieces[0 if v in f else 1 if v in b else 2].append(v)
            nxt.extend(x for x in pieces if x)
            c.work += 2 * len(vs)
            level_span = max(level_span, rounds + max(rf, rb) + 2)
        c.span += lg * level_span
        level = nxt
    return comp
