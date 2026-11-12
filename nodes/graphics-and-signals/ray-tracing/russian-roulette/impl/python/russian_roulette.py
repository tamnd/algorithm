# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/russian-roulette/. The authors are listed in prov/QF25TE.jsonl.

"""Russian roulette: stop a random sum early and keep its expected value.

A value X is kept with the probability q and then divided by q; otherwise it
is replaced by 0. The result has the expected value E[X] for any q in (0, 1].
Applied after each term of a sum, it gives a finite estimate of an infinite
series, which is how a path tracer stops its paths.
"""

import random
from collections.abc import Callable
from fractions import Fraction

Survival = Callable[[int, float], float]  # (index k, current weight) -> q in [0, 1]


def roulette(value: float, q: float, rng: random.Random) -> float:
    """One roulette step on a value that is already known."""
    if q > 0 and rng.random() < q:  # @line L1
        return value / q  # @line L2
    return 0.0  # @line L3


def series(a: Callable[[int], float], q: Survival, rng: random.Random, divide: bool = True) -> float:
    """An estimate of sum_{k >= 0} a(k) that stops after term k with probability 1 - q(k, w).

    w is the weight of the next term, 1 / (q_0 q_1 ... q_{k-1}). With divide=False
    the weight stays 1, which is the common mistake: it estimates a smaller sum.
    """
    total, w, k = 0.0, 1.0, 0  # @line L4
    while True:
        total += w * a(k)  # @line L5
        qk = q(k, w)  # @line L6
        if qk <= 0 or rng.random() >= qk:  # @line L7
            return total
        if divide:
            w /= qk  # @line L8
        k += 1  # @line L9


def outcomes(a: list[Fraction], q: Callable[[int, Fraction], Fraction], divide: bool = True) -> list[tuple[Fraction, Fraction]]:
    """All (probability, value) pairs of `series` on a finite list of terms.

    The sum stops for sure after the last term. The enumeration follows the
    same steps as `series`, with exact arithmetic and no random numbers.
    """
    out = []
    prob, w, total = Fraction(1), Fraction(1), Fraction(0)
    for k, ak in enumerate(a):
        total += w * ak
        qk = q(k, w) if k + 1 < len(a) else Fraction(0)
        assert 0 <= qk <= 1
        out.append((prob * (1 - qk), total))
        if qk == 0:
            break
        prob *= qk
        if divide:
            w /= qk
    return [(p, v) for p, v in out if p > 0]


def mean_and_variance(pairs: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    assert sum(p for p, _ in pairs) == 1
    m = sum(p * v for p, v in pairs)
    return m, sum(p * (v - m) ** 2 for p, v in pairs)


def expected_terms(n: int, q: Callable[[int, Fraction], Fraction]) -> Fraction:
    """The expected number of terms that `series` evaluates on n terms.

    A sum that survives k steps is in one state only, so the expected count is
    the sum over k of the probability to reach term k.
    """
    reach, w, count = Fraction(1), Fraction(1), Fraction(0)
    for k in range(n):
        count += reach
        if k + 1 < n:
            qk = q(k, w)
            reach *= qk
            if qk > 0:
                w /= qk
    return count
