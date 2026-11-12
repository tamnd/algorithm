# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/importance-sampling-off-policy/. The authors are listed in prov/5BH86H.jsonl.

import itertools
import random
from fractions import Fraction as F

from importance_sampling_off_policy import (
    episode_distribution,
    example_5_5_step,
    off_policy_estimates,
    sample_episode,
)

ACTIONS = [0, 1]


def small_step(s, a):
    """A three-step episodic MDP: stage 0, then stage 1 (states 1 or 2), then stage 2 (state 3), then the end."""
    if s == 0:
        return [(F(1, 3), F(1), 1), (F(2, 3), F(0), 2)] if a == 0 else [(F(1), F(2), 2)]
    if s in (1, 2):
        return [(F(1, 2), F(s), 3), (F(1, 2), F(-1), None)] if a == 0 else [(F(1), F(3 - s), 3)]
    return [(F(1), F(5), None)] if a == 0 else [(F(1, 4), F(-2), None), (F(3, 4), F(4), None)]


def pi(a, s):
    table = {0: F(1, 5), 1: F(9, 10), 2: F(1, 2), 3: F(2, 3)}
    return table[s] if a == 0 else 1 - table[s]


def mu(a, s):
    table = {0: F(1, 2), 1: F(1, 3), 2: F(3, 4), 3: F(1, 4)}
    return table[s] if a == 0 else 1 - table[s]


def ret(ep, gamma):
    return sum(gamma**t * r for t, (_, _, r) in enumerate(ep))


def test_ordinary_and_per_decision_are_unbiased_exactly() -> None:
    for gamma in (F(1), F(9, 10), F(1, 2)):
        v_pi = sum(p * ret(ep, gamma) for p, ep in episode_distribution(small_step, pi, ACTIONS, 0, 5))
        v_mu = sum(p * ret(ep, gamma) for p, ep in episode_distribution(small_step, mu, ACTIONS, 0, 5))
        dist = episode_distribution(small_step, mu, ACTIONS, 0, 5)
        assert sum(p for p, _ in dist) == 1
        e_ord = sum(p * off_policy_estimates([ep], pi, mu, gamma)[0] for p, ep in dist)
        e_pd = sum(p * off_policy_estimates([ep], pi, mu, gamma)[2] for p, ep in dist)
        e_w1 = sum(p * off_policy_estimates([ep], pi, mu, gamma)[1] for p, ep in dist)
        assert e_ord == v_pi and e_pd == v_pi
        assert e_w1 == v_mu != v_pi  # weighted IS on one episode returns G, so its mean is v_mu


def test_weighted_is_bias_shrinks_with_more_episodes() -> None:
    dist = episode_distribution(small_step, mu, ACTIONS, 0, 5)
    v_pi = sum(p * ret(ep, 1) for p, ep in episode_distribution(small_step, pi, ACTIONS, 0, 5))
    biases = []
    for n in (1, 2, 3):
        mean = F(0)
        for combo in itertools.product(dist, repeat=n):
            prob = 1
            for p, _ in combo:
                prob *= p
            mean += prob * off_policy_estimates([ep for _, ep in combo], pi, mu)[1]
        biases.append(abs(mean - v_pi))
    assert biases[0] > biases[1] > biases[2] > 0


def test_per_decision_has_lower_variance_here() -> None:
    dist = episode_distribution(small_step, mu, ACTIONS, 0, 5)

    def second_moment(k):
        return sum(p * off_policy_estimates([ep], pi, mu)[k] ** 2 for p, ep in dist)

    assert second_moment(2) < second_moment(0)


def test_example_5_5_unbiased_with_infinite_variance() -> None:
    pi55 = lambda a, s: F(1) if a == "left" else F(0)
    mu55 = lambda a, s: F(1, 2)
    acts = ["left", "right"]
    k_max = 30
    dist = episode_distribution(example_5_5_step, mu55, acts, 0, k_max + 1)
    mean = sum(p * off_policy_estimates([ep], pi55, mu55)[0] for p, ep in dist)
    second = sum(p * off_policy_estimates([ep], pi55, mu55)[0] ** 2 for p, ep in dist)
    # Truncated sums: the mean tends to v_pi = 1, the second moment is 0.2 sum_k 1.8^k, which diverges.
    assert mean == 1 - F(9, 10) ** (k_max + 1)
    assert second == F(1, 5) * sum(F(9, 5) ** k for k in range(k_max + 1))
    assert second > 10**7


def test_example_5_5_weighted_is_exact_after_one_success() -> None:
    pi55 = lambda a, s: 1.0 if a == "left" else 0.0
    mu55 = lambda a, s: 0.5
    acts = ["left", "right"]
    for seed in range(5):
        rng = random.Random(seed)
        eps = [sample_episode(example_5_5_step, mu55, acts, 0, rng) for _ in range(2000)]
        ordinary, weighted, _ = off_policy_estimates(eps, pi55, mu55)
        assert weighted == 1.0
        assert ordinary != 1.0


def test_on_policy_reduces_to_monte_carlo() -> None:
    rng = random.Random(1)
    eps = [sample_episode(small_step, pi, ACTIONS, 0, rng) for _ in range(50)]
    o, w, p = off_policy_estimates(eps, pi, pi, F(9, 10))
    mc = sum(ret(ep, F(9, 10)) for ep in eps) / len(eps)
    assert o == w == p == mc
