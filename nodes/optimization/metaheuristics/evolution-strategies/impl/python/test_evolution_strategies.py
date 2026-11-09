# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/evolution-strategies/. The authors are listed in prov/ZYGTRG.jsonl.

import math
import random

from evolution_strategies import ellipsoid, one_plus_one_es, sphere


def test_elitist_and_step_size_rule() -> None:
    n = 5
    d = math.sqrt(n + 1)
    for seed in range(10):
        trace = []
        x, fx, sigma = one_plus_one_es(sphere, [1.0] * n, 0.5, 300, random.Random(seed), trace)
        values = [t[0] for t in trace] + [fx]
        assert all(b <= a for a, b in zip(values, values[1:]))
        assert fx == sphere(x)
        s = sum(1 for t in trace if t[2])
        expected = math.log(0.5) + (s - (300 - s) / 4) / d
        assert math.isclose(math.log(sigma), expected, abs_tol=1e-9)
        # Each step multiplies sigma by exp(1/D) or exp(-1/(4D)).
        sigmas = [t[1] for t in trace] + [sigma]
        for (_, s0, ok), s1 in zip(trace, sigmas[1:]):
            assert math.isclose(math.log(s1 / s0), 1 / d if ok else -1 / (4 * d), rel_tol=1e-9)


def test_invariant_under_increasing_transformation() -> None:
    # The method only compares values, so exp(f) and 3 f + 7 give the same points.
    for g in (lambda x: math.exp(sphere(x)), lambda x: 3 * sphere(x) + 7):
        a = one_plus_one_es(sphere, [0.4, -0.3, 0.2], 0.3, 200, random.Random(1))
        b = one_plus_one_es(g, [0.4, -0.3, 0.2], 0.3, 200, random.Random(1))
        assert a[0] == b[0] and a[2] == b[2]


def test_invariant_under_translation() -> None:
    c = [5.0, -2.0, 1.0]
    shifted = lambda x: sphere([xi - ci for xi, ci in zip(x, c)])
    a = one_plus_one_es(sphere, [0.4, -0.3, 0.2], 0.3, 200, random.Random(2))
    b = one_plus_one_es(shifted, [0.4 + 5.0, -0.3 - 2.0, 0.2 + 1.0], 0.3, 200, random.Random(2))
    assert all(math.isclose(ai + ci, bi, abs_tol=1e-9) for ai, ci, bi in zip(a[0], c, b[0]))


def test_fixed_seed_reaches_optimum() -> None:
    n = 10
    x, fx, _ = one_plus_one_es(sphere, [1 / math.sqrt(n)] * n, 1.0, 4000, random.Random(0))
    assert fx < 1e-16


def test_ellipsoid_values_never_increase() -> None:
    trace = []
    x, fx, _ = one_plus_one_es(ellipsoid, [1.0] * 4, 1.0, 2000, random.Random(3), trace)
    assert fx == ellipsoid(x) and fx < ellipsoid([1.0] * 4)
    assert all(b[0] <= a[0] for a, b in zip(trace, trace[1:]))
