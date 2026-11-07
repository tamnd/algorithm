# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-iteration/. The authors are listed in prov/3W6N6C.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from chebyshev_iteration import CSR, chebyshev


def cheb(k, t):
    """T_k(t) by the three-term recurrence (exact for Fractions)."""
    a, b = 1, t
    if k == 0:
        return a
    for _ in range(k - 1):
        a, b = b, 2 * t * b - a
    return b


def mv(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def test_page_example_exact():
    a = [[F(2), F(-1)], [F(-1), F(2)]]
    b = [F(1), F(1)]
    tr = []
    res = chebyshev(a, b, F(1), F(3), tol=0, maxit=4, trace=tr)
    errs = [1 - xk[0] for xk in tr]
    assert errs == [1, F(1, 2), F(1, 7), F(1, 26), F(1, 97)]
    assert all(xk[0] == xk[1] for xk in tr)
    assert not res.converged and res.status == "maxit"


def test_one_by_one_and_equal_bounds():
    res = chebyshev([[F(4)]], [F(2)], F(4), F(4), tol=0)
    assert res.converged and res.iterations == 1 and res.x == [F(1, 2)]
    # A = c I with exact bounds: one step
    res = chebyshev([[F(3), 0], [0, F(3)]], [F(1), F(2)], F(3), F(3), tol=0)
    assert res.converged and res.iterations == 1


def test_random_diagonal_error_is_chebyshev_polynomial():
    rng = random.Random(31337)
    for trial in range(500):
        n = rng.randint(1, 4)
        lam = [F(rng.randint(1, 40), rng.randint(1, 4)) for _ in range(n)]
        lo = min(lam) - F(rng.randint(0, 2), 8)
        if lo <= 0:
            lo = min(lam)
        hi = max(lam) + F(rng.randint(0, 3), 4)
        if lo == hi:
            hi = lo + 1
        a = [[lam[i] if i == j else F(0) for j in range(n)] for i in range(n)]
        xt = [F(rng.randint(-5, 5)) for _ in range(n)]
        b = mv(a, xt)
        k = rng.randint(1, 6)
        tr = []
        chebyshev(a, b, lo, hi, tol=0, maxit=k, trace=tr)
        theta, delta = (hi + lo) / 2, (hi - lo) / 2
        for j, xj in enumerate(tr):
            tk = cheb(j, theta / delta)
            for i in range(n):
                expected = cheb(j, (theta - lam[i]) / delta) / tk * xt[i]
                assert xt[i] - xj[i] == expected
            # the error bound 1 / T_k(sigma) in the 2-norm
            e2 = sum((xt[i] - xj[i]) ** 2 for i in range(n))
            e02 = sum(t * t for t in xt)
            assert e2 * tk * tk <= e02


def laplacian(n):
    ptr, ind, data = [0], [], []
    for i in range(n):
        for j, v in ((i - 1, -1.0), (i, 2.0), (i + 1, -1.0)):
            if 0 <= j < n:
                ind.append(j)
                data.append(v)
        ptr.append(len(ind))
    return CSR(n, ptr, ind, data)


def test_iteration_count_matches_theory():
    n = 60
    a = laplacian(n)
    lmin = 2 - 2 * math.cos(math.pi / (n + 1))
    lmax = 2 - 2 * math.cos(n * math.pi / (n + 1))
    rng = random.Random(4)
    xt = [rng.uniform(-1, 1) for _ in range(n)]
    b = a.matvec(xt)
    eps = 1e-8
    res = chebyshev(a, b, lmin, lmax, tol=eps, maxit=5000)
    kappa = lmax / lmin
    q = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    # residual bound ||r_k|| <= 2 q^k ||r_0|| (symmetric A, exact bounds)
    kbound = math.ceil(math.log(2 * math.sqrt(sum(t * t for t in b)) / (eps * math.sqrt(sum(t * t for t in b)))) / math.log(1 / q))
    assert res.converged
    assert res.iterations <= kbound
    assert res.iterations >= kbound // 3  # the bound is not wildly pessimistic here
    assert res.iterations <= math.ceil(math.sqrt(kappa) / 2 * math.log(2 / eps))


def test_underestimated_lmax_diverges():
    n = 40
    a = laplacian(n)
    b = [1.0] * n
    res = chebyshev(a, b, 0.01, 2.0, tol=1e-10, maxit=3000)
    assert not res.converged and res.status == "diverged"


def test_underestimated_lmin_slower_but_ok():
    n = 40
    a = laplacian(n)
    b = [1.0] * n
    lmin = 2 - 2 * math.cos(math.pi / (n + 1))
    good = chebyshev(a, b, lmin, 4.0, tol=1e-8, maxit=5000)
    loose = chebyshev(a, b, lmin / 10, 4.0, tol=1e-8, maxit=5000)
    assert good.converged and loose.converged
    assert loose.iterations > good.iterations


def test_invalid_bounds_and_singular():
    with pytest.raises(ValueError):
        chebyshev([[1.0]], [1.0], 0.0, 1.0)
    with pytest.raises(ValueError):
        chebyshev([[1.0]], [1.0], -1.0, 1.0)
    # singular A with a bound lmin > 0 that is wrong: no convergence
    res = chebyshev([[1.0, 0.0], [0.0, 0.0]], [1.0, 1.0], 0.5, 1.0, maxit=300)
    assert not res.converged


def test_hilbert_with_gershgorin_bound():
    n = 4
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    xt = [1.0] * n
    b = mv(h, xt)
    lmax = max(sum(row) for row in h)  # Gershgorin / row sums
    lmin = 9.6e-5  # below lambda_min(H_4), which is about 9.670e-5
    res = chebyshev(h, b, lmin, lmax, tol=1e-12, maxit=5000, check=10)
    assert res.converged
    r = [bi - t for bi, t in zip(b, mv(h, res.x))]
    assert max(map(abs, r)) <= 1e-11 * max(map(abs, b))
