# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epsilon-greedy/. The authors are listed in prov/PHHMGW.jsonl.

import random
from fractions import Fraction as F

from epsilon_greedy import (
    auer_schedule,
    bernoulli_arms,
    constant,
    epsilon_greedy,
    greedy_arm,
    mean_regret,
    regret,
    schedule_values,
)

MEANS = [0.9, 0.6, 0.5]
SEEDS = range(20)


def test_greedy_arm() -> None:
    assert greedy_arm([0, 0], [0.0, 0.0]) == 0
    assert greedy_arm([1, 0], [1.0, 0.0]) == 1  # an arm never pulled goes first
    assert greedy_arm([2, 2], [1.0, 1.0]) == 0  # ties go to the smallest index
    assert greedy_arm([2, 4], [1.0, 3.0]) == 1


def test_auer_schedule_exact() -> None:
    # c = 5, d = 3/10, K = 3: c K / d^2 = 1500 / 9.
    vals = schedule_values(F(5), F(3, 10), 3, [1, 166, 167, 500, 1000])
    assert vals == [1, 1, F(1500, 9 * 167), F(1, 3), F(1, 6)]


def test_greedy_locks_on_worse_arm() -> None:
    # Seed 15: arm 0 (mean 0.9) pays 0 and arm 1 (mean 0.5) pays 1 on the first pulls.
    means = [0.9, 0.5]
    actions, rewards = epsilon_greedy(bernoulli_arms(means, random.Random(15)), 2, 1000, constant(0), random.Random(0))
    assert actions[:2] == [0, 1] and rewards[:2] == [0, 1]
    assert actions.count(0) == 1
    assert abs(regret(means, actions) - 0.4 * 999) < 1e-9


def test_constant_epsilon_is_linear() -> None:
    # Each round pulls each arm with probability at least eps / K, so
    # E[R_n] >= n * eps * sum(Delta_i) / K.
    eps, n = 0.1, 4000
    lower = n * eps * (0.3 + 0.4) / 3
    r1 = mean_regret(MEANS, n, constant(eps), SEEDS)
    r4 = mean_regret(MEANS, 4 * n, constant(eps), SEEDS)
    assert r1 >= 0.9 * lower
    assert 3.5 <= r4 / r1 <= 4.5


def test_decaying_schedule_is_logarithmic() -> None:
    # Theorem 3 of Auer, Cesa-Bianchi and Fischer with c = 5 and d = 0.3, the smallest gap.
    sched = auer_schedule(5, 0.3, 3)
    r = [mean_regret(MEANS, n, sched, SEEDS) for n in (1000, 4000, 16000)]
    assert r[0] < r[1] < r[2]
    # Each factor 4 in n adds about the same amount: the growth is in log n.
    assert r[2] / r[0] < 2.5
    assert 0.5 < (r[2] - r[1]) / (r[1] - r[0]) < 1.5
