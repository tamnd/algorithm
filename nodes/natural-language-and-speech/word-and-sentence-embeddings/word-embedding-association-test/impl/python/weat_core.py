# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-embedding-association-test/. The authors are listed in prov/R1EFZ2.jsonl.
"""The Word Embedding Association Test (WEAT) of Caliskan, Bryson and Narayanan 2017.

X and Y are two equal-size sets of target word vectors (for example flowers
and insects), and A and B are two sets of attribute word vectors (for example
pleasant and unpleasant words). The test returns the statistic s(X, Y, A, B),
the effect size d and the one-sided permutation p-value over the equal-size
partitions of X u Y. The vectors are given; the code does not train them.
"""

import math
import random
from itertools import combinations
from typing import List, Optional, Sequence, Tuple

Vector = Sequence[float]


def cosine(a: Vector, b: Vector) -> float:
    """The cosine a.b / (|a| |b|). Raise ValueError for a zero vector."""
    ab = math.fsum(x * y for x, y in zip(a, b))
    na = math.sqrt(math.fsum(x * x for x in a))
    nb = math.sqrt(math.fsum(y * y for y in b))
    if na == 0 or nb == 0:
        raise ValueError("the cosine of a zero vector is not defined")
    return ab / (na * nb)


def association(w: Vector, A: Sequence[Vector], B: Sequence[Vector]) -> float:
    """s(w, A, B): the mean cosine of w with A minus the mean cosine of w with B."""
    if not A or not B:
        raise ValueError("A and B must not be empty")
    return math.fsum(cosine(w, a) for a in A) / len(A) - math.fsum(cosine(w, b) for b in B) / len(B)


def _check_targets(X: Sequence[Vector], Y: Sequence[Vector]) -> None:
    if not X or len(X) != len(Y):
        raise ValueError("X and Y must be nonempty and of the same size")


def weat_statistic(X: Sequence[Vector], Y: Sequence[Vector], A: Sequence[Vector], B: Sequence[Vector]) -> float:
    """s(X, Y, A, B) = sum over x of s(x, A, B) minus sum over y of s(y, A, B)."""
    _check_targets(X, Y)
    return math.fsum(association(x, A, B) for x in X) - math.fsum(association(y, A, B) for y in Y)


def _std(values: List[float], ddof: int) -> float:
    m = math.fsum(values) / len(values)
    return math.sqrt(math.fsum((v - m) ** 2 for v in values) / (len(values) - ddof))


def effect_size(
    X: Sequence[Vector], Y: Sequence[Vector], A: Sequence[Vector], B: Sequence[Vector], ddof: int = 0
) -> float:
    """d = (mean over X of s - mean over Y of s) / std over X u Y of s.

    ddof = 0 divides the variance by |X u Y| (the population form, for which
    |d| <= 2), and ddof = 1 by |X u Y| - 1. Raise ValueError if every s is equal.
    """
    _check_targets(X, Y)
    sx = [association(x, A, B) for x in X]
    sy = [association(y, A, B) for y in Y]
    sd = _std(sx + sy, ddof)
    if sd == 0:
        raise ValueError("every association is equal, so the effect size is not defined")
    return (math.fsum(sx) / len(sx) - math.fsum(sy) / len(sy)) / sd


def weat(
    X: Sequence[Vector],
    Y: Sequence[Vector],
    A: Sequence[Vector],
    B: Sequence[Vector],
    ddof: int = 0,
    strict: bool = True,
) -> Tuple[float, float, float]:
    """Return (statistic, effect size, exact p-value).

    The p-value is the fraction of the C(2n, n) equal-size partitions (Xi, Yi)
    of X u Y with s(Xi, Yi, A, B) > s(X, Y, A, B), as in the paper. With
    strict = False the test uses >=, which counts the observed partition and
    so gives a p-value of at least 1 / C(2n, n).
    """
    _check_targets(X, Y)
    n = len(X)
    s = [association(w, A, B) for w in list(X) + list(Y)]  # @line L1
    total = math.fsum(s)  # @line L2
    observed = 2 * math.fsum(s[:n]) - total  # @line L3
    sd = _std(s, ddof)  # @line L4
    if sd == 0:
        raise ValueError("every association is equal, so the effect size is not defined")
    d = (math.fsum(s[:n]) / n - math.fsum(s[n:]) / n) / sd  # @line L5
    count = 0  # @line L6
    partitions = 0
    for xi in combinations(range(2 * n), n):  # @line L7
        si = 2 * math.fsum(s[k] for k in xi) - total  # @line L8
        if si > observed or (not strict and si == observed):  # @line L9
            count += 1
        partitions += 1  # @line L10
    return observed, d, count / partitions  # @line L11


def sampled_p_value(
    X: Sequence[Vector],
    Y: Sequence[Vector],
    A: Sequence[Vector],
    B: Sequence[Vector],
    samples: int,
    rng: Optional[random.Random] = None,
    strict: bool = True,
) -> float:
    """Estimate the p-value of weat from random equal-size partitions.

    Use it when C(2n, n) is too large to list. The estimate has a standard
    error of about sqrt(p (1 - p) / samples).
    """
    _check_targets(X, Y)
    if samples < 1:
        raise ValueError("samples must be positive")
    rng = rng or random.Random(0)
    n = len(X)
    s = [association(w, A, B) for w in list(X) + list(Y)]
    total = math.fsum(s)
    observed = 2 * math.fsum(s[:n]) - total
    idx = list(range(2 * n))
    count = 0
    for _ in range(samples):
        rng.shuffle(idx)
        si = 2 * math.fsum(s[k] for k in idx[:n]) - total
        if si > observed or (not strict and si == observed):
            count += 1
    return count / samples
