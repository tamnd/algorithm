# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-walk-power-grid-analysis/. The authors are listed in prov/4F39NW.jsonl.

import random
from fractions import Fraction

import pytest

from pgrid import Grid, mesh, random_mesh, solve
from random_walk_power_grid_analysis import WalkTables, estimate_drop, first_step_identity


def chain():
    """Pad (20 S) at node 0, wires of 10 S, loads 0.2 A at node 1 and 0.3 A at node 2."""
    g = Grid(3)
    g.add_wire(0, 1, Fraction(10))
    g.add_wire(1, 2, Fraction(10))
    g.gpad[0] = Fraction(20)
    g.cur = [Fraction(0), Fraction(2, 10), Fraction(3, 10)]
    return g


def test_chain_exact_drops():
    g = chain()
    x = solve(g.matrix(), g.cur)
    assert x == [Fraction(25, 1000), Fraction(75, 1000), Fraction(105, 1000)]
    assert first_step_identity(g, x) == [0, 0, 0]


def test_first_step_identity_holds_exactly_on_random_meshes():
    rng = random.Random(11)
    for _ in range(5):
        g = random_mesh(4, 4, rng)
        x = solve(g.matrix(), g.cur)
        assert all(v == 0 for v in first_step_identity(g, x))
        # and fails for a vector that is not the solution
        y = list(x)
        y[0] += 1
        assert any(v != 0 for v in first_step_identity(g, y))


def test_drops_are_nonnegative_and_the_inverse_is_nonnegative():
    rng = random.Random(12)
    g = random_mesh(4, 3, rng)
    a = g.matrix()
    for j in range(g.n):
        e = [Fraction(0)] * g.n
        e[j] = Fraction(1)
        assert all(v >= 0 for v in solve(a, e))


def test_estimate_on_chain_within_five_standard_errors():
    g = chain()
    rng = random.Random(1)
    for k, exact in [(0, 0.025), (1, 0.075), (2, 0.105)]:
        mean, se, _ = estimate_drop(g, k, 4000, rng)
        assert abs(mean - exact) <= 5 * se + 1e-12


def test_estimate_on_random_meshes():
    rng = random.Random(2)
    for _ in range(3):
        g = random_mesh(4, 4, rng, n_pads=3)
        x = solve(g.matrix(), g.cur)
        for k in rng.sample(range(g.n), 3):
            mean, se, _ = estimate_drop(g, k, 3000, rng)
            assert abs(mean - float(x[k])) <= 5 * se + 1e-12


def test_mean_walk_length():
    # Expected visits y solve G y = D 1, and steps = visits - 1.
    rng = random.Random(3)
    g = random_mesh(3, 3, rng, n_pads=2)
    d = [g.degree(m) for m in range(g.n)]
    y = solve(g.matrix(), d)
    k = 4
    _, _, steps = estimate_drop(g, k, 6000, rng)
    assert abs(steps - float(y[k] - 1)) < 0.08 * float(y[k])


def test_same_seed_same_answer():
    g = chain()
    a = estimate_drop(g, 2, 500, random.Random(7))
    b = estimate_drop(g, 2, 500, random.Random(7))
    assert a == b


def test_grid_without_pad_is_rejected():
    g = Grid(2)
    g.add_wire(0, 1, Fraction(1))
    with pytest.raises(ValueError):
        WalkTables(g)
