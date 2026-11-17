# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smoothed-particle-hydrodynamics/. The authors are listed in prov/9G16QJ.jsonl.

import math
from fractions import Fraction

import pytest

from smoothed_particle_hydrodynamics import (Particles, density, kernel, kernel_gradient, neighbour_pairs,
                                             riemann_exact, shock_tube, sph, step_count, totals)

LEFT, RIGHT = (1.0, 0.0, 1.0), (0.125, 0.0, 0.1)


def boole(f, a, b):
    """Boole's rule, exact for polynomials of degree at most 5."""
    xs = [a + (b - a) * Fraction(k, 4) for k in range(5)]
    return (b - a) / 90 * (7 * f(xs[0]) + 32 * f(xs[1]) + 12 * f(xs[2]) + 32 * f(xs[3]) + 7 * f(xs[4]))


def density_l1_error(res, t):
    """L1 error of the density against the exact Sod solution on [-0.4, 0.4], particle volumes m/rho."""
    return sum(abs(rho - riemann_exact(LEFT, RIGHT, 1.4, x / t)[0]) * m / rho
               for x, rho, m in zip(res.p.x, res.p.rho, res.p.m) if -0.4 < x < 0.4)


def test_kernel_moments_exactly():
    for h in (Fraction(1), Fraction(3, 7)):
        pieces = [(-2 * h, -h), (-h, 0 * h), (0 * h, h), (h, 2 * h)]
        moments = [sum(boole(lambda r: r ** k * kernel(r, h), a, b) for a, b in pieces) for k in range(4)]
        assert moments == [1, 0, h * h / 3, 0]
    assert kernel(Fraction(2), Fraction(1)) == 0 and kernel(Fraction(5, 2), Fraction(1)) == 0


def test_kernel_gradient_matches_finite_differences_and_is_odd():
    for r in (-1.7, -0.6, 0.3, 1.2, 1.9):
        fd = (kernel(r + 1e-6, 0.8) - kernel(r - 1e-6, 0.8)) / 2e-6
        assert abs(kernel_gradient(r, 0.8) - fd) < 1e-6
        assert kernel_gradient(-r, 0.8) == -kernel_gradient(r, 0.8)
    assert kernel_gradient(0.0, 1.0) == 0.0 and kernel_gradient(2.5, 1.0) == 0.0


def test_uniform_lattice_density_is_exact_when_h_equals_the_spacing():
    # sum_k W(k dp, dp) dp = 1 exactly, so an interior particle has density m/dp.
    assert sum(kernel(Fraction(k), Fraction(1)) for k in range(-2, 3)) == 1
    assert sum(kernel(Fraction(k), Fraction(6, 5)) for k in range(-3, 4)) == Fraction(3895, 3888)
    n, dp = 21, 0.05
    p = Particles([i * dp for i in range(n)], [0.0] * n, [dp * 2.0] * n, [1.0] * n, [dp] * n)
    rho = density(p, neighbour_pairs(p.x, p.h))
    assert abs(rho[n // 2] - 2.0) < 1e-12
    assert rho[0] < rho[n // 2]  # the free edge has fewer neighbours


def test_neighbour_pairs_against_brute_force():
    x = [0.0, 0.1, 0.35, 0.36, 0.9, 1.4, 1.41, 2.5]
    h = [0.1, 0.05, 0.2, 0.01, 0.3, 0.02, 0.4, 0.1]
    brute = [(i, j) for i in range(len(x)) for j in range(i + 1, len(x))
             if abs(x[i] - x[j]) < 2 * max(h[i], h[j])]
    assert neighbour_pairs(x, h) == brute


def test_exact_riemann_solution_of_the_sod_problem():
    rho, u, p = riemann_exact(LEFT, RIGHT, 1.4, 0.0)
    assert abs(p - 0.30313) < 1e-5 and abs(u - 0.92745) < 1e-5 and abs(rho - 0.42632) < 1e-5
    assert abs(riemann_exact(LEFT, RIGHT, 1.4, 1.5)[0] - 0.26557) < 1e-5
    assert riemann_exact(LEFT, RIGHT, 1.4, 1.8) == RIGHT and riemann_exact(LEFT, RIGHT, 1.4, -1.5) == LEFT


def test_sod_shock_tube_conservation_and_accuracy():
    errs = []
    for n_left in (80, 160):
        p0 = shock_tube(n_left)
        dt = 0.3 * min(p0.h) / 1.2
        res = sph(p0, 0.2, dt)
        m0, mom0, e0 = totals(p0)
        m1, mom1, e1 = totals(res.p)
        assert m1 == m0
        assert abs(mom1 - mom0) < 1e-14  # pairwise antisymmetric forces
        assert abs(e1 - e0) / e0 < 5e-5  # exact in the semi-discrete system, O(dt) error observed
        errs.append(density_l1_error(res, 0.2))
        if n_left == 160:
            shock_x = 1.7522 * 0.2  # exact shock speed 1.7522
            post = [x for x, rho in zip(res.p.x, res.p.rho) if 0.2 < x < 0.5 and rho > 0.2]
            assert abs(max(post) - shock_x) < 0.04
    assert errs[1] < 0.75 * errs[0] and errs[1] < 0.012


def test_galilean_invariance():
    p0 = shock_tube(40)
    dt = 0.3 * min(p0.h) / 1.2
    a = sph(p0, 0.05, dt)
    shifted = Particles(list(p0.x), [v + 0.3 for v in p0.v], list(p0.m), list(p0.e), list(p0.h))
    b = sph(shifted, 0.05, dt)
    assert max(abs((xb - 0.3 * 0.05) - xa) for xa, xb in zip(a.p.x, b.p.x)) < 1e-9
    assert max(abs(rb - ra) for ra, rb in zip(a.p.rho, b.p.rho)) < 1e-8


def test_pressureless_expanding_particles_move_ballistically():
    n = 11
    x0 = [0.1 * i for i in range(n)]
    p0 = Particles(list(x0), [xi for xi in x0], [0.1] * n, [0.0] * n, [0.12] * n)
    res = sph(p0, 0.5, 0.01, adapt_h=False)
    assert max(abs(x - 1.5 * xi) for x, xi in zip(res.p.x, x0)) < 1e-12
    assert max(abs(v - xi) for v, xi in zip(res.p.v, x0)) < 1e-12


def test_zero_steps_long_step_and_off_grid_final_step():
    p0 = shock_tube(20)
    r = sph(p0, 0.0, 0.01)
    assert r.steps == 0 and r.t == 0.0 and r.p.x == p0.x and r.p.rho is not None
    r = sph(p0, 0.004, 1.0)  # dt larger than the interval: one short step
    assert r.steps == 1 and r.t == 0.004
    r = sph(p0, 0.01, 0.004)  # 0.004, 0.008, then 0.002
    assert r.steps == 3 and abs(r.t - 0.01) < 1e-15
    assert step_count(Fraction(1), Fraction(1, 3)) == 3 and step_count(0.3, 0.1) == 3


def test_courant_factor_below_and_above_the_limit():
    p0 = shock_tube(80)
    e0 = totals(p0)[2]
    good = sph(p0, 0.2, 0.3 * min(p0.h) / 1.2)
    assert abs(totals(good.p)[2] - e0) / e0 < 1e-4 and min(good.p.e) > 0
    bad = sph(p0, 0.2, 1.0 * min(p0.h) / 1.2)
    assert abs(totals(bad.p)[2] - e0) / e0 > 1e3 or min(bad.p.e) < 0


def test_input_validation():
    with pytest.raises(ValueError):
        sph(Particles([], [], [], [], []), 1.0, 0.1)
    with pytest.raises(ValueError):
        sph(Particles([0.0, 1.0], [0.0], [1.0, 1.0], [1.0, 1.0], [1.0, 1.0]), 1.0, 0.1)
    with pytest.raises(ValueError):
        sph(Particles([0.0], [0.0], [0.0], [1.0], [1.0]), 1.0, 0.1)
    with pytest.raises(ValueError):
        step_count(1.0, 0.0)
    with pytest.raises(ValueError):
        step_count(-1.0, 0.1)
