# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adamw/. The authors are listed in prov/P87340.jsonl.

"""AdamW (decoupled weight decay) next to Adam with an L2 penalty.

Parameters are lists of numbers. All step functions follow Loshchilov and
Hutter (2019), Algorithm 2: alpha is the base step size, eta is the schedule
multiplier and lam is the weight decay factor. AdamW subtracts
eta * lam * theta directly; Adam with L2 adds lam * theta to the gradient.
"""

import math


def new_state(n):
    return {"t": 0, "m": [0.0] * n, "v": [0.0] * n}


def _adam_direction(g, state, beta1, beta2, eps):
    """Update the moments with g and return the vector m_hat / (sqrt(v_hat) + eps)."""
    state["t"] += 1
    t = state["t"]
    m, v = state["m"], state["v"]
    out = []
    for i, gi in enumerate(g):
        m[i] = beta1 * m[i] + (1 - beta1) * gi  # @line L4
        v[i] = beta2 * v[i] + (1 - beta2) * gi * gi  # @line L5
        m_hat = m[i] / (1 - beta1 ** t)  # @line L6
        v_hat = v[i] / (1 - beta2 ** t)
        out.append(m_hat / (math.sqrt(v_hat) + eps))
    return out


def adamw_step(theta, g, state, alpha=1e-3, beta1=0.9, beta2=0.999, eps=1e-8, lam=1e-2, eta=1.0):
    """One AdamW step. g is the gradient of the loss without any penalty."""
    d = _adam_direction(g, state, beta1, beta2, eps)
    return [th - eta * (alpha * di + lam * th) for th, di in zip(theta, d)]  # @line L8


def adam_l2_step(theta, g, state, alpha=1e-3, beta1=0.9, beta2=0.999, eps=1e-8, lam=1e-2, eta=1.0):
    """One step of Adam on the loss plus (lam / 2) * ||theta||^2."""
    g2 = [gi + lam * th for gi, th in zip(g, theta)]
    d = _adam_direction(g2, state, beta1, beta2, eps)
    return [th - eta * alpha * di for th, di in zip(theta, d)]


def adamw(grad, theta, steps, alpha=1e-3, beta1=0.9, beta2=0.999, eps=1e-8, lam=1e-2, schedule=None):
    """Run AdamW for the given number of steps; grad(theta, t) is the gradient at step t."""
    state = new_state(len(theta))  # @line L1
    path = [list(theta)]
    for t in range(1, steps + 1):  # @line L2
        g = grad(theta, t)  # @line L3
        eta = schedule(t) if schedule else 1.0  # @line L7
        theta = adamw_step(theta, g, state, alpha, beta1, beta2, eps, lam, eta)
        path.append(theta)
    return path  # @line L9


def adam_l2(grad, theta, steps, alpha=1e-3, beta1=0.9, beta2=0.999, eps=1e-8, lam=1e-2, schedule=None):
    state = new_state(len(theta))
    path = [list(theta)]
    for t in range(1, steps + 1):
        g = grad(theta, t)
        eta = schedule(t) if schedule else 1.0
        theta = adam_l2_step(theta, g, state, alpha, beta1, beta2, eps, lam, eta)
        path.append(theta)
    return path


def sgd_l2_step(theta, g, alpha, lam_l2):
    """SGD on the loss plus (lam_l2 / 2) ||theta||^2: theta - alpha (g + lam_l2 theta)."""
    return [th - alpha * (gi + lam_l2 * th) for th, gi in zip(theta, g)]


def sgdw_step(theta, g, alpha, lam):
    """SGD with decoupled weight decay: theta - alpha g - lam theta."""
    return [th - alpha * gi - lam * th for th, gi in zip(theta, g)]


def sgd_momentum_l2_step(theta, g, buf, alpha, beta, lam_l2):
    """Heavy ball with the L2 term inside the momentum buffer (Algorithm 1, L2 form)."""
    for i, (th, gi) in enumerate(zip(theta, g)):
        buf[i] = beta * buf[i] + alpha * (gi + lam_l2 * th)
    return [th - b for th, b in zip(theta, buf)]


def sgdw_momentum_step(theta, g, buf, alpha, beta, lam):
    """SGDW, Algorithm 1 of the paper with eta = 1: the decay stays out of the buffer."""
    for i, gi in enumerate(g):
        buf[i] = beta * buf[i] + alpha * gi
    return [th - b - lam * th for th, b in zip(theta, buf)]
