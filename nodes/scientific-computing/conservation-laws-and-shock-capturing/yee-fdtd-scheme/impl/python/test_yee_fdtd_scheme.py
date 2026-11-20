# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yee-fdtd-scheme/. The authors are listed in prov/Z3QKRQ.jsonl.

import math
import random
from fractions import Fraction

import pytest

from yee_fdtd_scheme import (cavity_mode, cfl_limit, discrete_omega, div_h, yee_1d_step,
                             yee_step, zeros)


def max_diff(A, B):
    return max(abs(a - b) for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def test_cfl_limit_values():
    assert abs(cfl_limit(0.1, 0.1) - 0.1 / math.sqrt(2)) < 1e-15
    assert abs(cfl_limit(0.1, 0.2) - 1 / math.sqrt(125)) < 1e-15


def test_discrete_cavity_mode_is_an_exact_solution():
    nx, ny, a, b = 12, 8, 1.0, 0.7
    dx, dy = a / nx, b / ny
    dt = 0.9 * cfl_limit(dx, dy)
    m, n = 2, 1
    w = discrete_omega(m * math.pi / a, n * math.pi / b, dx, dy, dt)
    Ez, Hx, Hy = cavity_mode(nx, ny, dx, dy, dt, m, n, w)
    for _ in range(60):
        yee_step(Ez, Hx, Hy, dx, dy, dt)
    E2, X2, Y2 = cavity_mode(nx, ny, dx, dy, dt, m, n, w, t0=60 * dt)
    assert max_diff(Ez, E2) < 1e-12 and max_diff(Hx, X2) < 1e-12 and max_diff(Hy, Y2) < 1e-12


def test_second_order_convergence_to_the_continuous_mode():
    a = b = 1.0
    T = 0.5
    w = math.pi * math.sqrt(2)                       # continuous TM_11 frequency
    errs = []
    for nx in (8, 16, 32):
        dx = a / nx
        steps = 2 * nx                               # dt = T / steps = 0.5 dx / 2
        dt = T / steps
        Ez, Hx, Hy = cavity_mode(nx, nx, dx, dx, dt, 1, 1, w)
        for _ in range(steps):
            yee_step(Ez, Hx, Hy, dx, dx, dt)
        ex = cavity_mode(nx, nx, dx, dx, dt, 1, 1, w, t0=T)[0]
        errs.append(max_diff(Ez, ex))
    r1, r2 = math.log2(errs[0] / errs[1]), math.log2(errs[1] / errs[2])
    assert 1.8 < r1 < 2.2 and 1.8 < r2 < 2.2


def test_discrete_divergence_of_h_is_kept_exactly():
    rng = random.Random(3)
    nx, ny = 6, 5
    dx, dy, dt = Fraction(1, 6), Fraction(1, 5), Fraction(1, 10)
    rnd = (lambda: Fraction(rng.randint(-9, 9), 7))
    Ez = [[rnd() if 0 < i < nx and 0 < j < ny else Fraction(0) for j in range(ny + 1)]
          for i in range(nx + 1)]
    Hx = [[rnd() for _ in range(ny)] for _ in range(nx + 1)]
    Hy = [[rnd() for _ in range(ny + 1)] for _ in range(nx)]
    d0 = div_h(Hx, Hy, dx, dy)
    assert any(v != 0 for row in d0 for v in row)
    for _ in range(5):
        yee_step(Ez, Hx, Hy, dx, dy, dt)
        assert div_h(Hx, Hy, dx, dy) == d0


def test_discrete_energy_is_conserved_exactly():
    rng = random.Random(2)
    nx, ny = 5, 4
    dx, dy, dt = Fraction(1, 5), Fraction(1, 4), Fraction(1, 9)   # below the limit 0.156
    Ez = [[Fraction(rng.randint(-9, 9)) if 0 < i < nx and 0 < j < ny else Fraction(0)
           for j in range(ny + 1)] for i in range(nx + 1)]
    Hx = [[Fraction(rng.randint(-9, 9)) for _ in range(ny)] for _ in range(nx + 1)]
    Hy = [[Fraction(rng.randint(-9, 9)) for _ in range(ny + 1)] for _ in range(nx)]

    def dot(A, B):
        return sum(a * b for ra, rb in zip(A, B) for a, b in zip(ra, rb))

    energies = []
    for _ in range(6):
        E0, X0, Y0 = [r[:] for r in Ez], [r[:] for r in Hx], [r[:] for r in Hy]
        yee_step(Ez, Hx, Hy, dx, dy, dt)
        energies.append(dot(E0, E0) + dot(X0, Hx) + dot(Y0, Hy))
    assert len(set(energies)) == 1


@pytest.mark.parametrize("factor,stable", [(0.99, True), (1.0, True), (1.02, False)])
def test_stability_limit(factor, stable):
    rng = random.Random(1)
    nx = ny = 20
    dx = dy = 1.0 / nx
    dt = factor * cfl_limit(dx, dy)
    Ez = [[rng.uniform(-1, 1) if 0 < i < nx and 0 < j < ny else 0.0 for j in range(ny + 1)]
          for i in range(nx + 1)]
    Hx, Hy = zeros(nx + 1, ny), zeros(nx, ny + 1)
    for _ in range(400):
        yee_step(Ez, Hx, Hy, dx, dy, dt)
    big = max(abs(v) for row in Ez for v in row)
    assert (big < 100) == stable


def test_magic_time_step_in_one_dimension_shifts_exactly():
    m = 32
    f = [max(0, 8 - abs(i - 10)) for i in range(m)]  # integer triangle pulse
    E = list(f)
    H = [-f[(i + 1) % m] for i in range(m)]           # right-moving wave, H at n - 1/2
    for n in range(1, 41):
        yee_1d_step(E, H, 1)
        assert E == [f[(i - n) % m] for i in range(m)]


def test_one_dimensional_scheme_has_numerical_dispersion_below_the_magic_step():
    m, lam, k = 64, 0.5, 8
    w = 2 * math.asin(lam * math.sin(math.pi * k / m))          # omega dt
    E = [math.cos(2 * math.pi * k * i / m) for i in range(m)]
    H = [-math.cos(2 * math.pi * k * (i + 0.5) / m + w / 2) * math.sin(math.pi * k / m)
         * lam / math.sin(w / 2) for i in range(m)]
    for _ in range(100):
        yee_1d_step(E, H, lam)
    ex = [math.cos(2 * math.pi * k * i / m - 100 * w) for i in range(m)]
    assert max(abs(a - b) for a, b in zip(E, ex)) < 1e-9
    assert w < 2 * math.pi * k / m * lam                       # slower than c


def test_rejects_unstable_step_in_mode_frequency():
    with pytest.raises(ValueError):
        discrete_omega(math.pi * 20, math.pi * 20, 0.05, 0.05, 0.04)
