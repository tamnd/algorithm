# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coloring-scc/. The authors are listed in prov/R4EPTY.jsonl.

"""Coloring SCC (max-label propagation), simulated round by round.

Each remaining vertex starts with its own label as its color, and colors
spread along the arcs, each vertex keeping the largest color it sees. Then
color(v) is the largest label of a vertex that reaches v. A vertex whose
color is its own label is a root, and its SCC is the set of vertices of its
color that reach it inside the color class, found by a backward BFS. All
these SCCs leave, and the process repeats on the rest.

Precondition: edges is a list of pairs (u, v) with 0 <= u, v < n, meaning the
arc u -> v. label, if given, holds n distinct numbers; by default it is a
random permutation drawn from rng.
Cost: an iteration does O(n + m) work per propagation round and O(n + m)
for the backward searches. Propagation takes at most n rounds and there are
at most n iterations, so the worst case is O(n^2 (n + m)) work; each round has
O(log n) span.
"""

import math
import random


class Cost:
    """Counters for work, span, outer iterations and propagation rounds."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.iterations = 0
        self.prop_rounds = 0


def coloring_scc(
    n: int,
    edges: list[tuple[int, int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    label: list[int] | None = None,
) -> list[int]:
    """Return comp with comp[u] == comp[v] exactly when u and v are in the same SCC."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 2)))
    if label is None:
        label = list(range(n))
        rng.shuffle(label)
    out: list[list[int]] = [[] for _ in range(n)]
    inn: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        out[u].append(v)
        inn[v].append(u)
    comp = [-1] * n
    live = list(range(n))
    while live:  # @line L1
        c.iterations += 1
        color = {v: label[v] for v in live}  # @line L2
        frontier = live
        while frontier:  # @line L3 (propagate until no color changes)
            c.prop_rounds += 1
            upd: dict[int, int] = {}
            for u in frontier:  # @line L4 (in parallel: color(v) <- max(color(v), color(u)) on live arcs)
                for v in out[u]:
                    c.work += 1
                    if v in color and color[u] > max(color[v], upd.get(v, color[v])):
                        upd[v] = color[u]  # a priority (max) write, applied at the end of the round
            color.update(upd)
            c.work += len(frontier)
            c.span += lg
            frontier = sorted(upd)
        roots = [v for v in live if color[v] == label[v]]  # @line L5 (the roots)
        longest = 0
        for r in roots:  # @line L6 (in parallel over the roots)
            seen = {r}
            front = [r]
            rounds = 0
            while front:  # backward BFS inside the color class of r
                rounds += 1
                nxt = []
                for v in front:
                    for u in inn[v]:
                        c.work += 1
                        if u in color and color[u] == color[r] and u not in seen:
                            seen.add(u)
                            nxt.append(u)
                front = nxt
            longest = max(longest, rounds)
            for v in seen:  # @line L7 (one SCC)
                comp[v] = r
        c.span += lg * (longest + 1)
        c.work += len(live)
        live = [v for v in live if comp[v] == -1]  # @line L8
    return comp  # @line L9
