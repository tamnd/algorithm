# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kannan-enumeration/. The authors are listed in prov/NY4D49.jsonl.

import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from kannan_enumeration import kannan_enumeration

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


def is_hkz(c):
    _, ns = gso_norms(c)
    n = len(c)
    return is_size_reduced(c) and all(ns[k] == svp_sq(projected_block(c, k, n - 1)) for k in range(n))


def test_worked_example():
    b = [[4, 0, 0], [-2, 3, 0], [1, 1, 3]]
    stats = {}
    c = kannan_enumeration(b, stats)
    assert c == [[-1, -1, -3], [2, 3, 0], [-2, 3, 0]]
    assert gso_norms(c)[1] == [11, Fraction(118, 11), Fraction(648, 59)]
    assert stats["swaps"] == 0
    assert same_lattice(b, c) and is_hkz(c)


def test_quasi_hkz_swaps():
    b = [[80, 0, 0, 0, 0], [40, 58, 0, 0, 0], [0, 29, 42, 0, 0], [0, 0, 21, 30, 0], [0, 0, 0, 15, 22]]
    stats = {}
    c = kannan_enumeration(b, stats)
    assert stats["swaps"] == 2
    assert c[0] == [0, 0, 0, 15, 22] and dot(c[0], c[0]) == 709 == svp_sq(b)
    assert same_lattice(b, c) and is_hkz(c)


def test_random_bases_are_hkz_reduced():
    rng = random.Random(61)
    count = 0
    for n, reps in ((2, 80), (3, 60), (4, 35), (5, 10), (6, 4)):
        for _ in range(reps):
            m = n + rng.randint(0, 1)
            b = random_basis(rng, n, m, -6, 6)
            c = kannan_enumeration(b)
            assert same_lattice(b, c)
            assert is_hkz(c)  # includes ||c_1||^2 = lambda_1^2
            count += 1
    assert count == 189


def test_skewed_bases():
    rng = random.Random(62)
    for _ in range(25):
        n = rng.randint(3, 5)
        diag = [rng.randint(30, 60)]
        for _ in range(n - 1):
            diag.append(max(2, diag[-1] * 3 // 4))
        b = [[0] * n for _ in range(n)]
        for i in range(n):
            b[i][i] = 2 * diag[i]
            if i:
                b[i][i - 1] = diag[i - 1]
        c = kannan_enumeration(b)
        assert same_lattice(b, c) and is_hkz(c)


def test_already_reduced_and_idempotent():
    eye = [[int(i == j) for j in range(5)] for i in range(5)]
    assert kannan_enumeration(eye) == eye
    rng = random.Random(63)
    for _ in range(30):
        n = rng.randint(1, 5)
        c = kannan_enumeration(random_basis(rng, n, n, -5, 5))
        assert gso_norms(kannan_enumeration(c))[1] == gso_norms(c)[1]


def test_dimension_one():
    assert kannan_enumeration([[-7, 3]]) == [[-7, 3]]
    assert kannan_enumeration([[Fraction(5, 2)]]) == [[Fraction(5, 2)]]


def test_nearly_dependent():
    rng = random.Random(64)
    for _ in range(20):
        n = rng.randint(2, 4)
        base = [rng.randint(1, 9) for _ in range(n)]
        b = [[x * 1000 + (i == j) for j, x in enumerate(base)] for i in range(n)]
        c = kannan_enumeration(b)
        assert same_lattice(b, c) and is_hkz(c)
    b = [[1, 0], [1, Fraction(1, 1000)]]
    c = kannan_enumeration(b)
    assert dot(c[0], c[0]) == Fraction(1, 10**6) and is_hkz(c)


def test_invalid_input():
    with pytest.raises(ValueError):
        kannan_enumeration([])
    with pytest.raises(ValueError):
        kannan_enumeration([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        kannan_enumeration([[1, 2], [3]])
