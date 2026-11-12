# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ucb1/. The authors are listed in prov/WS67AB.jsonl.

import math
import random

from ucb1 import bernoulli_arms, mean_regret_curve, regret, ucb1, ucb1_bound


def test_trace_of_the_page() -> None:
    actions, rewards = ucb1(bernoulli_arms([0.7, 0.5, 0.3], random.Random(3)), 3, 10)
    assert actions == [0, 1, 2, 0, 0, 0, 0, 1, 2, 2]
    assert rewards == [1, 0, 0, 1, 1, 1, 1, 0, 1, 1]


def test_index_by_hand() -> None:
    # Round 4 of the trace: arm 1 has mean 1 after one pull, so its index is 1 + sqrt(2 ln 3).
    assert abs(1 + math.sqrt(2 * math.log(3)) - 2.482) < 1e-3


def test_deterministic_arms() -> None:
    # Arm 1 always pays 1 and arm 0 always pays 0. Arm 0 is pulled only O(log n) times.
    n = 2000
    actions, _ = ucb1(lambda a: float(a == 1), 2, n)
    t0 = actions.count(0)
    # Arm 0 is pulled at round t only if sqrt(2 ln(t-1) / N_0) >= 1, so N_0 <= 2 ln n + 1.
    assert t0 <= 2 * math.log(n) + 1
    assert regret([0.0, 1.0], actions) == t0


def test_regret_under_bound_and_logarithmic() -> None:
    means = [0.9, 0.6, 0.3]
    cps = [1000, 2000, 4000, 8000, 16000]
    r = mean_regret_curve(means, cps, range(20))
    for value, n in zip(r, cps):
        assert value <= ucb1_bound(means, n)
    steps = [b - a for a, b in zip(r, r[1:])]
    # Each doubling of n adds about the same regret: growth like log n, not like n.
    assert all(0.6 * steps[0] <= s <= 1.5 * steps[0] for s in steps)
    assert r[-1] / r[0] < 3


def test_bound_formula() -> None:
    b = ucb1_bound([0.9, 0.6, 0.3], 1000)
    want = 8 * math.log(1000) * (1 / 0.3 + 1 / 0.6) + (1 + math.pi**2 / 3) * 0.9
    assert abs(b - want) < 1e-9
