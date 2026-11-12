# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/he-initialization/. The authors are listed in prov/ACVN3F.jsonl.
"""He (Kaiming) initialization for ReLU networks, the exact factor 1/2 of the rectifier, and a
simulation of the forward and backward second moments through a deep ReLU multilayer perceptron.

A weight matrix of a layer with fan_in inputs and fan_out outputs has fan_out rows and fan_in columns.
"""

import math
import random
from collections.abc import Callable
from fractions import Fraction

Vec = list[float]
Mat = list[list[float]]
Init = Callable[[int, int, random.Random], Mat]


def he_variance(fan_in: int, slope: Fraction = Fraction(0)) -> Fraction:
    """2 / ((1 + a^2) fan_in) for a leaky rectifier with negative slope a; a = 0 is ReLU."""
    return Fraction(2) / ((1 + slope * slope) * fan_in)


def he_normal(fan_in: int, fan_out: int, rng: random.Random) -> Mat:
    s = math.sqrt(2 / fan_in)
    return [[rng.gauss(0.0, s) for _ in range(fan_in)] for _ in range(fan_out)]


def he_uniform(fan_in: int, fan_out: int, rng: random.Random) -> Mat:
    a = math.sqrt(6 / fan_in)  # variance a^2 / 3 = 2 / fan_in
    return [[rng.uniform(-a, a) for _ in range(fan_in)] for _ in range(fan_out)]


def normal_with_variance(var_of_fan_in: Callable[[int], float]) -> Init:
    """Gaussian weights whose variance is a function of the fan-in, for comparisons."""
    def init(fan_in: int, fan_out: int, rng: random.Random) -> Mat:
        s = math.sqrt(var_of_fan_in(fan_in))
        return [[rng.gauss(0.0, s) for _ in range(fan_in)] for _ in range(fan_out)]
    return init


def leaky_relu(z: float, slope: float = 0.0) -> float:
    return z if z > 0 else slope * z


def second_moment_after(dist: list[tuple[Fraction, Fraction]], slope: Fraction = Fraction(0)) -> Fraction:
    """E[f(z)^2] for a leaky rectifier f and a finite law given as (value, probability) pairs."""
    return sum((p * (z if z > 0 else slope * z) ** 2 for z, p in dist), Fraction(0))


def second_moment(dist: list[tuple[Fraction, Fraction]]) -> Fraction:
    return sum((p * z * z for z, p in dist), Fraction(0))


def mean_square(vs: list[Vec]) -> float:
    return sum(v * v for vec in vs for v in vec) / sum(len(vec) for vec in vs)


def relu_network_moments(widths: list[int], init: Init, samples: int,
                         rng: random.Random) -> tuple[list[float], list[float]]:
    """Draw z_1 = W_1 x and z_l = W_l relu(z_(l-1)) with x ~ N(0, I). Then send g_L ~ N(0, I) back with
    g_(l-1) = relu'(z_(l-1)) * (W_l^T g_l). Return the mean squares of z_1 .. z_L and of g_L .. g_1."""
    ws = [init(widths[i], widths[i + 1], rng) for i in range(len(widths) - 1)]
    xs = [[rng.gauss(0.0, 1.0) for _ in range(widths[0])] for _ in range(samples)]
    layers: list[list[Vec]] = []
    hs = xs
    for w in ws:
        zs = [[sum(a * b for a, b in zip(row, h)) for row in w] for h in hs]
        layers.append(zs)
        hs = [[max(v, 0.0) for v in z] for z in zs]
    fwd = [mean_square(zs) for zs in layers]
    gs = [[rng.gauss(0.0, 1.0) for _ in range(widths[-1])] for _ in range(samples)]
    bwd = [mean_square(gs)]
    for l in range(len(ws) - 1, 0, -1):
        w, below = ws[l], layers[l - 1]
        new = []
        for g, z in zip(gs, below):
            back = [0.0] * len(w[0])
            for row, gi in zip(w, g):
                for j, a in enumerate(row):
                    back[j] += a * gi
            new.append([b if zj > 0 else 0.0 for b, zj in zip(back, z)])
        gs = new
        bwd.append(mean_square(gs))
    return fwd, bwd
