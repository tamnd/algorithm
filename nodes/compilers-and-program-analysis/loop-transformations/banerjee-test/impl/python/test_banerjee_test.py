# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banerjee-test/. The authors are listed in prov/PS0MQH.jsonl.

import random
from fractions import Fraction
from itertools import product

from banerjee_test import (
    banerjee_test,
    direction_vectors,
    level_bounds,
    level_vertices,
    real_witness,
    subscript_bounds,
)

DIRS = "<=>*"


def holds(rel, a, b) -> bool:
    return rel == "*" or (rel == "<" and a < b) or (rel == "=" and a == b) or (rel == ">" and a > b)


def sign(a, b) -> str:
    return "<" if a < b else ("=" if a == b else ">")


def value(sub, x):
    return sub[0] + sum(c * v for c, v in zip(sub[1:], x))


def box(bounds):
    return list(product(*[range(lo, hi + 1) for lo, hi in bounds]))


def brute_pairs(src, snk, bounds, psi=None):
    """All integer pairs (i, j) in the box with equal subscripts and directions psi."""
    pts = box(bounds)
    out = []
    for i in pts:
        for j in pts:
            if psi is not None and not all(holds(r, a, b) for r, a, b in zip(psi, i, j)):
                continue
            if all(value(f, i) == value(g, j) for f, g in zip(src, snk)):
                out.append((i, j))
    return out


def random_bounds(rng, k):
    top = {1: 8, 2: 6, 3: 4}[k]
    out = []
    for _ in range(k):
        lo = rng.randint(0, 2)
        out.append((lo, rng.randint(lo, top)))
    return out


def random_case(rng):
    k = rng.randint(1, 3)
    bounds = random_bounds(rng, k)
    m = rng.randint(1, 2)
    src, snk = [], []
    for _ in range(m):
        f = [rng.randint(-6, 6)] + [rng.randint(-4, 4) for _ in range(k)]
        g = [rng.randint(-6, 6)] + [rng.randint(-4, 4) for _ in range(k)]
        if rng.random() < 0.5:
            i = [rng.randint(lo, hi) for lo, hi in bounds]
            j = [rng.randint(lo, hi) for lo, hi in bounds]
            g[0] += value(f, i) - value(g, j)
        src.append(tuple(f))
        snk.append(tuple(g))
    psi = None if rng.random() < 0.3 else tuple(rng.choice(DIRS) for _ in range(k))
    return src, snk, bounds, psi


def in_region(x, y, bounds, psi):
    for l, (lo, hi) in enumerate(bounds):
        d = "*" if psi is None else psi[l]
        if not (lo <= x[l] <= hi and lo <= y[l] <= hi):
            return False
        if d == "<" and not x[l] + 1 <= y[l]:
            return False
        if d == ">" and not y[l] + 1 <= x[l]:
            return False
        if d == "=" and x[l] != y[l]:
            return False
    return True


def test_level_bounds_are_the_extremes_over_integer_points():
    # The vertices of each region are integer points, so the closed forms
    # must equal the min and max of a*x - b*y over the integer points.
    for a in range(-5, 6):
        for b in range(-5, 6):
            for lo in range(0, 3):
                for hi in range(lo, 8):
                    for d in DIRS:
                        pts = [(x, y) for x in range(lo, hi + 1) for y in range(lo, hi + 1) if holds(d, x, y)]
                        r = level_bounds(a, b, lo, hi, d)
                        if not pts:
                            assert r is None
                            assert level_vertices(lo, hi, d) == []
                            continue
                        vals = [a * x - b * y for x, y in pts]
                        assert r == (min(vals), max(vals)), (a, b, lo, hi, d)
                        vs = level_vertices(lo, hi, d)
                        assert all(p in pts for p in vs)
                        assert min(a * x - b * y for x, y in vs) == r[0]
                        assert max(a * x - b * y for x, y in vs) == r[1]


def test_subscript_bounds_over_the_whole_box():
    rng = random.Random(11)
    for _ in range(400):
        k = rng.randint(1, 3)
        bounds = random_bounds(rng, k)
        f = tuple(rng.randint(-5, 5) for _ in range(k + 1))
        g = tuple(rng.randint(-5, 5) for _ in range(k + 1))
        psi = tuple(rng.choice(DIRS) for _ in range(k))
        r = subscript_bounds(f, g, bounds, psi)
        vals = [
            sum(f[l + 1] * i[l] - g[l + 1] * j[l] for l in range(k))
            for i in box(bounds)
            for j in box(bounds)
            if all(holds(d, a, b) for d, a, b in zip(psi, i, j))
        ]
        if not vals:
            assert r is None
        else:
            assert r == (min(vals), max(vals))


def test_never_independent_when_dependent():
    rng = random.Random(12)
    dependent = 0
    for _ in range(1500):
        src, snk, bounds, psi = random_case(rng)
        sols = brute_pairs(src, snk, bounds, psi)
        answer = banerjee_test(src, snk, bounds, psi)
        if sols:
            dependent += 1
            assert answer == "maybe", (src, snk, bounds, psi, sols[0])
    assert dependent > 300


def test_exact_over_the_reals_for_one_subscript():
    # "maybe" comes with a real witness in the region; "independent" means
    # that c is outside [lo, hi], the exact range of the left side.
    rng = random.Random(13)
    maybes = 0
    for _ in range(3000):
        k = rng.randint(1, 3)
        bounds = random_bounds(rng, k)
        f = tuple(rng.randint(-7, 7) for _ in range(k + 1))
        g = tuple(rng.randint(-7, 7) for _ in range(k + 1))
        psi = tuple(rng.choice(DIRS) for _ in range(k))
        answer = banerjee_test([f], [g], bounds, psi)
        w = real_witness(f, g, bounds, psi)
        assert (w is not None) == (answer == "maybe")
        if w is None:
            continue
        maybes += 1
        x, y = w
        assert all(isinstance(v, (int, Fraction)) for v in x + y)
        assert in_region(x, y, bounds, psi)
        assert value(f, x) == value(g, y)
    assert maybes > 500


def test_direction_vectors_contain_every_true_direction():
    rng = random.Random(14)
    for _ in range(600):
        src, snk, bounds, _ = random_case(rng)
        k = len(bounds)
        found = direction_vectors(src, snk, bounds)
        true = {tuple(sign(a, b) for a, b in zip(i, j)) for i, j in brute_pairs(src, snk, bounds)}
        assert true <= found
        # The pruned search loses nothing against testing every plain vector.
        every = {p for p in product("<=>", repeat=k) if banerjee_test(src, snk, bounds, p) == "maybe"}
        assert found == every


def test_page_examples():
    # A[i] = A[i + 10] for i = 1..5: gcd 1, but i - j lies in [-4, 4].
    assert banerjee_test([(0, 1)], [(10, 1)], [(1, 5)]) == "independent"
    # A[2*i] = A[3*i + 2] for i = 1..3: real range [-7, 3] holds 2.
    assert subscript_bounds((0, 2), (2, 3), [(1, 3)]) == (-7, 3)
    assert banerjee_test([(0, 2)], [(2, 3)], [(1, 3)]) == "maybe"
    assert level_bounds(2, 3, 1, 3, "<") == (-7, -4)
    assert level_bounds(2, 3, 1, 3, "=") == (-3, -1)
    assert level_bounds(2, 3, 1, 3, ">") == (0, 3)
    assert direction_vectors([(0, 2)], [(2, 3)], [(1, 3)]) == {(">",)}
    assert brute_pairs([(0, 2)], [(2, 3)], [(1, 3)]) == []
    x, y = real_witness((0, 2), (2, 3), [(1, 3)], (">",))
    assert 2 * x[0] == 3 * y[0] + 2 and y[0] + 1 <= x[0]
    # X[i + 2*j] = X[i + 2*j - 1] in a 1..4 by 1..4 nest (page example).
    src, snk, bounds = [(0, 1, 2)], [(-1, 1, 2)], [(1, 4), (1, 4)]
    assert subscript_bounds(src[0], snk[0], bounds, ("=", "*")) == (-6, 6)
    assert subscript_bounds(src[0], snk[0], bounds, ("=", "<")) == (-6, -2)
    assert subscript_bounds(src[0], snk[0], bounds, ("=", "=")) == (0, 0)
    assert subscript_bounds(src[0], snk[0], bounds, ("=", ">")) == (2, 6)
    assert subscript_bounds(src[0], snk[0], bounds, ("<", ">")) == (-1, 5)
    found = direction_vectors(src, snk, bounds)
    true = {tuple(sign(a, b) for a, b in zip(i, j)) for i, j in brute_pairs(src, snk, bounds)}
    assert found == true == {("<", "="), ("<", ">"), (">", "<")}
