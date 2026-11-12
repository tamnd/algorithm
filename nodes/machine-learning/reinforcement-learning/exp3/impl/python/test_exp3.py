# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exp3/. The authors are listed in prov/N3XXFK.jsonl.

import math
import random
from fractions import Fraction

from exp3 import (
    best_fixed_arm_total,
    distribution,
    estimates,
    exp3,
    optimal_gamma,
    regret_bound,
    table_rewards,
)


def random_case(rng: random.Random, k: int):
    weights = [Fraction(rng.randint(1, 50), rng.randint(1, 50)) for _ in range(k)]
    gamma = Fraction(rng.randint(1, 10), 10)
    x = [Fraction(rng.randint(0, 8), 8) for _ in range(k)]
    return weights, gamma, x


def test_estimator_is_unbiased_exactly() -> None:
    rng = random.Random(5)
    for k in range(2, 7):
        for _ in range(30):
            weights, gamma, x = random_case(rng, k)
            p = distribution(weights, gamma)
            assert sum(p) == 1
            assert all(pi >= gamma / k for pi in p)
            # E[x_hat_i] = sum over the drawn arm a of p_a * (x_a / p_a if a = i else 0) = x_i.
            mean = [sum(p[a] * estimates(p, a, x[a])[i] for a in range(k)) for i in range(k)]
            assert mean == x


def test_estimator_moments_used_in_the_proof() -> None:
    rng = random.Random(6)
    for _ in range(50):
        weights, gamma, x = random_case(rng, 4)
        p = distribution(weights, gamma)
        for a in range(4):
            xh = estimates(p, a, x[a])
            assert sum(pi * v for pi, v in zip(p, xh)) == x[a]
            assert sum(pi * v * v for pi, v in zip(p, xh)) == x[a] * xh[a] <= xh[a]
            assert all(v <= Fraction(4) / gamma for v in xh)


def test_trace_of_the_page() -> None:
    table = [[1, 0, 0], [0, 1, 1], [1, 0, 1], [0, 1, 0], [1, 1, 0], [0, 0, 1]]
    trace: list = []
    actions, rewards = exp3(table_rewards(table), 3, 6, 0.3, random.Random(2), trace=trace)
    assert actions == [2, 2, 0, 0, 2, 2]
    assert rewards == [0, 1, 1, 0, 0, 1]
    assert [round(v, 3) for v in trace[2][0]] == [0.309, 0.309, 0.382]
    assert round(trace[2][3], 3) == 3.237
    assert [round(v, 3) for v in trace[3][0]] == [0.359, 0.288, 0.353]


def trap(n: int) -> list[list[float]]:
    """Arm 3 is best for the first tenth of the rounds, then arm 1 is best on average."""
    rows = []
    for t in range(n):
        if t < n // 10:
            rows.append([0.0, 0.0, 1.0])
        else:
            rows.append([float(t % 5 < 3), float(t % 2 == 0), float(t % 5 >= 3)])
    return rows


def test_regret_on_an_oblivious_sequence_is_under_the_bound() -> None:
    for n in (1000, 4000, 16000):
        table = trap(n)
        g_max = best_fixed_arm_total(table)
        gamma = optimal_gamma(3, n)  # g = n is an upper bound on G_max
        total = 0.0
        seeds = range(20)
        for s in seeds:
            _, rewards = exp3(table_rewards(table), 3, n, gamma, random.Random(s))
            total += g_max - sum(rewards)
        assert total / len(seeds) <= regret_bound(3, n)


def test_gamma_and_bound_formulas() -> None:
    assert optimal_gamma(3, 1) == 1.0
    g = 1000
    gamma = optimal_gamma(3, g)
    assert abs(gamma - math.sqrt(3 * math.log(3) / ((math.e - 1) * g))) < 1e-12
    # At this gamma, (e - 1) gamma g + K ln K / gamma equals the bound of Corollary 3.2.
    lhs = (math.e - 1) * gamma * g + 3 * math.log(3) / gamma
    assert abs(lhs - regret_bound(3, g)) < 1e-9


def test_long_run_does_not_overflow() -> None:
    _, rewards = exp3(lambda t, a: float(a == 0), 2, 50000, 0.5, random.Random(1))
    assert sum(rewards) > 0.7 * 50000
