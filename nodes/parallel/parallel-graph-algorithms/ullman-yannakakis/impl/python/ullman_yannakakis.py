# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ullman-yannakakis/. The authors are listed in prov/BAM5EM.jsonl.

"""Ullman-Yannakakis transitive closure with a random sample, simulated round by round.

Each vertex joins the sample S with probability p = min(1, c ln n / t). A
depth-bounded BFS from every vertex finds R(v), the vertices at most t arcs
from v. The sample graph H has an arc a -> b when b is in R(a), and its
closure is computed by repeated Boolean squaring. Then u reaches v when v is
in R(u), or v is in R(b) for a sampled b that a sampled a in R(u) reaches in H.
Rows are bit masks: bit v of row u is set when u reaches v (every vertex
reaches itself).

Precondition: edges is a list of pairs (u, v) with 0 <= u, v < n; t >= 1; c > 0.
The output is always a subset of the true closure, and equals it with
probability at least 1 - n^(3 - c).
Cost: with s = |S|, the work is O(n (n + m) + s^3 log s + n^2 s) and the span
is O(t log n + log^2 n): t BFS rounds, ceil(log2 s) squarings, and two
combining steps.
"""

import math
import random


class Cost:
    """Counters for work, span, BFS rounds, squarings and the sample size."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.bfs_rounds = 0
        self.squarings = 0
        self.sample = 0


def ullman_yannakakis(
    n: int,
    edges: list[tuple[int, int]],
    t: int,
    rng: random.Random | None = None,
    c: float = 4.0,
    cost: Cost | None = None,
    fixed: list[int] | None = None,
) -> list[int]:
    """Return the reflexive transitive closure as one bit mask per vertex.

    If fixed is given, it is used as the sample instead of the random one.
    """
    rng = rng if rng is not None else random.Random()
    cs = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 2)))
    out: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        out[u].append(v)
    p = min(1.0, c * math.log(max(n, 2)) / t)  # @line L1
    sample = sorted(set(fixed)) if fixed is not None else [v for v in range(n) if rng.random() < p]
    cs.sample = len(sample)
    cs.work += n
    cs.span += 1
    reach = [1 << v for v in range(n)]  # @line L2 (all BFS at once, t rounds)
    front = [[v] for v in range(n)]
    for _ in range(t):
        if not any(front):
            break
        cs.bfs_rounds += 1
        for v in range(n):
            nxt = []
            for x in front[v]:
                cs.work += 1 + len(out[x])
                for y in out[x]:
                    if not reach[v] >> y & 1:
                        reach[v] |= 1 << y
                        nxt.append(y)
            front[v] = nxt
        cs.span += lg
    pos = {a: i for i, a in enumerate(sample)}
    s = len(sample)
    h = [0] * s  # @line L3 (row i: the sample vertices that sample[i] reaches)
    for i, a in enumerate(sample):
        for b, j in pos.items():
            if reach[a] >> b & 1:
                h[i] |= 1 << j
    cs.work += s * s
    cs.span += 1
    for _ in range(math.ceil(math.log2(s)) if s > 1 else 0):  # @line L4
        cs.squarings += 1
        nh = []
        for i in range(s):  # @line L5 (H <- H or H.H)
            row = h[i]
            for j in range(s):
                if h[i] >> j & 1:
                    row |= h[j]
            nh.append(row)
        h = nh
        cs.work += s * s * s
        cs.span += lg
    closure = []
    for u in range(n):
        via = 0  # @line L6 (the sample vertices reached through the sample)
        for a, i in pos.items():
            if reach[u] >> a & 1:
                via |= h[i]
        row = reach[u]  # @line L7
        for j in range(s):
            if via >> j & 1:
                row |= reach[sample[j]]
        closure.append(row)
    cs.work += 2 * n * n * max(s, 1)
    cs.span += 2 * lg
    return closure  # @line L8
