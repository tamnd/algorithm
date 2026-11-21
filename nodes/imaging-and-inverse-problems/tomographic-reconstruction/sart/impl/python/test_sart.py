# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sart/. The authors are listed in prov/9QD7WM.jsonl.

import math
import random
from fractions import Fraction as F

import imgkit as ik
from sart import sart, view_sums, views_by_angle

# The 2 x 2 example of the page: a view of two rows, a view of two columns, and
# a diagonal view of three rays. The true image is (1, 2, 3, 5).
A = [[1, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [1, 0, 0, 1], [0, 1, 0, 0]]
ROWS = [[(j, F(w)) for j, w in enumerate(r) if w] for r in A]
XT = [1, 2, 3, 5]
Y = [sum(F(a) * b for a, b in zip(r, XT)) for r in A]
VIEWS = [[0, 1], [2, 3], [4, 5, 6]]


def _sparse(dense):
    return [[(j, w) for j, w in enumerate(r) if w != 0] for r in dense]


def _views_with_unit_column_sums(rng, sizes, n):
    """Random nonnegative views whose column sums are all 1, so C_v = I for every view."""
    dense, views = [], []
    for k in sizes:
        block = [[rng.random() + 0.1 for _ in range(n)] for _ in range(k)]
        for j in range(n):
            s = sum(block[i][j] for i in range(k))
            for i in range(k):
                block[i][j] /= s
        views.append(list(range(len(dense), len(dense) + k)))
        dense.extend(block)
    return dense, views


def _solve(m, b):
    """Gaussian elimination with partial pivoting for a small dense system."""
    n = len(b)
    a = [list(row) + [bi] for row, bi in zip(m, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(a[i][c]))
        a[c], a[p] = a[p], a[c]
        for i in range(c + 1, n):
            f = a[i][c] / a[c][c]
            for j in range(c, n + 1):
                a[i][j] -= f * a[c][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def test_worked_example_exact() -> None:
    seen = []
    sart(ROWS, 4, Y, VIEWS, lam=F(1), sweeps=2, order=[0, 2, 1], callback=lambda k, x: seen.append(x))
    assert seen[0] == [F(11, 8), F(19, 8), F(21, 8), F(37, 8)]
    assert seen[1] == [F(1), F(2), F(3), F(5)]
    # inside the first sweep: after the rows and after the diagonal view
    assert sart(ROWS, 4, Y, VIEWS, lam=F(1), sweeps=1, order=[0]) == [F(3, 2), F(3, 2), F(4), F(4)]
    assert sart(ROWS, 4, Y, VIEWS, lam=F(1), sweeps=1, order=[0, 2]) == [F(7, 4), F(2), F(3), F(17, 4)]


def test_relaxed_example_converges() -> None:
    seen = []
    sart(ROWS, 4, Y, VIEWS, lam=F(1, 2), sweeps=1, callback=lambda k, x: seen.append(x))
    assert seen[0] == [F(49, 32), F(61, 32), F(85, 32), F(113, 32)]
    x = sart(ROWS, 4, [float(v) for v in Y], VIEWS, lam=0.5, sweeps=60)
    assert max(abs(a - b) for a, b in zip(x, XT)) < 1e-12


def test_one_view_with_all_rays_is_one_sirt_step() -> None:
    rng = random.Random(1)
    m, n, lam = 7, 5, 0.7
    dense = [[rng.random() if rng.random() < 0.7 else 0.0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        dense[i][i % n] += 0.5
    y = [rng.uniform(0, 2) for _ in range(m)]
    x0 = [rng.uniform(0, 1) for _ in range(n)]
    r = [sum(row) for row in dense]
    c = [sum(dense[i][j] for i in range(m)) for j in range(n)]
    e = [(yi - sum(a * b for a, b in zip(row, x0))) / ri for row, yi, ri in zip(dense, y, r)]
    expect = [x0[j] + lam * sum(dense[i][j] * e[i] for i in range(m)) / c[j] for j in range(n)]
    x = sart(_sparse(dense), n, y, [list(range(m))], lam=lam, sweeps=1, x0=x0)
    assert max(abs(a - b) for a, b in zip(x, expect)) < 1e-14


def test_consistent_limit_is_the_nearest_solution() -> None:
    rng = random.Random(2)
    n = 6
    dense, views = _views_with_unit_column_sums(rng, (2, 2), n)
    m = len(dense)
    xt = [rng.uniform(0, 2) for _ in range(n)]
    y = [sum(a * b for a, b in zip(row, xt)) for row in dense]
    x0 = [rng.uniform(-1, 1) for _ in range(n)]
    # C_v = I, so the limit is the projection x0 + A^T (A A^T)^(-1) (y - A x0) of x0
    # onto {x : A x = y}. The rows of each view add up to the ones vector, so the
    # last row is a combination of the others and is left out of the formula.
    keep = dense[: m - 1]
    res = [yi - sum(a * b for a, b in zip(row, x0)) for row, yi in zip(keep, y)]
    aat = [[sum(p * q for p, q in zip(a, b)) for b in keep] for a in keep]
    u = _solve(aat, res)
    expect = [x0[j] + sum(row[j] * ui for row, ui in zip(keep, u)) for j in range(n)]
    for lam, order in ((1.0, None), (1.6, [1, 0]), (0.4, None)):
        x = sart(_sparse(dense), n, y, views, lam=lam, sweeps=3000, x0=x0, order=order)
        assert max(abs(a - b) for a, b in zip(x, expect)) < 1e-9


def test_inconsistent_data_sweeps_converge_to_a_lambda_dependent_limit() -> None:
    rng = random.Random(3)
    n = 4
    dense, views = _views_with_unit_column_sums(rng, (3, 3, 3), n)
    m = len(dense)
    y = [rng.uniform(0, 3) for _ in range(m)]
    rows = _sparse(dense)
    r = [sum(row) for row in dense]
    # the R-weighted least squares solution
    atra = [[sum(dense[i][p] * dense[i][q] / r[i] for i in range(m)) for q in range(n)] for p in range(n)]
    atry = [sum(dense[i][p] * y[i] / r[i] for i in range(m)) for p in range(n)]
    xls = _solve(atra, atry)
    gaps = []
    for lam in (1.0, 0.25):
        ends = []
        sart(rows, n, y, views, lam=lam, sweeps=3000, callback=lambda k, x: ends.append(x))
        assert max(abs(a - b) for a, b in zip(ends[-1], ends[-2])) < 1e-12
        gaps.append(max(abs(a - b) for a, b in zip(ends[-1], xls)))
    # measured: 0.172 for lam = 1 and 0.054 for lam = 1/4
    assert gaps[0] > 0.1
    assert gaps[1] < 0.5 * gaps[0]


def test_helper_matrix_has_equal_column_sums_in_every_view() -> None:
    n, nbins, na = 16, 23, 12
    rows = ik.parallel_beam_matrix(n, [k * math.pi / na for k in range(na)], nbins)
    _, cs = view_sums(rows, views_by_angle(na, nbins))
    ref = (2.0 / n) ** 2 / (2.0 * math.sqrt(2.0) / nbins)
    for c in cs:
        assert len(c) == n * n
        assert all(abs(v - ref) < 1e-12 for v in c.values())


def test_phantom_sart_beats_sirt_per_pass() -> None:
    n, nbins, na = 16, 23, 12
    rows = ik.parallel_beam_matrix(n, [k * math.pi / na for k in range(na)], nbins)
    xt = ik.flatten(ik.disk_phantom(n, 0.6))
    y = ik.sp_matvec(rows, xt)
    nt = math.sqrt(sum(t * t for t in xt))
    errs = []
    sart(rows, n * n, y, views_by_angle(na, nbins), lam=1.0, sweeps=10, callback=lambda k, x: errs.append(math.dist(x, xt) / nt))
    # SIRT with the same matrix, 10 passes through the data
    r = [sum(w for _, w in row) for row in rows]
    c = ik.sp_rmatvec(rows, [1.0] * len(rows), n * n)
    x = [0.0] * (n * n)
    for _ in range(10):
        e = [(yi - s) / ri if ri > 0 else 0.0 for yi, s, ri in zip(y, ik.sp_matvec(rows, x), r)]
        x = [xj + g / cj for xj, g, cj in zip(x, ik.sp_rmatvec(rows, e, n * n), c)]
    sirt_err = math.dist(x, xt) / nt
    assert errs[0] < 0.4
    assert errs[-1] < 0.12
    assert errs[-1] < 0.5 * sirt_err


def test_nonnegativity_option() -> None:
    y = [3.0, -1.0, 4.0, 6.0, -2.0, 0.5, 2.0]
    x = sart(_sparse(A), 4, y, VIEWS, lam=1.0, sweeps=30, nonneg=True)
    assert min(x) >= 0.0
