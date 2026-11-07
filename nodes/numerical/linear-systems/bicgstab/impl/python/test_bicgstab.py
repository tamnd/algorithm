# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bicgstab/. The authors are listed in prov/ED04G2.jsonl.

import math
import random
from fractions import Fraction as F

from bicgstab import CSR, bicgstab


def fr(m):
    return [[F(t) for t in row] for row in m]


def mv(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def dot(u, v):
    return sum(p * q for p, q in zip(u, v))


def bicg_residuals(a, b):
    """Exact BiCG residuals r_0, r_1, ... with shadow r_0 (reference)."""
    n = len(b)
    at = [[a[i][j] for i in range(n)] for j in range(n)]
    r = list(b)
    rt, p, pt = list(r), list(r), list(r)
    rho = dot(rt, r)
    out = [list(r)]
    for _ in range(n):
        if all(t == 0 for t in r) or rho == 0:
            break
        q, qt = mv(a, p), mv(at, pt)
        sigma = dot(pt, q)
        if sigma == 0:
            break
        al = rho / sigma
        r = [s - al * t for s, t in zip(r, q)]
        rt = [s - al * t for s, t in zip(rt, qt)]
        rn = dot(rt, r)
        be = rn / rho
        rho = rn
        p = [s + be * t for s, t in zip(r, p)]
        pt = [s + be * t for s, t in zip(rt, pt)]
        out.append(list(r))
    return out


def test_one_by_one():
    res = bicgstab([[F(4)]], [F(2)], tol=0)
    assert res.converged and res.x == [F(1, 2)] and res.iterations == 1


def test_page_example_exact():
    a = fr([[2, 1, 0], [-1, 2, 1], [0, -1, 2]])
    b = [F(1)] * 3
    res = bicgstab(a, b, tol=0)
    assert res.converged and res.iterations == 3
    assert res.x == [F(1, 3), F(1, 3), F(2, 3)]
    assert res.omegas == [F(1, 3), F(7, 20)]
    assert res.history == [3, F(1, 6), F(1, 105), 0]


def test_random_exact_product_form():
    # r_k(BiCGSTAB) = psi_k(A) r_k(BiCG), psi_k(t) = prod (1 - omega_i t).
    rng = random.Random(1107)
    fails = 0
    for trial in range(500):
        n = rng.randint(1, 5)
        a = fr([[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)])
        for i in range(n):
            a[i][i] += 7
        b = [F(rng.randint(-4, 4)) for _ in range(n)]
        if all(t == 0 for t in b):
            b[0] = F(1)
        res = bicgstab(a, b, tol=0)
        if not res.converged:
            fails += 1
            continue
        assert res.iterations <= n
        assert mv(a, res.x) == b
        ref = bicg_residuals(a, b)
        # check the product form for every completed full step
        for k, om in enumerate(res.omegas, start=1):
            if k >= len(ref):
                break
            v = ref[k]
            for w in res.omegas[:k]:
                av = mv(a, v)
                v = [s - w * t for s, t in zip(v, av)]
            assert dot(v, v) == res.history[k]
    assert fails < 50


def test_omega_breakdown():
    # symmetric indefinite: s = (4, 0) and t = A s = (0, 8) are orthogonal
    a = fr([[0, 2], [2, 1]])
    res = bicgstab(a, [F(0), F(-2)], tol=0)
    assert res.status == "omega-breakdown" and not res.converged
    assert res.x == [F(0), F(-2)]


def test_singular_reports_failure():
    res = bicgstab(fr([[1, 0], [0, 0]]), [F(0), F(1)], tol=0)
    assert res.status == "pivot-breakdown"
    res = bicgstab([[1.0, 0.0], [0.0, 0.0]], [1.0, 1.0], maxit=100)
    assert not res.converged


def test_convection_diffusion_true_residual():
    n = 200
    rows = []
    for i in range(n):
        row = [0.0] * n
        row[i] = 2.0
        if i > 0:
            row[i - 1] = -1.4
        if i < n - 1:
            row[i + 1] = -0.6
        rows.append(row)
    a = CSR.from_dense(rows)
    rng = random.Random(77)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = bicgstab(a, b, tol=1e-10, maxit=2000)
    assert res.converged
    r = [bi - t for bi, t in zip(b, mv(rows, res.x))]
    assert math.sqrt(dot(r, r)) <= 1e-8 * math.sqrt(dot(b, b))


def test_spd_iteration_count():
    n, kappa = 200, 50.0
    d = [1.0 + (kappa - 1.0) * i / (n - 1) for i in range(n)]
    a = CSR(n, list(range(n + 1)), list(range(n)), d)
    rng = random.Random(5)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = bicgstab(a, b, tol=1e-8, maxit=500)
    q = (math.sqrt(kappa) - 1) / (math.sqrt(kappa) + 1)
    kbound = math.ceil(math.log(2 * math.sqrt(kappa) / 1e-8) / math.log(1 / q))
    # observed, not a theorem: about the CG count, at two matvecs per step
    assert res.converged and res.iterations <= kbound


def test_imaginary_spectrum_stagnates():
    # Eigenvalues 0.01 +- i: omega minimizes ||s - omega A s|| along a nearly
    # orthogonal direction, so steps make tiny progress.
    blocks = 20
    n = 2 * blocks
    rows = [[0.0] * n for _ in range(n)]
    for k in range(blocks):
        i = 2 * k
        rows[i][i] = rows[i + 1][i + 1] = 0.01
        rows[i][i + 1] = 1.0 + 0.05 * k
        rows[i + 1][i] = -(1.0 + 0.05 * k)
    rng = random.Random(2)
    b = [rng.uniform(-1, 1) for _ in range(n)]
    res = bicgstab(rows, b, tol=1e-8, maxit=200)
    assert all(abs(w) < 0.05 for w in res.omegas)
    assert not res.converged  # 400 matvecs; GMRES needs 30 (see the page)


def test_hilbert_backward_error():
    n = 6
    h = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    b = [sum(row) for row in h]
    res = bicgstab(h, b, tol=1e-13, maxit=300)
    r = [bi - t for bi, t in zip(b, mv(h, res.x))]
    hn = max(sum(map(abs, row)) for row in h)
    eta = max(map(abs, r)) / (hn * max(map(abs, res.x)) + max(map(abs, b)))
    assert eta < 1e-12
