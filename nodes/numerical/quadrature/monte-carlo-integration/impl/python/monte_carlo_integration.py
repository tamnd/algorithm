# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-integration/. The authors are listed in prov/2FTF47.jsonl.

import math
import random
from typing import Callable, List, Sequence, Tuple


def monte_carlo(
    f: Callable[[List[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    n: int,
    rng: random.Random,
) -> Tuple[float, float]:
    """Plain Monte Carlo estimate of the integral of f over a box.

    The box is [lower[0], upper[0]] x ... x [lower[s-1], upper[s-1]], s >= 1.
    Precondition: n >= 2 samples; rng is a seeded random.Random, so a run is
    reproducible. If upper[k] < lower[k] for an odd number of k, the result is
    the oriented integral, with the same sign convention as in one dimension.
    Returns (estimate, standard error), the standard error being the sample
    standard deviation of V*f(X) divided by sqrt(n).
    Cost: exactly n evaluations of f, n*s uniform variates, O(1) extra memory
    besides one point. The mean and variance use Welford's one-pass update.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    if len(lower) != len(upper) or not lower:
        raise ValueError("lower and upper must have the same positive length")
    vol = 1.0
    for a, b in zip(lower, upper):
        vol *= b - a  # @line L1
    mean = 0.0  # @line L2
    m2 = 0.0
    for j in range(1, n + 1):  # @line L3
        x = [a + (b - a) * rng.random() for a, b in zip(lower, upper)]  # @line L4
        y = f(x)  # @line L5
        delta = y - mean  # @line L6
        mean += delta / j
        m2 += delta * (y - mean)
    var = m2 / (n - 1)  # @line L7
    return vol * mean, abs(vol) * math.sqrt(var / n)  # @line L8
