# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gauss-sieve/. The authors are listed in prov/6BDMG5.jsonl.

import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from gauss_sieve import gauss_sieve

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


KISSING = {1: 2, 2: 6, 3: 12, 4: 24, 5: 40, 6: 72}


def in_lattice(v, b):
    """v is an integer combination of the rows of b (b independent)."""
    d = dual(b)
    x = [dot(v, di) for di in d]
    return all(c.denominator == 1 for c in x) and combo(x, b) == [Fraction(c) for c in v]


def check_output(b, v, lst):
    nv = dot(v, v)
    assert nv > 0 and in_lattice(v, b)
    assert nv <= min(dot(r, r) for r in b)
    assert v in lst and nv == min(dot(w, w) for w in lst)
    assert len(lst) <= KISSING[len(b)]
    for i, u in enumerate(lst):
        assert any(u) and in_lattice(u, b)
        for w in lst[i + 1 :]:
            assert 2 * abs(dot(u, w)) <= min(dot(u, u), dot(w, w))


def test_worked_example():
    v, lst = gauss_sieve([[4, 4], [9, 10]], max_collisions=3)
    assert v == [2, 0]
    assert lst == [[1, 2], [2, 0]]
    check_output([[4, 4], [9, 10]], v, lst)


def test_random_lattices_against_exact_svp():
    rng = random.Random(20240611)
    total, hits = 0, 0
    for _ in range(110):
        n = rng.randint(2, 6)
        m = rng.randint(n, n + 1)
        b = random_basis(rng, n, m)
        v, lst = gauss_sieve(b, max_collisions=15, max_samples=600, seed=rng.randrange(10**6))
        check_output(b, v, lst)
        lam = svp_sq(b)
        assert dot(v, v) >= lam
        total += 1
        hits += dot(v, v) == lam
    assert hits >= 0.9 * total


def test_skewed_bases_keep_the_invariants():
    rng = random.Random(77)
    for _ in range(40):
        n = rng.randint(2, 5)
        c = random_basis(rng, n, n, -2, 2)
        u = [[int(i == j) for j in range(n)] for i in range(n)]
        for _ in range(6):
            i, j = rng.sample(range(n), 2)
            f = rng.randint(-3, 3)
            u[i] = [a + f * x for a, x in zip(u[i], u[j])]
        b = [combo(row, c) for row in u]
        v, lst = gauss_sieve(b, max_collisions=10, max_samples=300, seed=rng.randrange(10**6))
        check_output(b, v, lst)
        assert dot(v, v) >= svp_sq(b)


def test_no_samples_processes_only_the_basis():
    rng = random.Random(5)
    for _ in range(40):
        n = rng.randint(2, 6)
        b = random_basis(rng, n, n)
        v, lst = gauss_sieve(b, max_collisions=1, max_samples=0)
        check_output(b, v, lst)


def test_already_reduced_and_dimension_one():
    v, lst = gauss_sieve([[1, 0, 0], [0, 1, 0], [0, 0, 1]], max_collisions=5)
    assert dot(v, v) == 1 and len(lst) <= 6
    check_output([[1, 0, 0], [0, 1, 0], [0, 0, 1]], v, lst)
    v, lst = gauss_sieve([[7]], max_collisions=3)
    assert v == [7] and lst == [[7]]
    v, lst = gauss_sieve([[3, 4]], max_collisions=3)
    assert v == [3, 4] and lst == [[3, 4]]


def test_nearly_dependent():
    b = [[1, 0], [1, Fraction(1, 1000)]]
    v, lst = gauss_sieve(b, max_collisions=10)
    check_output(b, v, lst)
    assert dot(v, v) == Fraction(1, 10**6)
    b = [[100, 0, 0], [101, 1, 0], [99, 0, 1]]
    v, lst = gauss_sieve(b, max_collisions=20)
    check_output(b, v, lst)
    assert dot(v, v) == svp_sq(b)


def test_deterministic_for_a_seed():
    b = [[3, 1, -2, 0], [1, 4, 0, 2], [-2, 0, 5, 1], [0, 2, 1, 4]]
    assert gauss_sieve(b, seed=11) == gauss_sieve(b, seed=11)


def test_invalid_input():
    with pytest.raises(ValueError):
        gauss_sieve([])
    with pytest.raises(ValueError):
        gauss_sieve([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        gauss_sieve([[1, 2], [3]])
    with pytest.raises(ValueError):
        gauss_sieve([[1, 0]], max_collisions=0)
