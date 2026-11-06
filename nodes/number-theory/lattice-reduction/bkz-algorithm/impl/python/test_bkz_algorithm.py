# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bkz-algorithm/. The authors are listed in prov/TQ85KA.jsonl.

import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from bkz_algorithm import bkz


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


def projected_block(c, k, h):
    """The vectors pi_k(c_i) for k <= i <= h (0-based, inclusive)."""
    bs, ns = gso_norms(c)
    out = []
    for i in range(k, h + 1):
        v = [Fraction(a) for a in c[i]]
        for j in range(k):
            f = dot(c[i], bs[j]) / ns[j]
            v = [a - f * s for a, s in zip(v, bs[j])]
        out.append(v)
    return out


def is_size_reduced(c):
    bs, ns = gso_norms(c)
    return all(abs(dot(c[k], bs[j]) / ns[j]) <= Fraction(1, 2) for k in range(len(c)) for j in range(k))


def is_bkz_reduced(c, beta, delta):
    _, ns = gso_norms(c)
    n = len(c)
    for k in range(n):
        h = min(k + beta - 1, n - 1)
        if delta * ns[k] > svp_sq(projected_block(c, k, h)):
            return False
    return True


def test_worked_example():
    b = [[4, 0, 0], [-2, 3, 0], [1, 1, 3]]
    assert bkz(b, 2, Fraction(3, 4)) == b
    c = bkz(b, 3, Fraction(3, 4))
    assert c == [[-1, -1, -3], [2, 3, 0], [-2, 3, 0]]
    assert same_lattice(b, c) and is_bkz_reduced(c, 3, Fraction(3, 4))
    # the first block of the input has lambda_1^2 = 13 >= (3/4) 16, the whole lattice 11 < 12
    assert svp_sq(projected_block(b, 0, 1)) == 13 and svp_sq(b) == 11


def test_random_bases():
    rng = random.Random(51)
    count = 0
    for n, reps in ((2, 200), (3, 150), (4, 90), (5, 45), (6, 20)):
        for _ in range(reps):
            m = n + rng.randint(0, 1)
            b = random_basis(rng, n, m, -6, 6)
            beta = rng.randint(2, max(2, n))
            delta = rng.choice([Fraction(3, 4), Fraction(99, 100), Fraction(1)])
            c = bkz(b, beta, delta)
            assert same_lattice(b, c)
            assert is_size_reduced(c) and is_lll_reduced(c, delta)
            if n <= 4 or count % 2 == 0:
                assert is_bkz_reduced(c, beta, delta)
            count += 1
    assert count >= 500


def test_full_block_with_delta_one_is_hkz():
    rng = random.Random(52)
    for _ in range(80):
        n = rng.randint(2, 5)
        b = random_basis(rng, n, n, -5, 5)
        c = bkz(b, n, 1)
        _, ns = gso_norms(c)
        assert ns[0] == svp_sq(b)
        for k in range(n):
            assert ns[k] == svp_sq(projected_block(c, k, n - 1))


def test_block_two_delta_one_pairs_are_lagrange_reduced():
    rng = random.Random(53)
    for _ in range(80):
        n = rng.randint(2, 5)
        b = random_basis(rng, n, n, -5, 5)
        c = bkz(b, 2, 1)
        _, ns = gso_norms(c)
        for k in range(n - 1):
            assert ns[k] == svp_sq(projected_block(c, k, k + 1))


def test_idempotent_and_already_reduced():
    rng = random.Random(54)
    for _ in range(60):
        n = rng.randint(1, 5)
        b = random_basis(rng, n, n, -5, 5)
        c = bkz(b, 3)
        assert bkz(c, 3) == c
    eye = [[int(i == j) for j in range(4)] for i in range(4)]
    assert bkz(eye, 4) == eye


def test_dimension_one_and_block_larger_than_n():
    assert bkz([[-7, 3]], 2) == [[-7, 3]]
    b = [[4, 0, 0], [-2, 3, 0], [1, 1, 3]]
    assert bkz(b, 10, Fraction(3, 4)) == bkz(b, 3, Fraction(3, 4))


def test_nearly_dependent_basis():
    rng = random.Random(55)
    for _ in range(30):
        n = rng.randint(2, 4)
        base = [rng.randint(1, 9) for _ in range(n)]
        b = [[c * 1000 + (i == j) for j, c in enumerate(base)] for i in range(n)]
        c = bkz(b, n)
        assert same_lattice(b, c) and is_bkz_reduced(c, n, Fraction(99, 100))


def test_invalid_input():
    with pytest.raises(ValueError):
        bkz([[1, 2], [2, 4]], 2)
    with pytest.raises(ValueError):
        bkz([[1, 0], [0, 1]], 1)
    with pytest.raises(ValueError):
        bkz([[1, 0], [0, 1]], 2, Fraction(1, 4))
    with pytest.raises(ValueError):
        bkz([], 2)
