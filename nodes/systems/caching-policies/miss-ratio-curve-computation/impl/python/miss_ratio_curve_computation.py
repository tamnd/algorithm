# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miss-ratio-curve-computation/. The authors are listed in prov/XPW03J.jsonl.

"""Ways to compute the LRU miss ratio curve of a trace.

- simulate_curve: one LRU simulation per size, O(n) per size.
- mattson_distances: Mattson's LRU stack, O(n m) time.
- tree_distances: a Fenwick tree over time positions (Bennett and Kruskal), O(n log n) time.
- aet_curve: the average eviction time model of Hu et al., from reuse times, an approximation.

A reuse distance is the number of distinct other items since the last use of the same
item, or None for a first use. An LRU cache of size c hits exactly the requests with
distance < c.
"""

from collections import OrderedDict
from fractions import Fraction
from typing import Hashable, Sequence

Trace = Sequence[Hashable]


def simulate_curve(trace: Trace, max_size: int) -> list[Fraction]:
    """m(c) for c = 0..max_size by running LRU once for each size."""
    n = len(trace)
    curve = []
    for c in range(max_size + 1):
        cache: OrderedDict = OrderedDict()
        misses = 0
        for x in trace:
            if x in cache:
                cache.move_to_end(x)
            else:
                misses += 1
                if c > 0:
                    if len(cache) == c:
                        cache.popitem(last=False)
                    cache[x] = None
        curve.append(Fraction(misses, n))
    return curve


def mattson_distances(trace: Trace) -> list[int | None]:
    """The LRU stack: the depth of the item in the stack is its reuse distance."""
    stack: list = []  # the most recent item first
    out: list[int | None] = []
    for x in trace:
        try:
            d = stack.index(x)
        except ValueError:
            out.append(None)
        else:
            out.append(d)
            del stack[d]
        stack.insert(0, x)
    return out


class Fenwick:
    """Prefix sums over positions 1..n with point updates, both in O(log n)."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s


def tree_distances(trace: Trace) -> list[int | None]:
    """Mark the time of the last use of each item. The distance of a request at time t to an
    item last used at time p is the number of marks strictly between p and t."""
    n = len(trace)
    bit = Fenwick(n)
    last: dict = {}
    marks = 0
    out: list[int | None] = []
    for t, x in enumerate(trace, start=1):
        p = last.get(x)
        if p is None:
            out.append(None)
        else:
            out.append(marks - bit.prefix(p))  # marks after p; none is at t yet
            bit.add(p, -1)
            marks -= 1
        bit.add(t, 1)
        marks += 1
        last[x] = t
    return out


def curve_from_distances(distances: Sequence[int | None], max_size: int) -> list[Fraction]:
    """m(c) = 1 - (number of distances < c) / n, for c = 0..max_size."""
    n = len(distances)
    hist = [0] * (max_size + 1)
    for d in distances:
        if d is not None and d < max_size:
            hist[d] += 1
    curve, hits = [], 0
    for c in range(max_size + 1):
        curve.append(Fraction(n - hits, n))
        if c < max_size:
            hits += hist[c]
    return curve


def lru_curve(trace: Trace, max_size: int) -> list[Fraction]:
    """The exact LRU miss ratio curve in O(n log n + max_size) time."""
    return curve_from_distances(tree_distances(trace), max_size)


def aet_curve(trace: Trace, max_size: int) -> list[float]:
    """The AET model: P(t) is the fraction of requests whose reuse time is greater than t
    (first uses count as infinite). AET(c) is the least T with P(0) + ... + P(T - 1) >= c,
    and m(c) = P(AET(c))."""
    n = len(trace)
    count = [0] * (n + 2)  # count[r] = number of requests with reuse time r
    last: dict = {}
    for t, x in enumerate(trace):
        if x in last:
            count[t - last[x]] += 1
        last[x] = t
    tail = [0.0] * (n + 2)  # tail[t] = P(t)
    above = n - sum(count)  # first uses
    for t in range(n + 1, -1, -1):
        tail[t] = above / n
        above += count[t]
    curve = []
    area, T = 0.0, 0
    for c in range(max_size + 1):
        while area < c - 1e-12 and T <= n:
            area += tail[T]
            T += 1
        curve.append(tail[min(T, n + 1)])
    return curve
