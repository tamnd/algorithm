# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-family-distribution/. The authors are listed in prov/RGQ0M9.jsonl.

"""Exponential families p(x | eta) = h(x) exp(eta . T(x) - A(eta)).

Each family gives h, T and the closed-form log-partition A. The module
also computes A, E[T] and Cov[T] directly from the definition (by sums
or by the midpoint rule), finite-difference derivatives of A, the
maximum entropy distribution on a finite set with a given mean, and the
log-likelihood of an i.i.d. sample through the sufficient statistic.
"""

import math
from dataclasses import dataclass
from typing import Callable, List, Sequence


@dataclass
class Family:
    name: str
    T: Callable[[float], List[float]]
    log_h: Callable[[float], float]
    A: Callable[[Sequence[float]], float]
    support: str  # "binary", "count" or "real"


BERNOULLI = Family("Bernoulli", lambda x: [x], lambda x: 0.0, lambda e: math.log1p(math.exp(e[0])), "binary")
POISSON = Family("Poisson", lambda x: [x], lambda x: -math.lgamma(x + 1), lambda e: math.exp(e[0]), "count")
GAUSSIAN = Family(
    "Gaussian",
    lambda x: [x, x * x],
    lambda x: -0.5 * math.log(2 * math.pi),
    lambda e: -e[0] ** 2 / (4 * e[1]) - 0.5 * math.log(-2 * e[1]),
    "real",
)


def gaussian_natural(mu: float, var: float) -> List[float]:
    return [mu / var, -1 / (2 * var)]


def _points(fam: Family, eta: Sequence[float]):
    """Support points with their weights for summation or the midpoint rule."""
    if fam.support == "binary":
        return [(0, 1.0), (1, 1.0)]
    if fam.support == "count":
        return [(k, 1.0) for k in range(400)]
    mu = -eta[0] / (2 * eta[1])
    sd = math.sqrt(-1 / (2 * eta[1]))
    m, lo, hi = 40000, mu - 14 * sd, mu + 14 * sd
    h = (hi - lo) / m
    return [(lo + (i + 0.5) * h, h) for i in range(m)]


def _log_terms(fam: Family, eta: Sequence[float]):
    pts = _points(fam, eta)
    logs = [fam.log_h(x) + sum(e * t for e, t in zip(eta, fam.T(x))) + math.log(w) for x, w in pts]
    return pts, logs


def log_partition_direct(fam: Family, eta: Sequence[float]) -> float:
    """A(eta) = log of the sum (or integral) of h(x) exp(eta . T(x))."""
    _, logs = _log_terms(fam, eta)
    top = max(logs)
    return top + math.log(sum(math.exp(v - top) for v in logs))


def moments_direct(fam: Family, eta: Sequence[float]):
    """E[T] and Cov[T] under p(. | eta), from the definition."""
    pts, logs = _log_terms(fam, eta)
    top = max(logs)
    w = [math.exp(v - top) for v in logs]
    z = sum(w)
    ts = [fam.T(x) for x, _ in pts]
    d = len(ts[0])
    mean = [sum(wi * t[j] for wi, t in zip(w, ts)) / z for j in range(d)]
    cov = [[sum(wi * (t[j] - mean[j]) * (t[k] - mean[k]) for wi, t in zip(w, ts)) / z for k in range(d)] for j in range(d)]
    return mean, cov


def gradient(f: Callable[[Sequence[float]], float], eta: Sequence[float], h: float = 1e-5) -> List[float]:
    out = []
    for j in range(len(eta)):
        up = list(eta)
        dn = list(eta)
        up[j] += h
        dn[j] -= h
        out.append((f(up) - f(dn)) / (2 * h))
    return out


def hessian(f: Callable[[Sequence[float]], float], eta: Sequence[float], h: float = 1e-4) -> List[List[float]]:
    d = len(eta)
    H = [[0.0] * d for _ in range(d)]
    for j in range(d):
        for k in range(d):
            def at(dj: float, dk: float) -> float:
                e = list(eta)
                e[j] += dj
                e[k] += dk
                return f(e)
            H[j][k] = (at(h, h) - at(h, -h) - at(-h, h) + at(-h, -h)) / (4 * h * h)
    return H


def log_likelihood(fam: Family, eta: Sequence[float], xs: Sequence[float]) -> float:
    """sum_i log h(x_i) + eta . sum_i T(x_i) - n A(eta): the data enter through sum T."""
    n = len(xs)
    s = [sum(c) for c in zip(*(fam.T(x) for x in xs))]
    return sum(fam.log_h(x) for x in xs) + sum(e * t for e, t in zip(eta, s)) - n * fam.A(eta)


def max_entropy_on_finite_set(values: Sequence[float], target_mean: float) -> List[float]:
    """The distribution on `values` with mean target_mean and maximum entropy.

    It is p_k proportional to exp(eta * values[k]); eta solves A'(eta) =
    target_mean, found by bisection (A' is increasing because A is convex).
    """
    if not min(values) < target_mean < max(values):
        raise ValueError("the mean must lie strictly inside the range of the values")

    def dist(eta: float) -> List[float]:
        top = max(eta * v for v in values)
        w = [math.exp(eta * v - top) for v in values]
        z = sum(w)
        return [x / z for x in w]

    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if sum(p * v for p, v in zip(dist(mid), values)) < target_mean:
            lo = mid
        else:
            hi = mid
    return dist((lo + hi) / 2)


def entropy(p: Sequence[float]) -> float:
    return -sum(x * math.log(x) for x in p if x > 0)
