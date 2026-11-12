# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-actor-critic/. The authors are listed in prov/B23BP5.jsonl.

import math
import random

from soft_actor_critic import (actor_gradient, actor_objective, sac, sample_action, soft_bellman_operator,
                               soft_policy_evaluation, soft_policy_improvement, soft_policy_iteration,
                               soft_targets, temperature_step)


class FixedNoise:
    """Stands in for random.Random: gauss returns the given values in turn."""

    def __init__(self, values):
        self.values, self.i = list(values), 0

    def gauss(self, mu, sigma):
        v = self.values[self.i % len(self.values)]
        self.i += 1
        return v


def f(s):
    return [s]


def g(s, a):
    return [s * s, s * a, a * a, 1.0]


def dg(s, a):
    return [0.0, s, 2 * a, 0.0]


P = [[[1 / 2, 1 / 4], [0, 3 / 4]], [[1 / 2, 0], [0, 0]]]
R = [[1, 0], [0, 3]]


def soft_optimal_q(P, R, gamma, alpha, sweeps=200):
    V = [0.0, 0.0]
    for _ in range(sweeps):
        Q = [[R[s][a] + gamma * sum(p * v for p, v in zip(P[s][a], V)) for a in range(2)] for s in range(2)]
        V = [max(row) + alpha * math.log(sum(math.exp((q - max(row)) / alpha) for q in row)) for row in Q]
    return Q


def test_soft_target_by_hand():
    # s' = 2, xi = 1, theta = -1/2, std = 1: a' = -1 + 1 = 0, log pi = -1/2 - log(2 pi)/2
    # Q'_1 = -4, Q'_2 = -8 + 1 = -7; y = 1 + (1/2)(-7 + 1/2 + log(2 pi)/2)
    batch = [(0.0, 0.0, 1.0, 2.0, False), (0.0, 0.0, 5.0, 2.0, True)]
    ys = soft_targets(batch, 0.5, 1.0, [-0.5], 0.0, [-1, 0, -1, 0], [-2, 0, 0, 1], f, g, FixedNoise([1.0]), False)
    assert abs(ys[0] - (1 + 0.5 * (-7 + 0.5 + 0.5 * math.log(2 * math.pi)))) < 1e-12
    assert ys[1] == 5.0


def test_squashed_log_density_is_the_change_of_variables():
    theta, log_std, s = [0.3], math.log(0.7), 1.0
    for xi in [-1.5, -0.2, 0.4, 1.1]:
        a, logp = sample_action(theta, log_std, f, s, xi, True)
        # the distribution function of a = tanh(u) is Phi((atanh(a) - mu) / std); differentiate numerically
        cdf = lambda x: 0.5 * (1 + math.erf((math.atanh(x) - 0.3) / (0.7 * math.sqrt(2))))
        h = 1e-6
        assert abs((cdf(a + h) - cdf(a - h)) / (2 * h) - math.exp(logp)) < 1e-5


def test_reparameterized_actor_gradient_matches_finite_differences():
    rng = random.Random(3)
    states = [rng.uniform(-1, 1) for _ in range(8)]
    xis = [rng.gauss(0, 1) for _ in range(8)]
    w1, w2 = [-2.4, -2.8, -2.3, -0.9], [-2.5, -2.6, -2.4, -0.8]
    for squash in [False, True]:
        theta, log_std, alpha, h = [-0.4], math.log(0.3), 0.2, 1e-6
        gt, gl = actor_gradient(theta, log_std, w1, w2, states, xis, alpha, f, g, dg, squash)
        obj = lambda t, l: actor_objective(t, l, w1, w2, states, xis, alpha, f, g, squash)
        fd_t = (obj([theta[0] + h], log_std) - obj([theta[0] - h], log_std)) / (2 * h)
        fd_l = (obj(theta, log_std + h) - obj(theta, log_std - h)) / (2 * h)
        assert abs(gt[0] - fd_t) < 1e-6 and abs(gl - fd_l) < 1e-6


def test_temperature_moves_toward_the_target_entropy():
    low_entropy_logps = [1.0, 2.0]  # sampled entropy -1.5
    high_entropy_logps = [-3.0, -2.0]  # sampled entropy 2.5
    assert temperature_step(0.0, low_entropy_logps, 0.0, 0.1) > 0.0  # alpha rises
    assert temperature_step(0.0, high_entropy_logps, 0.0, 0.1) < 0.0  # alpha falls
    assert temperature_step(0.0, [-1.0, -1.0], 1.0, 0.1) == 0.0


def test_soft_policy_evaluation_is_the_fixed_point():
    pi = [[0.3, 0.7], [0.6, 0.4]]
    Q = soft_policy_evaluation(P, R, pi, 0.5, 1.0)
    TQ = soft_bellman_operator(P, R, pi, Q, 0.5, 1.0)
    assert max(abs(x - y) for r1, r2 in zip(Q, TQ) for x, y in zip(r1, r2)) < 1e-12


def test_soft_policy_improvement_never_lowers_q():
    rng = random.Random(0)
    for _ in range(30):
        pi = []
        for _ in range(2):
            x = rng.uniform(0.01, 0.99)
            pi.append([x, 1 - x])
        alpha = rng.choice([0.2, 1.0, 3.0])
        Q_old = soft_policy_evaluation(P, R, pi, 0.5, alpha)
        Q_new = soft_policy_evaluation(P, R, soft_policy_improvement(Q_old, alpha), 0.5, alpha)
        assert all(n >= o - 1e-12 for rn, ro in zip(Q_new, Q_old) for n, o in zip(rn, ro))


def test_soft_policy_iteration_converges_to_the_soft_optimum():
    alpha = 1.0
    history = soft_policy_iteration(P, R, 0.5, alpha, 12)
    target = soft_optimal_q(P, R, 0.5, alpha)
    pi, Q = history[-1]
    assert max(abs(x - y) for r1, r2 in zip(Q, target) for x, y in zip(r1, r2)) < 1e-10
    # Q increases along the iteration
    for (_, Qa), (_, Qb) in zip(history, history[1:]):
        assert all(b >= a - 1e-12 for ra, rb in zip(Qa, Qb) for a, b in zip(ra, rb))
    # no other policy has a larger soft Q anywhere
    rng = random.Random(1)
    for _ in range(30):
        other = [[x, 1 - x] for x in (rng.uniform(0.01, 0.99), rng.uniform(0.01, 0.99))]
        Qo = soft_policy_evaluation(P, R, other, 0.5, alpha)
        assert all(o <= t + 1e-10 for ro, rt in zip(Qo, target) for o, t in zip(ro, rt))


def lq_problem():
    Pr = (0.8 + math.sqrt(0.64 + 3.6)) / 1.8  # 0.9 P^2 - 0.8 P - 1 = 0
    k_star, q_aa = -0.9 * Pr / (1 + 0.9 * Pr), 1 + 0.9 * Pr

    def step(s, a, rng):
        return -(s * s + a * a), s + a, False

    def reset(rng):
        return rng.uniform(-1, 1)

    return step, reset, k_star, q_aa


def test_sac_learns_the_soft_optimal_gaussian_policy():
    # soft optimal policy of the scalar LQ problem: mean k* s, variance alpha / (2 q_aa)
    step, reset, k_star, q_aa = lq_problem()
    alpha = 0.1
    theta, log_std, w1, w2, _ = sac(step, reset, f, g, dg, [-0.2], math.log(0.3), [0.0] * 4, [-0.1, 0.0, -0.1, 0.0],
                                    0.9, 4000, random.Random(0), alpha=alpha, eta_actor=0.02, eta_critic=0.03,
                                    tau=0.05, horizon=10)
    assert abs(theta[0] - k_star) < 0.05
    assert abs(log_std - 0.5 * math.log(alpha / (2 * q_aa))) < 0.15


def test_sac_tunes_the_temperature():
    # target entropy of N(0, 0.2^2): the soft optimal std is 0.2 when alpha = 2 q_aa 0.04
    step, reset, k_star, q_aa = lq_problem()
    target = math.log(0.2) + 0.5 * math.log(2 * math.pi * math.e)
    theta, log_std, _, _, alpha = sac(step, reset, f, g, dg, [-0.2], math.log(0.3), [0.0] * 4,
                                      [-0.1, 0.0, -0.1, 0.0], 0.9, 6000, random.Random(0), alpha=0.5,
                                      target_entropy=target, eta_actor=0.02, eta_critic=0.03, eta_alpha=0.01,
                                      tau=0.05, horizon=10)
    assert abs(theta[0] - k_star) < 0.05
    assert abs(log_std - math.log(0.2)) < 0.1
    assert abs(alpha - 2 * q_aa * 0.04) < 0.03
