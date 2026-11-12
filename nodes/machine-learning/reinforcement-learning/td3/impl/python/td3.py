# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/td3/. The authors are listed in prov/K6H73Z.jsonl.

"""Twin delayed deep deterministic policy gradient (Fujimoto, van Hoof and Meger 2018) with linear models.

The actor is mu(s) = theta . f(s) (one action dimension); the two critics are
Q_j(s, a) = w_j . g(s, a), and dg(s, a) is the derivative of g in a. TD3
changes DDPG in three ways:
1. clipped double Q-learning: the target uses the smaller of two target critics;
2. delayed policy updates: the actor and all targets change once every d critic updates;
3. target policy smoothing: the target action gets clipped Gaussian noise.

The environment is a function step(s, a, rng) -> (r, s_next, done) and a
function reset(rng) -> s. The update functions also work with Fractions when
rng.gauss returns Fractions.

Cost per environment step: O(M (p + q)) for a minibatch of M transitions,
p actor features and q critic features; memory O(capacity + p + q).
"""

import random


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def clip(x, lo, hi):
    return lo if x < lo else hi if x > hi else x


def soft_update(target, online, tau):
    return [tau * o + (1 - tau) * t for t, o in zip(target, online)]


def smoothed_target_action(theta_t, f, s2, rng, sigma, c):
    """mu'(s') + clip(eps, -c, c) with eps ~ N(0, sigma^2)."""
    return dot(theta_t, f(s2)) + clip(rng.gauss(0, sigma), -c, c)


def clipped_double_q_targets(batch, gamma, theta_t, w1_t, w2_t, f, g, rng, sigma, c):
    """y = r + gamma (1 - done) min(Q'_1(s', a~), Q'_2(s', a~)) with one smoothed target action a~ per transition."""
    ys = []
    for s, a, r, s2, done in batch:
        if done:
            ys.append(r)
            continue
        a2 = smoothed_target_action(theta_t, f, s2, rng, sigma, c)  # @line L5
        ys.append(r + gamma * min(dot(w1_t, g(s2, a2)), dot(w2_t, g(s2, a2))))  # @line L6
    return ys


def critic_gradient(w, batch, ys, g):
    grad = [0 * x for x in w]
    for (s, a, _, _, _), y in zip(batch, ys):
        feats = g(s, a)
        err = dot(w, feats) - y
        grad = [gi + 2 * err * x / len(batch) for gi, x in zip(grad, feats)]
    return grad


def actor_gradient(theta, w, batch, f, dg):
    grad = [0 * x for x in theta]
    for s, _, _, _, _ in batch:
        feats = f(s)
        dq = dot(w, dg(s, dot(theta, feats)))
        grad = [gi + dq * x / len(batch) for gi, x in zip(grad, feats)]
    return grad


def update(params, batch, it, gamma, f, g, dg, rng, eta_actor, eta_critic, tau, sigma_target, c, d):
    """One TD3 update on a minibatch; params = (theta, w1, w2, theta_t, w1_t, w2_t); it counts critic updates from 1."""
    theta, w1, w2, theta_t, w1_t, w2_t = params
    ys = clipped_double_q_targets(batch, gamma, theta_t, w1_t, w2_t, f, g, rng, sigma_target, c)
    w1 = [x - eta_critic * y for x, y in zip(w1, critic_gradient(w1, batch, ys, g))]  # @line L7
    w2 = [x - eta_critic * y for x, y in zip(w2, critic_gradient(w2, batch, ys, g))]
    if it % d == 0:  # @line L8
        theta = [x + eta_actor * y for x, y in zip(theta, actor_gradient(theta, w1, batch, f, dg))]  # @line L9
        theta_t = soft_update(theta_t, theta, tau)  # @line L10
        w1_t = soft_update(w1_t, w1, tau)
        w2_t = soft_update(w2_t, w2, tau)
    return theta, w1, w2, theta_t, w1_t, w2_t


def td3(step, reset, f, g, dg, theta, w1, w2, gamma, steps, rng, minibatch=32, capacity=10000,
        eta_actor=1e-3, eta_critic=1e-2, tau=0.005, sigma_explore=0.1, sigma_target=0.2, c=0.5, d=2,
        horizon=50, warmup=100, low=None, high=None):
    """Run TD3 for a number of environment steps; returns (theta, w1, w2). w1 and w2 should start different."""
    params = (list(theta), list(w1), list(w2), list(theta), list(w1), list(w2))
    buffer, pos, it = [], 0, 0
    s, t_ep = reset(rng), 0
    for _ in range(steps):  # @line L1
        a = dot(params[0], f(s)) + rng.gauss(0, sigma_explore)  # @line L2
        if low is not None:
            a = clip(a, low, high)
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
        it += 1
        params = update(params, batch, it, gamma, f, g, dg, rng, eta_actor, eta_critic, tau, sigma_target, c, d)
    return params[0], params[1], params[2]
