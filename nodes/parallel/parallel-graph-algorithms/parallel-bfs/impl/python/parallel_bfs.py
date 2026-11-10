# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-bfs/. The authors are listed in prov/M17THE.jsonl.

"""Level-synchronous parallel BFS, simulated one synchronous PRAM step at a time.

Each parallel step reads only the state from before the step and then applies
its writes. Concurrent writes to one cell follow the CRCW arbitrary rule: the
simulator lets a seeded random generator pick the winner, so a test can run
many different winners. This is the same effect as a compare-and-swap.

Precondition: adj is a list of adjacency lists over the vertices 0 .. n - 1,
with no parallel edges, and 0 <= s < n. The graph may be directed.
Cost: work O(n + m), span O(D log n), where D is the number of levels.
"""

import random


class Cost:
    """Counters for the work (operations) and the span (steps on the critical path)."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.rounds = 0


def log2_ceil(k: int) -> int:
    """The number of tree levels that a scan or pack over k items needs."""
    return max(1, (k - 1).bit_length()) if k > 1 else 1


def arbitrary_write(writes: list[tuple[int, int]], rng: random.Random) -> dict[int, int]:
    """Resolve concurrent writes (address, value): one arbitrary writer wins at each address."""
    by_addr: dict[int, list[int]] = {}
    for addr, val in writes:
        by_addr.setdefault(addr, []).append(val)
    return {addr: rng.choice(vals) for addr, vals in by_addr.items()}


def exclusive_scan(xs: list[int]) -> list[int]:
    """Exclusive prefix sums. A parallel scan does this with O(k) work and O(log k) span."""
    out, total = [], 0
    for x in xs:
        out.append(total)
        total += x
    return out


def parallel_bfs(
    adj: list[list[int]], s: int, rng: random.Random | None = None, cost: Cost | None = None
) -> tuple[list[float], list[int | None]]:
    """Return (dist, parent) of a BFS from s. dist[v] is inf when v is not reachable."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    n = len(adj)
    inf = float("inf")
    dist: list[float] = [inf] * n  # @line L1
    parent: list[int | None] = [None] * n
    c.work += n
    c.span += 1
    dist[s], parent[s] = 0, s  # @line L2
    frontier, d = [s], 0
    while frontier:  # @line L3
        d += 1  # @line L4
        c.rounds += 1
        off = exclusive_scan([len(adj[u]) for u in frontier])  # @line L5
        k = off[-1] + len(adj[frontier[-1]])
        # step 1: every edge out of the frontier tries to claim its head (reads the old parent)
        writes = []
        for u in frontier:  # @line L6
            for v in adj[u]:  # @line L7
                if parent[v] is None:  # @line L8
                    writes.append((v, u))
        for v, u in arbitrary_write(writes, rng).items():
            parent[v] = u
        # step 2: each claimer reads back the winner and writes its own slot of C
        cand: list[int | None] = [None] * k
        for j, u in enumerate(frontier):  # @line L9
            for i, v in enumerate(adj[u]):  # @line L10
                if parent[v] == u and dist[v] == inf:  # @line L11
                    cand[off[j] + i] = v
        frontier = [v for v in cand if v is not None]  # @line L12
        for v in frontier:  # @line L13
            dist[v] = d
        c.work += len(off) + 3 * k + len(frontier)
        c.span += 2 * log2_ceil(k + 1) + 4
    return dist, parent  # @line L14
