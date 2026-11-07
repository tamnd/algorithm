# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mrrr-algorithm/. The authors are listed in prov/B3BDXW.jsonl.

import math
import random
from fractions import Fraction

import pytest

from mrrr_algorithm import dqds_progressive, mrrr, negcount, stqds, twisted_vector

U = 2.0**-53


def tnorm(a, b):
    """max row sum of |T|, an upper bound for ||T||_2."""
    n = len(a)
    return max(abs(a[i]) + (abs(b[i - 1]) if i > 0 else 0) + (abs(b[i]) if i < n - 1 else 0) for i in range(n))


def tmul(a, b, v):
    n = len(a)
    return [a[i] * v[i] + (b[i - 1] * v[i - 1] if i > 0 else 0) + (b[i] * v[i + 1] if i < n - 1 else 0) for i in range(n)]


def residual(a, b, r):
    worst = 0.0
    for lam, v in zip(r.values, r.vectors):
        tv = tmul(a, b, v)
        worst = max(worst, math.sqrt(sum((x - lam * y) ** 2 for x, y in zip(tv, v))))
    return worst / max(tnorm(a, b), 1e-300)


def orthogonality(r):
    n = len(r.vectors)
    v = r.vectors
    return max(abs(sum(x * y for x, y in zip(v[i], v[j])) - (i == j)) for i in range(n) for j in range(i, n))


def exact_count(a, b, x):
    """Exact number of eigenvalues below x: negative pivots of T - x I in rational arithmetic."""
    x = Fraction(x)
    count = 0
    q = None
    for k in range(len(a)):
        q = Fraction(a[k]) - x - (Fraction(b[k - 1]) ** 2 / q if k > 0 else 0)
        if q == 0:
            q = Fraction(-1, 10**60)  # an eigenvalue of a leading block exactly at x
        count += q < 0
    return count


def exact_det(a, b):
    """det T by the three-term recurrence of the leading minors, exactly."""
    p0, p1 = Fraction(1), Fraction(a[0])
    for k in range(1, len(a)):
        p0, p1 = p1, Fraction(a[k]) * p1 - Fraction(b[k - 1]) ** 2 * p0
    return p1


def check(a, b, r, c_res=4, c_orth=100):
    n = len(a)
    assert len(r.values) == n and all(x <= y for x, y in zip(r.values, r.values[1:]))
    assert residual(a, b, r) <= c_res * n * U
    assert orthogonality(r) <= c_orth * n * U


def random_tridiagonal(rng, n):
    return [rng.uniform(-1, 1) for _ in range(n)], [rng.uniform(-1, 1) for _ in range(n - 1)]


def wilkinson_plus(m):
    h = m // 2
    return [float(abs(h - k)) for k in range(m)], [1.0] * (m - 1)


def test_random_matrices_many_seeds():
    worst_res = worst_orth = 0.0
    for seed in range(40):
        rng = random.Random(seed)
        n = rng.randint(2, 40)
        a, b = random_tridiagonal(rng, n)
        r = mrrr(a, b)
        check(a, b, r)
        worst_res = max(worst_res, residual(a, b, r) / (n * U))
        worst_orth = max(worst_orth, orthogonality(r) / (n * U))
        assert r.twisted == n and r.fallbacks == 0  # one twisted factorization per eigenvector
    assert worst_res <= 2.0 and worst_orth <= 30.0  # observed: at most about 1.3 and 9 times n u


def test_eigenvalues_against_exact_counts_trace_and_determinant():
    for seed in range(12):
        rng = random.Random(100 + seed)
        n = rng.randint(2, 14)
        a = [float(rng.randint(-6, 6)) for _ in range(n)]
        b = [float(rng.choice([-3, -2, -1, 1, 2, 3])) for _ in range(n - 1)]
        r = mrrr(a, b)
        check(a, b, r)
        t = 8 * n * U * tnorm(a, b)
        for k, lam in enumerate(r.values, start=1):
            assert exact_count(a, b, lam - t) <= k - 1  # lambda_k >= lam - t
            assert exact_count(a, b, lam + t) >= k  # lambda_k <= lam + t
        assert abs(sum(r.values) - sum(a)) <= 4 * n * U * n * tnorm(a, b)
        det = float(exact_det(a, b))
        prod = math.prod(r.values)
        lam_abs = math.prod(abs(x) for x in r.values)
        assert abs(prod - det) <= 1e-10 * max(lam_abs, 1.0) * n


def test_known_spectra():
    n = 50  # second difference matrix: lambda_k = 2 - 2 cos(k pi / (n+1)), v_k(j) = sin(j k pi / (n+1))
    a, b = [2.0] * n, [-1.0] * (n - 1)
    r = mrrr(a, b)
    check(a, b, r)
    for k in range(1, n + 1):
        assert r.values[k - 1] == pytest.approx(2 - 2 * math.cos(k * math.pi / (n + 1)), abs=4 * U * 4)
        w = [math.sin(j * k * math.pi / (n + 1)) for j in range(1, n + 1)]
        nw = math.sqrt(sum(x * x for x in w))
        assert abs(abs(sum(x * y for x, y in zip(w, r.vectors[k - 1]))) / nw - 1) <= 1e-12
    n = 30  # Clement (Kac) matrix: eigenvalues -(n-1), -(n-3), ..., n-1
    a, b = [0.0] * n, [math.sqrt((i + 1) * (n - 1 - i)) for i in range(n - 1)]
    r = mrrr(a, b)
    check(a, b, r)
    assert r.values == pytest.approx([float(-(n - 1) + 2 * k) for k in range(n)], abs=1e-12)


def test_close_pairs_need_new_representations():
    a, b = wilkinson_plus(21)  # the two largest eigenvalues differ by 7.2e-14
    r = mrrr(a, b)
    check(a, b, r)
    assert r.max_depth >= 1 and r.representations > 1
    assert r.values[-1] - r.values[-2] == pytest.approx(7.1e-14, rel=0.05)
    assert abs(sum(x * y for x, y in zip(r.vectors[-1], r.vectors[-2]))) <= 21 * 100 * U


def test_glued_wilkinson_deep_tree():
    w, wb = wilkinson_plus(21)
    a = w * 4
    b = (wb + [1e-14]) * 3 + wb  # four copies glued by 1e-14: clusters of eigenvalues equal to about u
    r = mrrr(a, b)
    check(a, b, r, c_orth=20)  # observed: 8.7 n u
    assert r.max_depth >= 2 and r.fallbacks >= 1


def test_twisted_factorization_identities():
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randint(2, 9)
        d = [rng.uniform(0.5, 2) for _ in range(n)]
        l = [rng.uniform(-1, 1) for _ in range(n - 1)]
        mu = rng.uniform(-1, 3)
        dp, lp, _ = stqds(d, l, mu)
        p, um = dqds_progressive(d, l, mu)
        # L D L^T - mu I as a tridiagonal: diagonal and off-diagonal
        diag = [d[i] + (d[i - 1] * l[i - 1] ** 2 if i > 0 else 0) - mu for i in range(n)]
        off = [d[i] * l[i] for i in range(n - 1)]
        # top-down: L+ D+ L+^T has the same tridiagonal
        diag_p = [dp[i] + (dp[i - 1] * lp[i - 1] ** 2 if i > 0 else 0) for i in range(n)]
        assert diag_p == pytest.approx(diag, abs=1e-12) and [dp[i] * lp[i] for i in range(n - 1)] == pytest.approx(off)
        # bottom-up: U- D- U-^T with D-(i+1) = p(i+1) + d(i) l(i)^2 and D-(0) = p(0)
        dm = [p[0]] + [d[i] * l[i] ** 2 + p[i + 1] for i in range(n - 1)]
        diag_m = [dm[i] + (dm[i + 1] * um[i] ** 2 if i < n - 1 else 0) for i in range(n)]
        assert diag_m == pytest.approx(diag, abs=1e-12) and [dm[i + 1] * um[i] for i in range(n - 1)] == pytest.approx(off)
        # the twisted vector solves (L D L^T - mu I) z = gamma_r e_r
        z, rr, g = twisted_vector(d, l, mu)
        res = [diag[i] * z[i] + (off[i - 1] * z[i - 1] if i > 0 else 0) + (off[i] * z[i + 1] if i < n - 1 else 0) for i in range(n)]
        want = [g if i == rr else 0.0 for i in range(n)]
        assert res == pytest.approx(want, abs=1e-12)
        # the count of negative pivots is the number of eigenvalues below mu (Sylvester)
        assert negcount(d, l, mu) == sum(1 for x in dp if x < 0)


def test_cost_counts_and_quadratic_scaling():
    per = []
    for n in (25, 50, 100):
        rng = random.Random(n)
        a, b = random_tridiagonal(rng, n)
        r = mrrr(a, b)
        check(a, b, r)
        per.append(r.counts / n)
        assert r.twisted == n
    # each eigenvalue costs a bounded number of O(n) count sweeps, so the total is O(n^2) flops
    assert max(per) <= 70 and max(per) / min(per) <= 1.2


def test_page_example():
    a, b = wilkinson_plus(9)
    r = mrrr(a, b)
    check(a, b, r, c_orth=10)
    want = [-1.125422415673, 0.254718759826, 0.952584219075, 1.822717080887, 2.178284739550,
            3.177282919113, 3.247396472579, 4.745281240174, 4.747156984469]
    assert r.values == pytest.approx(want, abs=1e-12)
    assert (r.max_depth, r.representations, r.twisted, r.fallbacks) == (1, 2, 9, 0)
    v8, v9 = r.vectors[7], r.vectors[8]
    s8 = math.copysign(1, v8[8])
    s9 = math.copysign(1, v9[8])
    assert [round(s8 * x, 6) for x in v8] == [0.550094, 0.409975, 0.165427, 0.04417, 0.0, -0.04417, -0.165427, -0.409975, -0.550094][::-1]
    assert [round(s9 * x, 6) for x in v9] == [0.548707, 0.40997, 0.167575, 0.050386, 0.021228, 0.050386, 0.167575, 0.40997, 0.548707]
    assert sum(r.values) == pytest.approx(20.0, abs=1e-13)


def test_edge_cases():
    r = mrrr([], [])
    assert r.values == [] and r.vectors == []
    r = mrrr([5.0], [])
    assert r.values == [5.0] and r.vectors == [[1.0]]
    r = mrrr([1.0, 1.0], [1.0])  # eigenvalues 0 and 2
    assert r.values == pytest.approx([0.0, 2.0], abs=4 * U) and orthogonality(r) <= 4 * U
    a, b = [3.0, 1.0, 3.0, 2.0], [0.0, 0.0, 0.0]  # diagonal: splits into 1 by 1 blocks
    r = mrrr(a, b)
    assert r.values == [1.0, 2.0, 3.0, 3.0] and orthogonality(r) == 0
    a, b = [2.0] * 6, [1.0, 1.0, 0.0, 1.0, 1.0]  # two equal blocks: double eigenvalues across the split
    r = mrrr(a, b)
    check(a, b, r)
    for scale in (1e-150, 1e150):  # scaling
        a, b = random_tridiagonal(random.Random(3), 12)
        r0 = mrrr(a, b)
        r = mrrr([scale * x for x in a], [scale * x for x in b])
        assert [x / scale for x in r.values] == pytest.approx(r0.values, rel=1e-12, abs=1e-14)
        assert orthogonality(r) <= 100 * 12 * U
    a, b = [-x for x in wilkinson_plus(11)[0]], [1.0] * 10  # negative spectrum
    check(a, b, mrrr(a, b))
    with pytest.raises(ValueError):
        mrrr([1.0, 2.0], [])
