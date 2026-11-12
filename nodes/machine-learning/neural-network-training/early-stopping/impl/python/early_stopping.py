# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/early-stopping/. The authors are listed in prov/56QAAE.jsonl.
"""Early stopping with a patience rule: train, evaluate on held-out data every few steps, keep the best
parameters, and stop after `patience` evaluations without improvement. Also Prechelt's generalization
loss criterion, and the spectral filter of gradient descent on least squares that relates the number of
steps to a ridge penalty.
"""

import random
from typing import Callable


def early_stopping(step: Callable[[], None], params: Callable[[], object], val_loss: Callable[[], float],
                   eval_every: int, patience: int, max_steps: int) -> tuple[object, int, list[float]]:
    """Run `step` up to max_steps times, evaluating every eval_every steps. Stop once `patience`
    evaluations in a row have not improved on the best validation loss. Return the best parameters,
    the step at which they were seen, and the validation curve."""
    best, best_step, best_params = val_loss(), 0, params()
    curve = [best]
    bad, t = 0, 0
    while t < max_steps and bad < patience:
        for _ in range(eval_every):
            step()
            t += 1
        v = val_loss()
        curve.append(v)
        if v < best:
            best, best_step, best_params, bad = v, t, params(), 0
        else:
            bad += 1
    return best_params, best_step, curve


def generalization_loss(curve: list[float]) -> list[float]:
    """Prechelt's GL(t) = 100 (E_va(t) / min_{t' <= t} E_va(t') - 1)."""
    out, low = [], float("inf")
    for e in curve:
        low = min(low, e)
        out.append(100 * (e / low - 1))
    return out


def stop_by_gl(curve: list[float], alpha: float) -> int:
    """The first index at which GL exceeds alpha, or the last index if it never does."""
    for i, g in enumerate(generalization_loss(curve)):
        if g > alpha:
            return i
    return len(curve) - 1


def gd_least_squares(sigma: list, c: list, eta, steps: int) -> list:
    """Gradient descent from 0 on f(w) = (1/2) w^T Sigma w - c^T w, the least squares loss with
    Sigma = X^T X / n and c = X^T y / n. Returns all iterates w_0, ..., w_steps."""
    d = len(c)
    w = [0 * c[0]] * d
    out = [w]
    for _ in range(steps):
        g = [sum(sigma[i][j] * w[j] for j in range(d)) - c[i] for i in range(d)]
        w = [wi - eta * gi for wi, gi in zip(w, g)]
        out.append(w)
    return out


def gd_filter(s, eta, t: int):
    """The spectral filter of t steps of gradient descent: g_t(s) = (1 - (1 - eta s)^t) / s, and eta t at s = 0."""
    if s == 0:
        return eta * t
    return (1 - (1 - eta * s) ** t) / s


def ridge_filter(s, lam):
    """The spectral filter of ridge regression: 1 / (s + lam)."""
    return 1 / (s + lam)


def make_regression(rng: random.Random, n: int, d: int, noise: float) -> tuple[list, list]:
    """Rows with Gaussian features and a linear target with decaying coefficients plus Gaussian noise."""
    coef = [1.0 / (j + 1) for j in range(d)]
    xs = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n)]
    ys = [sum(a * b for a, b in zip(coef, x)) + noise * rng.gauss(0.0, 1.0) for x in xs]
    return xs, ys


def mse(w: list, xs: list, ys: list) -> float:
    return sum((sum(a * b for a, b in zip(w, x)) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def train_least_squares_with_early_stopping(train: tuple, val: tuple, eta: float, patience: int,
                                            max_steps: int) -> tuple[list, int, list[float]]:
    """Full-batch gradient descent on the training mean squared error, stopped by the patience rule."""
    xs, ys = train
    d, n = len(xs[0]), len(xs)
    state = {"w": [0.0] * d}

    def step() -> None:
        w = state["w"]
        r = [sum(a * b for a, b in zip(w, x)) - y for x, y in zip(xs, ys)]
        g = [2 * sum(ri * x[j] for ri, x in zip(r, xs)) / n for j in range(d)]
        state["w"] = [a - eta * b for a, b in zip(w, g)]

    return early_stopping(step, lambda: list(state["w"]), lambda: mse(state["w"], *val), 1, patience, max_steps)
