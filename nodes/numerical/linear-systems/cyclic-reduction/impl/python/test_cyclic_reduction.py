# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclic-reduction/. The authors are listed in prov/4MBFM8.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from cyclic_reduction import ZeroPivot, backward_error, cyclic_reduction, matvec, reduce_once

U = 2.0 ** -53


def dense(a, b, c):
    n = len(b)
    m = [[F(0)] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = F(b[i])
        if i > 0:
            m[i][i - 1] = F(a[i])
        if i + 1 < n:
            m[i][i + 1] = F(c[i])
    return m


def ge_nopivot(m, rhs):
    """Exact Gaussian elimination without pivoting; returns None at a zero pivot."""
    n = len(m)
    m = [row[:] + [r] for row, r in zip(m, rhs)]
    for k in range(n):
        if m[k][k] == 0:
            return None
        for i in range(k + 1, n):
            f = m[i][k] / m[k][k]
            if f:
                for j in range(k, n + 1):
                    m[i][j] -= f * m[k][j]
    x = [F(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def odd_even_perm(n):
    """The order of elimination used by cyclic reduction: all even indices of
    each level first, then recursively the odd ones."""
    idx = list(range(n))
    order = []
    while len(idx) > 1:
        order += idx[0::2]
        idx = idx[1::2]
    return order + idx


def rand_tri(rng, n, kind):
    a = [F(rng.randint(-5, 5)) for _ in range(n)]
    c = [F(rng.randint(-5, 5)) for _ in range(n)]
    if kind == "dominant":
        b = [(abs(a[i]) + abs(c[i]) + rng.randint(1, 4)) * rng.choice([-1, 1]) for i in range(n)]
    else:
        b = [F(rng.randint(-5, 5)) for _ in range(n)]
    a[0] = F(0)
    c[n - 1] = F(0)
    d = [F(rng.randint(-9, 9)) for _ in range(n)]
    return a, b, c, d


def test_page_example():
    n = 7
    a, b, c = [F(-1)] * n, [F(2)] * n, [F(-1)] * n
    a[0], c[n - 1] = F(0), F(0)
    d = [F(1), 0, 0, 0, 0, 0, F(1)]
    r1 = reduce_once(a, b, c, d)
    assert r1 == ([0, F(-1, 2), F(-1, 2)], [1, 1, 1], [F(-1, 2), F(-1, 2), 0], [F(1, 2), 0, F(1, 2)])
    r2 = reduce_once(*r1)
    assert r2 == ([0], [F(1, 2)], [0], [F(1, 2)])
    st = {}
    assert cyclic_reduction(a, b, c, d, st) == [1] * 7
    assert st == {"flops": 71, "levels": 2}


def test_exact_solution_and_breakdown_match_ge_on_permuted_matrix():
    """500 cases: CR equals exact GE without pivoting on P A P^T, including where it breaks down."""
    rng = random.Random(1)
    broke = solved = 0
    for t in range(500):
        n = rng.randint(1, 18)
        a, b, c, d = rand_tri(rng, n, "dominant" if t % 2 else "general")
        p = odd_even_perm(n)
        m = dense(a, b, c)
        pm = [[m[i][j] for j in p] for i in p]
        y = ge_nopivot(pm, [d[i] for i in p])
        try:
            x = cyclic_reduction(a, b, c, d)
        except ZeroPivot:
            assert y is None
            broke += 1
            continue
        assert y is not None
        xp = [None] * n
        for k, i in enumerate(p):
            xp[i] = y[k]
        assert x == xp
        assert matvec(a, b, c, x) == d
        solved += 1
    assert broke > 10 and solved > 300


def test_reduced_system_is_schur_complement():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(2, 12)
        a, b, c, d = rand_tri(rng, n, "dominant")
        ra, rb, rc, rd = reduce_once(a, b, c, d)
        m = dense(a, b, c)
        ev, od = list(range(0, n, 2)), list(range(1, n, 2))
        # A_ee is diagonal because no two even unknowns are coupled.
        for i in od:
            for j in od:
                if abs(i - j) > 4:
                    continue  # entries this far apart are zero on both sides
                s = m[i][j] - sum(m[i][k] * m[k][j] / m[k][k] for k in ev)
                ki, kj = i // 2, j // 2
                want = rb[ki] if ki == kj else ra[ki] if kj == ki - 1 else rc[ki] if kj == ki + 1 else 0
                assert s == want
            assert rd[i // 2] == d[i] - sum(m[i][k] * d[k] / m[k][k] for k in ev)


def test_flop_count_and_depth():
    for k in range(1, 11):
        n = 2 ** k - 1
        st = {}
        cyclic_reduction([1.0] * n, [4.0] * n, [1.0] * n, [1.0] * n, st)
        assert st["flops"] == 17 * n - 16 * k
        assert st["levels"] == k - 1
    for n in range(1, 400):
        st = {}
        cyclic_reduction([1.0] * n, [4.0] * n, [1.0] * n, [1.0] * n, st)
        assert st["levels"] == n.bit_length() - 1
        assert 17 * n - 16 * n.bit_length() <= st["flops"] <= 17 * n


def test_dominance_ratio_squares():
    """Strict row dominance beta < 1 becomes at most beta^2 after one reduction (exact)."""
    rng = random.Random(3)

    def beta(a, b, c):
        n = len(b)
        return max((abs(a[i]) * (i > 0) + abs(c[i]) * (i + 1 < n)) / abs(b[i]) for i in range(n))

    for _ in range(500):
        n = rng.randint(2, 30)
        a, b, c, d = rand_tri(rng, n, "dominant")
        b0 = beta(a, b, c)
        assert b0 < 1
        ra, rb, rc, rd = reduce_once(a, b, c, d)
        assert beta(ra, rb, rc) <= b0 * b0


def test_backward_error_diagonally_dominant_and_spd_floats():
    """Observed: eta <= u log2(n + 1) on 1000 random systems (no theorem with this constant)."""
    rng = random.Random(4)
    for t in range(1000):
        n = rng.randint(1, 120)
        if t % 2:
            a = [rng.uniform(-1, 1) for _ in range(n)]
            c = [rng.uniform(-1, 1) for _ in range(n)]
            b = [(abs(a[i]) + abs(c[i])) * rng.uniform(1.01, 3) * rng.choice([-1, 1]) for i in range(n)]
        else:
            l = [rng.uniform(0.1, 2) for _ in range(n)]
            m = [rng.uniform(-2, 2) for _ in range(n)]
            b = [l[i] ** 2 + (m[i - 1] ** 2 if i > 0 else 0) for i in range(n)]
            a = [0.0] + [m[i - 1] * l[i - 1] for i in range(1, n)]
            c = [m[i] * l[i] for i in range(n - 1)] + [0.0]
        d = [rng.uniform(-1, 1) for _ in range(n)]
        x = cyclic_reduction(a, b, c, d)
        assert backward_error(a, b, c, d, x) <= U * math.log2(n + 1) + 1e-300


def test_poisson_levels_stay_toeplitz():
    for k in range(2, 8):
        n = 2 ** k - 1
        s = ([F(0)] + [F(-1)] * (n - 1), [F(2)] * n, [F(-1)] * (n - 1) + [F(0)], [F(1)] * n)
        lev = 0
        while len(s[1]) > 1:
            s = reduce_once(*s)
            lev += 1
            m = len(s[1])
            h = F(1, 2 ** lev)
            assert s[1] == [2 * h] * m
            assert s[0][1:] == [-h] * (m - 1) and s[2][:-1] == [-h] * (m - 1)


def test_edge_cases():
    assert cyclic_reduction([], [], [], []) == []
    assert cyclic_reduction([0.0], [4.0], [0.0], [2.0]) == [0.5]
    with pytest.raises(ZeroPivot):
        cyclic_reduction([0], [0], [0], [1])
    # Diagonal.
    assert cyclic_reduction([F(0)] * 5, [F(i + 1) for i in range(5)], [F(0)] * 5, [F(1)] * 5) == [F(1, i + 1) for i in range(5)]
    # Lower bidiagonal (triangular).
    n = 9
    a, b, c = [F(0)] + [F(1)] * (n - 1), [F(1)] * n, [F(0)] * n
    x = cyclic_reduction(a, b, c, [F(1)] * n)
    assert x == [F(1), 0, 1, 0, 1, 0, 1, 0, 1]
    # Nonsingular but needs a row swap: CR without pivoting breaks down.
    with pytest.raises(ZeroPivot):
        cyclic_reduction([0, 1.0], [0.0, 0.0], [1.0, 0], [1.0, 2.0])


def test_singular_reports_failure():
    rng = random.Random(6)
    for _ in range(100):
        n = rng.randint(2, 40)
        # Neumann Laplacian: rows sum to zero, singular.
        a = [F(0)] + [F(-1)] * (n - 1)
        c = [F(-1)] * (n - 1) + [F(0)]
        b = [F(2)] * n
        b[0] = b[-1] = F(1)
        s = F(rng.randint(1, 5))
        with pytest.raises(ZeroPivot):
            cyclic_reduction([s * v for v in a], [s * v for v in b], [s * v for v in c], [F(1)] * n)
    with pytest.raises(ZeroPivot):
        cyclic_reduction([0, 1], [1, 1], [1, 0], [1, 1])


def test_tiny_pivot_is_unstable_like_ge_without_pivoting():
    eps = 1e-17
    a, b, c, d = [0.0, 1.0], [eps, 1.0], [1.0, 0.0], [1.0, 2.0]
    x = cyclic_reduction(a, b, c, d)
    # True solution is about (1, 1); the computed x0 is far off.
    assert backward_error(a, b, c, d, x) > 0.1
    # Symmetric indefinite but dominant: fine.
    x = cyclic_reduction([0.0, 1.0, 1.0], [-3.0, 3.0, -3.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0])
    assert backward_error([0.0, 1.0, 1.0], [-3.0, 3.0, -3.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0], x) < 4 * U


def test_large_system_and_agreement_with_known_solution():
    rng = random.Random(7)
    n = 30000
    a = [rng.uniform(-1, 1) for _ in range(n)]
    c = [rng.uniform(-1, 1) for _ in range(n)]
    b = [abs(a[i]) + abs(c[i]) + 1.0 for i in range(n)]
    xt = [rng.uniform(-1, 1) for _ in range(n)]
    d = matvec(a, b, c, xt)
    x = cyclic_reduction(a, b, c, d)
    assert max(abs(p - q) for p, q in zip(x, xt)) < 1e-13
