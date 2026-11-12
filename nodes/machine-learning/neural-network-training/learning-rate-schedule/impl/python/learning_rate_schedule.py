# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-rate-schedule/. The authors are listed in prov/2F4BBA.jsonl.

"""Learning rate schedules for a training loop.

Each schedule is a function of the optimizer step t (t = 0 is the first
step) that returns the learning rate for that step. The functions accept
ints, floats or fractions.Fraction values, so that tests can check the
rational ones exactly.
"""

import math
from fractions import Fraction


def constant(t, eta):
    return eta


def step_decay(t, eta0, gamma, step_size):
    """eta0 * gamma ** floor(t / step_size): multiply by gamma every step_size steps."""
    return eta0 * gamma ** (t // step_size)


def multi_step_decay(t, eta0, gamma, milestones):
    """eta0 * gamma ** (the number of milestones m with m <= t)."""
    return eta0 * gamma ** sum(1 for m in milestones if m <= t)


def exponential_decay(t, eta0, gamma):
    return eta0 * gamma ** t


def polynomial_decay(t, eta0, total, power, eta_end=0):
    """eta_end + (eta0 - eta_end) * (1 - t / total) ** power, and eta_end after total."""
    if t >= total:
        return eta_end
    return eta_end + (eta0 - eta_end) * (1 - Fraction(t, total)) ** power


def cosine_annealing(t, eta_max, eta_min, total):
    """SGDR without restarts: eta_min + (eta_max - eta_min) (1 + cos(pi t / total)) / 2."""
    if t >= total:
        return eta_min
    return eta_min + (eta_max - eta_min) * (1 + math.cos(math.pi * t / total)) / 2


def sgdr_position(t, t0, t_mult):
    """Return (t_cur, t_i): the step inside the current cycle and its length.

    Cycle i has length t0 * t_mult ** i; the cycles follow each other.
    """
    t_i = t0
    while t >= t_i:
        t -= t_i
        t_i *= t_mult
    return t, t_i


def sgdr(t, eta_max, eta_min, t0, t_mult=1):
    """Cosine annealing with warm restarts (Loshchilov and Hutter 2017)."""
    t_cur, t_i = sgdr_position(t, t0, t_mult)
    return eta_min + (eta_max - eta_min) * (1 + math.cos(math.pi * t_cur / t_i)) / 2


def linear_warmup(t, warmup, eta_start, eta_peak, after):
    """Rise linearly from eta_start at t = 0 to eta_peak at t = warmup.

    From t = warmup on, return after(t - warmup), a schedule that should
    start at eta_peak.
    """
    if t < warmup:
        return eta_start + (eta_peak - eta_start) * Fraction(t, warmup)
    return after(t - warmup)


def linear_scaling(eta_ref, batch, batch_ref):
    """The linear scaling rule of Goyal et al.: eta = eta_ref * batch / batch_ref."""
    return eta_ref * Fraction(batch, batch_ref)


def inverse_sqrt(step, d_model, warmup):
    """Vaswani et al. (2017), equation 3, with step counted from 1.

    lrate = d_model^(-1/2) * min(step^(-1/2), step * warmup^(-3/2)).
    """
    if step < 1:
        raise ValueError("the inverse square root schedule counts steps from 1")
    return d_model ** -0.5 * min(step ** -0.5, step * warmup ** -1.5)


def one_cycle(t, total, eta_max, div=10, final_div=10000, cycle_frac=Fraction(9, 10)):
    """Smith's 1cycle policy with linear pieces.

    The cycle covers the first cycle_frac of the steps: the rate rises
    linearly from eta_max / div to eta_max in the first half of the cycle
    and falls back to eta_max / div in the second half. In the remaining
    steps it falls linearly to eta_max / final_div.
    """
    low = eta_max / div if isinstance(eta_max, float) else Fraction(eta_max) / div
    end = eta_max / final_div if isinstance(eta_max, float) else Fraction(eta_max) / final_div
    cycle = int(total * cycle_frac)
    half = cycle // 2
    if t <= half:
        return low + (eta_max - low) * Fraction(t, half)
    if t <= 2 * half:
        return eta_max - (eta_max - low) * Fraction(t - half, half)
    rest = total - 2 * half
    if t >= total:
        return end
    return low - (low - end) * Fraction(t - 2 * half, rest)


def one_cycle_momentum(t, total, beta_max=Fraction(95, 100), beta_min=Fraction(85, 100), cycle_frac=Fraction(9, 10)):
    """The momentum that goes with one_cycle: it falls while the rate rises."""
    cycle = int(total * cycle_frac)
    half = cycle // 2
    if t <= half:
        return beta_max - (beta_max - beta_min) * Fraction(t, half)
    if t <= 2 * half:
        return beta_min + (beta_max - beta_min) * Fraction(t - half, half)
    return beta_max


def train_with_schedule(theta, grad, schedule, steps, direction=None, batches=None):
    """Run TRAIN-WITH-SCHEDULE on a scalar parameter.

    grad(theta, batch) is the minibatch gradient, direction(g) is the
    optimizer direction (the gradient itself for plain SGD) and schedule(t)
    is the learning rate. Returns the list of iterates theta_0, ..., theta_T.
    """
    direction = direction or (lambda g: g)
    path = [theta]
    for t in range(steps):  # @line L1
        batch = batches[t] if batches is not None else None  # @line L2
        g = grad(theta, batch)  # @line L3
        u = direction(g)  # @line L4
        eta = schedule(t)  # @line L5
        theta = theta - eta * u  # @line L6
        path.append(theta)
    return path  # @line L7


def sgd_with_schedule(grad, w, schedule, steps):
    """Plain gradient descent w <- w - eta_t * grad(w) with eta_t = schedule(t)."""
    return train_with_schedule(w, lambda th, _b: grad(th), schedule, steps)
