# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-push-relabel/. The authors are listed in prov/R2Q1DA.jsonl.

"""Synchronous parallel push-relabel maximum flow, simulated pulse by pulse.

In one pulse, every active vertex (a vertex other than s and t with excess)
pushes the excess it had at the start of the pulse along its admissible arcs,
with respect to the labels at the start of the pulse. Then every vertex that
still has excess and has no admissible arc is relabeled, again from the labels
at the start of the pulse. Two ends of one arc pair are never both admissible,
so the pushes of one pulse do not interfere.

Precondition: arcs is a list of triples (u, v, c) with 0 <= u, v < n and an
integer capacity c >= 0; s != t.
Cost: fewer than 4 n^2 pulses. Each pulse reads the arcs of the active and
relabeled vertices, O(n + m) work, with O(log n) span for the prefix sums
that split the excess and for the minimum of the neighbour labels.
"""

import math


class Cost:
    """Counters for work, span, pulses, pushes and relabels."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.pulses = 0
        self.pushes = 0
        self.relabels = 0


def parallel_push_relabel(
    n: int, arcs: list[tuple[int, int, int]], s: int, t: int, cost: Cost | None = None
) -> tuple[int, list[int]]:
    """Return the maximum flow value and the flow on each input arc."""
    c = cost if cost is not None else Cost()
    lg = max(1, math.ceil(math.log2(n + 2)))
    to: list[int] = []
    res: list[int] = []
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, cap in arcs:  # arc 2i is the input arc, 2i + 1 its reverse
        adj[u].append(len(to))
        to.append(v)
        res.append(cap)
        adj[v].append(len(to))
        to.append(u)
        res.append(0)
    d = [0] * n  # @line L1
    d[s] = n
    ex = [0] * n
    for a in adj[s]:  # @line L2
        if a % 2 == 0 and to[a] != s and res[a] > 0:
            x = res[a]
            res[a] = 0
            res[a ^ 1] += x
            ex[to[a]] += x
            ex[s] -= x
    c.work += n + len(adj[s])
    c.span += lg
    while True:
        active = [v for v in range(n) if v != s and v != t and ex[v] > 0]  # @line L3
        if not active:
            break
        c.pulses += 1
        d0 = d[:]  # @line L4
        got = [0] * n
        for v in active:  # @line L5
            rem = ex[v]
            for a in adj[v]:  # @line L6 (fill the admissible arcs in order)
                if rem == 0:
                    break
                w = to[a]
                if res[a] > 0 and d0[v] == d0[w] + 1:
                    x = min(rem, res[a])
                    res[a] -= x
                    res[a ^ 1] += x
                    rem -= x
                    got[w] += x
                    c.pushes += 1
            ex[v] = rem
            c.work += 1 + len(adj[v])
        for w in range(n):  # @line L7 (the sum of what arrives)
            ex[w] += got[w]
        for v in range(n):  # @line L8
            if v == s or v == t or ex[v] == 0:
                continue
            c.work += 1 + len(adj[v])
            if any(res[a] > 0 and d0[v] == d0[to[a]] + 1 for a in adj[v]):
                continue
            d[v] = 1 + min(d0[to[a]] for a in adj[v] if res[a] > 0)  # @line L9
            c.relabels += 1
        c.work += n
        c.span += 3 * lg
    flow = [res[2 * i + 1] for i in range(len(arcs))]
    return ex[t], flow  # @line L10
