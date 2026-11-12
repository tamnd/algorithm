# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fitted-q-iteration/. The authors are listed in prov/BSTS37.jsonl.

import math
import random
from fractions import Fraction as F

from fitted_q_iteration import (
    empirical_mdp,
    fitted_q_iteration,
    greedy,
    knn_regressor,
    q_value_iteration,
    tabular_regressor,
)

EXAMPLE = [("A", 0, 0, "A"), ("A", 1, 0, "B"), ("B", 0, 1, None), ("B", 1, 0, "A"), ("B", 0, 0, None)]


def test_worked_example() -> None:
    qs = fitted_q_iteration(EXAMPLE, [0, 1], F(9, 10), 4, tabular_regressor, history=True)
    table = [[q(s, a) for s in "AB" for a in (0, 1)] for q in qs]
    half = F(1, 2)
    assert table[1] == [0, 0, half, 0]
    assert table[2] == [0, F(9, 20), half, 0]
    assert table[3] == [F(81, 200), F(9, 20), half, F(81, 200)]
    assert table[4] == table[3]
    assert greedy(qs[4], [0, 1])("A") == 1 and greedy(qs[4], [0, 1])("B") == 0


def random_data(rng, n):
    """Transitions of a 4-state, 3-action MDP with Fraction rewards; some pairs never appear."""
    data = []
    for _ in range(n):
        s, a = rng.randrange(4), rng.randrange(3)
        if (s, a) == (3, 2):
            continue
        u = rng.random()
        s_next = None if u < 0.2 else rng.randrange(5) if s < 3 else rng.randrange(3)
        data.append((s, a, F(rng.randrange(-3, 6), 2), None if s_next == 4 else s_next))
    return data


def test_tabular_fqi_is_value_iteration_on_the_empirical_mdp() -> None:
    rng = random.Random(0)
    for _ in range(5):
        data = random_data(rng, rng.randrange(5, 60))
        gamma = F(rng.randrange(1, 10), 10)
        fqi = fitted_q_iteration(data, [0, 1, 2], gamma, 8, tabular_regressor, history=True)
        vi = q_value_iteration(*empirical_mdp(data), [0, 1, 2], gamma, 8)
        for q_fqi, q_vi in zip(fqi, vi):
            for s in range(4):
                for a in range(3):
                    assert q_fqi(s, a) == q_vi.get((s, a), 0)


def test_fqi_with_an_averager_contracts() -> None:
    rng = random.Random(1)
    data = [(rng.random(), rng.choice([-1, 1]), rng.random(), rng.random() if rng.random() < 0.9 else None) for _ in range(200)]
    qs = fitted_q_iteration(data, [-1, 1], 0.8, 12, knn_regressor(4), history=True)
    grid = [i / 50 for i in range(50)] + [s for s, _, _, _ in data]

    def gap(k):
        return max(abs(qs[k + 1](x, a) - qs[k](x, a)) for x in grid for a in (-1, 1))

    for k in range(1, 11):
        assert gap(k) <= 0.8 * gap(k - 1) + 1e-12


def line_step(x, a):
    """Move 0.1 left or right on [0, 1); reaching 1 ends the episode with reward 1."""
    y = max(0.0, x + 0.1 * a)
    return (1.0, None) if y >= 1 - 1e-12 else (0.0, y)


def test_knn_fqi_on_a_continuous_line() -> None:
    rng = random.Random(0)
    data = []
    for _ in range(1000):
        x, a = rng.random(), rng.choice([-1, 1])
        r, y = line_step(x, a)
        data.append((x, a, r, y))
    gamma = 0.9
    q = fitted_q_iteration(data, [-1, 1], gamma, 30, knn_regressor(5))
    policy = greedy(q, [-1, 1])
    mids = [0.05 + 0.1 * j for j in range(10)]
    assert all(policy(x) == 1 for x in mids)
    for x in mids:
        v_star = gamma ** (math.ceil(round((1 - x) / 0.1, 6)) - 1)
        assert abs(q(x, 1) - v_star) < 0.05
