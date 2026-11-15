# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/practical-dependence-tests/. The authors are listed in prov/B1R5XX.jsonl.

import random
from itertools import product

from practical_dependence_tests import EMPTY, FREE, dependence, level_view, meet, siv_kind, siv_solve


def value(sub, x):
    return sub[0] + sum(c * v for c, v in zip(sub[1:], x))


def sign(a, b):
    return "<" if a < b else ("=" if a == b else ">")


def box(bounds):
    return list(product(*[range(lo, hi + 1) for lo, hi in bounds]))


def brute_pairs(src, snk, bounds):
    pts = box(bounds)
    return [(i, j) for i in pts for j in pts if all(value(f, i) == value(g, j) for f, g in zip(src, snk))]


def points(state, lo, hi):
    """The set of pairs of a level state, by enumeration."""
    if state[0] == "empty":
        return set()
    if state[0] == "free":
        return {(x, y) for x in range(lo, hi + 1) for y in range(lo, hi + 1)}
    if state[0] == "point":
        return {(state[1], state[2])}
    _, i0, j0, p, q, tlo, thi = state
    return {(i0 + p * t, j0 + q * t) for t in range(tlo, thi + 1)}


def random_bounds(rng, k):
    top = {1: 8, 2: 6, 3: 4}[k]
    out = []
    for _ in range(k):
        lo = rng.randint(0, 2)
        out.append((lo, rng.randint(lo, top)))
    return out


def random_subscript(rng, k, used):
    f = [rng.randint(-5, 5)] + [0] * k
    g = [rng.randint(-5, 5)] + [0] * k
    for l in used:
        f[l + 1] = rng.choice([0, 1, 1, -1, 2, rng.randint(-4, 4)])
        g[l + 1] = rng.choice([0, 1, 1, -1, 2, f[l + 1], -f[l + 1], rng.randint(-4, 4)])
    return f, g


def random_case(rng):
    k = rng.randint(1, 3)
    bounds = random_bounds(rng, k)
    m = rng.randint(1, 3)
    src, snk = [], []
    i = [rng.randint(lo, hi) for lo, hi in bounds]
    j = [rng.randint(lo, hi) for lo, hi in bounds]
    meet_here = rng.random() < 0.6
    for _ in range(m):
        size = rng.choice([0, 1, 1, 1, 2, 2, 3])
        used = rng.sample(range(k), min(size, k))
        f, g = random_subscript(rng, k, used)
        if meet_here:
            g[0] += value(f, i) - value(g, j)
        src.append(tuple(f))
        snk.append(tuple(g))
    return src, snk, bounds


def check(src, snk, bounds):
    res = dependence(src, snk, bounds)
    pairs = brute_pairs(src, snk, bounds)
    true_dirs = {tuple(sign(a, b) for a, b in zip(i, j)) for i, j in pairs}
    if pairs:
        assert not res["independent"], (src, snk, bounds, pairs[0])
    if res["independent"]:
        return res, pairs
    assert true_dirs <= res["directions"], (src, snk, bounds, true_dirs, res)
    if res["exact"]:
        assert true_dirs == res["directions"], (src, snk, bounds, true_dirs, res)
        assert pairs, (src, snk, bounds, res)
    for l, d in enumerate(res["distances"]):
        if d is not None:
            assert all(j[l] - i[l] == d for i, j in pairs), (src, snk, bounds, l, d)
    return res, pairs


def test_siv_tests_are_exact():
    for a in range(-4, 5):
        for b in range(-4, 5):
            if a == 0 and b == 0:
                continue
            for c in range(-9, 10):
                for lo, hi in [(1, 1), (1, 2), (0, 4), (1, 8), (2, 7)]:
                    st = siv_solve(a, b, c, lo, hi)
                    want = {(x, y) for x in range(lo, hi + 1) for y in range(lo, hi + 1) if a * x - b * y == c}
                    assert points(st, lo, hi) == want, (a, b, c, lo, hi, st)
                    if st[0] == "line":
                        assert st[5] < st[6]


def test_siv_kinds():
    assert siv_kind(3, 3) == "strong"
    assert siv_kind(0, 2) == "weak-zero"
    assert siv_kind(2, 0) == "weak-zero"
    assert siv_kind(2, -2) == "weak-crossing"
    assert siv_kind(2, 3) == "exact"


def test_meet_is_exact():
    rng = random.Random(21)
    for _ in range(3000):
        lo = rng.randint(0, 2)
        hi = rng.randint(lo, 8)
        st = FREE
        want = points(FREE, lo, hi)
        for _ in range(rng.randint(1, 3)):
            a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-8, 8)
            st = meet(st, a, b, c, lo, hi)
            want = {(x, y) for x, y in want if a * x - b * y == c}
            assert points(st, lo, hi) == want, (st, want)


def test_level_view_is_exact():
    rng = random.Random(22)
    for _ in range(3000):
        lo = rng.randint(0, 2)
        hi = rng.randint(lo, 8)
        a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-8, 8)
        st = meet(FREE, a, b, c, lo, hi) if rng.random() < 0.8 else FREE
        for d in "<=>":
            v = level_view(st, d, lo, hi)
            want = {(x, y) for x, y in points(st, lo, hi) if sign(x, y) == d}
            if v is None:
                assert not want
            elif v[0] == "free":
                assert want == points(FREE, lo, hi) - {(x, y) for x, y in points(FREE, lo, hi) if sign(x, y) != d}
            else:
                assert points(v, lo, hi) == want


def test_never_independent_when_dependent_and_exact_when_claimed():
    rng = random.Random(23)
    dependent = exact = miv = 0
    for _ in range(2500):
        src, snk, bounds = random_case(rng)
        res, pairs = check(src, snk, bounds)
        dependent += bool(pairs)
        exact += res["exact"]
        miv += not res["exact"]
    assert dependent > 500
    assert exact > 1000
    assert miv > 50


def test_page_examples():
    # A[i + 1][j] = A[i][j] in an 8 by 8 nest: strong SIV twice, distance (1, 0).
    res, _ = check([(1, 1, 0), (0, 0, 1)], [(0, 1, 0), (0, 0, 1)], [(1, 8), (1, 8)])
    assert res["directions"] == {("<", "=")} and res["distances"] == [1, 0] and res["exact"]
    # A[i][i] = A[i][i + 1]: the delta test proves independence.
    res, _ = check([(0, 1), (0, 1)], [(0, 1), (1, 1)], [(1, 8)])
    assert res["independent"]
    # A[2*i] = A[3*i + 2] for i = 1..3: the exact SIV test proves independence.
    assert dependence([(0, 2)], [(2, 3)], [(1, 3)])["independent"]
    # A[5] = A[7]: ZIV.
    assert dependence([(5, 0)], [(7, 0)], [(1, 8)])["independent"]
    # Weak-zero: a write of A[i] and a read of A[1] in each iteration, i = 1..8.
    # Only iteration 1 writes A[1], and iterations 1..8 read it.
    res, _ = check([(0, 1)], [(1, 0)], [(1, 8)])
    assert res["directions"] == {("<",), ("=",)} and res["distances"] == [None]
    # Weak-crossing: A[i] = A[9 - i], i = 1..8: i + j = 9.
    res, _ = check([(0, 1)], [(9, -1)], [(1, 8)])
    assert res["directions"] == {("<",), (">",)}
    # The coupled example of the page: A[i + 1][i + j] = A[i][i + j], 1..6 by 1..6.
    src, snk, bounds = [(1, 1, 0), (0, 1, 1)], [(0, 1, 0), (0, 1, 1)], [(1, 6), (1, 6)]
    res, _ = check(src, snk, bounds)
    assert res["exact"] and res["directions"] == {("<", ">")} and res["distances"] == [1, -1]
    # An MIV pair that stays MIV: A[i + j] = A[i + j - 1] in a 1..4 by 1..4 nest.
    res, pairs = check([(0, 1, 1)], [(-1, 1, 1)], [(1, 4), (1, 4)])
    assert not res["exact"]
    assert {tuple(sign(a, b) for a, b in zip(i, j)) for i, j in pairs} == res["directions"]
    # The state constants of the module.
    assert EMPTY == ("empty",) and FREE == ("free",)
