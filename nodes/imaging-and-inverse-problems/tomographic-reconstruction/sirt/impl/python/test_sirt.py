# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sirt/. The authors are listed in prov/KFR7FZ.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
import imgla as la
from sirt import row_col_sums, sirt, weighted_residual

# The 2 x 2 example of the page: two row sums, two column sums, one diagonal.
A = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 0, 1]]
ROWS = [[(j, F(w)) for j, w in enumerate(r) if w] for r in A]
Y = [F(v) for v in (3, 7, 4, 6, 5)]


def _sparse(dense):
    return [[(j, w) for j, w in enumerate(r) if w != 0] for r in dense]


def _scaled(dense):
    """B = R^(1/2) A C^(1/2) as a dense float matrix, and the vectors r and c."""
    r, c = row_col_sums(_sparse(dense), len(dense[0]))
    b = [[float(a) / math.sqrt(r[i] * c[j]) for j, a in enumerate(row)] for i, row in enumerate(dense)]
    return b, r, c


def test_worked_example_exact() -> None:
    seen = []
    sirt(ROWS, 4, Y, lam=F(1), iters=3, callback=lambda k, x: seen.append(x))
    assert seen[0] == [F(2), F(9, 4), F(11, 4), F(3)]
    assert seen[1] == [F(5, 3), F(17, 8), F(23, 8), F(10, 3)]
    assert seen[2] == [F(13, 9), F(33, 16), F(47, 16), F(32, 9)]
    assert [weighted_residual(ROWS, Y, x) for x in seen] == [F(17, 8), F(265, 288), F(4177, 10368)]


def test_consistent_system_converges_to_the_solution() -> None:
    for lam in (0.5, 1.0, 1.9):
        x, _ = sirt(ROWS, 4, [float(v) for v in Y], lam=lam, iters=400)
        assert max(abs(a - b) for a, b in zip(x, (1, 2, 3, 4))) < 1e-9


def test_scaled_matrix_has_norm_one() -> None:
    rng = random.Random(3)
    for dense in (A, [[rng.random() for _ in range(5)] for _ in range(8)]):
        _, s, _ = la.svd(_scaled(dense)[0])
        assert abs(s[0] - 1.0) < 1e-12


def test_limit_is_the_weighted_least_squares_solution() -> None:
    rng = random.Random(4)
    m, n = 8, 5
    dense = [[rng.choice((0.0, rng.random())) + 0.05 for _ in range(n)] for _ in range(m)]
    y = [rng.uniform(0, 3) for _ in range(m)]
    rows = _sparse(dense)
    r, _ = row_col_sums(rows, n)
    # normal equations A^T R A x = A^T R y
    atra = [[sum(dense[i][p] * dense[i][q] / r[i] for i in range(m)) for q in range(n)] for p in range(n)]
    atry = [sum(dense[i][p] * y[i] / r[i] for i in range(m)) for p in range(n)]
    xs = la.solve(atra, atry)
    x, _ = sirt(rows, n, y, lam=1.5, iters=3000)
    assert max(abs(a - b) for a, b in zip(x, xs)) < 1e-8


def test_underdetermined_limit_has_minimal_weighted_norm() -> None:
    rng = random.Random(5)
    m, n = 3, 6
    dense = [[rng.random() for _ in range(n)] for _ in range(m)]
    y = [rng.uniform(1, 2) for _ in range(m)]
    rows = _sparse(dense)
    _, c = row_col_sums(rows, n)
    # x = C A^T (A C A^T)^(-1) y with C = diag(1 / c_j)
    aca = [[sum(dense[p][j] * dense[q][j] / c[j] for j in range(n)) for q in range(m)] for p in range(m)]
    u = la.solve(aca, y)
    xs = [sum(dense[i][j] * u[i] for i in range(m)) / c[j] for j in range(n)]
    x, _ = sirt(rows, n, y, lam=1.0, iters=3000)
    assert max(abs(a - b) for a, b in zip(x, xs)) < 1e-9


def test_filter_factors() -> None:
    rng = random.Random(6)
    m, n, k, lam = 7, 4, 9, 0.8
    dense = [[rng.random() for _ in range(n)] for _ in range(m)]
    y = [rng.uniform(-1, 1) for _ in range(m)]
    b, r, c = _scaled(dense)
    u, s, v = la.svd(b)
    bv = [yi / math.sqrt(ri) for yi, ri in zip(y, r)]
    z = [0.0] * n
    for q in range(n):
        f = 1.0 - (1.0 - lam * s[q] ** 2) ** k
        coef = f * sum(u[i][q] * bv[i] for i in range(m)) / s[q]
        for j in range(n):
            z[j] += coef * v[j][q]
    expect = [zj / math.sqrt(cj) for zj, cj in zip(z, c)]
    x, _ = sirt(_sparse(dense), n, y, lam=lam, iters=k)
    assert max(abs(a - e) for a, e in zip(x, expect)) < 1e-12


def test_weighted_residual_does_not_increase() -> None:
    rng = random.Random(7)
    m, n = 9, 6
    dense = [[rng.random() if rng.random() < 0.7 else 0.0 for _ in range(n)] for _ in range(m)]
    y = [rng.uniform(0, 2) for _ in range(m)]
    rows = _sparse(dense)
    for lam in (0.3, 1.0, 1.95):
        res = [weighted_residual(rows, y, [0.0] * n)]
        sirt(rows, n, y, lam=lam, iters=60, callback=lambda k, x: res.append(weighted_residual(rows, y, x)))
        assert all(b <= a * (1 + 1e-12) + 1e-15 for a, b in zip(res, res[1:]))


def test_relaxation_above_two_diverges() -> None:
    y = [3.0, 7.0, 4.0, 6.0, 5.1]
    x, _ = sirt(ROWS, 4, y, lam=2.2, iters=80)
    assert max(abs(t) for t in x) > 1e3


def test_phantom_reconstruction_and_discrepancy_stop() -> None:
    n, nbins = 16, 23
    angles = [k * math.pi / 12 for k in range(12)]
    rows = ik.parallel_beam_matrix(n, angles, nbins)
    xt = ik.flatten(ik.disk_phantom(n, 0.6))
    yt = ik.sp_matvec(rows, xt)
    nt = math.sqrt(sum(t * t for t in xt))
    errs = []
    sirt(rows, n * n, yt, 1.0, 100, callback=lambda k, x: errs.append(math.dist(x, xt) / nt))
    assert errs[-1] < 0.5 * errs[0]
    rng = random.Random(8)
    sigma = 0.02 * max(yt)
    yd = [t + rng.gauss(0.0, sigma) for t in yt]
    delta = math.sqrt(len(yd)) * sigma
    x, k = sirt(rows, n * n, yd, 1.0, 400, delta=delta)
    e = [a - sum(w * x[j] for j, w in row) for row, a in zip(rows, yd)]
    assert 0 < k < 400
    assert math.sqrt(sum(t * t for t in e)) <= 1.01 * delta


def test_nonnegativity_option() -> None:
    y = [3.0, -1.0, 4.0, 6.0, 0.5]
    x, _ = sirt(ROWS, 4, y, lam=1.0, iters=50, nonneg=True)
    assert min(x) >= 0.0
