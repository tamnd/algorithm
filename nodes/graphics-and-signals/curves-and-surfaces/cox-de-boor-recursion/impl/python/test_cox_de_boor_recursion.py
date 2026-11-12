# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cox-de-boor-recursion/. The authors are listed in prov/GGMD1V.jsonl.

import random
from fractions import Fraction

import pytest

from cox_de_boor_recursion import all_basis_values, basis_functions, cox_de_boor, find_span


def random_knots(rng, p, n, lo=0, hi=6, max_mult=None):
    """A sorted knot vector of n + p + 2 integers with a nonempty domain."""
    if max_mult is None:
        max_mult = p + 1
    while True:
        knots = sorted(rng.randint(lo, hi) for _ in range(n + p + 2))
        mults = [knots.count(v) for v in set(knots)]
        if max(mults) <= max_mult and knots[p] < knots[n + 1]:
            return knots


def random_param(rng, a, b, den=12):
    """A random Fraction in [a, b) on a grid that also hits the knots."""
    k = rng.randint(0, (b - a) * den - 1)
    return a + Fraction(k, den)


def divided_difference(xs, f):
    """[x_0, ..., x_r] f for distinct xs, by the recursive table."""
    table = [Fraction(f(x)) for x in xs]
    for level in range(1, len(xs)):
        table = [
            (table[i + 1] - table[i]) / (xs[i + level] - xs[i]) for i in range(len(table) - 1)
        ]
    return table[0]


def test_example_of_the_page():
    knots = [0, 0, 0, 1, 2, 3, 3, 3]
    p = 2
    u = Fraction(3, 2)
    mu = find_span(knots, p, u)
    assert mu == 3
    assert basis_functions(knots, p, mu, u) == [Fraction(1, 8), Fraction(3, 4), Fraction(1, 8)]
    assert all_basis_values(knots, p, u) == [0, Fraction(1, 8), Fraction(3, 4), Fraction(1, 8), 0]


def test_find_span_matches_linear_scan():
    rng = random.Random(1)
    for _ in range(500):
        p = rng.randint(0, 4)
        n = rng.randint(p, p + 5)
        knots = random_knots(rng, p, n)
        u = random_param(rng, knots[p], knots[n + 1])
        mu = find_span(knots, p, u)
        assert knots[mu] <= u < knots[mu + 1]
        assert p <= mu <= n
        assert mu == max(i for i in range(len(knots) - 1) if knots[i] <= u)


def test_triangle_matches_the_recursion_as_written():
    rng = random.Random(2)
    for _ in range(600):
        p = rng.randint(0, 4)
        n = rng.randint(p, p + 5)
        knots = random_knots(rng, p, n)
        u = random_param(rng, knots[p], knots[n + 1])
        fast = all_basis_values(knots, p, u)
        slow = [cox_de_boor(knots, i, p, u) for i in range(n + 1)]
        assert fast == slow


def test_partition_of_unity_exact():
    rng = random.Random(3)
    for _ in range(600):
        p = rng.randint(0, 4)
        n = rng.randint(p, p + 5)
        knots = random_knots(rng, p, n)
        u = random_param(rng, knots[p], knots[n + 1])
        values = [cox_de_boor(knots, i, p, u) for i in range(n + 1)]
        assert all(v >= 0 for v in values)
        assert sum(values) == 1
        # The closed last span gives 1 at the right end of the domain too.
        assert sum(all_basis_values(knots, p, knots[n + 1])) == 1


def test_right_end_needs_the_closing_rule():
    # Clamped right end: the half-open recursion gives 0 there for every i.
    knots = [0, 0, 0, 1, 2, 2, 2]
    p, n = 2, 3
    assert all(cox_de_boor(knots, i, p, 2) == 0 for i in range(n + 1))
    assert all_basis_values(knots, p, 2) == [0, 0, 0, 1]
    # A right end with a further span: the half-open rule already gives 1.
    knots = [0, 1, 2, 3, 4, 5, 6]
    p, n = 2, 3
    assert sum(cox_de_boor(knots, i, p, 4) for i in range(n + 1)) == 1


def test_sum_is_below_one_outside_the_domain():
    knots = [0, 1, 2, 3, 4, 5, 6]
    p, n = 2, 3
    u = Fraction(1, 2)
    assert sum(cox_de_boor(knots, i, p, u) for i in range(n + 1)) == Fraction(1, 8)
    u = Fraction(11, 2)
    assert sum(cox_de_boor(knots, i, p, u) for i in range(n + 1)) == Fraction(1, 8)


def test_local_support_and_positivity():
    rng = random.Random(4)
    for _ in range(500):
        p = rng.randint(0, 3)
        n = rng.randint(p, p + 4)
        knots = random_knots(rng, p, n)
        i = rng.randint(0, n)
        u = random_param(rng, knots[0], knots[-1])
        v = cox_de_boor(knots, i, p, u)
        if not knots[i] <= u < knots[i + p + 1]:
            assert v == 0
        elif knots[i] < u:
            assert v > 0


def test_against_divided_differences_of_truncated_powers():
    # For simple knots, N_(i,p)(u) = (u_(i+p+1) - u_i) [u_i, ..., u_(i+p+1)] (x - u)_+^p.
    rng = random.Random(5)
    for _ in range(500):
        p = rng.randint(1, 4)
        n = rng.randint(p, p + 3)
        knots = sorted(rng.sample(range(0, 15), n + p + 2))
        i = rng.randint(0, n)
        u = random_param(rng, knots[0], knots[-1], den=5)
        xs = knots[i : i + p + 2]

        def trunc(x, u=u, p=p):
            return (x - u) ** p if x > u else 0

        ref = (xs[-1] - xs[0]) * divided_difference(xs, trunc)
        assert cox_de_boor(knots, i, p, u) == ref


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        find_span([0, 0, 1, 1], 1, 2)
    with pytest.raises(ValueError):
        basis_functions([0, 0, 1, 1, 1], 1, 2, 1)
