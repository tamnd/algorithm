# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/miss-ratio-curve/. The authors are listed in prov/38ZHAR.jsonl.

"""Miss ratio curves: by simulation at each size, from LRU reuse distances, and the
lower convex hull that Talus reaches by splitting a cache in two shadow partitions."""

from collections import OrderedDict, deque
from fractions import Fraction
from typing import Callable, Hashable, Sequence

Trace = Sequence[Hashable]


def lru_misses(trace: Trace, c: int) -> int:
    cache: OrderedDict = OrderedDict()
    misses = 0
    for x in trace:
        if x in cache:
            cache.move_to_end(x)
            continue
        misses += 1
        if c == 0:
            continue
        if len(cache) == c:
            cache.popitem(last=False)
        cache[x] = None
    return misses


def fifo_misses(trace: Trace, c: int) -> int:
    queue: deque = deque()
    members: set = set()
    misses = 0
    for x in trace:
        if x in members:
            continue
        misses += 1
        if c == 0:
            continue
        if len(queue) == c:
            members.discard(queue.popleft())
        queue.append(x)
        members.add(x)
    return misses


def miss_ratio_curve(trace: Trace, sizes: Sequence[int], misses: Callable[[Trace, int], int] = lru_misses) -> list[Fraction]:
    """m(c) for each c in sizes, by one simulation per size."""
    n = len(trace)
    return [Fraction(misses(trace, c), n) for c in sizes]


def reuse_distances(trace: Trace) -> list[int | None]:
    """For each request, the number of distinct other items since the last use (None if first use)."""
    stack: list = []  # most recent first
    out: list[int | None] = []
    for x in trace:
        if x in stack:
            d = stack.index(x)
            stack.pop(d)
            out.append(d)
        else:
            out.append(None)
        stack.insert(0, x)
    return out


def lru_curve_from_distances(trace: Trace, max_size: int) -> list[Fraction]:
    """m(c) for c = 0..max_size: an LRU cache of size c hits exactly when the distance is below c."""
    n = len(trace)
    hist = [0] * (max_size + 1)
    for d in reuse_distances(trace):
        if d is not None and d < max_size:
            hist[d] += 1
    curve, hits = [], 0
    for c in range(max_size + 1):
        curve.append(Fraction(n - hits, n))
        if c < max_size:
            hits += hist[c]
    return curve


def lower_convex_hull(points: Sequence[tuple[Fraction, Fraction]]) -> list[tuple[Fraction, Fraction]]:
    """Lower convex hull of points sorted by x (monotone chain)."""
    hull: list = []
    for p in sorted(points):
        while len(hull) >= 2:
            (x1, y1), (x2, y2) = hull[-2], hull[-1]
            if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) <= 0:
                hull.pop()
            else:
                break
        hull.append(p)
    return hull


def talus_split(alpha: Fraction, beta: Fraction, s: Fraction) -> tuple[Fraction, Fraction]:
    """Talus: for alpha <= s <= beta, the stream fraction rho and the size s1 of the first partition.

    The first partition gets rho of the stream and size s1 = rho * alpha, so it behaves as a
    cache of size alpha; the second gets the rest and size s - s1, so it behaves as one of
    size beta. The miss ratio is rho * m(alpha) + (1 - rho) * m(beta).
    """
    if not alpha <= s <= beta or alpha == beta:
        raise ValueError("need alpha <= s <= beta and alpha < beta")
    rho = Fraction(beta - s, beta - alpha)
    return rho, rho * alpha
