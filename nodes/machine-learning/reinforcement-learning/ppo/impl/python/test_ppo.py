# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppo/. The authors are listed in prov/K21R8T.jsonl.

import math
import random
from fractions import Fraction as F

from ppo import (
    adapt_kl_coefficient,
    clipped_objective,
    clipped_slope,
    gae,
    objective,
    objective_gradient,
    policy,
    ppo,
    score,
)

EPS = F(1, 5)


def test_exact_cases():
    # (r, adv, objective, slope in r) with eps = 1/5, so the clip range is [4/5, 6/5]
    cases = [
        (F(1), F(2), F(2), F(2)),
        (F(9, 10), F(2), F(9, 5), F(2)),
        (F(3, 2), F(2), F(12, 5), F(0)),  # good action already more likely: no push
        (F(1, 2), F(2), F(1), F(2)),  # good action less likely: full push back
        (F(1), F(-2), F(-2), F(-2)),
        (F(11, 10), F(-2), F(-11, 5), F(-2)),
        (F(1, 2), F(-2), F(-8, 5), F(0)),  # bad action already less likely: no push
        (F(3, 2), F(-2), F(-3), F(-2)),  # bad action more likely: full push back
    ]
    for r, adv, obj, slope in cases:
        assert clipped_objective(r, adv, EPS) == obj
        assert clipped_slope(r, adv, EPS) == slope


def test_objective_is_a_pessimistic_bound_with_the_right_slope():
    h = F(1, 1000)
    for k in range(1, 30):
        r = F(k, 10)
        for adv in range(-3, 4):
            adv = F(adv)
            obj = clipped_objective(r, adv, EPS)
            assert obj <= r * adv
            if 1 - EPS <= r <= 1 + EPS:
                assert obj == r * adv
            if r not in (1 - EPS, 1 + EPS):
                assert (clipped_objective(r + h, adv, EPS) - obj) / h == clipped_slope(r, adv, EPS)


def test_gradient_at_old_policy_is_the_policy_gradient_estimate():
    rng = random.Random(1)
    for _ in range(20):
        n, k, m = 3, 3, 4
        pi = []
        for _ in range(n):
            w = [rng.randint(1, 5) for _ in range(k)]
            pi.append([F(x, sum(w)) for x in w])
        phi = [[[F(rng.randint(-2, 2)) for _ in range(m)] for _ in range(k)] for _ in range(n)]
        batch = [(rng.randrange(n), rng.randrange(k), F(rng.randint(-5, 5)), 0) for _ in range(8)]
        want = [sum(adv * score(pi, phi, s, a)[i] for s, a, adv, _ in batch) / len(batch) for i in range(m)]
        assert objective_gradient(pi, pi, phi, batch, EPS) == want


def test_gradient_matches_finite_differences():
    rng = random.Random(2)
    n, k, m = 3, 3, 4
    phi = [[[rng.uniform(-1, 1) for _ in range(m)] for _ in range(k)] for _ in range(n)]
    for _ in range(10):
        old = [rng.uniform(-1, 1) for _ in range(m)]
        theta = [t + rng.uniform(-0.5, 0.5) for t in old]
        pi_old = policy(old, phi)
        batch = [(rng.randrange(n), rng.randrange(k), rng.uniform(-2, 2), 0) for _ in range(10)]
        g = objective_gradient(policy(theta, phi), pi_old, phi, batch, 0.2)
        h = 1e-6
        for i in range(m):
            up = [t + (h if j == i else 0) for j, t in enumerate(theta)]
            dn = [t - (h if j == i else 0) for j, t in enumerate(theta)]
            fd = (objective(policy(up, phi), pi_old, batch, 0.2) - objective(policy(dn, phi), pi_old, batch, 0.2)) / (2 * h)
            assert abs(fd - g[i]) < 1e-6


def ascend(adv, clipped, steps, eta=0.5):
    phi = [[[1.0, 0.0], [0.0, 1.0]]]
    old = [0.0, 0.0]
    pi_old = policy(old, phi)
    theta, history = list(old), []
    for _ in range(steps):
        pi = policy(theta, phi)
        if clipped:
            g = objective_gradient(pi, pi_old, phi, [(0, 0, adv, 0)], 0.2)
        else:
            g = [adv * x * pi[0][0] / pi_old[0][0] for x in score(pi, phi, 0, 0)]
        theta = [t + eta * gi for t, gi in zip(theta, g)]
        history.append(list(theta))
    return history, policy(theta, phi)[0][0] / pi_old[0][0]


def test_updates_stop_outside_the_clip_range():
    for adv in [1.0, -1.0]:
        history, r = ascend(adv, True, 300)
        assert history[-1] == history[100]  # the parameters stopped moving
        assert (r >= 1.2 and r < 1.5) if adv > 0 else (r <= 0.8 and r > 0.5)
        _, r_plain = ascend(adv, False, 300)
        assert (r_plain > 1.9) if adv > 0 else (r_plain < 0.1)  # the unclipped ratio runs to its limit


def test_gae_segment():
    adv = gae([1.0, 2.0, 3.0], [0.5, 0.5, 0.5], [False, False, False], 4.0, 0.5, 1.0)
    # lam = 1: the discounted return with a bootstrap from the last value, minus V
    assert adv == [1 + 0.5 * 2 + 0.25 * 3 + 0.125 * 4 - 0.5, 2 + 0.5 * 3 + 0.25 * 4 - 0.5, 3 + 0.5 * 4 - 0.5]
    adv = gae([1.0, 2.0, 3.0], [0.5, 0.5, 0.5], [False, True, False], 4.0, 0.5, 1.0)
    # the episode ends after step 1, so step 1 does not look past it
    assert adv == [1 + 0.5 * 2 - 0.5, 2 - 0.5, 3 + 0.5 * 4 - 0.5]


def test_adaptive_kl_rule():
    assert adapt_kl_coefficient(1.0, 0.001, 0.01) == 0.5
    assert adapt_kl_coefficient(1.0, 0.02, 0.01) == 2.0
    assert adapt_kl_coefficient(1.0, 0.012, 0.01) == 1.0


def test_ppo_learns():
    P = [[[0.5, 0.25], [0.0, 0.75]], [[0.5, 0.0], [0.0, 0.0]]]
    R = [[1.0, 0.0], [0.0, 3.0]]
    phi = [[[1.0 if i == s * 2 + a else 0.0 for i in range(4)] for a in range(2)] for s in range(2)]
    theta, V = ppo(P, R, [1.0, 0.0], 0.5, 0.95, [0.0] * 4, phi, 4, 32, 30, 4, 32, 0.2, 0.5, 0.5, random.Random(0))
    pi = policy(theta, phi)
    assert pi[0][0] > 0.9 and pi[1][1] > 0.9
    assert abs(V[0] - 11 / 6) < 0.3 and abs(V[1] - 3) < 0.5
    assert all(math.isfinite(t) for t in theta)
