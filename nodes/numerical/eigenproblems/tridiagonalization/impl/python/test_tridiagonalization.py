# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tridiagonalization/. The authors are listed in prov/9W3V78.jsonl.

import math
import random
from fractions import Fraction

import pytest

from tridiagonalization import house, tridiagonalize

U = 2.0**-53


def rand_sym(n, rng, scale=1.0):
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            a[i][j] = a[j][i] = scale * rng.uniform(-1, 1)
    return a


def full_t(d, e):
    n = len(d)
    t = [[0.0] * n for _ in range(n)]
    for i in range(n):
        t[i][i] = d[i]
    for i in range(n - 1):
        t[i][i + 1] = t[i + 1][i] = e[i]
    return t


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def fro(a):
    return math.sqrt(sum(t * t for r in a for t in r))


def backward_error(a, r):
    qt = matmul(matmul(r.q, full_t(r.d, r.e)), transpose(r.q))
    diff = [[qt[i][j] - a[i][j] for j in range(len(a))] for i in range(len(a))]
    return fro(diff) / max(fro(a), 1e-300)


def orth_error(q):
    n = len(q)
    g = matmul(transpose(q), q)
    return fro([[g[i][j] - (i == j) for j in range(n)] for i in range(n)])


def charpoly_exact(a):
    """Coefficients c_0..c_n of det(x I - A) by Faddeev-LeVerrier in exact rationals."""
    n = len(a)
    A = [[Fraction(t) for t in r] for r in a]
    c = [Fraction(0)] * (n + 1)
    c[n] = Fraction(1)
    m = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        am = [[sum(A[i][l] * m[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        for i in range(n):
            am[i][i] += c[n - k + 1]
        m = am
        am2 = [[sum(A[i][l] * m[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c[n - k] = -sum(am2[i][i] for i in range(n)) / k
    return c


def charpoly_tridiag_exact(d, e):
    """Coefficients of det(x I - T) by the three-term recurrence in exact rationals."""
    p0, p1 = [Fraction(1)], [-Fraction(d[0]), Fraction(1)]
    for k in range(1, len(d)):
        dk, b2 = Fraction(d[k]), Fraction(e[k - 1]) ** 2
        new = [Fraction(0)] * (k + 2)
        for i, cf in enumerate(p1):
            new[i + 1] += cf
            new[i] -= dk * cf
        for i, cf in enumerate(p0):
            new[i] -= b2 * cf
        p0, p1 = p1, new
    return p1 if len(d) > 0 else p0


def sturm_count(d, e, x):
    """Number of eigenvalues of T below x (LDL^T pivots of T - x I)."""
    cnt, q = 0, 1.0
    for i in range(len(d)):
        b2 = e[i - 1] ** 2 if i > 0 else 0.0
        q = d[i] - x - (b2 / q if i > 0 else 0.0)
        if q == 0.0:
            q = -U * (abs(x) + 1.0)
        if q < 0:
            cnt += 1
    return cnt


def eig_bisect(d, e):
    bound = max(abs(d[i]) + (abs(e[i - 1]) if i > 0 else 0) + (abs(e[i]) if i < len(e) else 0) for i in range(len(d)))
    out = []
    for k in range(1, len(d) + 1):
        lo, hi = -bound - 1, bound + 1
        for _ in range(100):
            mid = (lo + hi) / 2
            if sturm_count(d, e, mid) >= k:
                hi = mid
            else:
                lo = mid
        out.append((lo + hi) / 2)
    return out


def random_orthogonal_similarity(lams, rng):
    n = len(lams)
    a = [[float(lams[i]) * (i == j) for j in range(n)] for i in range(n)]
    for _ in range(3):
        v = [rng.gauss(0, 1) for _ in range(n)]
        vv = sum(t * t for t in v)
        p = [[(i == j) - 2 * v[i] * v[j] / vv for j in range(n)] for i in range(n)]
        a = matmul(matmul(p, a), p)
    for i in range(n):  # exact symmetry
        for j in range(i):
            a[i][j] = a[j][i] = (a[i][j] + a[j][i]) / 2
    return a


def test_house_maps_to_multiple_of_e1():
    rng = random.Random(1)
    for _ in range(50):
        x = [rng.uniform(-1, 1) for _ in range(rng.randint(1, 8))]
        v, beta, alpha = house(x)
        s = beta * sum(vi * xi for vi, xi in zip(v, x))
        y = [xi - s * vi for xi, vi in zip(x, v)]
        assert abs(y[0] - alpha) <= 4 * U * abs(alpha)
        assert all(abs(t) <= 8 * U * abs(alpha) for t in y[1:])
        assert abs(abs(alpha) - math.sqrt(sum(t * t for t in x))) <= 4 * U * abs(alpha)


def test_textbook_example_matches_exact_rationals():
    a = [[4, 1, -2, 2], [1, 2, 0, 1], [-2, 0, 3, -2], [2, 1, -2, -1]]
    r = tridiagonalize(a)
    d_exact = [4, Fraction(10, 3), Fraction(-33, 25), Fraction(149, 75)]
    e_exact = [-3, Fraction(-5, 3), Fraction(68, 75)]
    assert all(abs(x - float(y)) <= 1e-14 for x, y in zip(r.d, d_exact))
    assert all(abs(x - float(y)) <= 1e-14 for x, y in zip(r.e, e_exact))
    assert abs(r.q[1][0]) == 0.0 and r.q[0][0] == 1.0
    assert abs(r.q[1][1] + 1 / 3) <= 1e-15 and abs(r.q[2][1] - 2 / 3) <= 1e-15
    assert backward_error(a, r) <= 10 * U * 4


def test_backward_error_and_orthogonality_many_seeds():
    for seed in range(40):
        rng = random.Random(seed)
        n = rng.randint(1, 22)
        a = rand_sym(n, rng)
        r = tridiagonalize(a)
        assert len(r.d) == n and len(r.e) == n - 1
        assert backward_error(a, r) <= 4 * n * U
        assert orth_error(r.q) <= 4 * n * U


def test_invariants_trace_frobenius_determinant():
    for seed in range(20):
        rng = random.Random(100 + seed)
        n = rng.randint(2, 7)
        a = rand_sym(n, rng)
        r = tridiagonalize(a)
        assert abs(sum(r.d) - sum(a[i][i] for i in range(n))) <= 4 * n * U * fro(a)
        assert abs(fro(full_t(r.d, r.e)) - fro(a)) <= 4 * n * U * fro(a)
        da = charpoly_exact(a)[0] * (-1) ** n
        dt = charpoly_tridiag_exact(r.d, r.e)[0] * (-1) ** n
        assert abs(float(da - dt)) <= 20 * n * U * fro(a) ** n


def test_characteristic_polynomial_exact_reference():
    for seed in range(20):
        rng = random.Random(200 + seed)
        n = rng.randint(1, 7)
        a = rand_sym(n, rng)
        r = tridiagonalize(a)
        ca = charpoly_exact(a)
        ct = charpoly_tridiag_exact(r.d, r.e)
        nrm = fro(a)
        for k in range(n + 1):
            assert abs(float(ca[k] - ct[k])) <= 20 * n * U * math.comb(n, k) * nrm ** (n - k)


def test_known_spectrum_recovered_by_bisection():
    for seed in range(10):
        rng = random.Random(300 + seed)
        n = rng.randint(2, 16)
        lams = sorted(rng.uniform(-5, 5) for _ in range(n))
        if seed % 3 == 0:  # clusters and an exact double eigenvalue
            lams[1] = lams[0]
            lams[-1] = lams[-2] + 1e-9
        a = random_orthogonal_similarity(lams, rng)
        r = tridiagonalize(a, want_q=False)
        got = eig_bisect(r.d, r.e)
        assert max(abs(x - y) for x, y in zip(got, lams)) <= 50 * n * U * 5


def test_edge_cases():
    assert tridiagonalize([[3.0]]) == ([3.0], [], [[1.0]], (0, 0))
    r = tridiagonalize([[1.0, 2.0], [2.0, 5.0]])
    assert r.d == [1.0, 5.0] and r.e == [2.0] and r.q == [[1.0, 0.0], [0.0, 1.0]]
    t = full_t([1.0, 2.0, 3.0, 4.0, 5.0], [0.5, -1.0, 0.0, 2.0])
    r = tridiagonalize(t)  # already tridiagonal: nothing changes and Q = I exactly
    assert r.d == [1.0, 2.0, 3.0, 4.0, 5.0] and r.e == [0.5, -1.0, 0.0, 2.0]
    assert r.q == [[float(i == j) for j in range(5)] for i in range(5)]
    z = tridiagonalize([[0.0] * 6 for _ in range(6)])
    assert z.d == [0.0] * 6 and z.e == [0.0] * 5
    diag = tridiagonalize([[float(i + 1) * (i == j) for j in range(4)] for i in range(4)])
    assert diag.d == [1.0, 2.0, 3.0, 4.0] and diag.e == [0.0] * 3
    with pytest.raises(ValueError):
        tridiagonalize([])
    with pytest.raises(ValueError):
        tridiagonalize([[1.0, 2.0]])


def test_block_diagonal_input_gives_zero_offdiagonal():
    rng = random.Random(7)
    b1, b2 = rand_sym(3, rng), rand_sym(3, rng)
    a = [[0.0] * 6 for _ in range(6)]
    for i in range(3):
        for j in range(3):
            a[i][j], a[3 + i][3 + j] = b1[i][j], b2[i][j]
    r = tridiagonalize(a)
    assert abs(r.e[2]) <= 4 * U * fro(a)
    assert backward_error(a, r) <= 24 * U


def test_scaling_extremes():
    for scale in (1e150, 1e-150):
        rng = random.Random(11)
        a = rand_sym(8, rng, scale)
        r = tridiagonalize(a)
        assert backward_error(a, r) <= 32 * U
        assert orth_error(r.q) <= 32 * U


def test_upper_triangle_ignored_and_want_q_false_agrees():
    rng = random.Random(12)
    a = rand_sym(9, rng)
    b = [row[:] for row in a]
    for i in range(9):
        for j in range(i + 1, 9):
            b[i][j] = 1e9  # garbage in the strict upper triangle
    r1, r2 = tridiagonalize(a), tridiagonalize(b, want_q=False)
    assert r1.d == r2.d and r1.e == r2.e and r2.q is None


def test_flop_counts_approach_four_thirds_n_cubed():
    ratios = []
    for n in (10, 20, 40):
        r = tridiagonalize(rand_sym(n, random.Random(n)))
        ratios.append((r.flops[0] / (4 * n**3 / 3), r.flops[1] / (4 * n**3 / 3)))
    # the exact sums are 4n^3/3 + O(n^2), so the ratios decrease towards 1
    assert ratios[0][0] > ratios[1][0] > ratios[2][0] > 1.0
    assert abs(ratios[2][0] - 1) < 0.15 and abs(ratios[2][1] - 1) < 0.15


def test_backward_error_growth_is_mild():
    worst = {}
    for n in (4, 8, 16, 32):
        worst[n] = max(backward_error(a, tridiagonalize(a)) for a in (rand_sym(n, random.Random(n * 10 + s)) for s in range(3)))
    # observed errors are a small multiple of u, far below the c n u worst-case bound
    assert all(worst[n] <= 2 * n * U for n in worst)
