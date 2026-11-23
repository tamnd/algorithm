# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimized-local-hashing/. The authors are listed in prov/4AE9P1.jsonl.
"""Optimized local hashing (Wang, Blocki, Li and Jha, USENIX Security 2017).

Each client picks a random hash function H from a family that maps the domain
{0, ..., d - 1} into {0, ..., g - 1}, hashes its value, and applies generalized
randomized response over the g hash values. It sends the hash function (its
seed) and the noisy hash value. The collector counts, for each candidate value
v, the reports whose hash function maps v to the reported value, and removes
the bias. The choice g = e^epsilon + 1 minimizes the variance.

The parameter exp_epsilon is the exact rational number e^epsilon, so the coin
is exact. The family here is the family of all functions from the domain to
{0, ..., g - 1}, indexed by a seed s in [0, g^d): H_s(v) is digit v of s in
base g. It is exactly uniform, which the proofs use; a deployment uses a
family with a short seed. random.Random is used only so that the tests are
reproducible; a deployment needs a cryptographic source of randomness.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence

Report = tuple[int, int]


@dataclass(frozen=True)
class AllFunctions:
    """All g^d functions from {0, ..., d - 1} to {0, ..., g - 1}; seed s gives H_s(v) = digit v of s in base g."""

    d: int
    g: int

    def __post_init__(self) -> None:
        if self.d < 1 or self.g < 2:
            raise ValueError("need d >= 1 and g >= 2")

    @property
    def seeds(self) -> int:
        return self.g ** self.d

    def hash(self, seed: int, v: int) -> int:
        return (seed // self.g ** v) % self.g


def optimal_range(exp_epsilon: Fraction) -> int:
    """The integer g >= 2 that minimizes Var*; the real minimizer is g = e^epsilon + 1.

    With t = g - 1, Var* is proportional to e^2 / t + t, which is convex, so the
    best integer t is floor(e) or floor(e) + 1, and floor(e) + 1 wins exactly
    when e^2 > floor(e) (floor(e) + 1). Precondition: exp_epsilon > 1.
    """
    e = Fraction(exp_epsilon)
    if e <= 1:
        raise ValueError("need exp_epsilon > 1")
    t = e.numerator // e.denominator
    if e * e > t * (t + 1):
        t += 1
    return t + 1


def keep_probability(exp_epsilon: Fraction, g: int) -> Fraction:
    """p = e^epsilon / (e^epsilon + g - 1), the chance that the true hash value is sent."""
    e = Fraction(exp_epsilon)
    return e / (e + g - 1)


def olh_report(v: int, exp_epsilon: Fraction, family: AllFunctions, rng: random.Random) -> Report:
    """One OLH report (seed, y) of the value v.

    Precondition: 0 <= v < d and exp_epsilon >= 1 is rational. The report is
    epsilon-LDP. Cost: O(1) arithmetic and three uniform draws.
    """
    if not 0 <= v < family.d:
        raise ValueError("value out of the domain")
    if Fraction(exp_epsilon) < 1:
        raise ValueError("need exp_epsilon >= 1")
    p = keep_probability(exp_epsilon, family.g)
    s = rng.randrange(family.seeds)  # @line L1
    x = family.hash(s, v)  # @line L2
    if rng.randrange(p.denominator) < p.numerator:  # @line L3
        return (s, x)  # @line L4
    r = rng.randrange(family.g - 1)  # @line L5
    y = r if r < x else r + 1
    return (s, y)


def olh_estimate(reports: Sequence[Report], exp_epsilon: Fraction, family: AllFunctions) -> list[Fraction]:
    """Unbiased estimates of the count of each value 0, ..., d - 1.

    Precondition: the reports come from olh_report with the same parameters,
    and exp_epsilon > 1. Cost: O(n d) hash evaluations for n reports.
    """
    if Fraction(exp_epsilon) <= 1:
        raise ValueError("the estimate needs epsilon > 0")
    n = len(reports)
    g = family.g
    p = keep_probability(exp_epsilon, g)
    out = []
    for v in range(family.d):
        support = sum(1 for s, y in reports if family.hash(s, v) == y)  # @line L6
        out.append((support - Fraction(n, g)) / (p - Fraction(1, g)))  # @line L7
    return out  # @line L8


def report_pmf(v: int, exp_epsilon: Fraction, family: AllFunctions) -> dict[Report, Fraction]:
    """The exact pmf of olh_report(v) over all pairs (seed, y)."""
    g = family.g
    p = keep_probability(exp_epsilon, g)
    other = (1 - p) / (g - 1)
    weight = Fraction(1, family.seeds)
    out = {}
    for s in range(family.seeds):
        x = family.hash(s, v)
        for y in range(g):
            out[(s, y)] = weight * (p if y == x else other)
    return out


def variance_formula(n: int, n_v: int, exp_epsilon: Fraction, g: int) -> Fraction:
    """The exact variance of the estimate of a value held by n_v of the n clients."""
    p = keep_probability(exp_epsilon, g)
    q = Fraction(1, g)
    return (n_v * p * (1 - p) + (n - n_v) * q * (1 - q)) / (p - q) ** 2


def approximate_variance(n: int, exp_epsilon: Fraction, g: int) -> Fraction:
    """Var* = n q (1 - q) / (p - q)^2 with q = 1/g, the variance when n_v is small against n."""
    p = keep_probability(exp_epsilon, g)
    q = Fraction(1, g)
    return n * q * (1 - q) / (p - q) ** 2
