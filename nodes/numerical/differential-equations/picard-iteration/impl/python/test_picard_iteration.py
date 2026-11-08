# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/picard-iteration/. The authors are listed in prov/56X5PF.jsonl.

import math
from fractions import Fraction

import pytest

from picard_iteration import picard_iteration, picard_polynomial, pmul


def test_exponential_iterates_are_taylor_polynomials():
    ys = picard_polynomial(lambda s, y: y, 1, 6)
    for k, p in enumerate(ys):
        assert p == [Fraction(1, math.factorial(j)) for j in range(k + 1)]


def test_continuous_error_bound_for_exponential():
    # |e - y^(k)(1)| <= e / (k+1)!  (M = e, L = 1, t - t0 = 1)
    ys = picard_polynomial(lambda s, y: y, 1, 8)
    for k, p in enumerate(ys):
        err = math.e - float(sum(p))
        assert 0 < err <= math.e / math.factorial(k + 1)


def test_riccati_iterates_agree_to_degree_k():
    # y' = y^2, y(0) = 1, solution 1/(1 - s) = 1 + s + s^2 + ...
    ys = picard_polynomial(lambda s, y: pmul(y, y), 1, 4)
    for k, p in enumerate(ys):
        assert p[:k + 1] == [Fraction(1)] * (k + 1)
    assert ys[3] == [1, 1, 1, 1, Fraction(2, 3), Fraction(1, 3), Fraction(1, 9), Fraction(1, 63)]


def test_fixed_point_is_trapezoidal_rule():
    for m in (16, 64):
        r = picard_iteration(lambda t, y: y, 0.0, 1.0, 1.0, m=m)
        trap = ((1 + 0.5 / m) / (1 - 0.5 / m)) ** m
        assert r.converged and abs(r.y - trap) < 1e-12


def test_observed_order_two_and_iteration_count():
    f = lambda t, y: -2 * t * y * y          # solution 1/(1 + t^2)
    errs, its = [], []
    for m in (10, 20, 40, 80):
        r = picard_iteration(f, 0.0, 1.0, 1.0, m=m)
        errs.append(abs(r.y - 0.5))
        its.append(r.iterations[0])
    orders = [math.log2(errs[i] / errs[i + 1]) for i in range(3)]
    assert all(abs(p - 2) < 0.02 for p in orders)
    assert max(its) <= 20


def test_two_exact_iterations_with_fractions():
    r = picard_iteration(lambda t, y: y, Fraction(0), Fraction(1), Fraction(1), m=4,
                         max_iter=2, keep_grid=True)
    assert not r.converged
    for t, y in zip(r.grid, r.values):
        assert y == 1 + t + t * t / 2       # trapezoid is exact on linear integrands


def test_windows_cut_the_work():
    evals = []
    for w in (1, 2, 5, 10, 20):
        r = picard_iteration(lambda t, y: -y, 0.0, 1.0, 10.0, m=400 // w, windows=w)
        assert r.converged and abs(r.y - math.exp(-10)) < 3e-8
        evals.append(r.f_evals)
    assert evals == sorted(evals, reverse=True)
    assert evals[0] > 3 * evals[-1]


def test_stiff_problem_needs_short_windows():
    f = lambda t, y: -1000 * y
    r = picard_iteration(f, 0.0, 1.0, 1.0, m=10)
    assert not r.converged                  # L * dt / 2 = 50 > 1: diverges
    r = picard_iteration(f, 0.0, 1.0, 1.0, m=10, windows=100)
    assert r.converged and abs(r.y) < 1e-10  # L * dt / 2 = 1/2


def test_vector_harmonic_oscillator():
    r = picard_iteration(lambda t, y: [y[1], -y[0]], 0.0, [1.0, 0.0], 1.0, m=64)
    assert r.converged
    assert abs(r.y[0] - math.cos(1)) < 2e-5 and abs(r.y[1] + math.sin(1)) < 2e-5


def test_edge_cases():
    r = picard_iteration(lambda t, y: y, 0.5, 2.0, 0.5)
    assert r.y == 2.0 and r.f_evals == 0 and r.iterations == [] and r.converged
    r = picard_iteration(lambda t, y: y, 0.0, 1.0, 1.0, m=1)   # one trapezoid
    assert abs(r.y - 3.0) < 1e-10           # (1 + 1/2)/(1 - 1/2)
    r = picard_iteration(lambda t, y: y, 0.0, 1.0, 1.0, m=8, keep_grid=True)
    assert len(r.grid) == 9 and r.grid[-1] == 1.0
    with pytest.raises(ValueError):
        picard_iteration(lambda t, y: y, 0.0, 1.0, 1.0, m=0)
    with pytest.raises(ValueError):
        picard_iteration(lambda t, y: y, 1.0, 1.0, 0.0)
    with pytest.raises(ValueError):
        picard_polynomial(lambda s, y: y, 1, -1)
