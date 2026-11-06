# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deep-lll/. The authors are listed in prov/NEWYCT.jsonl.

import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from deep_lll import deep_lll


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


def svp_sq(b):
    """Exact lambda_1^2 by pruned enumeration on a test-local LLL basis.

    With Gram-Schmidt data of C, ||x C||^2 = sum_j (x_j + sum_{i>j} x_i mu_ij)^2 N_j, so the
    coefficients can be fixed from the last to the first, keeping partial sums <= best.
    """
    c = lll(b)
    bs, ns = gso_norms(c)
    n = len(c)
    mu = [[dot(c[i], bs[j]) / ns[j] for j in range(n)] for i in range(n)]
    best = [dot(c[0], c[0])]

    def search(j, x, partial):
        if j < 0:
            if any(x):
                best[0] = min(best[0], partial)
            return
        centre = -sum((x[i] * mu[i][j] for i in range(j + 1, n)), Fraction(0))
        w = sqrt_up((best[0] - partial) / ns[j])
        for xj in range(floor(centre - w), floor(centre + w) + 1):
            add = (centre - xj) ** 2 * ns[j]
            if partial + add <= best[0]:
                x[j] = xj
                search(j - 1, x, partial + add)
        x[j] = 0

    search(n - 1, [0] * n, Fraction(0))
    return best[0]


def same_lattice(b, c):
    """C = U B with U integral and det U = +-1."""
    g = inverse([[dot(u, v) for v in b] for u in b])
    u = [[sum((dot(ci, b[k]) * g[k][j] for k in range(len(b))), Fraction(0)) for j in range(len(b))] for ci in c]
    if any(x.denominator != 1 for row in u for x in row):
        return False
    return abs(det(u)) == 1


def det(a):
    a = [row[:] for row in a]
    n = len(a)
    s = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if a[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            a[c], a[p] = a[p], a[c]
            s = -s
        s *= a[c][c]
        for r in range(c + 1, n):
            f = a[r][c] / a[c][c]
            a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return s


def is_deep_reduced(c, delta):
    bs, ns = gso_norms(c)
    n = len(c)
    for k in range(n):
        mu = [dot(c[k], bs[j]) / ns[j] for j in range(k)]
        if any(abs(x) > Fraction(1, 2) for x in mu):
            return False
        for i in range(k):
            proj = ns[k] + sum((mu[j] ** 2 * ns[j] for j in range(i, k)), Fraction(0))
            if proj < delta * ns[i]:
                return False
    return True


def is_lll_reduced(c, delta):
    bs, ns = gso_norms(c)
    for k in range(1, len(c)):
        mu = dot(c[k], bs[k - 1]) / ns[k - 1]
        if ns[k] < (delta - mu * mu) * ns[k - 1]:
            return False
    return True


def test_worked_example():
    b = [[4, 0, 0], [-2, 3, 0], [1, 1, 3]]
    assert is_lll_reduced(b, Fraction(3, 4)) and not is_deep_reduced(b, Fraction(3, 4))
    c = deep_lll(b)
    assert c == [[1, 1, 3], [2, 3, 0], [2, -3, 0]]
    assert same_lattice(b, c) and is_deep_reduced(c, Fraction(3, 4))
    assert svp_sq(b) == 11


def test_random_bases():
    rng = random.Random(41)
    count = 0
    for n, reps in ((2, 200), (3, 160), (4, 90), (5, 40), (6, 15)):
        for _ in range(reps):
            m = n + rng.randint(0, 1)
            b = random_basis(rng, n, m, -6, 6)
            delta = rng.choice([Fraction(3, 4), Fraction(99, 100), Fraction(1), Fraction(1, 2)])
            c = deep_lll(b, delta)
            assert same_lattice(b, c)
            assert is_deep_reduced(c, delta)
            assert is_lll_reduced(c, delta)
            if n <= 4 or count % 3 == 0:
                alpha = 1 / (delta - Fraction(1, 4))
                assert dot(c[0], c[0]) <= alpha ** (n - 1) * svp_sq(b)
            count += 1
    assert count >= 500


def test_dimension_two_with_delta_one_is_shortest():
    rng = random.Random(42)
    for _ in range(200):
        b = random_basis(rng, 2, rng.randint(2, 3), -20, 20)
        c = deep_lll(b, 1)
        assert dot(c[0], c[0]) == svp_sq(b)


def test_idempotent_and_already_reduced():
    rng = random.Random(43)
    for _ in range(100):
        n = rng.randint(1, 5)
        b = random_basis(rng, n, n, -5, 5)
        c = deep_lll(b)
        assert deep_lll(c) == c
    eye = [[int(i == j) for j in range(4)] for i in range(4)]
    assert deep_lll(eye) == eye


def test_dimension_one():
    assert deep_lll([[-7, 3]]) == [[-7, 3]]
    assert deep_lll([[Fraction(5, 2)]]) == [[Fraction(5, 2)]]


def test_nearly_dependent_basis():
    rng = random.Random(44)
    for _ in range(40):
        n = rng.randint(2, 4)
        base = [rng.randint(1, 9) for _ in range(n)]
        b = [[c * 1000 + (i == j) for j, c in enumerate(base)] for i in range(n)]
        c = deep_lll(b)
        assert same_lattice(b, c) and is_deep_reduced(c, Fraction(3, 4))


def test_invalid_input():
    with pytest.raises(ValueError):
        deep_lll([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        deep_lll([[1, 0], [0, 1]], Fraction(1, 4))
    with pytest.raises(ValueError):
        deep_lll([[1, 0], [0, 1]], Fraction(11, 10))
    with pytest.raises(ValueError):
        deep_lll([])
