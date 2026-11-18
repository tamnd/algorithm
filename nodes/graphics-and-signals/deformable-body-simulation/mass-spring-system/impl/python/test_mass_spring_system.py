# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mass-spring-system/. The authors are listed in prov/4B6KHP.jsonl.

"""Tests of the mass-spring system: forces, momentum, the step limit and lattice anisotropy."""

import math
import random

from anim import num_grad
import mass_spring_system as ms


def perturbed_grid(rng, nx=4, ny=3, amount=0.15):
    x, springs = ms.grid(nx, ny, 1.0, 100.0, 50.0, 20.0)
    x = [(p[0] + rng.uniform(-amount, amount), p[1] + rng.uniform(-amount, amount)) for p in x]
    return x, springs


def test_force_is_minus_gradient():
    rng = random.Random(1)
    x, springs = perturbed_grid(rng)
    n = len(x)
    zero_v = [(0.0, 0.0)] * n
    f = ms.forces(x, zero_v, [1.0] * n, springs)

    def energy(flat):
        pts = [(flat[2 * i], flat[2 * i + 1]) for i in range(n)]
        return ms.spring_energy(pts, springs)

    flat = [c for p in x for c in p]
    g = num_grad(energy, flat, 1e-6)
    scale = max(abs(c) for c in g)
    for i in range(n):
        for d in range(2):
            assert abs(f[i][d] + g[2 * i + d]) <= 1e-6 * scale


def test_zero_force_at_rest_and_after_rigid_motion():
    x, springs = ms.grid(4, 4, 0.5, 80.0, 40.0, 10.0)
    n = len(x)
    zv = [(0.0, 0.0)] * n
    for th, t in ((0.0, (0.0, 0.0)), (0.7, (1.0, -2.0)), (2.5, (0.3, 0.4))):
        c, s = math.cos(th), math.sin(th)
        y = [(c * p[0] - s * p[1] + t[0], s * p[0] + c * p[1] + t[1]) for p in x]
        f = ms.forces(y, zv, [1.0] * n, springs)
        assert max(abs(v) for fi in f for v in fi) < 1e-10


def test_momentum_conserved_with_damping():
    rng = random.Random(4)
    x, springs = perturbed_grid(rng, 5, 4, 0.2)
    n = len(x)
    mass = [rng.uniform(0.5, 2.0) for _ in range(n)]
    inv = [1.0 / m for m in mass]
    v = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    p0 = ms.momentum(x, v, mass)
    for _ in range(300):
        x, v = ms.step(x, v, inv, mass, springs, 0.005, damping=0.5)
    p1 = ms.momentum(x, v, mass)
    ref = max(1.0, max(abs(c) for c in p0))
    for a, b in zip(p0, p1):
        assert abs(a - b) <= 1e-10 * ref


def oscillator(dt, steps, k=100.0, m=1.0):
    """One mass on a spring of rest length 1 to a fixed point; return the largest |stretch|."""
    x = [(0.0, 0.0), (1.1, 0.0)]
    v = [(0.0, 0.0), (0.0, 0.0)]
    springs = [(0, 1, 1.0, k)]
    big = 0.0
    for _ in range(steps):
        x, v = ms.step(x, v, [0.0, 1.0 / m], [1.0, m], springs, dt)
        big = max(big, abs(x[1][0] - 1.0))
        if big > 1e6:
            break
    return big


def test_step_limit_check_value():
    assert abs(ms.step_limit(100.0, 1.0) - 0.2) < 1e-15
    assert oscillator(0.19, 2000) < 1.0
    assert oscillator(0.21, 2000) > 1e3


def test_energy_band_symplectic_euler():
    # k = m = 1, stretch 1, dt = 0.1: E stays in [0.5 / 1.05, 0.5 / 0.95].
    # The rest length is 10, so the spring never passes through zero length.
    x = [(0.0, 0.0), (11.0, 0.0)]
    v = [(0.0, 0.0), (0.0, 0.0)]
    springs = [(0, 1, 10.0, 1.0)]
    lo, hi = 1.0, 0.0
    for _ in range(10000):
        x, v = ms.step(x, v, [0.0, 1.0], [1.0, 1.0], springs, 0.1)
        e = ms.spring_energy(x, springs) + ms.kinetic_energy(v, [0.0, 1.0])
        lo, hi = min(lo, e), max(hi, e)
    assert 0.476190 <= lo and hi <= 0.526316
    assert lo < 0.4763 and hi > 0.5262


def lattice_energy(k, k_d, strain, angle, cells=6):
    """Energy per cell of a periodic patch under the affine map x -> x + strain (d . x) d."""
    x, springs = ms.grid(cells + 2, cells + 2, 1.0, k, k_d, 0.0)
    c, s = math.cos(angle), math.sin(angle)
    y = [(p[0] + strain * (c * p[0] + s * p[1]) * c, p[1] + strain * (c * p[0] + s * p[1]) * s) for p in x]
    # count only the springs whose lower left end is inside the inner cells x cells block,
    # so that each lattice cell holds one horizontal, one vertical and two diagonal springs
    e = 0.0
    n = cells + 2
    for a, b, rest, kk in springs:
        ia, ja = a % n, a // n
        ib, jb = b % n, b // n
        lo_i, lo_j = min(ia, ib), min(ja, jb)
        if 0 <= lo_i < cells and 0 <= lo_j < cells:
            e += 0.5 * kk * (math.dist(y[a], y[b]) - rest) ** 2
    return e / cells ** 2


def test_lattice_anisotropy():
    eps = 1e-4
    for k_d in (0.0, 25.0, 50.0):
        for ang in (0.0, 0.3, math.pi / 4):
            got = lattice_energy(100.0, k_d, eps, ang)
            want = ms.uniaxial_energy_per_cell(100.0, k_d, 1.0, eps, ang)
            assert abs(got - want) <= 1e-3 * want
    # structural springs only: half as stiff at 45 degrees as along an axis
    r = ms.uniaxial_energy_per_cell(100.0, 0.0, 1.0, 1.0, math.pi / 4) / ms.uniaxial_energy_per_cell(100.0, 0.0, 1.0, 1.0, 0.0)
    assert abs(r - 0.5) < 1e-12
    # k_d = k / 2 gives the same uniaxial stiffness in every direction
    vals = [ms.uniaxial_energy_per_cell(100.0, 50.0, 1.0, 1.0, a) for a in (0.0, 0.2, 0.5, math.pi / 4)]
    assert max(vals) - min(vals) < 1e-9
