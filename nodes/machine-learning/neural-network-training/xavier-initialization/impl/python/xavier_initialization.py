# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xavier-initialization/. The authors are listed in prov/HGZT7G.jsonl.
"""Xavier (Glorot) initialization of a multilayer perceptron, and a simulation of the forward and
backward second moments through depth.

A weight matrix of a layer with fan_in inputs and fan_out outputs has fan_out rows and fan_in columns.
Xavier draws each entry i.i.d. with mean 0 and variance 2 / (fan_in + fan_out).
"""

import math
import random
from collections.abc import Callable
from fractions import Fraction

Vec = list[float]
Mat = list[list[float]]
Init = Callable[[int, int, random.Random], Mat]


def xavier_variance(fan_in: int, fan_out: int) -> Fraction:
    """The target variance 2 / (fan_in + fan_out), the harmonic mean of 1 / fan_in and 1 / fan_out."""
    return Fraction(2, fan_in + fan_out)


def xavier_uniform_limit(fan_in: int, fan_out: int) -> float:
    """The limit a of U[-a, a] with a^2 / 3 = 2 / (fan_in + fan_out), so a = sqrt(6 / (fan_in + fan_out))."""
    return math.sqrt(6 / (fan_in + fan_out))


def xavier_uniform(fan_in: int, fan_out: int, rng: random.Random) -> Mat:
    a = xavier_uniform_limit(fan_in, fan_out)
    return [[rng.uniform(-a, a) for _ in range(fan_in)] for _ in range(fan_out)]


def xavier_normal(fan_in: int, fan_out: int, rng: random.Random) -> Mat:
    s = math.sqrt(2 / (fan_in + fan_out))
    return [[rng.gauss(0.0, s) for _ in range(fan_in)] for _ in range(fan_out)]


def scaled_normal(factor: float) -> Init:
    """Gaussian weights with variance factor * 2 / (fan_in + fan_out), to show a mismatched scale."""
    def init(fan_in: int, fan_out: int, rng: random.Random) -> Mat:
        s = math.sqrt(factor * 2 / (fan_in + fan_out))
        return [[rng.gauss(0.0, s) for _ in range(fan_in)] for _ in range(fan_out)]
    return init


def matvec(w: Mat, x: Vec) -> Vec:
    return [sum(a * b for a, b in zip(row, x)) for row in w]


def matvec_t(w: Mat, g: Vec) -> Vec:
    """W^T g, the backward pass of z = W x with respect to x."""
    out = [0.0] * len(w[0])
    for row, gi in zip(w, g):
        for j, a in enumerate(row):
            out[j] += a * gi
    return out


def mean_square(vs: list[Vec]) -> float:
    return sum(v * v for vec in vs for v in vec) / sum(len(vec) for vec in vs)


def forward_moments(widths: list[int], init: Init, act: Callable[[float], float], samples: int,
                    rng: random.Random) -> list[float]:
    """Draw one network z_l = W_l act(z_(l-1)) with z_0 = x, x ~ N(0, I), and return the mean square of
    z_l for l = 0 .. L over the samples. For act = identity this is the forward variance of the layer."""
    ws = [init(widths[i], widths[i + 1], rng) for i in range(len(widths) - 1)]
    zs = [[rng.gauss(0.0, 1.0) for _ in range(widths[0])] for _ in range(samples)]
    out = [mean_square(zs)]
    for w in ws:
        zs = [matvec(w, [act(v) for v in z]) for z in zs]
        out.append(mean_square(zs))
    return out


def backward_moments(widths: list[int], init: Init, samples: int, rng: random.Random) -> list[float]:
    """Draw one linear network and send gradients g_L ~ N(0, I) back with g_(l-1) = W_l^T g_l.
    Return the mean square of g_l for l = L down to 0."""
    ws = [init(widths[i], widths[i + 1], rng) for i in range(len(widths) - 1)]
    gs = [[rng.gauss(0.0, 1.0) for _ in range(widths[-1])] for _ in range(samples)]
    out = [mean_square(gs)]
    for w in reversed(ws):
        gs = [matvec_t(w, g) for g in gs]
        out.append(mean_square(gs))
    return out
