# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/galton-watson-process/. The authors are listed in prov/1ZKR7A.jsonl.

import math
import random
from fractions import Fraction as F

from biostoch import check_mean, mean_var
from galton_watson_process import (
    extinction_probability,
    generation_mean,
    generation_pmf,
    generation_variance,
    offspring_mean,
    offspring_variance,
    pgf,
    poisson_pgf,
    simulate,
    simulate_poisson,
    smallest_root_quadratic,
)

EXAMPLE = [F(1, 4), F(1, 4), F(1, 2)]


def test_poisson_check_values():
    assert abs(extinction_probability(poisson_pgf(1.5)) - 0.417188) < 5e-7
    assert abs(extinction_probability(poisson_pgf(2.0)) - 0.203188) < 5e-7


def test_subcritical_and_critical_go_extinct():
    assert abs(extinction_probability(poisson_pgf(0.9)) - 1.0) < 1e-9
    # At m = 1 the iteration creeps up: P(Z_n > 0) is about 2 / (n sigma^2).
    q = extinction_probability(poisson_pgf(1.0), eps=0.0, max_iter=1000)
    assert abs((1.0 - q) - 2.0 / 1000) < 1e-4


def test_one_child_always_never_dies():
    p = [F(0), F(1)]
    assert offspring_mean(p) == 1
    assert extinction_probability(lambda s: pgf(p, s)) == 0.0
    assert smallest_root_quadratic([F(0), F(1), F(0)]) == 0


def test_example_moments_and_root():
    assert offspring_mean(EXAMPLE) == F(5, 4)
    assert offspring_variance(EXAMPLE) == F(11, 16)
    assert smallest_root_quadratic(EXAMPLE) == F(1, 2)
    assert pgf(EXAMPLE, F(1, 2)) == F(1, 2)
    q = extinction_probability(lambda s: pgf(EXAMPLE, s))
    assert abs(q - 0.5) < 1e-11


def test_generation_pmf_exact():
    assert generation_pmf(EXAMPLE, 1) == EXAMPLE
    assert generation_pmf(EXAMPLE, 2) == [F(11, 32), F(1, 8), F(9, 32), F(1, 8), F(1, 8)]
    m, v = offspring_mean(EXAMPLE), offspring_variance(EXAMPLE)
    for n in range(0, 5):
        pmf = generation_pmf(EXAMPLE, n)
        assert sum(pmf) == 1
        mean = sum(k * x for k, x in enumerate(pmf))
        var = sum(k * k * x for k, x in enumerate(pmf)) - mean * mean
        assert mean == generation_mean(m, n)
        assert var == generation_variance(m, v, n)
    # P(Z_n = 0) = f_n(0), the iterates of the extinction loop.
    q = F(0)
    for n in range(1, 5):
        q = pgf(EXAMPLE, q)
        assert generation_pmf(EXAMPLE, n)[0] == q
    # Two ancestors: the generating function is squared.
    two = generation_pmf(EXAMPLE, 2, z0=2)
    assert two[0] == F(11, 32) ** 2


def test_simulation_matches_exact_law():
    rng = random.Random(20261118)
    n, gens = 3000, 4
    pmf = generation_pmf(EXAMPLE, gens)
    p0 = float(pmf[0])
    finals, dead = [], 0
    for _ in range(n):
        path = simulate(rng, EXAMPLE, gens)
        z = path[-1] if len(path) == gens + 1 else 0
        finals.append(z)
        dead += z == 0
    assert check_mean(dead / n, p0, p0 * (1 - p0), n)
    m, v = offspring_mean(EXAMPLE), offspring_variance(EXAMPLE)
    mean, _ = mean_var(finals)
    assert check_mean(mean, float(generation_mean(m, gens)), float(generation_variance(m, v, gens)), n)


def test_poisson_simulation_extinction_frequency():
    rng = random.Random(7)
    n, gens, m = 4000, 30, 2.0
    exact = 0.0
    for _ in range(gens):
        exact = math.exp(m * (exact - 1.0))  # f_30(0) = P(Z_30 = 0)
    dead = 0
    for _ in range(n):
        path = simulate_poisson(rng, m, gens, cap=400)
        dead += path[-1] == 0
    # A path that passes the cap dies later with probability below q^400, which is negligible.
    assert check_mean(dead / n, exact, exact * (1 - exact), n)
    assert abs(exact - 0.203188) < 1e-6
