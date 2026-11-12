# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppo/. The authors are listed in prov/K21R8T.jsonl.

"""Proximal policy optimization with the clipped surrogate (Schulman et al. 2017).

An MDP is (P, R): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends, and R[s][a] is
the reward. The policy is pi(a|s) proportional to exp(theta . phi[s][a]); the
critic is a table V[s]. A sample is (s, a, adv, ret).

The functions on probabilities (clipped_objective, objective_gradient) also
work with Fractions.

Cost of one iteration: O(n_actors * horizon * (1 + epochs) * A * k) for A
actions and k policy parameters, plus the environment steps.
"""

import math
import random


def clip(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def clipped_objective(r, adv, eps):
    """min(r adv, clip(r, 1 - eps, 1 + eps) adv) for one sample with probability ratio r."""
    return min(r * adv, clip(r, 1 - eps, 1 + eps) * adv)


def clipped_slope(r, adv, eps):
    """Derivative of clipped_objective in r; 0 once the ratio has moved past the clip range in the direction that helps."""
    if (adv > 0 and r < 1 + eps) or (adv < 0 and r > 1 - eps):
        return adv
    return 0 * adv


def policy(theta, phi):
    out = []
    for rows in phi:
        z = [sum(t * f for t, f in zip(theta, row)) for row in rows]
        m = max(z)
        e = [math.exp(x - m) for x in z]
        out.append([x / sum(e) for x in e])
    return out


def score(pi, phi, s, a):
    return [phi[s][a][i] - sum(pi[s][b] * phi[s][b][i] for b in range(len(pi[s]))) for i in range(len(phi[s][a]))]


def objective(pi, pi_old, batch, eps):
    return sum(clipped_objective(pi[s][a] / pi_old[s][a], adv, eps) for s, a, adv, _ in batch) / len(batch)


def objective_gradient(pi, pi_old, phi, batch, eps):
    """Gradient in theta of the mean clipped objective; d r / d theta = r psi(s, a)."""
    g = [0 * pi[0][0]] * len(phi[0][0])
    for s, a, adv, _ in batch:
        r = pi[s][a] / pi_old[s][a]
        c = clipped_slope(r, adv, eps) * r / len(batch)
        g = [gi + c * p for gi, p in zip(g, score(pi, phi, s, a))]
    return g


def gae(rewards, values, dones, last_value, gamma, lam):
    """Truncated generalized advantage estimates for one segment; dones[t] is True if the episode ended after step t."""
    adv = [0.0] * len(rewards)
    run, nxt = 0.0, last_value
    for t in range(len(rewards) - 1, -1, -1):
        live = 0.0 if dones[t] else 1.0
        delta = rewards[t] + gamma * nxt * live - values[t]
        run = delta + gamma * lam * live * run
        adv[t] = run
        nxt = values[t]
    return adv


def adapt_kl_coefficient(beta, d, d_target):
    """The adaptive KL penalty rule of the paper (Section 4)."""
    if d < d_target / 1.5:
        return beta / 2
    if d > d_target * 1.5:
        return beta * 2
    return beta


def env_step(P, R, mu, s, a, rng):
    r = R[s][a]
    u, acc = rng.random(), 0.0
    for t, p in enumerate(P[s][a]):
        acc += p
        if u < acc:
            return r, t, False
    return r, rng.choices(range(len(mu)), weights=mu)[0], True


def ppo(P, R, mu, gamma, lam, theta, phi, n_actors, horizon, iterations, epochs, minibatch,
        eps, eta, eta_v, rng):
    """PPO-Clip with n_actors parallel actors, segments of fixed length and a tabular critic."""
    theta = list(theta)
    V = [0.0] * len(P)
    states = [rng.choices(range(len(mu)), weights=mu)[0] for _ in range(n_actors)]
    for _ in range(iterations):  # @line L1
        pi = policy(theta, phi)
        batch = []
        for i in range(n_actors):  # @line L2
            seg, s = [], states[i]
            for _ in range(horizon):
                a = rng.choices(range(len(pi[s])), weights=pi[s])[0]
                r, s_next, done = env_step(P, R, mu, s, a, rng)
                seg.append((s, a, r, done))
                s = s_next
            states[i] = s
            adv = gae([x[2] for x in seg], [V[x[0]] for x in seg], [x[3] for x in seg], V[s], gamma, lam)  # @line L3
            batch += [(x[0], x[1], A, A + V[x[0]]) for x, A in zip(seg, adv)]
        pi_old = pi  # @line L4
        for _ in range(epochs):  # @line L5
            rng.shuffle(batch)
            for j in range(0, len(batch), minibatch):
                mb = batch[j:j + minibatch]
                pi = policy(theta, phi)
                g = objective_gradient(pi, pi_old, phi, mb, eps)  # @line L6
                theta = [t + eta * gi for t, gi in zip(theta, g)]  # @line L7
                for s, _, _, ret in mb:
                    V[s] += eta_v * (ret - V[s]) / len(mb)  # @line L8
    return theta, V
