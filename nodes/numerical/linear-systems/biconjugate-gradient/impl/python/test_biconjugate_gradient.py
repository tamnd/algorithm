# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/biconjugate-gradient/. The authors are listed in prov/4SSPDC.jsonl.

import math
import random
from fractions import Fraction as F

from biconjugate_gradient import CSR, bicg

U = 2.0**-53


def fr(m):
    return [[F(t) for t in row] for row in m]


def mv(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def test_one_by_one():
    res = bicg([[F(5)]], [F(10)], tol=0)
    assert res.converged and res.iterations == 1 and res.x == [F(2)]


def test_page_example_exact():
    a = fr([[2, 1, 0], [-1, 2, 1], [0, -1, 2]])
    b = [F(1)] * 3
    tr = []
    res = bicg(a, b, tol=0, trace=tr)
    assert res.converged and res.iterations == 3
    assert res.x == [F(1, 3), F(1, 3), F(2, 3)]
    assert tr[1][0] == [F(-1, 2), 0, F(1, 2)]
    assert tr[2][0] == [F(1, 7), F(-2, 7), F(1, 7)]
    assert res.history == [3, F(1, 2), F(6, 49), 0]


def test_random_exact_termination_and_biorthogonality():
    rng = random.Random(4242)
    breakdowns = 0
    for trial in range(500):
        n = rng.randint(1, 5)
        a = fr([[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)])
        for i in range(n):
            a[i][i] += 6
        b = [F(rng.randint(-4, 4)) for _ in range(n)]
        if all(t == 0 for t in b):
            b[0] = F(1)
        shadow = [F(rng.randint(-4, 4)) for _ in range(n)] if trial % 2 else None
        if shadow is not None and all(t == 0 for t in shadow):
            shadow[0] = F(1)
        tr = []
        res = bicg(a, b, shadow=shadow, tol=0, trace=tr)
        if not res.converged:
            assert res.status in ("rho-breakdown", "pivot-breakdown")
            breakdowns += 1
            continue
        assert res.iterations <= n
        assert mv(a, res.x) == b
        k = len(tr)
        for i in range(k):
            for j in range(k):
                if i != j:
                    assert dot(tr[i][1], tr[j][0]) == 0  # r~_i . r_j
                    assert dot(tr[i][3], mv(a, tr[j][2])) == 0  # p~_i . A p_j
    assert breakdowns < 50


def test_symmetric_shadow_equals_residual():
    # For symmetric A and r~_0 = r_0, r~_k = r_k: BiCG is CG done twice.
    a = fr([[4, 1, 0, 0], [1, 3, 1, 0], [0, 1, 2, 1], [0, 0, 1, 5]])
    b = [F(1), F(2), F(3), F(4)]
    tr = []
    res = bicg(a, b, tol=0, trace=tr)
    assert res.converged and res.iterations == 4
    for r, rt, p, pt in tr:
        assert r == rt and p == pt


def test_pivot_and_rho_breakdown():
    res = bicg(fr([[0, 1], [1, 0]]), [F(1), F(0)], tol=0)
    assert res.status == "pivot-breakdown"
    res = bicg(fr([[1, 0], [0, 1]]), [F(1), F(0)], shadow=[F(0), F(1)], tol=0)
    assert res.status == "rho-breakdown"


def test_singular_reports_failure():
    res = bicg(fr([[1, 0], [0, 0]]), [F(0), F(1)], tol=0)
    assert not res.converged
    res = bicg([[1.0, 0.0], [0.0, 0.0]], [1.0, 1.0])
    assert not res.converged


def convection_diffusion(n, c):
    rows = []
    for i in range(n):
        row = [0.0] * n
        row[i] = 2.0
        if i > 0:
            row[i - 1] = -1.0 - c
        if i < n - 1:
            row[i + 1] = -1.0 + c
        rows.append(row)
    return rows


def test_float_convection_diffusion_and_nonmonotone():
    n = 150
    rows = convection_diffusion(n, 0.3)
    a = CSR.from_dense(rows)
    rng = random.Random(7)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = bicg(a, b, tol=1e-10, maxit=2000)
    assert res.converged
    r = [bi - t for bi, t in zip(b, mv(rows, res.x))]
    assert math.sqrt(dot(r, r)) <= 1e-9 * math.sqrt(dot(b, b))
    h = res.history
    assert any(h[k + 1] > h[k] for k in range(len(h) - 1))  # not monotone


def test_spd_matches_cg_iteration_count_bound():
    n, kappa = 200, 50.0
    d = [1.0 + (kappa - 1.0) * i / (n - 1) for i in range(n)]
    a = CSR(n, list(range(n + 1)), list(range(n)), d)
    rng = random.Random(9)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = bicg(a, b, tol=1e-8, maxit=500)
    q = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    # CG bound in the A-norm turns into a residual bound with sqrt(kappa).
    kbound = math.ceil(math.log(2 * math.sqrt(kappa) / 1e-8) / math.log(1 / q))
    assert res.converged and res.iterations <= kbound


def test_hilbert_backward_error():
    n = 6
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    b = [sum(row) for row in h]
    res = bicg(h, b, tol=1e-13, maxit=300)
    assert res.converged
    r = [bi - t for bi, t in zip(b, mv(h, res.x))]
    hn = max(sum(map(abs, row)) for row in h)
    eta = max(map(abs, r)) / (hn * max(map(abs, res.x)) + max(map(abs, b)))
    assert eta < 1e-12
