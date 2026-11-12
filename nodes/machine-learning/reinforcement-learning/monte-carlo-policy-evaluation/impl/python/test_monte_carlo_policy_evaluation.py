# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-policy-evaluation/. The authors are listed in prov/WSWCCF.jsonl.

import random
from fractions import Fraction as F

from monte_carlo_policy_evaluation import constant_alpha_mc, generate_episode, mc_policy_evaluation

# The worked example of the page, gamma = 1.
EP1 = [("A", 3), ("A", 2), ("B", -4), ("A", 4), ("B", -3)]
EP2 = [("B", -2), ("A", 3), ("B", -3)]


def test_worked_example_first_visit():
    V, N = mc_policy_evaluation([EP1], F(1))
    assert V == {"A": 2, "B": -3} and N == {"A": 1, "B": 1}
    V, N = mc_policy_evaluation([EP1, EP2], F(1))
    assert V == {"A": 1, "B": F(-5, 2)} and N == {"A": 2, "B": 2}


def test_worked_example_every_visit():
    V, N = mc_policy_evaluation([EP1], F(1), first_visit=False)
    assert V == {"A": F(2, 3), "B": -3}
    V, N = mc_policy_evaluation([EP1, EP2], F(1), first_visit=False)
    assert V == {"A": F(1, 2), "B": F(-11, 4)} and N == {"A": 4, "B": 4}


def test_discounted_returns():
    V, _ = mc_policy_evaluation([EP1], F(1, 2))
    # G_0 = 3 + 2/2 - 4/4 + 4/8 - 3/16, G_2 = -4 + 4/2 - 3/4
    assert V["A"] == 3 + F(2, 2) - F(4, 4) + F(4, 8) - F(3, 16)
    assert V["B"] == -4 + F(4, 2) - F(3, 4)


def test_empty_and_single():
    assert mc_policy_evaluation([], 1) == ({}, {})
    assert mc_policy_evaluation([[("s", 5)]], 1) == ({"s": 5}, {"s": 1})


def test_loop_state_estimates():
    # One state, reward 1 per step, k visits: first-visit gives k, every-visit (k + 1) / 2.
    for k in range(1, 12):
        ep = [("s", 1)] * k
        assert mc_policy_evaluation([ep], F(1))[0]["s"] == k
        assert mc_policy_evaluation([ep], F(1), first_visit=False)[0]["s"] == F(k + 1, 2)


def loop_step(s, a, rng):
    # Continue with probability 1/2, reward 1 per step: v(s) = 2.
    return 1, s, rng.random() >= 0.5


def test_bias_of_single_episode_estimates():
    rng = random.Random(7)
    m = 40000
    fv = ev = 0.0
    for _ in range(m):
        ep = generate_episode("s", loop_step, lambda s, r: 0, rng)
        fv += mc_policy_evaluation([ep], 1.0)[0]["s"]
        ev += mc_policy_evaluation([ep], 1.0, first_visit=False)[0]["s"]
    assert abs(fv / m - 2.0) < 0.03  # unbiased: mean 2
    assert abs(ev / m - 1.5) < 0.02  # biased: mean 3/2


def walk_step(s, a, rng):
    # Random walk of Sutton and Barto, Example 6.2: states 1..5, start 3.
    s2 = s + (1 if rng.random() < 0.5 else -1)
    if s2 == 6:
        return 1, None, True
    if s2 == 0:
        return 0, None, True
    return 0, s2, False


def test_random_walk_converges():
    rng = random.Random(1)
    eps = [generate_episode(3, walk_step, lambda s, r: 0, rng) for _ in range(4000)]
    for fv in (True, False):
        V, _ = mc_policy_evaluation(eps, 1.0, first_visit=fv)
        for s in range(1, 6):
            assert abs(V[s] - s / 6) < 0.03


def brute(episodes, gamma, first_visit):
    rets = {}
    for ep in episodes:
        seen = set()
        for t, (s, _) in enumerate(ep):
            G = sum(gamma ** k * ep[t + k][1] for k in range(len(ep) - t))
            if first_visit and s in seen:
                continue
            seen.add(s)
            rets.setdefault(s, []).append(G)
    return {s: sum(v) / len(v) for s, v in rets.items()}


def test_random_against_brute_force():
    rng = random.Random(2024)
    for _ in range(500):
        eps = [[(rng.randrange(3), F(rng.randint(-3, 3))) for _ in range(rng.randint(1, 6))] for _ in range(rng.randint(1, 3))]
        g = F(rng.randint(0, 4), 4)
        for fv in (True, False):
            assert mc_policy_evaluation(eps, g, fv)[0] == brute(eps, g, fv)


def test_constant_alpha_one_is_last_return():
    V = constant_alpha_mc([EP1], F(1), F(1), first_visit=True)
    assert V == {"A": 2, "B": -3}
