# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-bootstrap/. The authors are listed in prov/Q86QP6.jsonl.

import math
import random
from typing import Callable, Sequence

Statistic = Callable[[Sequence[float]], float]


def moving_block_resample(x: Sequence[float], l: int, rng: random.Random) -> list:
    """One moving block bootstrap resample of Kunsch (1989): k = ceil(n/l) blocks of l
    consecutive values, with start points drawn uniformly from the N = n - l + 1 possible ones,
    joined and cut to length n."""
    n = len(x)
    if not 1 <= l <= n:
        raise ValueError("need 1 <= l <= n")
    k = -(-n // l)  # @line L1
    big_n = n - l + 1
    out = []  # @line L3
    for _ in range(k):  # @line L4
        start = rng.randrange(big_n)  # @line L5
        out.extend(x[start : start + l])  # @line L6
    return out[:n]  # @line L7


def circular_block_resample(x: Sequence[float], l: int, rng: random.Random) -> list:
    """Politis and Romano (1992): blocks may wrap around the end, so all n start points are used."""
    n = len(x)
    if not 1 <= l <= n:
        raise ValueError("need 1 <= l <= n")
    out = []
    for _ in range(-(-n // l)):
        start = rng.randrange(n)
        out.extend(x[(start + t) % n] for t in range(l))
    return out[:n]


def stationary_resample(x: Sequence[float], p: float, rng: random.Random) -> list:
    """Politis and Romano (1994): blocks of geometric length with mean 1/p, which wrap around.
    Each step starts a new block with probability p, else it continues the current one."""
    n = len(x)
    if not 0 < p <= 1:
        raise ValueError("need 0 < p <= 1")
    i = rng.randrange(n)
    out = [x[i]]
    while len(out) < n:
        i = rng.randrange(n) if rng.random() < p else (i + 1) % n
        out.append(x[i])
    return out


def block_bootstrap(
    x: Sequence[float],
    statistic: Statistic,
    b: int,
    rng: random.Random,
    l: int | None = None,
    method: str = "moving",
    p: float | None = None,
) -> list:
    """b block bootstrap replicates of the statistic. method is 'moving', 'circular' or 'stationary'."""
    reps = []
    for _ in range(b):  # @line L2
        if method == "moving":
            xs = moving_block_resample(x, l, rng)
        elif method == "circular":
            xs = circular_block_resample(x, l, rng)
        elif method == "stationary":
            xs = stationary_resample(x, p if p is not None else 1.0 / l, rng)
        else:
            raise ValueError("unknown method")
        reps.append(statistic(xs))  # @line L8
    return reps  # @line L9


def standard_deviation(values: Sequence[float]) -> float:
    m = math.fsum(values) / len(values)
    return math.sqrt(math.fsum((v - m) ** 2 for v in values) / (len(values) - 1))


def mbb_mean_moments(x: Sequence, l: int) -> tuple:
    """The exact bootstrap mean and variance of the resample mean under the moving block
    bootstrap, when l divides n: the resample mean is the average of k = n/l block means drawn
    independently and uniformly from the N = n - l + 1 block means."""
    n = len(x)
    if n % l:
        raise ValueError("this closed form needs l to divide n")
    k, big_n = n // l, n - l + 1
    blocks = [sum(x[j : j + l]) / l for j in range(big_n)]
    centre = sum(blocks) / big_n
    return centre, sum((v - centre) ** 2 for v in blocks) / (big_n * k)


def circular_autocovariance(x: Sequence, lag: int):
    n = len(x)
    m = sum(x) / n
    return sum((x[j] - m) * (x[(j + lag) % n] - m) for j in range(n)) / n


def stationary_mean_variance(x: Sequence, p) -> object:
    """The exact bootstrap variance of the resample mean under the stationary bootstrap
    (Politis and Romano 1994): c(0)/n + (2/n) sum_{i=1}^{n-1} (1 - i/n) (1 - p)^i c(i),
    with the circular autocovariances c(i)."""
    n = len(x)
    total = circular_autocovariance(x, 0) / n
    for i in range(1, n):
        total += 2 * (n - i) * (1 - p) ** i * circular_autocovariance(x, i) / (n * n)
    return total
