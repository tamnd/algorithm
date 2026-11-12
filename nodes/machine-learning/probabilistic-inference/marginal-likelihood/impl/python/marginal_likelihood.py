# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/marginal-likelihood/. The authors are listed in prov/04WZ19.jsonl.

"""Marginal likelihood (model evidence) for the beta-Bernoulli model.

The model: theta ~ Beta(a, b), and x_1..x_n are 0/1 outcomes that are
i.i.d. Bernoulli(theta) given theta. The evidence of one ordered sequence
with s ones and f zeros is B(a + s, b + f) / B(a, b). The module computes
it exactly, by the chain rule of predictive probabilities, by grid
integration, by the Laplace approximation and by the BIC formula.
"""

import math
from fractions import Fraction
from typing import Callable, Sequence


def log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def beta_int(a: int, b: int) -> Fraction:
    """B(a, b) = (a-1)! (b-1)! / (a+b-1)! for positive integers."""
    return Fraction(math.factorial(a - 1) * math.factorial(b - 1), math.factorial(a + b - 1))


def evidence_exact(a: int, b: int, data: Sequence[int]) -> Fraction:
    """p(x_1..x_n) = B(a + s, b + f) / B(a, b), exact, for integer a, b >= 1."""
    s = sum(data)
    return beta_int(a + s, b + len(data) - s) / beta_int(a, b)


def evidence_chain_rule(a: Fraction, b: Fraction, data: Sequence[int]) -> Fraction:
    """p(x_1..x_n) = prod_i p(x_i | x_1..x_{i-1}), one predictive step at a time."""
    a, b = Fraction(a), Fraction(b)
    p = Fraction(1)
    for x in data:
        up = a / (a + b)
        p *= up if x == 1 else 1 - up
        if x == 1:
            a += 1
        else:
            b += 1
    return p


def evidence_point(theta: Fraction, data: Sequence[int]) -> Fraction:
    """Evidence of the model with no free parameter: theta fixed."""
    s = sum(data)
    return Fraction(theta) ** s * (1 - Fraction(theta)) ** (len(data) - s)


def bayes_factor(p1: Fraction, p0: Fraction) -> Fraction:
    """K = p(D | M1) / p(D | M0). Posterior odds = K times prior odds."""
    return p1 / p0


def log_evidence(a: float, b: float, s: int, f: int) -> float:
    return log_beta(a + s, b + f) - log_beta(a, b)


def log_evidence_grid(prior: Callable[[float], float], s: int, f: int, m: int = 20000) -> float:
    """log of the integral of theta^s (1-theta)^f prior(theta) by the midpoint rule."""
    h = 1.0 / m
    logs = []
    for i in range(m):
        t = (i + 0.5) * h
        pr = prior(t)
        if pr > 0:
            logs.append(s * math.log(t) + f * math.log(1 - t) + math.log(pr))
    top = max(logs)
    return top + math.log(sum(math.exp(v - top) for v in logs) * h)


def log_evidence_laplace(a: float, b: float, s: int, f: int) -> float:
    """Laplace approximation in theta around the posterior mode.

    g(theta) = log p(D | theta) + log p(theta). Then
    log p(D) is about g(mode) + (1/2) log(2 pi) - (1/2) log(-g''(mode)).
    Needs a + s > 1 and b + f > 1 so that the mode is inside (0, 1).
    """
    al, be = a + s - 1, b + f - 1
    mode = al / (al + be)
    g = al * math.log(mode) + be * math.log(1 - mode) - log_beta(a, b)
    curv = al / mode ** 2 + be / (1 - mode) ** 2
    return g + 0.5 * math.log(2 * math.pi) - 0.5 * math.log(curv)


def log_evidence_bic(s: int, f: int, d: int = 1) -> float:
    """Schwarz: log p(D) is about log p(D | MLE) - (d/2) log n."""
    n = s + f
    ll = (s * math.log(s / n) if s else 0.0) + (f * math.log(f / n) if f else 0.0)
    return ll - 0.5 * d * math.log(n)
