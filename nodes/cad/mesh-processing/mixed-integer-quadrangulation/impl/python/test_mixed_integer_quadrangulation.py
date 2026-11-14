# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-integer-quadrangulation/. The authors are listed in prov/SKTZEV.jsonl.

import random
from fractions import Fraction

from mixed_integer_quadrangulation import (
    brute_force,
    direct_rounding,
    energy,
    greedy_rounding,
    minimize,
    toy_grid,
)


def random_instance(rng):
    ncol = rng.randint(3, 5)
    ny = rng.randint(1, 2)
    xs = [Fraction(0)]
    for _ in range(ncol - 1):
        xs.append(xs[-1] + Fraction(rng.randint(2, 9), 4))
    h = Fraction(rng.randint(3, 9), 5)
    features = set(rng.sample(range(1, ncol), rng.randint(1, min(3, ncol - 1))))
    bend = {}
    for i in range(ncol):
        for j in range(ny + 1):
            for e in (((i, j), (i + 1, j)), ((i, j), (i, j + 1))):
                bend[e] = Fraction(rng.randint(-3, 3), 10)
    return toy_grid(xs, ny, h, features, bend)


def test_example_of_the_page() -> None:
    xs = [Fraction(0), Fraction(2), Fraction(7, 2)]
    n, terms, integer, pinned = toy_grid(xs, 1, Fraction(9, 5), {0, 1, 2})
    assert n == 3 and integer == [0, 1, 2] and pinned == {0: 0}
    relaxed = minimize(n, terms, pinned)
    assert relaxed == [0, Fraction(18, 5), Fraction(63, 10)]
    assert energy(terms, relaxed) == 0
    g, order = greedy_rounding(n, terms, integer, pinned)
    assert order == [2, 1]
    assert g == [0, 3, 6]
    assert energy(terms, g) == Fraction(9, 10)
    d = direct_rounding(n, terms, integer, pinned)
    assert d == [0, 4, 6]
    assert energy(terms, d) == Fraction(13, 10)
    b = brute_force(n, terms, integer, pinned)
    assert b == [0, 4, 7]
    assert energy(terms, b) == Fraction(1, 2)


def test_rounding_bounds_on_random_grids() -> None:
    rng = random.Random(2009)
    greedy_worse = greedy_better_than_direct = 0
    for _ in range(40):
        n, terms, integer, pinned = random_instance(rng)
        relaxed = minimize(n, terms, pinned)
        g, order = greedy_rounding(n, terms, integer, pinned)
        d = direct_rounding(n, terms, integer, pinned)
        b = brute_force(n, terms, integer, pinned)
        e0, eg, ed, eb = (energy(terms, x) for x in (relaxed, g, d, b))
        assert sorted(order) == [k for k in integer if k not in pinned]
        for x in (g, d, b):
            assert all(x[k].denominator == 1 for k in integer)
            assert all(x[k] == v for k, v in pinned.items())
        assert e0 <= eb <= eg and eb <= ed
        greedy_worse += eg > eb
        greedy_better_than_direct += eg < ed
    # Measured: both effects occur on these seeds; neither is a theorem.
    assert greedy_worse > 0 and greedy_better_than_direct > 0


def test_relaxed_solution_is_a_minimum() -> None:
    rng = random.Random(7)
    for _ in range(10):
        n, terms, integer, pinned = random_instance(rng)
        x = minimize(n, terms, pinned)
        e = energy(terms, x)
        for k in range(n):
            if k in pinned:
                continue
            for d in (Fraction(1, 7), Fraction(-1, 7)):
                y = list(x)
                y[k] += d
                assert energy(terms, y) > e


def test_integer_targets_give_zero_energy() -> None:
    xs = [Fraction(k) for k in range(5)]
    n, terms, integer, pinned = toy_grid(xs, 2, Fraction(2), {1, 2, 3, 4})
    g, _ = greedy_rounding(n, terms, integer, pinned)
    assert energy(terms, g) == 0
    assert [g[k] for k in integer] == [2, 4, 6, 8]
