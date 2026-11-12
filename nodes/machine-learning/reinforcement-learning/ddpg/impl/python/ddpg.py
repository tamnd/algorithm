# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ddpg/. The authors are listed in prov/CP12JX.jsonl.

"""Deep deterministic policy gradient (Lillicrap et al. 2016) with linear function approximators.

The actor is mu(s) = theta . f(s) for actor features f(s) (one action dimension).
The critic is Q(s, a) = w . g(s, a) for critic features g(s, a), and dg(s, a)
is the derivative of g in a. The algorithm keeps target copies theta' and w',
a replay buffer and Ornstein-Uhlenbeck exploration noise, as in the paper;
the networks are replaced by linear models so that every step can be followed
exactly. The update functions also work with Fractions.

The environment is a function step(s, a, rng) -> (r, s_next, done) and a
function reset(rng) -> s.

Cost per environment step: O(M (p + q)) for a minibatch of M transitions,
p actor features and q critic features; memory O(capacity + p + q).
"""

import math
import random


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def soft_update(target, online, tau):
    """target <- tau online + (1 - tau) target."""
    return [tau * o + (1 - tau) * t for t, o in zip(target, online)]


def ou_step(x, rng, theta=0.15, sigma=0.2, mean=0, dt=1):
    """One step of an Ornstein-Uhlenbeck process: dx = theta (mean - x) dt + sigma dW."""
    noise = sigma * math.sqrt(dt) * rng.gauss(0.0, 1.0) if sigma else 0
    return x + theta * (mean - x) * dt + noise


def critic_targets(batch, gamma, actor_target, critic_target, f, g):
    """y = r + gamma (1 - done) Q'(s', mu'(s')) with the target actor and the target critic."""
    out = []
    for s, a, r, s2, done in batch:
        if done:
            out.append(r)
        else:
            out.append(r + gamma * dot(critic_target, g(s2, dot(actor_target, f(s2)))))
    return out


def critic_gradient(w, batch, ys, g):
    """Gradient in w of (1/M) sum (Q_w(s, a) - y)^2."""
    grad = [0 * x for x in w]
    for (s, a, _, _, _), y in zip(batch, ys):
        feats = g(s, a)
        err = dot(w, feats) - y
        grad = [gi + 2 * err * x / len(batch) for gi, x in zip(grad, feats)]
    return grad


def actor_gradient(theta, w, batch, f, dg):
    """(1/M) sum grad_theta mu(s) d_a Q_w(s, a) at a = mu(s), the deterministic policy gradient."""
    grad = [0 * x for x in theta]
    for s, _, _, _, _ in batch:
        feats = f(s)
        dq = dot(w, dg(s, dot(theta, feats)))
        grad = [gi + dq * x / len(batch) for gi, x in zip(grad, feats)]
    return grad


def ddpg(step, reset, f, g, dg, theta, w, gamma, steps, rng, minibatch=32, capacity=10000,
         eta_actor=1e-3, eta_critic=1e-2, tau=0.01, ou_theta=0.15, ou_sigma=0.2, horizon=50, warmup=100):
    """Run DDPG for a number of environment steps; returns (theta, w)."""
    theta, w = list(theta), list(w)
    theta_t, w_t = list(theta), list(w)
    buffer, pos = [], 0
    s, x, t_ep = reset(rng), 0.0, 0
    for _ in range(steps):  # @line L1
        x = ou_step(x, rng, ou_theta, ou_sigma)
        a = dot(theta, f(s)) + x  # @line L2
        r, s2, done = step(s, a, rng)
        if len(buffer) < capacity:  # @line L3
            buffer.append((s, a, r, s2, done))
        else:
            buffer[pos] = (s, a, r, s2, done)
            pos = (pos + 1) % capacity
        t_ep += 1
        if done or t_ep >= horizon:
            s, x, t_ep = reset(rng), 0.0, 0
        else:
            s = s2
        if len(buffer) < warmup:
            continue
        batch = rng.sample(buffer, minibatch)  # @line L4
        ys = critic_targets(batch, gamma, theta_t, w_t, f, g)  # @line L5
        gw = critic_gradient(w, batch, ys, g)
        w = [wi - eta_critic * gi for wi, gi in zip(w, gw)]  # @line L6
        ga = actor_gradient(theta, w, batch, f, dg)
        theta = [ti + eta_actor * gi for ti, gi in zip(theta, ga)]  # @line L7
        w_t = soft_update(w_t, w, tau)  # @line L8
        theta_t = soft_update(theta_t, theta, tau)
    return theta, w
