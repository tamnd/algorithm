# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lincoln-petersen-estimator/. The authors are listed in prov/XD1A1J.jsonl.
"""The Lincoln-Petersen estimator of a closed population size.

Model: a closed population of N animals. The first sample marks M distinct
animals. The second sample is a simple random sample of C distinct animals,
and R of them are marked, so R is hypergeometric with mean M C / N.

All estimates are exact fractions.Fraction values. Cost: Theta(M + C)
expected time with the hash set of line L1, and Theta(M) extra space.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Iterable, Optional


@dataclass(frozen=True)
class Estimate:
    """The counts and the estimates of one marking study."""

    marked: int
    caught: int
    recaptured: int
    lincoln_petersen: Optional[Fraction]
    chapman: Fraction
    chapman_variance: Fraction


def _check_counts(m: int, c: int, r: int) -> None:
    if m < 0 or c < 0 or r < 0 or r > m or r > c:
        raise ValueError("need 0 <= R <= min(M, C)")


def chapman(m: int, c: int, r: int) -> Fraction:
    """Chapman's estimate (M + 1)(C + 1)/(R + 1) - 1."""
    _check_counts(m, c, r)
    return Fraction((m + 1) * (c + 1), r + 1) - 1


def chapman_variance(m: int, c: int, r: int) -> Fraction:
    """The variance estimate (M + 1)(C + 1)(M - R)(C - R)/((R + 1)^2 (R + 2))."""
    _check_counts(m, c, r)
    return Fraction((m + 1) * (c + 1) * (m - r) * (c - r), (r + 1) ** 2 * (r + 2))


def lincoln_petersen_counts(m: int, c: int, r: int) -> Optional[Fraction]:
    """The classic estimate M C / R, or None when R = 0."""
    _check_counts(m, c, r)
    if r == 0:
        return None
    return Fraction(m * c, r)


def hypergeometric_mle(m: int, c: int, r: int) -> int:
    """The largest integer N that maximizes the hypergeometric likelihood of
    R = r, which is floor(M C / R). Requires R >= 1."""
    _check_counts(m, c, r)
    if r == 0:
        raise ValueError("the likelihood has no maximum when R = 0")
    return (m * c) // r


def lincoln_petersen(first: Iterable[Hashable], second: Iterable[Hashable]) -> Estimate:
    """Estimate the population size from two lists of animal identifiers.

    Precondition: the identifiers in each list are distinct. The first list
    holds the marked animals, the second list the animals of the recapture.
    """
    first = list(first)
    second = list(second)
    marked = set(first)  # @line L1
    if len(marked) != len(first):
        raise ValueError("the first sample has a repeated identifier")
    if len(set(second)) != len(second):
        raise ValueError("the second sample has a repeated identifier")
    m = len(marked)
    c = len(second)  # @line L2
    r = sum(1 for animal in second if animal in marked)  # @line L3
    n_c = chapman(m, c, r)  # @line L4
    v_c = chapman_variance(m, c, r)  # @line L5
    n_lp = lincoln_petersen_counts(m, c, r)  # @line L6
    return Estimate(m, c, r, n_lp, n_c, v_c)  # @line L7
