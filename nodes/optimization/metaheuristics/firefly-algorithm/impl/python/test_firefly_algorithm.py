# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/firefly-algorithm/. The authors are listed in prov/BF1W32.jsonl.

import math
import random

from firefly_algorithm import attractiveness, firefly_algorithm, firefly_move, rastrigin, sphere


def test_attractiveness() -> None:
    assert attractiveness(1.0, 0.1, 0.0) == 1.0
    assert math.isclose(attractiveness(1.0, 0.1, 17.0), math.exp(-1.7), rel_tol=1e-15)
    assert attractiveness(0.7, 0.0, 1e6) == 0.7  # gamma = 0: constant pull
    assert attractiveness(1.0, 1e6, 1.0) == 0.0  # very large gamma: no pull


def test_move_trace() -> None:
    sc = [10.0, 10.0]
    y = firefly_move([3.0, 1.0], [-1.0, 0.0], 1.0, 0.1, 0.2, [0.75, 0.25], sc)
    b = math.exp(-1.7)
    assert math.isclose(y[0], 3.0 - 4.0 * b + 0.5, rel_tol=1e-15)
    assert math.isclose(y[1], 1.0 - 1.0 * b - 0.5, rel_tol=1e-15)
    assert math.isclose(y[0], 2.7692659037890617, rel_tol=1e-12)
    # The example of the page.
    y1 = firefly_move([1.0, 2.0], [-1.0, 0.0], 1.0, 0.1, 0.2, [0.5, 0.5], sc)
    assert all(math.isclose(a, c, rel_tol=1e-12) for a, c in zip(y1, [0.10134207176555687, 1.1013420717655569]))
    y3 = firefly_move([3.0, 1.0], y1, 1.0, 0.1, 0.2, [0.9, 0.1], sc)
    assert all(math.isclose(a, c, rel_tol=1e-12) for a, c in zip(y3, [2.550180618010971, 0.2436958373976411]))
    y3 = firefly_move(y3, [-1.0, 0.0], 1.0, 0.1, 0.2, [0.1, 0.9], sc)
    assert all(math.isclose(a, c, rel_tol=1e-12) for a, c in zip(y3, [0.7494989134164939, 0.9750058206890614]))
    assert math.isclose(sphere(y3), 1.512384971590055, rel_tol=1e-12)


def test_reduction_to_a_pull_toward_a_better_point() -> None:
    # With gamma = 0 and alpha = 0 the move is x + beta0 (x_j - x): the PSO position update
    # with inertia 0, no personal term and the social coefficient times r fixed to beta0.
    rng = random.Random(5)
    for _ in range(100):
        x = [rng.uniform(-5, 5) for _ in range(4)]
        g = [rng.uniform(-5, 5) for _ in range(4)]
        b0 = rng.random()
        u = [rng.random() for _ in range(4)]
        y = firefly_move(x, g, b0, 0.0, 0.0, u, [1.0] * 4)
        v = [b0 * (gk - xk) for xk, gk in zip(x, g)]  # PSO velocity with w = 0, c1 = 0, c2 r2 = b0
        assert all(math.isclose(yk, xk + vk, rel_tol=1e-12, abs_tol=1e-12) for yk, xk, vk in zip(y, x, v))
    assert firefly_move([1.0, 2.0], [3.0, -2.0], 1.0, 0.0, 0.0, [0.3, 0.9], [1.0, 1.0]) == [3.0, -2.0]


def test_moves_go_toward_brighter_and_best_is_kept() -> None:
    evaluated: list[float] = []

    def f(x):
        v = rastrigin(x)
        evaluated.append(v)
        return v

    moves = []

    def check(t, i, xi, xj, u):
        assert rastrigin(xj) < rastrigin(xi)  # only toward a brighter firefly
        moves.append(t)

    g, fg, hist = firefly_algorithm(f, [-5.12] * 3, [5.12] * 3, 6, 1.0, 0.1, 0.2, 0.97, 40, random.Random(1), check)
    assert fg == min(evaluated) and fg == rastrigin(g)
    assert all(hist[t + 1] <= hist[t] for t in range(len(hist) - 1))
    assert len(evaluated) == 6 + len(moves)  # one evaluation per move
    assert all(-5.12 <= v <= 5.12 for v in g)
    assert max(moves.count(t) for t in range(40)) <= 6 * 5


def test_collapse_without_noise() -> None:
    # alpha = 0, gamma = 0, beta0 = 1: every move jumps onto a brighter firefly, so after one
    # iteration all fireflies sit on the initial best point and nothing changes after that.
    rng = random.Random(7)
    start = [[rng.uniform(-5.0, 5.0) for _ in range(3)] for _ in range(8)]
    best0 = min(start, key=sphere)
    g, fg, hist = firefly_algorithm(sphere, [-5.0] * 3, [5.0] * 3, 8, 1.0, 0.0, 0.0, 1.0, 10, random.Random(7))
    assert g == best0 and fg == sphere(best0)
    assert hist == [fg] * 11


def test_fixed_seed_runs() -> None:
    g, fg, _ = firefly_algorithm(sphere, [-5.12] * 5, [5.12] * 5, 15, 1.0, 0.1, 0.2, 0.97, 300, random.Random(0))
    assert fg < 1e-8 and fg == sphere(g)
    g, fg, _ = firefly_algorithm(rastrigin, [-5.12] * 2, [5.12] * 2, 15, 1.0, 0.1, 0.2, 0.97, 300, random.Random(0))
    assert fg < 1e-8 and all(abs(v) < 1e-4 for v in g)
