# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anderson-darling-test/. The authors are listed in prov/7ZCNKW.jsonl.

import math
import random
from typing import Callable


def ad_statistic_u(u: list[float]) -> float:
    """A^2 from the sorted values u_1 <= ... <= u_n of F_0 at the data."""
    n = len(u)
    if u[0] <= 0.0 or u[-1] >= 1.0:  # @line L2
        return math.inf
    s = math.fsum((2 * i - 1) * (math.log(u[i - 1]) + math.log1p(-u[n - i]))
                  for i in range(1, n + 1))  # @line L3
    return -n - s / n  # @line L4


def ad_statistic(x: list[float], cdf: Callable[[float], float]) -> float:
    """The Anderson-Darling statistic A^2 of the sample x against the CDF F_0."""
    return ad_statistic_u(sorted(cdf(v) for v in x))  # @line L1


def adinf_cdf(z: float, steps: int = 4000) -> float:
    """P(A^2_inf <= z) for the limit law A^2_inf = sum_j Z_j^2 / (j (j + 1)).

    Uses the series of Anderson and Darling (1954), in the form
    (sqrt(2 pi)/z) sum_j C(-1/2, j) (4j + 1) exp(-a_j) I_j with a_j = (4j + 1)^2 pi^2 / (8 z)
    and I_j = integral_0^inf exp(z / (8 (w^2 + 1)) - a_j w^2) dw, each I_j by Simpson's
    rule on [0, W] where the integrand is below exp(-40) beyond W.
    """
    if z <= 0.0:
        return 0.0
    total, coef, j = 0.0, 1.0, 0
    while True:
        a = (4 * j + 1) ** 2 * math.pi**2 / (8 * z)
        width = math.sqrt((40.0 + z / 8.0) / a)
        h = width / steps
        acc = 0.0
        for i in range(steps + 1):
            w = i * h
            f = math.exp(z / (8.0 * (w * w + 1.0)) - a * w * w)
            acc += f if i in (0, steps) else (4.0 * f if i % 2 else 2.0 * f)
        term = coef * (4 * j + 1) * math.exp(-a) * acc * h / 3.0
        total += term
        if abs(term) < 1e-17 and j > 2:
            break
        j += 1
        coef *= -(2 * j - 1) / (2 * j)
    return min(1.0, max(0.0, math.sqrt(2 * math.pi) / z * total))


def ad_test(
    x: list[float],
    cdf: Callable[[float], float],
    method: str = "asymptotic",
    b: int = 9999,
    rng: random.Random | None = None,
) -> tuple[float, float]:
    """Anderson-Darling test of H0: the data have the continuous, fully specified CDF F_0.

    Returns (A^2, p). method "asymptotic" uses the limit law; method
    "monte-carlo" simulates b samples of n uniforms (the exact null law of
    A^2 for every continuous F_0) and returns (1 + count) / (1 + b), where
    count is the number of simulated values at least the observed one.
    """
    if not x:
        raise ValueError("need at least one observation")
    a2 = ad_statistic(x, cdf)
    if math.isinf(a2):
        return a2, 0.0
    if method == "asymptotic":  # @line L5
        return a2, max(0.0, 1.0 - adinf_cdf(a2))
    if method != "monte-carlo":
        raise ValueError("unknown method")
    if rng is None:
        raise ValueError("pass rng = random.Random(seed) for the Monte Carlo p-value")
    n = len(x)
    count = 0
    for _ in range(b):  # @line L6
        sim = sorted(rng.random() for _ in range(n))
        if ad_statistic_u(sim) >= a2:
            count += 1
    return a2, (1 + count) / (1 + b)  # @line L7
