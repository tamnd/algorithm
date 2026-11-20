# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pocs-partial-fourier/. The authors are listed in prov/KZJ4DM.jsonl.

import cmath
import math
import random

import pytest

from imgkit import ellipse_phantom, MODIFIED_SHEPP_LOGAN, pixel_centers
from pocs_partial_fourier import (
    partial_mask,
    pocs_1d,
    pocs_2d,
    project_data,
    project_phase,
    reference_phase,
    unitary_dft,
    unitary_idft,
    zero_filled_1d,
)


def dist(a, b):
    return math.sqrt(sum(abs(u - v) ** 2 for u, v in zip(a, b)))


def gauss_solve(a, b):
    """Gaussian elimination with partial pivoting for a small dense real system."""
    n = len(a)
    m = [list(row) + [bi] for row, bi in zip(a, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for j in range(c, n + 1):
                m[r][j] -= f * m[c][j]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
    return x


def brute_least_squares(y, k0, p):
    """The real rho that fits F_u(rho p) to the acquired data best, from the normal equations."""
    n = len(y)
    mask = partial_mask(n, k0)
    rows, rhs = [], []
    for k in range(n):
        if not mask[k]:
            continue
        coef = [cmath.exp(-2j * math.pi * j * k / n) / math.sqrt(n) * p[j] for j in range(n)]
        rows.append([c.real for c in coef])
        rhs.append(y[k].real)
        rows.append([c.imag for c in coef])
        rhs.append(y[k].imag)
    ata = [[sum(r[i] * r[j] for r in rows) for j in range(n)] for i in range(n)]
    atb = [sum(r[i] * b for r, b in zip(rows, rhs)) for i in range(n)]
    rho = gauss_solve(ata, atb)
    return [r * pj for r, pj in zip(rho, p)]


def masked(y, k0):
    m = partial_mask(len(y), k0)
    return [v if a else complex(-7.0, 3.0) for v, a in zip(y, m)]


def test_projections_are_idempotent():
    rng = random.Random(5)
    n, k0 = 16, 3
    y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    p = [cmath.exp(1j * rng.uniform(-3, 3)) for _ in range(n)]
    mask = partial_mask(n, k0)
    a = project_phase(x, p)
    assert dist(project_phase(a, p), a) < 1e-12
    b = project_data(x, y, mask)
    assert dist(project_data(b, y, mask), b) < 1e-12
    # Orthogonality of the residual in the real inner product.
    for _ in range(5):
        r = rng.gauss(0, 1)
        u = [r * pj for pj in p]
        assert abs(sum((ui.conjugate() * (xi - ai)).real for ui, xi, ai in zip(u, x, a))) < 1e-12


def test_constant_phase_signed_real_is_recovered():
    rng = random.Random(6)
    for n, k0 in ((16, 3), (32, 5)):
        rho = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        ph = cmath.exp(0.9j)
        x_true = [ph * r for r in rho]
        y = masked(unitary_dft(x_true), k0)
        out = pocs_1d(y, k0, iters=300)
        assert dist(out, x_true) / dist(x_true, [0] * n) < 1e-6


def test_constant_phase_error_halves_each_iteration():
    rng = random.Random(10)
    n, k0 = 32, 6
    rho = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    ph = cmath.exp(-0.4j)
    x_true = [ph * r for r in rho]
    y = unitary_dft(x_true)
    hist = []
    pocs_1d(y, k0, iters=8, phase=[ph] * n, history=hist)
    d = [dist(zero_filled_1d(y, k0), x_true)] + [dist(h, x_true) for h in hist]
    for a, b in zip(d, d[1:]):
        assert b == pytest.approx(a / 2, rel=1e-9)


def test_matches_brute_force_least_squares_with_given_phase():
    rng = random.Random(7)
    n, k0 = 16, 2
    xs = [-1 + (2 * j + 1) / n for j in range(n)]
    p = [cmath.exp(1j * (0.3 + 1.2 * x - 0.4 * x * x)) for x in xs]
    rho = [rng.uniform(0.0, 2.0) for _ in range(n)]
    y = masked(unitary_dft([r * pj for r, pj in zip(rho, p)]), k0)
    ref = brute_least_squares(y, k0, p)
    out = pocs_1d(y, k0, iters=400, phase=p)
    assert dist(out, ref) < 1e-6
    assert dist(ref, [r * pj for r, pj in zip(rho, p)]) < 1e-8


def test_distance_to_solution_never_grows():
    rng = random.Random(8)
    n, k0 = 32, 4
    xs = [-1 + (2 * j + 1) / n for j in range(n)]
    p = [cmath.exp(1j * (1.0 - 0.8 * x)) for x in xs]
    z = [rng.uniform(0.0, 1.0) * pj for pj in p]
    y = unitary_dft(z)
    hist = []
    pocs_1d(y, k0, iters=60, phase=p, history=hist)
    x0 = zero_filled_1d(y, k0)
    d = [dist(x0, z)] + [dist(h, z) for h in hist]
    for a, b in zip(d, d[1:]):
        assert b <= a + 1e-12
    assert d[-1] < 0.2 * d[0]


def test_inconsistent_data_still_settles():
    rng = random.Random(9)
    n, k0 = 16, 3
    y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    hist = []
    pocs_1d(y, k0, iters=400, history=hist)
    assert dist(hist[-1], hist[-2]) < 1e-8


def test_reference_phase_is_exact_for_constant_phase():
    n, k0 = 16, 3
    ph = cmath.exp(-2.0j)
    rho = [0.0, 0.5, 1.0, 1.0, 2.0, 2.0, 1.0, 0.0, 0.0, 0.3, 0.3, 0.3, 0.0, 0.0, 1.0, 0.2]
    p = reference_phase(unitary_dft([ph * r for r in rho]), k0)
    assert max(abs(v - ph) for v in p) < 1e-12


def test_2d_smooth_phase_beats_zero_filling():
    n, k0 = 16, 3
    rho = ellipse_phantom(n, MODIFIED_SHEPP_LOGAN)
    xs, ys = pixel_centers(n)
    x = [[rho[i][j] * cmath.exp(1j * (0.4 + 0.5 * xs[j] - 0.6 * ys[i] + 0.2 * xs[j] * ys[i])) for j in range(n)] for i in range(n)]
    rows = [unitary_dft(r) for r in x]
    ks = [list(r) for r in zip(*[unitary_dft(list(c)) for c in zip(*rows)])]
    out = pocs_2d(ks, k0, iters=30)
    err_p = math.sqrt(sum((abs(out[i][j]) - rho[i][j]) ** 2 for i in range(n) for j in range(n)))
    zf = [[0.0] * n for _ in range(n)]
    for j in range(n):
        col = [unitary_idft(ks[a])[j] for a in range(n)]
        img = zero_filled_1d(col, k0)
        for i in range(n):
            zf[i][j] = abs(img[i])
    err_z = math.sqrt(sum((zf[i][j] - rho[i][j]) ** 2 for i in range(n) for j in range(n)))
    assert err_p < 0.8 * err_z


def test_bad_arguments():
    with pytest.raises(ValueError):
        pocs_1d([0j] * 8, 3)
