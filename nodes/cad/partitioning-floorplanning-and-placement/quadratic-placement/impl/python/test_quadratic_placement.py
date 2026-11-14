# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-placement/. The authors are listed in prov/01NV03.jsonl.

import random
from fractions import Fraction

import pytest

from quadratic_placement import (
    build_system,
    conjugate_gradient,
    hpwl,
    quadratic_placement,
    quadratic_wirelength,
)


def gauss_solve(M, b):
    """Reference: Gaussian elimination with Fractions on a dense copy."""
    n = len(b)
    a = [[Fraction(M[i].get(j, 0)) for j in range(n)] + [Fraction(b[i])] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if a[r][c] != 0)
        a[c], a[piv] = a[piv], a[c]
        for r in range(n):
            if r != c and a[r][c] != 0:
                f = a[r][c] / a[c][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    return [a[i][n] / a[i][i] for i in range(n)]


def random_instance(rng, n, q, m):
    pads = [(rng.randint(0, 10), rng.randint(0, 10)) for _ in range(q)]
    nets = []
    for i in range(n):  # every cell gets a net to a pad or to an earlier cell, so all are anchored
        nets.append([i, n + rng.randrange(q)] if i == 0 or rng.random() < 0.3 else [i, rng.randrange(i)])
    for _ in range(m):
        k = min(rng.choice([2, 2, 3, 4]), n + q)
        nets.append(rng.sample(range(n + q), k))
    weights = [rng.randint(1, 3) for _ in nets]
    return nets, pads, weights


def test_chain_closed_form():
    # pads at x = 0 and x = L, cells 1 .. n in a chain: x_i = i L / (n + 1)
    for n in range(1, 9):
        L = 7
        nets = [[n, 0]] + [[i, i + 1] for i in range(n - 1)] + [[n - 1, n + 1]]
        pads = [(0, 0), (L, 0)]
        pos = quadratic_placement(n, nets, pads)
        assert [x for x, _ in pos] == [Fraction((i + 1) * L, n + 1) for i in range(n)]
        assert all(y == 0 for _, y in pos)


def test_exact_cg_matches_gaussian_elimination():
    rng = random.Random(2026)
    for _ in range(60):
        n = rng.randint(1, 7)
        nets, pads, weights = random_instance(rng, n, rng.randint(1, 3), rng.randint(0, 6))
        A, bx, by = build_system(n, nets, pads, weights)
        for b in (bx, by):
            x, steps, hist = conjugate_gradient(A, b)
            assert x == gauss_solve(A, b)
            assert steps <= n and hist[-1] == 0


def test_float_cg_close_to_exact():
    rng = random.Random(7)
    for _ in range(40):
        n = rng.randint(2, 12)
        nets, pads, weights = random_instance(rng, n, 2, rng.randint(0, 10))
        ex = quadratic_placement(n, nets, pads, weights)
        fl = quadratic_placement(n, nets, pads, weights, exact=False, tol=1e-13)
        for (a, b), (c, d) in zip(ex, fl):
            assert abs(float(a) - c) < 1e-8 and abs(float(b) - d) < 1e-8


def test_solution_is_the_minimum():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(1, 6)
        nets, pads, weights = random_instance(rng, n, 2, 4)
        pos = quadratic_placement(n, nets, pads, weights)
        best = quadratic_wirelength(pos, n, nets, pads, weights)
        for _ in range(10):
            i = rng.randrange(n)
            d = (Fraction(rng.randint(-5, 5), 7), Fraction(rng.randint(-5, 5), 7))
            moved = list(pos)
            moved[i] = (pos[i][0] + d[0], pos[i][1] + d[1])
            assert quadratic_wirelength(moved, n, nets, pads, weights) >= best


def test_example_of_the_page():
    # cells a, b, c, d = 0 .. 3; pads P = 4 at (0, 0) and Q = 5 at (6, 3)
    nets = [[4, 0], [0, 1], [0, 2], [1, 2, 3], [3, 5]]
    pads = [(0, 0), (6, 3)]
    pos = quadratic_placement(4, nets, pads)
    assert pos == [
        (Fraction(12, 7), Fraction(6, 7)),
        (Fraction(18, 7), Fraction(9, 7)),
        (Fraction(18, 7), Fraction(9, 7)),
        (Fraction(30, 7), Fraction(15, 7)),
    ]
    assert hpwl(pos, 4, nets, pads) == Fraction(72, 7)
    assert quadratic_wirelength(pos, 4, nets, pads) == Fraction(90, 7)
    A, bx, _ = build_system(4, nets, pads)
    _, steps, hist = conjugate_gradient(A, bx)
    assert steps == 3 and hist == [36, Fraction(9, 2), Fraction(144, 25), 0]


def test_unanchored_component_is_rejected():
    with pytest.raises(ValueError):
        build_system(3, [[0, 1], [2, 3]], [(0, 0)])
