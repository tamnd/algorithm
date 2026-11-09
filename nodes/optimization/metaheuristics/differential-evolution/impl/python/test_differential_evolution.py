# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-evolution/. The authors are listed in prov/R0J5VG.jsonl.

import math
import random

from differential_evolution import (
    binomial_crossover,
    differential_evolution,
    random_population,
    rastrigin,
    repair,
    sphere,
)


def test_repair_keeps_points_in_the_box() -> None:
    lo, hi = [-1.0, 0.0], [1.0, 2.0]
    assert repair([-3.0, 5.0], [0.5, 1.0], lo, hi) == [-0.25, 1.5]
    assert repair([0.2, 0.3], [0.5, 1.0], lo, hi) == [0.2, 0.3]


def test_population_stays_in_the_box_and_values_never_increase() -> None:
    n = 4
    lo, hi = [-2.0] * n, [3.0] * n
    rng = random.Random(0)
    pop = random_population(lo, hi, 12, rng)
    trace = []
    # F = 1.5 sends many mutants out of the box, so the repair is used.
    differential_evolution(rastrigin, pop, 1.5, 0.9, 60, rng, (lo, hi), trace)
    prev = [rastrigin(x) for x in pop]
    for population, values in trace:
        assert all(a <= xj <= b for x in population for xj, a, b in zip(x, lo, hi))
        assert values == [rastrigin(x) for x in population]
        assert all(v <= p for v, p in zip(values, prev))
        prev = values


def test_binomial_crossover() -> None:
    rng = random.Random(1)
    x, v = [0.0] * 6, [1.0] * 6
    for _ in range(1000):
        assert sum(binomial_crossover(x, v, 0.0, rng)) == 1.0  # only jrand
        assert sum(binomial_crossover(x, v, 1.0, rng)) == 6.0
    trials = 100000
    mean = sum(sum(binomial_crossover(x, v, 0.3, rng)) for _ in range(trials)) / trials
    assert abs(mean - (1 + 5 * 0.3)) < 0.02


def test_invariant_under_increasing_transformation() -> None:
    lo, hi = [-3.0] * 3, [3.0] * 3
    pop = random_population(lo, hi, 10, random.Random(2))
    a = differential_evolution(sphere, pop, 0.5, 0.9, 30, random.Random(3), (lo, hi))
    b = differential_evolution(lambda x: math.exp(sphere(x)), pop, 0.5, 0.9, 30, random.Random(3), (lo, hi))
    assert a[0] == b[0]


def test_cr_one_is_invariant_under_linear_maps() -> None:
    # With CR = 1 and no bounds, the run on f(A^-1 x) from A P is A times the run on f from P.
    a = [[2.0, 1.0], [-0.5, 1.5]]
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    inv = [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]
    mul = lambda m, x: [m[0][0] * x[0] + m[0][1] * x[1], m[1][0] * x[0] + m[1][1] * x[1]]
    f = lambda x: (x[0] - 1) ** 2 + 10 * (x[1] + 0.5) ** 2
    g = lambda y: f(mul(inv, y))
    pop = random_population([-2.0, -2.0], [2.0, 2.0], 8, random.Random(4))
    ta, tb = [], []
    differential_evolution(f, pop, 0.7, 1.0, 25, random.Random(5), None, ta)
    differential_evolution(g, [mul(a, x) for x in pop], 0.7, 1.0, 25, random.Random(5), None, tb)
    for (pa, _), (pb, _) in zip(ta, tb):
        for x, y in zip(pa, pb):
            assert all(math.isclose(s, t, abs_tol=1e-9) for s, t in zip(mul(a, x), y))


def test_fixed_seed_reaches_optimum() -> None:
    n = 5
    lo, hi = [-5.0] * n, [5.0] * n
    rng = random.Random(0)
    x, fx = differential_evolution(sphere, random_population(lo, hi, 30, rng), 0.5, 0.9, 400, rng, (lo, hi))
    assert fx < 1e-10
    n = 3
    lo, hi = [-5.12] * n, [5.12] * n
    rng = random.Random(0)
    x, fx = differential_evolution(rastrigin, random_population(lo, hi, 30, rng), 0.5, 0.1, 400, rng, (lo, hi))
    assert fx < 1e-8
