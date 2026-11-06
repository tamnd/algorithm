# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schnorr-euchner-enumeration/. The authors are listed in prov/ARHDFM.jsonl.

import itertools
import random
from fractions import Fraction
from math import ceil, floor, isqrt

import pytest

from schnorr_euchner_enumeration import schnorr_euchner_cvp, schnorr_euchner_svp


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), 0)


def inverse(a):
    """Exact inverse of a square Fraction matrix by Gauss-Jordan elimination."""
    n = len(a)
    m = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def combine(b, x):
    return [sum((x[i] * b[i][t] for i in range(len(b))), 0) for t in range(len(b[0]))]


def int_range(center, r2):
    """All integers z with (z - center)^2 <= r2, for Fractions center and r2 >= 0."""
    lo = floor(center) - isqrt(floor(r2)) - 2
    hi = floor(center) + isqrt(floor(r2)) + 2
    return [z for z in range(lo, hi + 1) if (z - center) ** 2 <= r2]


def brute_svp(b):
    """Minimum of ||sum x_i b_i||^2 over x != 0, by searching a proved box.

    If ||v||^2 <= R2 with R2 = min ||b_i||^2, then |x_i| = |<v, d_i>| <= ||v|| ||d_i||,
    where d_i are the dual basis vectors and ||d_i||^2 = (G^-1)_ii.
    """
    n = len(b)
    gi = inverse([[dot(u, v) for v in b] for u in b])
    r2 = min(dot(u, u) for u in b)
    ranges = [int_range(Fraction(0), r2 * gi[i][i]) for i in range(n)]
    best = None
    for x in itertools.product(*ranges):
        if any(x):
            v = combine(b, x)
            s = dot(v, v)
            if best is None or s < best:
                best = s
    return best


def brute_cvp(b, t, d2):
    """Minimum of ||t - sum x_i b_i||^2, given d2 = squared distance of some lattice vector.

    Let y be the coordinates of the projection t' of t onto the span. A closest v has
    ||v - t'||^2 <= d2, so |x_i - y_i| <= ||v - t'|| ||d_i||.
    """
    n = len(b)
    gi = inverse([[dot(u, v) for v in b] for u in b])
    r = [Fraction(dot(t, u)) for u in b]
    y = [sum((r[j] * gi[j][i] for j in range(n)), Fraction(0)) for i in range(n)]
    ranges = [int_range(y[i], d2 * gi[i][i]) for i in range(n)]
    best = None
    for x in itertools.product(*ranges):
        v = combine(b, x)
        diff = [Fraction(p) - q for p, q in zip(t, v)]
        s = dot(diff, diff)
        if best is None or s < best:
            best = s
    return best


def box_size(b, r2):
    gi = inverse([[dot(u, v) for v in b] for u in b])
    size = 1
    for i in range(len(b)):
        size *= 2 * isqrt(floor(r2 * gi[i][i])) + 3
    return size


def check_svp(b):
    v, x, s = schnorr_euchner_svp(b)
    assert any(x)
    assert v == combine(b, x)
    assert s == dot(v, v)
    assert s == brute_svp(b)
    return s


def random_independent(rng, n, m, lo, hi):
    while True:
        b = [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]
        try:
            inverse([[dot(u, v) for v in b] for u in b])
            return b
        except StopIteration:
            continue


def skew(rng, b, steps):
    """Apply random elementary integer row operations: the lattice is unchanged."""
    b = [list(r) for r in b]
    n = len(b)
    for _ in range(steps):
        i, j = rng.sample(range(n), 2)
        k = rng.choice([-2, -1, 1, 2])
        b[i] = [p + k * q for p, q in zip(b[i], b[j])]
    return b


def test_worked_example():
    b = [[1, 2, 3, 4], [2, 5, 7, 9], [3, 7, 11, 14], [4, 9, 14, 20]]
    v, x, s = schnorr_euchner_svp(b)
    assert s == 1 and v == combine(b, x)
    assert check_svp(b) == 1


def test_three_dim_example():
    b = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    v, x, s = schnorr_euchner_svp(b)
    assert s == 1 and v in ([0, 1, 0], [0, -1, 0])


def test_dimension_one():
    v, x, s = schnorr_euchner_svp([[-3, 4]])
    assert s == 25 and x in ([1], [-1])
    v, x, s = schnorr_euchner_cvp([[2]], [Fraction(7, 2)])
    assert s == Fraction(1, 4) and x in ([1], [2])


def test_already_reduced_and_orthogonal():
    assert schnorr_euchner_svp([[1, 0, 0], [0, 1, 0], [0, 0, 1]])[2] == 1
    assert check_svp([[3, 0, 0], [0, 2, 0], [0, 0, 5]]) == 4
    assert check_svp([[2, 0], [-1, 2]]) == 4


def test_nearly_dependent():
    b = [[1, 0], [1000, 1]]
    assert check_svp(b) == 1
    b = [[1, 1, 0], [1, 1, 1], [100, 101, 0]]
    assert check_svp(b) == brute_svp(b)


def test_fraction_entries():
    b = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(-1, 4), Fraction(2, 3)]]
    check_svp(b)


def test_random_svp():
    rng = random.Random(20251106)
    count = 0
    for n in range(2, 7):
        for _ in range(25 if n < 6 else 12):
            b = random_independent(rng, n, n + rng.randint(0, 1), -4, 4)
            if n <= 4:
                b = skew(rng, b, 3)
            if box_size(b, min(dot(u, u) for u in b)) > 60000:
                continue
            check_svp(b)
            count += 1
    assert count >= 80


def test_random_cvp():
    rng = random.Random(77)
    count = 0
    for n in range(2, 6):
        for _ in range(20):
            b = random_independent(rng, n, n + rng.randint(0, 1), -4, 4)
            t = [Fraction(rng.randint(-40, 40), rng.randint(1, 4)) for _ in range(len(b[0]))]
            v, x, s = schnorr_euchner_cvp(b, t)
            assert v == combine(b, x)
            diff = [p - q for p, q in zip(t, v)]
            assert s == dot(diff, diff)
            gi_off = s  # the found distance is a valid radius for the brute-force box
            if box_size(b, gi_off) > 60000:
                continue
            assert s == brute_cvp(b, t, s)
            count += 1
    assert count >= 40


def test_cvp_lattice_point_target():
    b = [[2, 1, 0], [0, 3, 1], [1, 0, 4]]
    t = combine(b, [3, -2, 5])
    v, x, s = schnorr_euchner_cvp(b, t)
    assert s == 0 and x == [3, -2, 5]


def test_errors():
    with pytest.raises(ValueError):
        schnorr_euchner_svp([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        schnorr_euchner_svp([[1, 2], [3]])
    with pytest.raises(ValueError):
        schnorr_euchner_svp([])
    with pytest.raises(ValueError):
        schnorr_euchner_cvp([[1, 0], [0, 1]], [1, 2, 3])
