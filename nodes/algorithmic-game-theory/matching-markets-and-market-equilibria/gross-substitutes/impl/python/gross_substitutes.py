# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gross-substitutes/. The authors are listed in prov/9N457B.jsonl.
"""Two checks of the gross substitutes property for a valuation on a few goods.

A valuation is a function v from a frozenset of the goods 0, ..., m - 1 to a number, with
v(empty set) = 0. At prices p the utility of a bundle S is v(S) - sum of p over S, and the
demand set D(p) holds the bundles of maximum utility. The valuation has gross substitutes when
for all prices p <= p' and every S in D(p) some T in D(p') contains {j in S : p_j = p'_j}.

check_by_prices tests this definition directly on a finite set of price vectors. It is a brute
force check, meant for 3 goods. check_local tests the local exchange conditions of Reijnierse,
van Gellekom and Potters (2002), which are equivalent to gross substitutes.
"""

from fractions import Fraction
from itertools import combinations, product
from typing import Callable, Optional

Valuation = Callable[[frozenset], object]


def bundles(m: int) -> list[frozenset]:
    return [frozenset(c) for k in range(m + 1) for c in combinations(range(m), k)]


def demand(v: Valuation, prices, m: int) -> list[frozenset]:
    """All bundles of maximum utility at the given prices."""
    util = {S: v(S) - sum((prices[j] for j in S), Fraction(0)) for S in bundles(m)}
    best = max(util.values())
    return [S for S, u in util.items() if u == best]


def check_by_prices(v: Valuation, m: int, points) -> Optional[tuple]:
    """Test the definition on all price vectors with coordinates in points.

    Return None if no violation is found, or a witness (p, q, S): p <= q, S is in D(p), and no
    bundle of D(q) contains the goods of S whose price did not change.
    """
    vecs = list(product(sorted(set(points)), repeat=m))
    dem = {p: demand(v, p, m) for p in vecs}
    for p in vecs:
        for q in vecs:
            if all(a <= b for a, b in zip(p, q)):
                for S in dem[p]:
                    keep = frozenset(j for j in S if p[j] == q[j])
                    if not any(keep <= T for T in dem[q]):
                        return (p, q, S)
    return None


def check_local(v: Valuation, m: int) -> Optional[tuple]:
    """Test the conditions of Reijnierse, van Gellekom and Potters on every bundle S and
    distinct goods i, j, k outside S:

        v(S + i + j) + v(S) <= v(S + i) + v(S + j)
        v(S + i + j) + v(S + k) <= max(v(S + i + k) + v(S + j), v(S + j + k) + v(S + i))

    Return None if both hold everywhere, or a witness (S, i, j) or (S, i, j, k).
    """
    for S in bundles(m):
        out = [x for x in range(m) if x not in S]
        for i, j in combinations(out, 2):
            if v(S | {i, j}) + v(S) > v(S | {i}) + v(S | {j}):
                return (S, i, j)
            for k in out:
                if k in (i, j):
                    continue
                lhs = v(S | {i, j}) + v(S | {k})
                rhs = max(v(S | {i, k}) + v(S | {j}), v(S | {j, k}) + v(S | {i}))
                if lhs > rhs:
                    return (S, i, j, k)
    return None
