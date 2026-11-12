# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-reinforcement-learning/. The authors are listed in prov/5XWNRJ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from inverse_reinforcement_learning import (expected_features, feature_counts, grid,
                                            log_likelihood, maxent_irl, ng_russell_condition,
                                            optimal_policies, path_features, sample_paths)


def random_mdp(rng, n=3, k=2, den=4):
    P = []
    for _ in range(k):
        rows = []
        for _ in range(n):
            cuts = sorted(rng.randint(0, den) for _ in range(n - 1))
            parts = [b - a for a, b in zip([0] + cuts, cuts + [den])]
            rows.append([Fraction(p, den) for p in parts])
        P.append(rows)
    return P


def all_policies(n, k):
    return [list(p) for p in itertools.product(range(k), repeat=n)]


def test_ng_russell_condition_matches_brute_force():
    rng = random.Random(0)
    gamma = Fraction(9, 10)
    checked = 0
    for _ in range(40):
        n, k = rng.choice([(2, 2), (3, 2), (3, 3)])
        P = random_mdp(rng, n, k)
        R = [Fraction(rng.randint(-3, 3)) for _ in range(n)]
        opt = optimal_policies(P, R, gamma)
        for pol in all_policies(n, k):
            assert ng_russell_condition(P, R, gamma, pol) == (tuple(pol) in opt)
            checked += 1
    assert checked > 200


def test_constant_rewards_make_every_policy_optimal():
    rng = random.Random(1)
    gamma = Fraction(3, 4)
    for c in (0, 1, -5):
        P = random_mdp(rng, 3, 3)
        R = [Fraction(c)] * 3
        for pol in all_policies(3, 3):
            assert ng_russell_condition(P, R, gamma, pol)


def brute_force_features(env, theta):
    num = [0.0] * env.d
    z = 0.0
    for acts in itertools.product(range(env.k), repeat=env.T - 1):
        f = path_features(env, acts)
        w = math.exp(sum(t * x for t, x in zip(theta, f)))
        z += w
        num = [a + w * x for a, x in zip(num, f)]
    return [a / z for a in num], math.log(z)


def test_forward_backward_matches_enumeration():
    env = grid(horizon=5)
    for theta in ([0.0, 0.0, 0.0], [2.0, -1.5, 0.3], [-1.0, 0.7, 1.2]):
        exact, _ = brute_force_features(env, theta)
        mu = expected_features(env, theta)
        assert max(abs(a - b) for a, b in zip(exact, mu)) < 1e-10


def test_gradient_is_feature_difference():
    env = grid(horizon=4)
    demos = sample_paths(env, [1.0, -1.0, 0.5], 30, random.Random(2))
    target = feature_counts(env, demos)
    theta = [0.2, 0.1, -0.3]
    mu = expected_features(env, theta)
    h = 1e-6
    for j in range(env.d):
        up = list(theta)
        dn = list(theta)
        up[j] += h
        dn[j] -= h
        fd = (log_likelihood(env, up, demos) - log_likelihood(env, dn, demos)) / (2 * h)
        assert abs(fd - (target[j] - mu[j])) < 1e-6


def test_maxent_irl_recovers_the_reward_from_exact_counts():
    env = grid(horizon=5)
    true = [2.0, -1.5, 0.3]
    target = expected_features(env, true)
    theta = maxent_irl(env, target)
    assert max(abs(a - b) for a, b in zip(theta, true)) < 1e-6
    assert max(abs(a - b) for a, b in zip(expected_features(env, theta), target)) < 1e-9


def test_maxent_irl_matches_sampled_demonstrations():
    env = grid(horizon=5)
    demos = sample_paths(env, [2.0, -1.5, 0.3], 300, random.Random(3))
    target = feature_counts(env, demos)
    theta = maxent_irl(env, target)
    assert max(abs(a - b) for a, b in zip(expected_features(env, theta), target)) < 1e-8
    # the fitted reward still prefers the goal and avoids the water
    assert theta[0] > 0 and theta[1] < 0
    # the maximum likelihood theta is at least as likely as the true one
    assert log_likelihood(env, theta, demos) >= log_likelihood(env, [2.0, -1.5, 0.3], demos) - 1e-12
