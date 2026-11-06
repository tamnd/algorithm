# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fincke-pohst-enumeration/. The authors are listed in prov/0T8BFG.jsonl.

import itertools
import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from fincke_pohst_enumeration import fincke_pohst


def dot(u, v):
    return sum((Fraction(a) * b for a, b in zip(u, v)), Fraction(0))


def combo(x, b):
    return [sum((xi * row[j] for xi, row in zip(x, b)), Fraction(0)) for j in range(len(b[0]))]


def sub(u, v):
    return [a - c for a, c in zip(u, v)]


def inverse(a):
    """Exact inverse of a square rational matrix (test-local, row reduction)."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        m[c] = [x / m[c][c] for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def dual(b):
    """Rows d_i with <d_i, b_j> = [i = j] in the span of b: D = (B B^T)^-1 B."""
    gi = inverse([[dot(u, v) for v in b] for u in b])
    return [combo(gi[i], b) for i in range(len(b))]


def gso_norms(b):
    bs, norms = [], []
    for row in b:
        w = [Fraction(c) for c in row]
        for s, ns in zip(bs, norms):
            if ns != 0:
                w = sub(w, [dot(row, s) / ns * c for c in s])
        bs.append(w)
        norms.append(dot(w, w))
    return bs, norms


def lll(b):
    """Textbook exact LLL with delta = 3/4 (test-local), used only to shrink oracle boxes."""
    b = [[Fraction(c) for c in row] for row in b]
    k = 1
    while k < len(b):
        bs, ns = gso_norms(b[: k + 1])
        for j in range(k - 1, -1, -1):
            q = floor(dot(b[k], bs[j]) / ns[j] + Fraction(1, 2))
            if q:
                b[k] = sub(b[k], [q * c for c in b[j]])
        mu = dot(b[k], bs[k - 1]) / ns[k - 1]
        nk = ns[k]
        if nk >= (Fraction(3, 4) - mu * mu) * ns[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            k = max(k - 1, 1)
    return b


def sqrt_up(q):
    """A rational upper bound for the square root of a nonnegative rational."""
    k = 10**6
    return Fraction(isqrt(q.numerator * k * k // q.denominator) + 1, k)


def random_basis(rng, n, m, lo=-4, hi=4):
    while True:
        b = [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]
        _, ns = gso_norms(b)
        if all(x != 0 for x in ns):
            return b


def random_target(rng, m, scale=6):
    return [Fraction(rng.randint(-scale * 8, scale * 8), rng.randint(1, 8)) for _ in range(m)]


def ball_brute(b, t, r):
    """All lattice vectors within squared distance r of t, as a set of tuples.

    C is an LLL basis of the same lattice and d_i its dual rows. A vector v = x C with
    ||t - v||^2 <= r has |x_i - <t, d_i>| = |<t - v, d_i>| <= sqrt(r) ||d_i||, so the
    box below contains every such vector.
    """
    c = lll(b)
    d = dual(c)
    ranges = []
    for di in d:
        centre = dot(t, di)
        w = sqrt_up(r * dot(di, di))
        ranges.append(range(floor(centre - w), floor(centre + w) + 1))
    out = set()
    for x in itertools.product(*ranges):
        v = combo(x, c)
        e = sub(t, v)
        if dot(e, e) <= r:
            out.add(tuple(v))
    return out


def as_vectors(b, xs):
    return [tuple(combo(x, b)) for x in xs]


def node_bound(b, r):
    _, ns = gso_norms(b)
    n = len(b)
    total = Fraction(0)
    for k in range(n):
        p = Fraction(1)
        for i in range(k, n):
            p *= 2 * sqrt_up(r / ns[i]) + 1
        total += p
    return total


def test_worked_example():
    t = [Fraction(7, 10), Fraction(23, 10)]
    nodes = [0]
    assert fincke_pohst([[2, 0], [1, 2]], 3, t, nodes) == [[-1, 1], [0, 1]]
    assert nodes == [4]
    assert fincke_pohst([[2, 0], [1, 2]], 4) == [[-1, 0], [0, 0], [1, 0]]
    assert len(fincke_pohst([[2, 0], [1, 2]], 5)) == 7


def test_same_points_in_a_bad_basis():
    t = [Fraction(7, 10), Fraction(23, 10)]
    good = fincke_pohst([[2, 0], [1, 2]], 3, t)
    bad = fincke_pohst([[4, 4], [9, 10]], 3, t)
    assert sorted(as_vectors([[2, 0], [1, 2]], good)) == sorted(as_vectors([[4, 4], [9, 10]], bad))


def test_random_against_brute_force_ball():
    rng = random.Random(31)
    count = 0
    for n, reps in ((2, 220), (3, 160), (4, 90), (5, 30), (6, 12)):
        for _ in range(reps):
            m = n + rng.randint(0, 1)
            b = random_basis(rng, n, m, -3, 3)
            t = random_target(rng, m, 2) if rng.random() < 0.7 else [Fraction(0)] * m
            r = Fraction(rng.randint(0, 24), rng.randint(1, 4))
            nodes = [0]
            xs = fincke_pohst(b, r, t, nodes)
            assert len(set(map(tuple, xs))) == len(xs)
            for x in xs:
                assert all(isinstance(xi, int) for xi in x)
                e = sub(t, combo(x, b))
                assert dot(e, e) <= r
            assert set(as_vectors(b, xs)) == ball_brute(b, t, r)
            assert nodes[0] <= node_bound(b, r)
            count += 1
    assert count >= 500


def test_output_order_is_lexicographic_from_the_last_coordinate():
    rng = random.Random(32)
    for _ in range(100):
        n = rng.randint(1, 4)
        b = random_basis(rng, n, n)
        xs = fincke_pohst(b, rng.randint(0, 30), random_target(rng, n, 2))
        keys = [tuple(reversed(x)) for x in xs]
        assert keys == sorted(keys)


def test_shortest_vector_from_enumeration():
    rng = random.Random(33)
    for _ in range(120):
        n = rng.randint(2, 5)
        b = random_basis(rng, n, n, -4, 4)
        c0 = lll(b)[0]
        r = dot(c0, c0)  # at least lambda_1^2, and small after LLL
        xs = [x for x in fincke_pohst(b, r) if any(x)]
        assert xs
        best = min(dot(combo(x, b), combo(x, b)) for x in xs)
        others = ball_brute(b, [Fraction(0)] * n, r)
        assert best == min(dot(v, v) for v in others if any(v))


def test_dimension_one():
    rng = random.Random(34)
    for _ in range(300):
        a = rng.randint(1, 20) * rng.choice([-1, 1])
        t = Fraction(rng.randint(-300, 300), rng.randint(1, 7))
        r = Fraction(rng.randint(0, 200), rng.randint(1, 3))
        xs = fincke_pohst([[a]], r, [t])
        assert xs == [[k] for k in range(-400, 401) if (t - k * a) ** 2 <= r]


def test_zero_radius_and_boundary():
    assert fincke_pohst([[1, 0], [0, 1]], 0, [1, 2]) == [[1, 2]]
    assert fincke_pohst([[1, 0], [0, 1]], 0, [Fraction(1, 2), 0]) == []
    # points exactly on the sphere are included
    assert fincke_pohst([[1, 0], [0, 1]], 1) == [[0, -1], [-1, 0], [0, 0], [1, 0], [0, 1]]


def test_target_outside_span():
    assert fincke_pohst([[1, 0, 0]], 1, [0, 0, 2]) == []
    assert fincke_pohst([[1, 0, 0]], 4, [0, 0, 2]) == [[0]]
    assert fincke_pohst([[1, 0, 0]], 5, [Fraction(1, 2), 0, 2]) == [[0], [1]]


def test_already_reduced_and_nearly_dependent():
    rng = random.Random(35)
    for _ in range(60):
        n = rng.randint(2, 4)
        base = [rng.randint(-3, 3) for _ in range(n)]
        b = [[c * 50 + (i == j) for j, c in enumerate(base)] for i in range(n)]
        _, ns = gso_norms(b)
        if any(q == 0 for q in ns):
            continue
        t = random_target(rng, n, 4)
        r = Fraction(rng.randint(0, 12))
        assert set(as_vectors(b, fincke_pohst(b, r, t))) == ball_brute(b, t, r)
    b = [[3, 0, 0], [0, 4, 0], [0, 0, 5]]
    assert len(fincke_pohst(b, 16)) == 5


def test_invalid_input():
    with pytest.raises(ValueError):
        fincke_pohst([[1, 2], [2, 4]], 1)
    with pytest.raises(ValueError):
        fincke_pohst([], 1)
    with pytest.raises(ValueError):
        fincke_pohst([[1, 2]], 1, [0])
