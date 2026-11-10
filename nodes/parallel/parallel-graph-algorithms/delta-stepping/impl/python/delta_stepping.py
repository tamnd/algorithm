# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-stepping/. The authors are listed in prov/CXP7SG.jsonl.

"""Delta-stepping single-source shortest paths, simulated phase by phase.

Bucket i holds the vertices whose tentative distance lies in [i*delta,
(i+1)*delta). The smallest nonempty bucket is emptied in phases: each phase
relaxes the light edges (weight <= delta) of all vertices in the bucket at
once, and vertices whose distance drops back into the bucket are handled in
the next phase. When the bucket stays empty, the heavy edges of all vertices
removed from it are relaxed once.

Precondition: edges is a list of triples (u, v, w) with 0 <= u, v < n and
w >= 0, meaning the arc u -> v of weight w; delta > 0.
Cost: each vertex is handled only in the bucket of its final distance, at
most l + 1 times, where l is the most edges on a piece of weight below delta
of a shortest path with fewest edges. So the work is O((n + m)(l + 1)) plus
O(log n) per nonempty bucket, and each phase has O(log n) span.
"""

import heapq
import math


class Cost:
    """Counters for work, span, phases, nonempty buckets and relaxations."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.phases = 0
        self.buckets = 0
        self.relaxations = 0


def delta_stepping(
    n: int, edges: list[tuple[int, int, float]], s: int, delta: float, cost: Cost | None = None
) -> list[float]:
    """Return the shortest distances from s, with math.inf for unreachable vertices."""
    c = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 2)))
    light: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    heavy: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        (light if w <= delta else heavy)[u].append((v, w))
    dist = [math.inf] * n
    bucket: dict[int, set[int]] = {}
    where = [-1] * n  # the bucket a vertex is in, or -1
    heap: list[int] = []  # indices of buckets that may be nonempty

    def relax(w: int, x: float) -> None:
        if x < dist[w]:
            if where[w] != -1:
                bucket[where[w]].discard(w)
            i = math.floor(x / delta)
            if i not in bucket or not bucket[i]:
                bucket[i] = set()
                heapq.heappush(heap, i)
            bucket[i].add(w)
            where[w] = i
            dist[w] = x

    relax(s, 0.0)  # @line L1
    while heap:  # @line L2
        i = heapq.heappop(heap)  # @line L3 (the smallest nonempty bucket)
        if not bucket.get(i):
            continue
        c.buckets += 1
        c.work += lg
        settled: set[int] = set()  # @line L4
        while bucket[i]:  # @line L5 (one phase per pass)
            c.phases += 1
            cur = sorted(bucket[i])
            req = [(w, dist[v] + x) for v in cur for w, x in light[v]]  # @line L6
            for v in cur:  # @line L7
                where[v] = -1
            settled.update(cur)
            bucket[i] = set()
            best: dict[int, float] = {}
            for w, x in req:  # @line L8 (a minimum write per target, then the moves)
                if x < best.get(w, math.inf):
                    best[w] = x
            for w, x in best.items():
                relax(w, x)
            c.relaxations += len(req)
            c.work += len(cur) + len(req)
            c.span += 2 * lg
        req = [(w, dist[v] + x) for v in sorted(settled) for w, x in heavy[v]]  # @line L9
        best = {}
        for w, x in req:  # @line L10
            if x < best.get(w, math.inf):
                best[w] = x
        for w, x in best.items():
            relax(w, x)
        c.relaxations += len(req)
        c.work += len(settled) + len(req)
        c.span += 2 * lg
    return dist  # @line L11
