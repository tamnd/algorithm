# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/incompressible-sph/. The authors are listed in prov/H0ZQP6.jsonl.
import math
import random

from incompressible_sph import (
    density,
    divergence,
    gradient,
    isph,
    kernel_2d,
    kernel_derivative_2d,
    kinetic_energy,
    laplacian_matrix,
    lattice,
    momentum,
    neighbour_pairs,
    pressure_solve,
    project,
    taylor_green,
    viscous_term,
)
from scisparse import spmatvec


def setup(n=12, jitter=0.3, seed=1, velocity=taylor_green):
    s = lattice(n, velocity=velocity, jitter=jitter, seed=seed)
    vol = 1.0 / (n * n)
    return s, vol, neighbour_pairs(s.x, s.y, s.box, s.h)


def test_kernel_normalization_and_lattice_density():
    h = 0.3
    steps = 4000
    total = 0.0
    for k in range(steps):  # integral of W over the disc of radius 2h
        r = (k + 0.5) * 2 * h / steps
        total += kernel_2d(r, h) * 2 * math.pi * r * 2 * h / steps
    assert abs(total - 1) < 1e-6
    eps = 1e-6
    for r in (0.1, 0.35, 0.5):
        num = (kernel_2d(r + eps, h) - kernel_2d(r - eps, h)) / (2 * eps)
        assert abs(num - kernel_derivative_2d(r, h)) < 1e-5
    s, vol, pairs = setup(jitter=0.0)
    rho = density(pairs, len(s.x), vol, s.h)
    assert max(abs(r - 0.9997573067) for r in rho) < 1e-9  # lattice sum, h = 1.2 dx


def test_neighbour_pairs_match_brute_force():
    s, vol, pairs = setup(n=10, jitter=0.8, seed=3)
    found = {(i, j) for i, j, *_ in pairs}
    brute = set()
    n = len(s.x)
    for i in range(n):
        for j in range(i + 1, n):
            dx = (s.x[i] - s.x[j] + 0.5) % 1.0 - 0.5
            dy = (s.y[i] - s.y[j] + 0.5) % 1.0 - 0.5
            if dx * dx + dy * dy < 4 * s.h * s.h:
                brute.add((i, j))
    assert found == brute


def test_laplacian_matrix_is_symmetric_with_zero_row_sums():
    s, vol, pairs = setup()
    A = laplacian_matrix(pairs, len(s.x), vol, s.h)
    for i, row in enumerate(A):
        assert abs(sum(row.values())) < 1e-9 * row[i]
        for j, a in row.items():
            assert abs(a - A[j][i]) < 1e-12 * row[i]
            assert (a > 0) if j == i else (a <= 0)
    rng = random.Random(7)
    x = [rng.uniform(-1, 1) for _ in A]
    ax = spmatvec(A, x)
    assert sum(a * b for a, b in zip(x, ax)) > 0  # positive on a nonconstant vector


def test_pressure_solve_is_consistent():
    s, vol, pairs = setup()
    phi, its = pressure_solve(pairs, s.u, s.v, vol, s.h)
    assert its < len(s.x)
    div = divergence(pairs, s.u, s.v, vol)
    mean = sum(div) / len(div)
    A = laplacian_matrix(pairs, len(s.x), vol, s.h)
    res = [a + d - mean for a, d in zip(spmatvec(A, phi), div)]  # -L phi + (D v - mean)
    assert max(abs(r) for r in res) < 1e-9 * max(abs(d) for d in div)
    assert abs(sum(phi)) < 1e-9 * max(abs(p) for p in phi)


def test_pair_terms_conserve_momentum_and_viscosity_dissipates():
    s, vol, pairs = setup()
    rng = random.Random(11)
    phi = [rng.uniform(-1, 1) for _ in s.x]
    gx, gy = gradient(pairs, phi, vol)
    assert abs(sum(gx)) < 1e-10 and abs(sum(gy)) < 1e-10
    u = [rng.uniform(-1, 1) for _ in s.x]
    v = [rng.uniform(-1, 1) for _ in s.x]
    au, av = viscous_term(pairs, u, v, vol, 0.1, s.h)
    assert abs(sum(au)) < 1e-10 and abs(sum(av)) < 1e-10
    assert sum(a * b for a, b in zip(u, au)) + sum(a * b for a, b in zip(v, av)) < 0


def test_uniform_flow_and_gravity_are_kept_exactly():
    s = lattice(12, velocity=lambda x, y: (0.3, -0.2), jitter=0.3, seed=5)
    s1, infos = isph(s, 0.01, 5, nu=0.05)
    assert max(abs(a - 0.3) for a in s1.u) < 1e-14 and max(abs(b + 0.2) for b in s1.v) < 1e-14
    assert all(info.cg_iterations == 0 for info in infos)
    for i in range(len(s.x)):
        assert abs((s1.x[i] - s.x[i] - 0.015 + 0.5) % 1.0 - 0.5) < 1e-12
        assert abs((s1.y[i] - s.y[i] + 0.010 + 0.5) % 1.0 - 0.5) < 1e-12
    s2, _ = isph(lattice(12), 0.01, 4, g=(0.0, -1.0))
    assert max(abs(b + 0.04) for b in s2.v) < 1e-14


def tg_plus_gradient(x, y):
    a, b = taylor_green(x, y)
    k = 2 * math.pi  # add the gradient of sin(kx) sin(ky) / k
    return a + math.cos(k * x) * math.sin(k * y), b + math.sin(k * x) * math.cos(k * y)


def rms_distance_to_tg(s, u, v):
    tot = 0.0
    for i in range(len(s.x)):
        a, b = taylor_green(s.x[i], s.y[i])
        tot += (u[i] - a) ** 2 + (v[i] - b) ** 2
    return math.sqrt(tot / len(s.x))


def test_projection_removes_a_gradient_field():
    errs = []
    for n in (12, 16):
        s, vol, pairs = setup(n=n, jitter=0.0, velocity=tg_plus_gradient)
        u, v, phi, its = project(pairs, s.u, s.v, vol, s.h)
        assert abs(rms_distance_to_tg(s, s.u, s.v) - math.sqrt(0.5)) < 1e-12
        errs.append(rms_distance_to_tg(s, u, v))
    assert abs(errs[0] - 0.1177) < 2e-4 and abs(errs[1] - 0.0683) < 2e-4
    s, vol, pairs = setup(jitter=0.3, velocity=tg_plus_gradient)
    u, v, phi, its = project(pairs, s.u, s.v, vol, s.h)
    assert 0.2 < rms_distance_to_tg(s, u, v) < 0.26  # disorder error, does not shrink with n
    assert abs(sum(u) - sum(s.u)) < 1e-12 and abs(sum(v) - sum(s.v)) < 1e-12


def test_taylor_green_decay_rate():
    ratios = []
    for n in (12, 16):
        s = lattice(n, velocity=taylor_green)
        s1, infos = isph(s, 0.002, 20, nu=0.05)
        rate = -math.log(kinetic_energy(s1) / kinetic_energy(s)) / 0.04
        ratios.append(rate / (16 * math.pi ** 2 * 0.05))
        assert max(i.div_after for i in infos) < 0.6 * max(i.div_before for i in infos)
        mx, my = momentum(s1)
        assert abs(mx) < 1e-14 and abs(my) < 1e-14
        rho = density(neighbour_pairs(s1.x, s1.y, 1.0, s1.h), n * n, 1.0 / (n * n), s1.h)
        assert max(abs(r / 0.9997573067 - 1) for r in rho) < 0.004
    assert abs(ratios[0] - 0.93606) < 2e-4 and abs(ratios[1] - 0.95917) < 2e-4
    assert abs(1 - ratios[1]) < abs(1 - ratios[0])


def test_rejects_bad_input():
    s = lattice(12)
    for dt, steps in ((0.0, 1), (0.01, -1)):
        try:
            isph(s, dt, steps)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        neighbour_pairs([0.1], [0.1], 1.0, 0.2)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
