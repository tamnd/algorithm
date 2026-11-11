# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unequal-letter-cost-coding/. The authors are listed in prov/QF16XK.jsonl.

"""Optimal binary prefix codes when the letter 0 costs a and the letter 1
costs b (positive integers), by a level-by-level dynamic program in the
style of Golin and Rote (1998), and by brute force for checking.

The cost of a codeword is the sum of the costs of its letters; the cost
of a code is sum(w[i] * cost(codeword i)). Sort the weights so that
w[0] >= w[1] >= ...: some optimal code gives cheaper codewords to heavier
symbols, so the leaves can be handed out in this order, level by level,
where the level of a node is the cost of the path to it.

State (m, v): m symbols already have a leaf, and v[k] nodes wait at the
level k + 1 below the current one, for k < C = max(a, b). Moving one
level down costs the total weight of the symbols without a leaf. At the
new level, q of the waiting nodes become leaves and the others become
inner nodes, each with children at a and b levels further down. There
are O(n^(C+1)) states and O(n) choices for q, so O(n^(C+2)) time.
"""

import functools
import math
from typing import Sequence


def optimal_cost(weights: Sequence[int], a: int = 1, b: int = 2) -> tuple[int, list[int]]:
    """Least cost and the sorted leaf costs of an optimal code."""
    n = len(weights)
    if n == 0 or a <= 0 or b <= 0:
        raise ValueError("need symbols and positive letter costs")
    if n == 1:
        return 0, [0]
    w = sorted(weights, reverse=True)
    rest = [0] * (n + 1)  # rest[m] = w[m] + ... + w[n-1]
    for i in range(n - 1, -1, -1):
        rest[i] = rest[i + 1] + w[i]
    c = max(a, b)

    @functools.lru_cache(maxsize=None)
    def best(m: int, v: tuple) -> tuple[int, int]:
        """(least remaining cost, best q) with m leaves given and v waiting."""
        if m == n and not any(v):
            return 0, 0
        if not any(v):
            return math.inf, 0
        here, after = v[0], list(v[1:]) + [0]
        out = (math.inf, 0)
        for q in range(min(here, n - m) + 1):
            r = here - q  # the inner nodes at this level
            nxt = list(after)
            nxt[a - 1] += r
            nxt[b - 1] += r
            if m + q + sum(nxt) > n:  # every node needs a leaf of its own
                continue
            sub = best(m + q, tuple(nxt))[0]
            if sub < out[0]:
                out = (sub, q)
        # Every symbol without a leaf yet lies at this level or deeper.
        return out[0] + rest[m], out[1]

    start = [0] * c
    start[a - 1] += 1
    start[b - 1] += 1
    total = best(0, tuple(start))[0]
    # Recover the leaf costs.
    levels, m, v, level = [], 0, tuple(start), 1
    while m < n:
        _, q = best(m, v)
        levels += [level] * q
        r = v[0] - q
        nxt = list(v[1:]) + [0]
        nxt[a - 1] += r
        nxt[b - 1] += r
        m, v, level = m + q, tuple(nxt), level + 1
    return total, levels


@functools.lru_cache(maxsize=None)
def _shapes(n: int, a: int, b: int) -> frozenset:
    """All sorted tuples of leaf costs of full binary trees with n leaves."""
    if n == 1:
        return frozenset({(0,)})
    out = set()
    for k in range(1, n):
        for left in _shapes(k, a, b):
            for right in _shapes(n - k, a, b):
                out.add(tuple(sorted([x + a for x in left] + [y + b for y in right])))
    return frozenset(out)


def brute_force(weights: Sequence[int], a: int = 1, b: int = 2) -> int:
    """Least cost over all full binary trees, heaviest symbol on the cheapest leaf."""
    w = sorted(weights, reverse=True)
    return min(sum(x * y for x, y in zip(w, costs)) for costs in _shapes(len(w), a, b))


def capacity_root(a: int, b: int) -> float:
    """The root c > 1 of c^-a + c^-b = 1; log2(c) is the channel capacity per unit cost."""
    lo, hi = 1.0, 2.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid**-a + mid**-b > 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
