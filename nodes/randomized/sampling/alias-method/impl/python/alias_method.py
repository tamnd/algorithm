# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alias-method/. The authors are listed in prov/95DG3T.jsonl.

"""Walker's alias method with Vose's linear-time construction.

The main version is exact. The weights are non-negative integers (or
fractions, which are scaled to integers), all table entries are integers,
and a sample uses two uniform integer draws. So the sample is i with
probability exactly w[i] / W, where W = sum(w), in the model where the
generator gives exact uniform integers. Construction takes O(n) arithmetic
operations and a sample takes O(1).

A float version is also given. It is the version most libraries use. It is
exact only up to the rounding of the table entries.
"""

import math
import random
from fractions import Fraction
from typing import List, Sequence, Tuple, Union

Number = Union[int, Fraction]


def to_integer_weights(weights: Sequence[Number]) -> List[int]:
    """Scale non-negative rational weights to integers with the same ratios."""
    fr = [Fraction(w) for w in weights]
    if any(w < 0 for w in fr):
        raise ValueError("weights must be non-negative")
    den = 1
    for w in fr:
        den = den * w.denominator // math.gcd(den, w.denominator)
    return [int(w * den) for w in fr]


def alias_build(weights: Sequence[Number]) -> Tuple[List[int], List[int], int]:
    """Build the alias table (prob, alias, W) for the given weights.

    Precondition: at least one weight, all weights >= 0, and the sum > 0.
    Column i keeps itself when a uniform t in [0, W) is below prob[i],
    and gives alias[i] otherwise. Cost: O(n) operations on integers.
    """
    w = to_integer_weights(weights)
    n = len(w)
    if n == 0 or sum(w) == 0:
        raise ValueError("need at least one positive weight")
    W = sum(w)  # @line L1
    q = [n * wi for wi in w]  # @line L1
    small = [i for i in range(n) if q[i] < W]  # @line L2
    large = [i for i in range(n) if q[i] >= W]  # @line L2
    prob = [0] * n
    alias = list(range(n))
    while small and large:  # @line L3
        l = small.pop()  # @line L4
        g = large.pop()  # @line L4
        prob[l] = q[l]  # @line L5
        alias[l] = g  # @line L5
        q[g] = q[g] - (W - q[l])  # @line L6
        if q[g] < W:  # @line L7
            small.append(g)  # @line L7
        else:
            large.append(g)  # @line L7
    for i in large + small:  # @line L8
        prob[i] = W  # @line L8
        alias[i] = i  # @line L8
    return prob, alias, W  # @line L9


def alias_sample(prob: List[int], alias: List[int], W: int, rng: random.Random) -> int:
    """Draw one index from the table. Two uniform integer draws, O(1) time."""
    i = rng.randrange(len(prob))  # @line L10
    t = rng.randrange(W)  # @line L11
    if t < prob[i]:  # @line L12
        return i  # @line L12
    return alias[i]  # @line L12


def alias_distribution(prob: List[int], alias: List[int], W: int) -> List[Fraction]:
    """The exact output distribution of a table, by counting the n * W outcomes."""
    n = len(prob)
    count = [0] * n
    for i in range(n):
        count[i] += prob[i]
        count[alias[i]] += W - prob[i]
    return [Fraction(c, n * W) for c in count]


def alias_build_float(p: Sequence[float]) -> Tuple[List[float], List[int]]:
    """Vose's construction in floating point. p need not sum to exactly 1.

    The leftover columns get probability 1. This hides the rounding error
    of the loop, so the table is exact only up to that rounding.
    """
    n = len(p)
    total = math.fsum(p)
    q = [n * x / total for x in p]
    small = [i for i in range(n) if q[i] < 1.0]
    large = [i for i in range(n) if q[i] >= 1.0]
    prob = [0.0] * n
    alias = list(range(n))
    while small and large:
        l = small.pop()
        g = large.pop()
        prob[l] = q[l]
        alias[l] = g
        q[g] = (q[g] + q[l]) - 1.0
        if q[g] < 1.0:
            small.append(g)
        else:
            large.append(g)
    for i in large + small:
        prob[i] = 1.0
    return prob, alias


def alias_sample_float(prob: List[float], alias: List[int], rng: random.Random) -> int:
    """Draw one index from a float table with one integer and one float draw."""
    i = rng.randrange(len(prob))
    return i if rng.random() < prob[i] else alias[i]
