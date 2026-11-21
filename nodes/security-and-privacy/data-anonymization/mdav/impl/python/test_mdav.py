# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mdav/. The authors are listed in prov/HMJJKR.jsonl.
import random
from collections import Counter
from fractions import Fraction

import pytest

from mdav import mdav, microaggregate, sse

PAGE = [(1, 1), (2, 1), (1, 2), (8, 8), (9, 8), (8, 9), (5, 1), (5, 2), (6, 1), (4, 9)]


def ref_mdav(x, k):
    """An independent MDAV: full sorts instead of selections, sets instead of lists."""

    def cen(ids):
        return tuple(Fraction(sum(x[i][a] for i in ids), len(ids)) for a in range(len(x[0])))

    def d2(p, q):
        return sum((Fraction(a) - Fraction(b)) ** 2 for a, b in zip(p, q))

    def far(ids, p):
        best = max(d2(x[i], p) for i in ids)
        return min(i for i in ids if d2(x[i], p) == best)

    def grp(ids, r):
        order = sorted(ids - {r}, key=lambda i: (d2(x[i], x[r]), i))
        return {r} | set(order[: k - 1])

    rest = set(range(len(x)))
    out = []
    while len(rest) >= 3 * k:
        r = far(rest, cen(rest))
        g = grp(rest, r)
        out.append(g)
        rest -= g
        s = far(rest, x[r])
        g = grp(rest, s)
        out.append(g)
        rest -= g
    if len(rest) >= 2 * k:
        r = far(rest, cen(rest))
        g = grp(rest, r)
        out.append(g)
        rest -= g
    out.append(rest)
    return [sorted(g) for g in out]


def partitions(items):
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        for j in range(len(p)):
            yield p[:j] + [[first] + p[j]] + p[j + 1 :]
        yield [[first]] + p


def best_sse(x, k):
    best = None
    for p in partitions(list(range(len(x)))):
        if all(k <= len(g) <= 2 * k - 1 for g in p):
            v = sse(x, p)
            if best is None or v < best:
                best = v
    return best


def test_page_example() -> None:
    groups = mdav(PAGE, 3)
    assert groups == [[3, 4, 5], [0, 1, 2], [6, 7, 8, 9]]
    _, masked = microaggregate(PAGE, 3)
    assert masked[0] == [Fraction(4, 3), Fraction(4, 3)]
    assert masked[3] == [Fraction(25, 3), Fraction(25, 3)]
    assert masked[9] == [5, Fraction(13, 4)]
    assert sse(PAGE, groups) == Fraction(593, 12)


def test_not_optimal() -> None:
    x = [(1,), (1,), (3,), (3,), (4,)]
    groups = mdav(x, 2)
    assert groups == [[2, 4], [0, 1, 3]]
    assert sse(x, groups) == Fraction(19, 6)
    assert best_sse(x, 2) == Fraction(2, 3)
    assert sse(x, [[0, 1], [2, 3, 4]]) == Fraction(2, 3)


def test_edge_cases() -> None:
    assert mdav([(3, 4)], 1) == [[0]]
    assert mdav([(1,), (2,), (3,)], 3) == [[0, 1, 2]]
    assert mdav([(1,), (2,), (3,), (4,), (5,)], 3) == [[0, 1, 2, 3, 4]]
    assert mdav([(0,)] * 6, 2) == [[0, 1], [2, 3], [4, 5]]
    with pytest.raises(ValueError):
        mdav([(1,), (2,)], 3)
    with pytest.raises(ValueError):
        mdav([(1,)], 0)


def test_against_reference() -> None:
    rng = random.Random(20050601)
    for _ in range(600):
        n = rng.randint(1, 14)
        d = rng.randint(1, 3)
        k = rng.randint(1, min(n, 4))
        x = [tuple(rng.randint(0, 6) for _ in range(d)) for _ in range(n)]
        groups = mdav(x, k)
        assert groups == ref_mdav(x, k)
        flat = sorted(i for g in groups for i in g)
        assert flat == list(range(n))
        assert all(len(g) == k for g in groups[:-1])
        assert k <= len(groups[-1]) <= 2 * k - 1
        _, masked = microaggregate(x, k)
        counts = Counter(tuple(m) for m in masked)
        assert all(counts[tuple(m)] >= k for m in masked)
        for a in range(d):
            assert sum(m[a] for m in masked) == sum(r[a] for r in x)


def test_never_below_optimum() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(2, 7)
        k = rng.randint(1, min(n, 3))
        x = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)]
        assert sse(x, mdav(x, k)) >= best_sse(x, k)


def test_float_input() -> None:
    x = [(0.5, 0.25), (0.75, 0.5), (10.0, 10.5), (10.25, 9.75)]
    assert mdav(x, 2) == [[2, 3], [0, 1]]
