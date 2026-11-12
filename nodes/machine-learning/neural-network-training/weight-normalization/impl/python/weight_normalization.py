# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-normalization/. The authors are listed in prov/88JWRJ.jsonl.
"""Weight normalization (Salimans and Kingma 2016): w = g v / ||v||. The gradients with respect to the
scale g and the direction parameter v, the data-dependent initialization, and a logistic unit trained
with it by gradient descent.
"""

import math
import random

Vec = list[float]


def dot(a: Vec, b: Vec) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: Vec) -> float:
    return math.sqrt(dot(a, a))


def weight(v: Vec, g: float) -> Vec:
    """w = g v / ||v||, so ||w|| = |g| and w points along v (for g > 0)."""
    n = norm(v)
    return [g * x / n for x in v]


def wn_grads(v: Vec, g: float, grad_w: Vec) -> tuple[float, Vec]:
    """Given dL/dw, return dL/dg = (dL/dw . v) / ||v|| and
    dL/dv = (g / ||v||) dL/dw - (g dL/dg / ||v||^2) v."""
    n2 = dot(v, v)
    n = math.sqrt(n2)
    gg = dot(grad_w, v) / n
    gv = [g / n * a - g * gg / n2 * x for a, x in zip(grad_w, v)]
    return gg, gv


def wn_grads_exact(v: list, g, grad_w: list, norm_v) -> tuple:
    """The same formulas for exact types (fractions) when ||v|| is known exactly."""
    n2 = sum(x * x for x in v)
    gg = sum(a * x for a, x in zip(grad_w, v)) / norm_v
    gv = [g / norm_v * a - g * gg / n2 * x for a, x in zip(grad_w, v)]
    return gg, gv


def sigmoid(t: float) -> float:
    if t >= 0:
        return 1 / (1 + math.exp(-t))
    e = math.exp(t)
    return e / (1 + e)


def logistic_loss(w: Vec, b: float, xs: list[Vec], ys: list[int]) -> float:
    """The mean logistic loss of the unit sigma(w . x + b) on labels in {0, 1}."""
    total = 0.0
    for x, y in zip(xs, ys):
        t = dot(w, x) + b
        total += math.log1p(math.exp(-abs(t))) + max(t, 0.0) - y * t
    return total / len(xs)


def logistic_grad(w: Vec, b: float, xs: list[Vec], ys: list[int]) -> tuple[Vec, float]:
    gw = [0.0] * len(w)
    gb = 0.0
    for x, y in zip(xs, ys):
        r = sigmoid(dot(w, x) + b) - y
        gb += r
        for j, xj in enumerate(x):
            gw[j] += r * xj
    m = len(xs)
    return [a / m for a in gw], gb / m


def data_dependent_init(v: Vec, xs: list[Vec]) -> tuple[float, float]:
    """Section 3 of Salimans and Kingma: with t = v . x / ||v|| over a batch, set g = 1 / std(t) and
    b = -mean(t) / std(t), so that the pre-activations g t + b have mean 0 and variance 1 on the batch."""
    n = norm(v)
    ts = [dot(v, x) / n for x in xs]
    mu = sum(ts) / len(ts)
    sd = math.sqrt(sum((t - mu) ** 2 for t in ts) / len(ts))
    return 1 / sd, -mu / sd


def train_unit(xs: list[Vec], ys: list[int], steps: int, eta: float, rng: random.Random) -> list[float]:
    """Gradient descent on (v, g, b) for a weight-normalized logistic unit. Returns the losses."""
    d = len(xs[0])
    v = [rng.gauss(0.0, 0.05) for _ in range(d)]
    g, b = data_dependent_init(v, xs)
    losses = []
    for _ in range(steps):
        w = weight(v, g)
        losses.append(logistic_loss(w, b, xs, ys))
        gw, gb = logistic_grad(w, b, xs, ys)
        gg, gv = wn_grads(v, g, gw)
        v = [a - eta * c for a, c in zip(v, gv)]
        g -= eta * gg
        b -= eta * gb
    return losses
