# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-mesh-method/. The authors are listed in prov/Y8XKSA.jsonl.
import cmath
import math
import random

import pytest

from particle_mesh_method import (
    deposit,
    fft,
    fft2,
    field_from_potential,
    pm_forces,
    pm_run,
    solve_poisson,
)


def dft(a, inverse=False):
    n = len(a)
    sign = 1 if inverse else -1
    out = [sum(a[j] * cmath.exp(sign * 2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]
    return [x / n for x in out] if inverse else out


def laplacian(phi, lx, ly):
    nx, ny = len(phi), len(phi[0])
    dx, dy = lx / nx, ly / ny
    out = [[0.0] * ny for _ in range(nx)]
    for i in range(nx):
        for j in range(ny):
            out[i][j] = (phi[(i + 1) % nx][j] - 2 * phi[i][j] + phi[i - 1][j]) / dx**2
            if ny > 1:
                out[i][j] += (phi[i][(j + 1) % ny] - 2 * phi[i][j] + phi[i][j - 1]) / dy**2
    return out


def test_fft_matches_dft():
    rng = random.Random(1)
    for n in (1, 2, 4, 8, 16, 32):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        assert fft(a) == pytest.approx(dft(a), abs=1e-9)
        assert fft(a, inverse=True) == pytest.approx(dft(a, inverse=True), abs=1e-9)
        assert fft(fft(a), inverse=True) == pytest.approx(a, abs=1e-12)
    with pytest.raises(ValueError):
        fft([1, 2, 3])


def test_fft2_matches_double_dft():
    rng = random.Random(2)
    g = [[complex(rng.uniform(-1, 1)) for _ in range(4)] for _ in range(8)]
    got = fft2(g)
    for kx in range(8):
        for ky in range(4):
            want = sum(
                g[i][j] * cmath.exp(-2j * math.pi * (i * kx / 8 + j * ky / 4)) for i in range(8) for j in range(4)
            )
            assert got[kx][ky] == pytest.approx(want, abs=1e-9)


def test_poisson_solution_satisfies_discrete_equation():
    rng = random.Random(3)
    for nx, ny, lx, ly in ((8, 8, 1.0, 1.0), (16, 4, 2.0, 0.5), (32, 1, 3.0, 1.0)):
        s = rng.uniform(-3, 3)
        rho = [[rng.uniform(0, 2) for _ in range(ny)] for _ in range(nx)]
        phi = solve_poisson(rho, lx, ly, s)
        mean = sum(map(sum, rho)) / (nx * ny)
        lap = laplacian(phi, lx, ly)
        for i in range(nx):
            for j in range(ny):
                assert lap[i][j] == pytest.approx(s * (rho[i][j] - mean), abs=1e-9)
        assert sum(map(sum, phi)) == pytest.approx(0, abs=1e-9)


def test_page_example():
    f = pm_forces([[2.0, 0.0], [5.0, 0.0]], [1.0, 1.0], 8, 1, 8.0, 1.0, 1.0)
    assert f[0][0] == pytest.approx(0.125, abs=1e-12)
    assert f[1][0] == pytest.approx(-0.125, abs=1e-12)
    phi = solve_poisson(deposit([[2.0, 0.0], [5.0, 0.0]], [1, 1], 8, 1, 8.0, 1.0), 8.0, 1.0, 1.0)
    want = [0.375, 0.125, -0.375, -0.125, -0.125, -0.375, 0.125, 0.375]
    assert [p[0] for p in phi] == pytest.approx(want, abs=1e-12)


def test_1d_sawtooth_force_is_exact_on_nodes():
    # The periodic 1D force of mass m2 on mass m1 at offset d = x2 - x1 in (0, L) is s m1 m2 (1/2 - d/L).
    rng = random.Random(4)
    m, length = 16, 16.0
    for _ in range(40):
        a = rng.randrange(m)
        d = rng.randint(2, m - 2)
        b = (a + d) % m
        m1, m2 = rng.uniform(0.5, 2), rng.uniform(0.5, 2)
        s = rng.uniform(0.5, 2)
        f = pm_forces([[float(a), 0.0], [float(b), 0.0]], [m1, m2], m, 1, length, 1.0, s)
        want = s * m1 * m2 * (0.5 - d / length)
        assert f[0][0] == pytest.approx(want, abs=1e-9)
        assert f[1][0] == pytest.approx(-want, abs=1e-9)


def test_zero_self_force_and_zero_total_force():
    rng = random.Random(5)
    for _ in range(20):
        nx, ny = rng.choice([4, 8, 16]), rng.choice([1, 4, 8])
        lx, ly = rng.uniform(1, 3), rng.uniform(1, 3)
        p = [[rng.uniform(0, lx), rng.uniform(0, ly)]]
        f = pm_forces(p, [1.0], nx, ny, lx, ly, 1.0)
        assert f[0] == pytest.approx([0.0, 0.0], abs=1e-12)
        n = rng.randint(2, 40)
        ps = [[rng.uniform(0, lx), rng.uniform(0, ly)] for _ in range(n)]
        ws = [rng.uniform(-1, 2) for _ in range(n)]
        f = pm_forces(ps, ws, nx, ny, lx, ly, rng.uniform(-2, 2))
        assert sum(v[0] for v in f) == pytest.approx(0, abs=1e-12)
        assert sum(v[1] for v in f) == pytest.approx(0, abs=1e-12)


def test_grid_field_is_second_order():
    # rho = 1 + 0.5 cos(k x) gives g = -0.5 s sin(k x) / k in the continuum.
    length, s = 2.0, 3.0
    k = 2 * math.pi / length
    errs = []
    for m in (16, 32, 64):
        dx = length / m
        rho = [[1 + 0.5 * math.cos(k * i * dx)] for i in range(m)]
        gx, _ = field_from_potential(solve_poisson(rho, length, 1.0, s), length, 1.0)
        errs.append(max(abs(gx[i][0] + 0.5 * s * math.sin(k * i * dx) / k) for i in range(m)))
    for e1, e2 in zip(errs, errs[1:]):
        assert 3.8 < e1 / e2 < 4.2


def test_run_conserves_momentum_and_is_reversible():
    rng = random.Random(6)
    nx = ny = 8
    lx = ly = 1.0
    n = 30
    ps = [[rng.uniform(0, lx), rng.uniform(0, ly)] for _ in range(n)]
    vs = [[rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1)] for _ in range(n)]
    ms = [rng.uniform(0.5, 1.5) for _ in range(n)]
    p0 = [sum(m * v[c] for m, v in zip(ms, vs)) for c in range(2)]
    x, v = pm_run(ps, vs, ms, ms, nx, ny, lx, ly, 0.5, 0.01, 40)
    p1 = [sum(m * u[c] for m, u in zip(ms, v)) for c in range(2)]
    assert p1 == pytest.approx(p0, abs=1e-12)
    xb, vb = pm_run(x, [[-a, -b] for a, b in v], ms, ms, nx, ny, lx, ly, 0.5, 0.01, 40)
    for a, b in zip(xb, ps):
        dxp = (a[0] - b[0] + 0.5 * lx) % lx - 0.5 * lx
        dyp = (a[1] - b[1] + 0.5 * ly) % ly - 0.5 * ly
        assert abs(dxp) < 1e-9 and abs(dyp) < 1e-9
    for a, b in zip(vb, vs):
        assert [-a[0], -a[1]] == pytest.approx(b, abs=1e-9)


def test_two_body_attraction_in_2d_points_along_the_separation():
    # Two equal masses on a large grid attract along the line that joins them.
    f = pm_forces([[6.0, 8.0], [10.0, 8.0]], [1.0, 1.0], 16, 16, 16.0, 16.0, 1.0)
    assert f[0][0] > 0 and f[1][0] < 0
    assert f[0][1] == pytest.approx(0, abs=1e-12)
    assert f[0][0] == pytest.approx(-f[1][0], abs=1e-12)
