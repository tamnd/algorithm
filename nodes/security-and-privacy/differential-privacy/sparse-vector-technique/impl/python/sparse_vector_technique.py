# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-vector-technique/. The authors are listed in prov/QVW2C4.jsonl.
"""The sparse vector technique: AboveThreshold and its cutoff form Sparse.

This follows Dwork and Roth (2014), Algorithms 1 and 2. A query is a
function from the dataset to a real number with sensitivity at most
`sensitivity` under the neighbor relation the caller uses (add/remove in the
tests). The queries may be chosen adaptively: `queries` may be a generator
that looks at the earlier outputs.

The code uses random.Random so that the tests can be repeated, and it adds
float noise. Both are fine for study and wrong for a deployment: a real
release needs a cryptographic source of randomness and an exact sampler,
because float noise leaks through its low-order bits (Mironov 2012;
Canonne, Kamath and Steinke 2020).
"""

from __future__ import annotations

import math
import random
from typing import Callable, Iterable, TypeVar

D = TypeVar("D")


def laplace_noise(b: float, rng: random.Random) -> float:
    """One draw of Lap(b), the density (1/(2b)) exp(-|z|/b), by the inverse CDF.

    Precondition: b > 0. Cost: one uniform draw and O(1) time.
    """
    u = rng.random() - 0.5
    while u == -0.5:  # the open interval (-1/2, 1/2) excludes -1/2
        u = rng.random() - 0.5
    s = (u > 0) - (u < 0)
    return -b * s * math.log(1.0 - 2.0 * abs(u))


def above_threshold(
    x: D,
    queries: Iterable[Callable[[D], float]],
    threshold: float,
    sensitivity: float,
    epsilon: float,
    rng: random.Random,
) -> list[bool]:
    """Run AboveThreshold and return its outputs: False for bottom, True for top.

    The run stops after the first True, or when the queries run out.
    Precondition: every query has sensitivity at most `sensitivity` > 0, and
    epsilon > 0. Then the output list is epsilon-DP (Dwork-Roth Theorem 3.23).
    Cost: one evaluation of each query asked, and one Laplace draw per query
    plus one for the threshold.
    """
    if sensitivity <= 0 or epsilon <= 0:
        raise ValueError("sensitivity and epsilon must be positive")
    t_hat = threshold + laplace_noise(2.0 * sensitivity / epsilon, rng)  # @line L1
    out: list[bool] = []
    for f in queries:  # @line L2
        nu = laplace_noise(4.0 * sensitivity / epsilon, rng)  # @line L3
        if f(x) + nu >= t_hat:  # @line L4
            out.append(True)  # @line L5
            return out
        out.append(False)  # @line L6
    return out


def sparse(
    x: D,
    queries: Iterable[Callable[[D], float]],
    threshold: float,
    cutoff: int,
    sensitivity: float,
    epsilon: float,
    rng: random.Random,
) -> list[bool]:
    """Sparse with cutoff c and delta = 0 (Dwork-Roth Algorithm 2).

    It is AboveThreshold run again after each top, with sigma = 2 c sensitivity / epsilon
    for the threshold noise and 2 sigma for the query noise, and a fresh
    noisy threshold after each top. It stops after `cutoff` tops. The output
    is epsilon-DP by basic composition of `cutoff` runs that are each
    (epsilon / cutoff)-DP. Cost: as above_threshold, per query.
    """
    if cutoff < 1:
        raise ValueError("cutoff must be at least 1")
    sigma = 2.0 * cutoff * sensitivity / epsilon
    t_hat = threshold + laplace_noise(sigma, rng)
    out: list[bool] = []
    count = 0
    for f in queries:
        nu = laplace_noise(2.0 * sigma, rng)
        if f(x) + nu >= t_hat:
            out.append(True)
            count += 1
            if count >= cutoff:
                return out
            t_hat = threshold + laplace_noise(sigma, rng)
        else:
            out.append(False)
    return out


def accuracy_alpha(k: int, beta: float, epsilon: float, sensitivity: float = 1.0) -> float:
    """The alpha of Dwork-Roth Theorem 3.24: 8 sensitivity (ln k + ln(2 / beta)) / epsilon.

    With probability at least 1 - beta, over a stream of k queries, no top
    has a value below T - alpha and no bottom has a value above T + alpha.
    """
    return 8.0 * sensitivity * (math.log(k) + math.log(2.0 / beta)) / epsilon
