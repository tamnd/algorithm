# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proper-generalized-decomposition/. The authors are listed in prov/TWTF98.jsonl.
import math
import random

import pytest

from proper_generalized_decomposition import (
    Laplace2D,
    dot,
    norm2,
    pgd,
    residual_terms,
    times_left,
    times_right,
    to_dense,
    tri_apply,
    tri_solve,
)


def dense(terms, nx, ny):
    return to_dense(terms, nx, ny)


def apply_a(op, v):
    """Kx V + V Ky for a dense nx by ny matrix V."""
    nx, ny = op.nx, op.ny
    out = [[0.0] * ny for _ in range(nx)]
    for j in range(ny):
        col = op.kx_apply([v[i][j] for i in range(nx)])
        for i in range(nx):
            out[i][j] += col[i]
    for i in range(nx):
        row = op.ky_apply(v[i])
        for j in range(ny):
            out[i][j] += row[j]
    return out


def inner(p, q):
    return sum(a * b for ra, rb in zip(p, q) for a, b in zip(ra, rb))


def energy_functional(op, fd, v):
    """J(V) = 1/2 <V, A V> - <F, V>."""
    return 0.5 * inner(v, apply_a(op, v)) - inner(fd, v)


def sine_solve(op, fd):
    """Reference solution of Kx U + U Ky = F by the discrete sine transform in each direction."""
    nx, ny = op.nx, op.ny
    sx = [[math.sqrt(2.0 / (nx + 1)) * math.sin((i + 1) * (k + 1) * math.pi / (nx + 1)) for k in range(nx)] for i in range(nx)]
    sy = [[math.sqrt(2.0 / (ny + 1)) * math.sin((i + 1) * (k + 1) * math.pi / (ny + 1)) for k in range(ny)] for i in range(ny)]
    lx = [op.kx[0] + 2 * op.kx[1] * math.cos((k + 1) * math.pi / (nx + 1)) for k in range(nx)]
    ly = [op.ky[0] + 2 * op.ky[1] * math.cos((k + 1) * math.pi / (ny + 1)) for k in range(ny)]
    t = [[sum(sx[i][k] * fd[i][j] for i in range(nx)) for j in range(ny)] for k in range(nx)]
    g = [[sum(t[k][j] * sy[j][l] for j in range(ny)) / (lx[k] + ly[l]) for l in range(ny)] for k in range(nx)]
    t2 = [[sum(sx[i][k] * g[k][l] for k in range(nx)) for l in range(ny)] for i in range(nx)]
    return [[sum(t2[i][l] * sy[j][l] for l in range(ny)) for j in range(ny)] for i in range(nx)]


def gauss_solve(m, b):
    n = len(b)
    a = [list(row) + [bi] for row, bi in zip(m, b)]
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(a[i][k]))
        a[k], a[piv] = a[piv], a[k]
        for i in range(k + 1, n):
            c = a[i][k] / a[k][k]
            for j in range(k, n + 1):
                a[i][j] -= c * a[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (a[i][n] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def jacobi_eigenvalues(a, sweeps=60):
    n = len(a)
    a = [list(r) for r in a]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= 1e-30 * sum(a[i][i] ** 2 for i in range(n)):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    a[k][p], a[k][q] = c * a[k][p] - s * a[k][q], s * a[k][p] + c * a[k][q]
                for k in range(n):
                    a[p][k], a[q][k] = c * a[p][k] - s * a[q][k], s * a[p][k] + c * a[q][k]
    return sorted((a[i][i] for i in range(n)), reverse=True)


def rel_errors(op, u, modes):
    """Relative energy and Frobenius errors of the first m modes, m = 1..len(modes)."""
    eu, fu = inner(u, apply_a(op, u)), inner(u, u)
    out = []
    for m in range(1, len(modes) + 1):
        um = dense(modes[:m], op.nx, op.ny)
        e = [[p - q for p, q in zip(ra, rb)] for ra, rb in zip(u, um)]
        out.append((math.sqrt(max(inner(e, apply_a(op, e)), 0.0) / eu), math.sqrt(inner(e, e) / fu)))
    return out


def random_rhs(rng, nx, ny, s):
    return [([rng.gauss(0, 1) for _ in range(nx)], [rng.gauss(0, 1) for _ in range(ny)]) for _ in range(s)]


def test_tridiagonal_solve():
    rng = random.Random(1)
    rhs = [rng.gauss(0, 1) for _ in range(9)]
    z = tri_solve(5.0, -2.0, rhs)
    assert tri_apply(5.0, -2.0, z) == pytest.approx(rhs, abs=1e-12)
    assert tri_solve(3.0, -1.0, [6.0]) == [2.0]


def test_sine_reference_against_the_kronecker_system():
    rng = random.Random(2)
    op = Laplace2D(4, 3, 1.0, 0.3)
    nx, ny = 4, 3
    fd = [[rng.gauss(0, 1) for _ in range(ny)] for _ in range(nx)]
    cols = []
    for c in range(nx * ny):
        e = [[1.0 if i * ny + j == c else 0.0 for j in range(ny)] for i in range(nx)]
        ae = apply_a(op, e)
        cols.append([ae[i][j] for i in range(nx) for j in range(ny)])
    mat = [[cols[c][r] for c in range(nx * ny)] for r in range(nx * ny)]
    x = gauss_solve(mat, [fd[i][j] for i in range(nx) for j in range(ny)])
    u = sine_solve(op, fd)
    assert [u[i][j] for i in range(nx) for j in range(ny)] == pytest.approx(x, rel=1e-10, abs=1e-12)


def test_separated_operations_against_dense():
    rng = random.Random(3)
    op = Laplace2D(6, 5, 1.0, 2.0)
    f = random_rhs(rng, 6, 5, 2)
    modes = random_rhs(rng, 6, 5, 3)
    terms = residual_terms(op, f, modes)
    rd = dense(terms, 6, 5)
    ad = apply_a(op, dense(modes, 6, 5))
    fd = dense(f, 6, 5)
    assert max(abs(rd[i][j] - fd[i][j] + ad[i][j]) for i in range(6) for j in range(5)) < 1e-9
    assert norm2(terms) == pytest.approx(inner(rd, rd), rel=1e-10)
    x, y = [rng.gauss(0, 1) for _ in range(6)], [rng.gauss(0, 1) for _ in range(5)]
    assert times_right(terms, y) == pytest.approx([dot(row, y) for row in rd], rel=1e-10, abs=1e-9)
    assert times_left(terms, x) == pytest.approx([sum(x[i] * rd[i][j] for i in range(6)) for j in range(5)], rel=1e-10, abs=1e-9)


def test_one_mode_for_a_product_of_eigenvectors():
    nx, ny = 10, 7
    op = Laplace2D(nx, ny, 1.0, 1.0)
    sx = [math.sin(2 * (i + 1) * math.pi / (nx + 1)) for i in range(nx)]
    sy = [math.sin(3 * (j + 1) * math.pi / (ny + 1)) for j in range(ny)]
    modes, res, _ = pgd(op, [(sx, sy)], 5, tol=1e-9)
    assert len(modes) == 1 and res[-1] <= 1e-9
    u = sine_solve(op, dense([(sx, sy)], nx, ny))
    um = dense(modes, nx, ny)
    assert max(abs(a - b) for ra, rb in zip(u, um) for a, b in zip(ra, rb)) < 1e-12


def test_half_steps_minimize_and_the_energy_error_does_not_grow():
    rng = random.Random(4)
    nx, ny = 8, 6
    op = Laplace2D(nx, ny, 1.0, 2.0)
    f = random_rhs(rng, nx, ny, 3)
    fd = dense(f, nx, ny)
    u = sine_solve(op, fd)
    modes, _, _ = pgd(op, f, 30, tol=1e-14)
    errs = [e for e, _ in rel_errors(op, u, modes)]
    assert all(b <= a * (1 + 1e-12) for a, b in zip([1.0] + errs, errs))
    assert errs[9] == pytest.approx(1.074e-3, rel=1e-2) and errs[-1] < 1e-5
    # the energy identity |U - V|_A^2 = 2 (J(V) - J(U))
    v = dense(modes[:3], nx, ny)
    e = [[p - q for p, q in zip(ra, rb)] for ra, rb in zip(u, v)]
    assert inner(e, apply_a(op, e)) == pytest.approx(2 * (energy_functional(op, fd, v) - energy_functional(op, fd, u)), rel=1e-8)
    # the X step is the exact minimizer for its Y: random changes of X raise J
    from proper_generalized_decomposition import solve_x

    base = modes[:2]
    terms = residual_terms(op, f, base)
    y = [rng.gauss(0, 1) for _ in range(ny)]
    x = solve_x(op, terms, y)
    j0 = energy_functional(op, fd, dense(base + [(x, y)], nx, ny))
    assert j0 < energy_functional(op, fd, dense(base, nx, ny))
    for _ in range(10):
        dx = [t + 1e-3 * rng.gauss(0, 1) for t in x]
        assert energy_functional(op, fd, dense(base + [(dx, y)], nx, ny)) > j0


def test_example_numbers():
    n = 30
    op = Laplace2D(n, n, 1.0, 1.0)
    f = [([1.0] * n, [1.0] * n)]
    u = sine_solve(op, dense(f, n, n))
    modes, res, _ = pgd(op, f, 8, tol=1e-12)
    errs = rel_errors(op, u, modes)
    assert [e for e, _ in errs[:3]] == pytest.approx([3.199e-2, 3.482e-3, 8.037e-4], rel=1e-3)
    assert errs[5][0] == pytest.approx(2.052e-5, rel=1e-2) and errs[7][0] == pytest.approx(5.166e-7, rel=1e-2)
    assert [fr for _, fr in errs[:3]] == pytest.approx([9.193e-3, 7.118e-4, 3.793e-4], rel=1e-3)
    assert res[1] == pytest.approx(0.1226, rel=1e-3)
    # the SVD of the exact solution is better in the Frobenius norm at the same rank
    lam = jacobi_eigenvalues([[sum(u[k][i] * u[k][j] for k in range(n)) for j in range(n)] for i in range(n)])
    tail = [math.sqrt(sum(lam[m:]) / sum(lam)) for m in (1, 2, 3)]
    assert tail == pytest.approx([9.146e-3, 5.040e-4, 4.624e-5], rel=1e-2)
    assert all(t <= fr for t, (_, fr) in zip(tail, errs))
