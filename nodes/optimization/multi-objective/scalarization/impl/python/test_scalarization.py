# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scalarization/. The authors are listed in prov/YDZF9D.jsonl.

import random
from fractions import Fraction as Fr

from scalarization import (
    achievement,
    cleanup,
    epsilon_constraint,
    epsilon_constraint_front,
    goal_programming,
    lexicographic,
    sweep,
    tchebycheff,
    tchebycheff_value,
    weighted_sum,
)

# The running example: a, b, c, d, e, f, g.
EX = [(2, 9), (3, 6), (4, 7), (5, 4), (7, 3), (8, 5), (9, 1)]
A, B, C, D, E, F, G = range(7)


def dominates(a, b) -> bool:
    return all(x <= y for x, y in zip(a, b)) and tuple(a) != tuple(b)


def strictly_less(a, b) -> bool:
    return all(x < y for x, y in zip(a, b))


def pareto(Y):
    """Brute force: check all pairs."""
    return {i for i, y in enumerate(Y) if not any(dominates(z, y) for z in Y)}


def weak_pareto(Y):
    return {i for i, y in enumerate(Y) if not any(strictly_less(z, y) for z in Y)}


def test_example_front() -> None:
    assert pareto(EX) == {A, B, D, E, G}


def test_example_weighted_sum() -> None:
    def ws(l):
        return set(weighted_sum(EX, (l, 1 - l)))

    assert ws(Fr(9, 10)) == {A}
    assert ws(Fr(3, 4)) == {A, B}
    assert ws(Fr(2, 3)) == {B}
    assert ws(Fr(1, 2)) == {B, D}
    assert ws(Fr(9, 20)) == {D}
    assert ws(Fr(3, 7)) == {D, G}
    assert ws(Fr(1, 5)) == {G}
    for t in range(0, 1001):
        assert E not in ws(Fr(t, 1000))


def test_example_tchebycheff() -> None:
    z = (1, 0)
    for i in pareto(EX):
        w = tuple(Fr(1, EX[i][k] - z[k]) for k in range(2))
        assert tchebycheff(EX, w, z) == [i]
        assert tchebycheff_value(EX[i], w, z) == 1


def test_example_epsilon_constraint() -> None:
    expect = {9: A, 8: B, 7: B, 6: B, 5: D, 4: D, 3: E, 2: G, 1: G}
    for eps, i in expect.items():
        assert epsilon_constraint(EX, 0, (None, eps)) == [i]
    assert epsilon_constraint(EX, 0, (None, 0)) == []
    assert epsilon_constraint_front(EX) == [A, B, D, E, G]


def test_example_achievement_and_goals() -> None:
    assert achievement(EX, (4, 4), (1, 1)) == [D]
    assert achievement(EX, (6, 2), (1, 1)) == [E]
    # Goals at the ideal point: the same as the weighted sum.
    assert goal_programming(EX, (2, 1), (1, 2)) == weighted_sum(EX, (1, 2))
    # Attainable goals: every vector that meets them has value 0.
    assert set(goal_programming(EX, (8, 7), (1, 1))) == {B, C, D, E, F}
    assert lexicographic(EX, (0, 1)) == [A]
    assert lexicographic(EX, (1, 0)) == [G]


def test_cleanup_and_sweep() -> None:
    Y = [(0, 2), (0, 1), (1, 0), (3, 0)]
    # (0, 2) and (3, 0) are weakly but not properly Pareto optimal.
    assert tchebycheff(Y, (1, Fr(1, 3)), (-1, -1)) == [0, 1]
    assert cleanup(Y, 0) == 1
    assert cleanup(Y, 3) == 2

    def tch(y, w):
        return tchebycheff_value(y, w, (-1, -1))

    thetas = [(Fr(t, 10), 1 - Fr(t, 10)) for t in range(1, 10)]
    S = sweep(Y, tch, thetas, weak=True)
    assert set(S) <= pareto(Y)
    assert set(S) == {1, 2}


def random_instance(rng: random.Random):
    p = rng.randint(2, 4)
    n = rng.randint(1, 10)
    hi = rng.choice([3, 5, 9])
    return [tuple(rng.randint(0, hi) for _ in range(p)) for _ in range(n)], p


def test_random_theorems() -> None:
    rng = random.Random(20261109)
    for _ in range(800):
        Y, p = random_instance(rng)
        P, W = pareto(Y), weak_pareto(Y)
        ideal = [min(y[k] for y in Y) for k in range(p)]
        z = [v - 1 for v in ideal]

        # Weighted sum, lam > 0: every optimum is Pareto optimal.
        lam = [Fr(rng.randint(1, 9)) for _ in range(p)]
        assert set(weighted_sum(Y, lam)) <= P
        # lam >= 0, lam != 0: weakly Pareto optimal; a unique optimum is Pareto optimal.
        lam0 = [Fr(rng.randint(0, 2)) for _ in range(p)]
        if any(lam0):
            opt = weighted_sum(Y, lam0)
            assert set(opt) <= W
            if len({Y[i] for i in opt}) == 1:
                assert set(opt) <= P

        # Tchebycheff with a utopia point: weakly Pareto optimal optima.
        w = [Fr(rng.randint(1, 9)) for _ in range(p)]
        opt = tchebycheff(Y, w, z)
        assert set(opt) <= W
        if len({Y[i] for i in opt}) == 1:
            assert set(opt) <= P
        # Augmented: every optimum is Pareto optimal.
        assert set(tchebycheff(Y, w, z, Fr(1, rng.randint(1, 50)))) <= P

        # Each Pareto optimal point is found, with the weights 1/(y_i - z_i).
        for i in P:
            wi = [Fr(1, Y[i][k] - z[k]) for k in range(p)]
            assert {Y[j] for j in tchebycheff(Y, wi, z)} == {Y[i]}
            # Augmented form: unique optimum for rho < delta / C.
            others = [y for y in Y if y != Y[i]]
            if others:
                delta = min(max(wi[k] * (y[k] - Y[i][k]) for k in range(p)) for y in others)
                assert delta > 0
                C = max(sum(max(0, Y[i][k] - y[k]) for k in range(p)) for y in others)
                rho = delta / (2 * C) if C else Fr(1)
                assert {Y[j] for j in tchebycheff(Y, wi, z, rho)} == {Y[i]}

        # Epsilon-constraint: weakly Pareto optimal; unique optimum is Pareto optimal.
        k = rng.randrange(p)
        eps = [rng.randint(0, 9) for _ in range(p)]
        opt = epsilon_constraint(Y, k, eps)
        assert set(opt) <= W
        if opt and len({Y[i] for i in opt}) == 1:
            assert set(opt) <= P
        # With eps = y-hat, every optimum has the image y-hat, for each k.
        for i in P:
            for kk in range(p):
                assert {Y[j] for j in epsilon_constraint(Y, kk, Y[i])} == {Y[i]}

        # Achievement function: a weakly Pareto optimal y-hat as reference is optimal.
        for i in W:
            assert i in achievement(Y, Y[i], w)
        zbar = [rng.randint(-2, 10) for _ in range(p)]
        assert set(achievement(Y, zbar, w)) <= W
        assert set(achievement(Y, zbar, w, Fr(1, 20))) <= P

        # Goal programming with goals at or below the ideal point.
        goals = [v - rng.randint(0, 3) for v in ideal]
        assert set(goal_programming(Y, goals, w)) <= P

        # Lexicographic optima are Pareto optimal, and equal a weighted sum
        # with the weights M^(p-1), ..., 1 when M exceeds the range.
        order = list(range(p))
        rng.shuffle(order)
        lex = lexicographic(Y, order)
        assert set(lex) <= P
        M = max(max(y) for y in Y) - min(min(y) for y in Y) + 1
        lw = [0] * p
        for r, obj in enumerate(order):
            lw[obj] = M ** (p - 1 - r)
        assert weighted_sum(Y, lw) == lex

        # The sweep with the cleanup solve returns only Pareto optimal indices.
        thetas = [[Fr(rng.randint(1, 9)) for _ in range(p)] for _ in range(4)]
        S = sweep(Y, lambda y, t: tchebycheff_value(y, t, z), thetas, weak=True)
        assert set(S) <= P

        # Two objectives: the epsilon-constraint loop gives the front.
        if p == 2:
            front = epsilon_constraint_front(Y)
            assert {Y[i] for i in front} == {Y[i] for i in P}
            assert len(front) == len({Y[i] for i in P})


def test_unsupported_point_needs_tchebycheff() -> None:
    # The discrete counterexample: (0.6, 0.6) is Pareto optimal but no
    # positive weighted sum selects it.
    Y = [(Fr(0), Fr(1)), (Fr(1), Fr(0)), (Fr(3, 5), Fr(3, 5))]
    assert pareto(Y) == {0, 1, 2}
    for t in range(1, 100):
        assert 2 not in weighted_sum(Y, (Fr(t, 100), 1 - Fr(t, 100)))
    z = (Fr(-1), Fr(-1))
    w = (1 / (Fr(3, 5) + 1), 1 / (Fr(3, 5) + 1))
    assert tchebycheff(Y, w, z) == [2]
