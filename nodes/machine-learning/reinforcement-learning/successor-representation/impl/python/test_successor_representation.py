# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/successor-representation/. The authors are listed in prov/FGK3ES.jsonl.

import random
from fractions import Fraction as F

from successor_representation import successor_matrix, td_successor, values

H = F(1, 2)
CHAIN = [[H, H, 0, 0], [H, 0, H, 0], [0, H, 0, H], [0, 0, H, H]]


def random_chain(rng, n):
    rows = []
    for _ in range(n):
        w = [rng.randrange(0, 4) for _ in range(n)]
        w[rng.randrange(n)] += 1
        rows.append([F(x, sum(w)) for x in w])
    return rows


def test_worked_example() -> None:
    m = successor_matrix(CHAIN, H)
    assert m[0] == [F(41, 28), F(11, 28), F(3, 28), F(1, 28)]
    assert values(m, [0, 0, 0, 1]) == [F(1, 28), F(3, 28), F(11, 28), F(41, 28)]


def test_m_is_the_inverse_and_v_is_m_r() -> None:
    rng = random.Random(0)
    for n in (1, 2, 3, 5):
        p = random_chain(rng, n)
        gamma = F(rng.randrange(1, 10), 10)
        m = successor_matrix(p, gamma)
        for i in range(n):
            for j in range(n):
                assert sum(m[i][k] * ((k == j) - gamma * p[k][j]) for k in range(n)) == (i == j)
            assert sum(m[i]) == 1 / (1 - gamma)
        r = [F(rng.randrange(-5, 6)) for _ in range(n)]
        v = values(m, r)
        for i in range(n):
            assert v[i] == r[i] + gamma * sum(p[i][j] * v[j] for j in range(n))


def test_m_is_the_fixed_point_of_the_expected_td_update() -> None:
    rng = random.Random(1)
    p = random_chain(rng, 4)
    gamma = F(4, 5)
    m = successor_matrix(p, gamma)
    for s in range(4):
        for j in range(4):
            assert (s == j) + gamma * sum(p[s][t] * m[t][j] for t in range(4)) - m[s][j] == 0


def test_revaluation_needs_no_relearning() -> None:
    m = successor_matrix(CHAIN, F(9, 10))
    for r in ([0, 0, 0, 1], [1, 0, 0, 0], [F(1, 2), -1, 2, 0]):
        v = values(m, r)
        for i in range(4):
            assert v[i] == r[i] + F(9, 10) * sum(CHAIN[i][j] * v[j] for j in range(4))


def test_td_learned_m_approaches_the_inverse() -> None:
    exact = [[float(x) for x in row] for row in successor_matrix(CHAIN, F(1, 2))]

    def error(steps, seed):
        m = td_successor(CHAIN, 0.5, steps, random.Random(seed), alpha=1.0, decay=0.7)
        return max(abs(a - b) for r1, r2 in zip(m, exact) for a, b in zip(r1, r2))

    for seed in range(3):
        assert error(50000, seed) < 0.03
        assert error(50000, seed) < error(500, seed)
