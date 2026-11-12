# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-actor-critic/. The authors are listed in prov/B23BP5.jsonl.

"""Soft actor-critic (Haarnoja et al. 2018) with linear models, and tabular soft policy iteration.

Function approximation part (one action dimension):
  actor   u = theta . f(s) + exp(log_std) xi with xi ~ N(0, 1), and a = tanh(u) if squash else u;
  critics Q_j(s, a) = w_j . g(s, a) for j = 1, 2, where dg(s, a) is the derivative of g in a;
  temperature alpha = exp(log_alpha), tuned to a target entropy when target_entropy is not None.
The critics regress on the soft target r + gamma (min_j Q'_j(s', a') - alpha log pi(a' | s'))
with a fresh a' ~ pi(. | s'); the actor minimizes alpha log pi(a | s) - min_j Q_j(s, a) with the
reparameterized action a = a(s, xi); the target critics are moving averages.
The environment is step(s, a, rng) -> (r, s_next, done) and reset(rng) -> s.
Cost per environment step: O(M (p + q)) for a minibatch of M transitions, p actor features and
q critic features; memory O(capacity + p + q).

Tabular part: soft policy evaluation (iterating the soft Bellman operator of a fixed policy) and
soft policy improvement (pi_new proportional to exp(Q / alpha)); each evaluation sweep costs
O(|S|^2 |A|) and each improvement O(|S| |A|).
"""

import math
import random

LOG_2PI = math.log(2 * math.pi)


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def soft_update(target, online, tau):
    return [tau * o + (1 - tau) * t for t, o in zip(target, online)]


def sample_action(theta, log_std, f, s, xi, squash):
    """Reparameterized action a(s, xi) and its log density log pi(a | s)."""
    u = dot(theta, f(s)) + math.exp(log_std) * xi
    logp = -0.5 * xi * xi - log_std - 0.5 * LOG_2PI
    if not squash:
        return u, logp
    a = math.tanh(u)
    return a, logp - math.log(1 - a * a + 1e-12)


def soft_targets(batch, gamma, alpha, theta, log_std, w1_t, w2_t, f, g, rng, squash):
    """y = r + gamma (1 - done) (min_j Q'_j(s', a') - alpha log pi(a' | s')) with a fresh a' ~ pi(. | s')."""
    ys = []
    for s, a, r, s2, done in batch:
        if done:
            ys.append(r)
            continue
        a2, logp2 = sample_action(theta, log_std, f, s2, rng.gauss(0, 1), squash)  # @line L5
        ys.append(r + gamma * (min(dot(w1_t, g(s2, a2)), dot(w2_t, g(s2, a2))) - alpha * logp2))  # @line L6
    return ys


def critic_gradient(w, batch, ys, g):
    grad = [0 * x for x in w]
    for (s, a, _, _, _), y in zip(batch, ys):
        feats = g(s, a)
        err = dot(w, feats) - y
        grad = [gi + 2 * err * x / len(batch) for gi, x in zip(grad, feats)]
    return grad


def actor_objective(theta, log_std, w1, w2, states, xis, alpha, f, g, squash):
    """Sample policy loss (1/M) sum_i (alpha log pi(a_i | s_i) - min_j Q_j(s_i, a_i)) with a_i = a(s_i, xi_i)."""
    total = 0.0
    for s, xi in zip(states, xis):
        a, logp = sample_action(theta, log_std, f, s, xi, squash)
        total += alpha * logp - min(dot(w1, g(s, a)), dot(w2, g(s, a)))
    return total / len(states)


def actor_gradient(theta, log_std, w1, w2, states, xis, alpha, f, g, dg, squash):
    """Exact gradient of actor_objective in (theta, log_std), through the reparameterized action."""
    gt, gl = [0.0] * len(theta), 0.0
    std = math.exp(log_std)
    for s, xi in zip(states, xis):
        a, _ = sample_action(theta, log_std, f, s, xi, squash)
        w = w1 if dot(w1, g(s, a)) <= dot(w2, g(s, a)) else w2
        dq = dot(w, dg(s, a))
        if squash:
            dl_du = 2 * alpha * a - dq * (1 - a * a)  # d/du of -alpha log(1 - tanh(u)^2) is 2 alpha tanh(u)
        else:
            dl_du = -dq  # log pi(a(s, xi) | s) does not depend on the mean once xi is fixed
        gt = [x + dl_du * y / len(states) for x, y in zip(gt, f(s))]
        gl += (dl_du * std * xi - alpha) / len(states)
    return gt, gl


def temperature_step(log_alpha, logps, target_entropy, eta):
    """Gradient step on J(alpha) = E[-alpha log pi - alpha H_target], taken in log alpha:
    alpha rises when the sampled entropy -mean(log pi) is below the target, and falls when it is above."""
    entropy = -sum(logps) / len(logps)
    return log_alpha - eta * (entropy - target_entropy)


def update(params, batch, gamma, f, g, dg, rng, eta_actor, eta_critic, eta_alpha, tau, target_entropy, squash):
    """One SAC update; params = (theta, log_std, w1, w2, w1_t, w2_t, log_alpha)."""
    theta, log_std, w1, w2, w1_t, w2_t, log_alpha = params
    alpha = math.exp(log_alpha)
    ys = soft_targets(batch, gamma, alpha, theta, log_std, w1_t, w2_t, f, g, rng, squash)
    w1 = [x - eta_critic * y for x, y in zip(w1, critic_gradient(w1, batch, ys, g))]  # @line L7
    w2 = [x - eta_critic * y for x, y in zip(w2, critic_gradient(w2, batch, ys, g))]
    states = [b[0] for b in batch]
    xis = [rng.gauss(0, 1) for _ in states]
    gt, gl = actor_gradient(theta, log_std, w1, w2, states, xis, alpha, f, g, dg, squash)
    theta, log_std = [x - eta_actor * y for x, y in zip(theta, gt)], log_std - eta_actor * gl  # @line L8
    if target_entropy is not None:
        logps = [sample_action(theta, log_std, f, s, xi, squash)[1] for s, xi in zip(states, xis)]
        log_alpha = temperature_step(log_alpha, logps, target_entropy, eta_alpha)  # @line L9
    w1_t, w2_t = soft_update(w1_t, w1, tau), soft_update(w2_t, w2, tau)  # @line L10
    return theta, log_std, w1, w2, w1_t, w2_t, log_alpha


def sac(step, reset, f, g, dg, theta, log_std, w1, w2, gamma, steps, rng, alpha=0.1, target_entropy=None,
        minibatch=32, capacity=10000, eta_actor=1e-3, eta_critic=1e-2, eta_alpha=1e-3, tau=0.005,
        squash=False, horizon=50, warmup=100):
    """Run SAC for a number of environment steps; returns (theta, log_std, w1, w2, alpha)."""
    params = (list(theta), log_std, list(w1), list(w2), list(w1), list(w2), math.log(alpha))
    buffer, pos = [], 0
    s, t_ep = reset(rng), 0
    for _ in range(steps):  # @line L1
        a, _ = sample_action(params[0], params[1], f, s, rng.gauss(0, 1), squash)  # @line L2
        r, s2, done = step(s, a, rng)
        if len(buffer) < capacity:  # @line L3
            buffer.append((s, a, r, s2, done))
        else:
            buffer[pos] = (s, a, r, s2, done)
            pos = (pos + 1) % capacity
        t_ep += 1
        if done or t_ep >= horizon:
            s, t_ep = reset(rng), 0
        else:
            s = s2
        if len(buffer) < warmup:
            continue
        batch = rng.sample(buffer, minibatch)  # @line L4
        params = update(params, batch, gamma, f, g, dg, rng, eta_actor, eta_critic, eta_alpha, tau,
                        target_entropy, squash)
    theta, log_std, w1, w2, _, _, log_alpha = params
    return theta, log_std, w1, w2, math.exp(log_alpha)


# Tabular soft policy iteration. P[s][a][t] is a transition probability (rows may sum to less
# than 1; the missing mass ends the episode), R[s][a] the expected reward, pi[s][a] > 0 a policy.

def soft_bellman_operator(P, R, pi, Q, gamma, alpha):
    """(T^pi Q)(s, a) = R(s, a) + gamma sum_t P(t | s, a) V(t), V(t) = sum_b pi(b | t) (Q(t, b) - alpha log pi(b | t))."""
    V = [sum(p * (q - alpha * math.log(p)) for p, q in zip(pi[t], Q[t])) for t in range(len(R))]
    return [[R[s][a] + gamma * dot(P[s][a], V) for a in range(len(R[s]))] for s in range(len(R))]


def soft_policy_evaluation(P, R, pi, gamma, alpha, sweeps=200):
    """Iterate T^pi from Q = 0 (Lemma 1 of the paper); the error after k sweeps is O(gamma^k)."""
    Q = [[0.0] * len(row) for row in R]
    for _ in range(sweeps):
        Q = soft_bellman_operator(P, R, pi, Q, gamma, alpha)
    return Q


def soft_policy_improvement(Q, alpha):
    """pi_new(a | s) = exp(Q(s, a) / alpha) / Z(s), the minimizer of the KL divergence of Lemma 2."""
    out = []
    for row in Q:
        m = max(row)
        z = [math.exp((q - m) / alpha) for q in row]
        out.append([x / sum(z) for x in z])
    return out


def soft_policy_iteration(P, R, gamma, alpha, iterations, sweeps=200):
    """Alternate evaluation and improvement from the uniform policy; returns the list of (pi, Q^pi)."""
    pi = [[1 / len(row)] * len(row) for row in R]
    history = []
    for _ in range(iterations):
        Q = soft_policy_evaluation(P, R, pi, gamma, alpha, sweeps)
        history.append((pi, Q))
        pi = soft_policy_improvement(Q, alpha)
    return history
