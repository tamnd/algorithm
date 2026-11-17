# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/infinite-alleles-model/. The authors are listed in prov/AWDSAS.jsonl.
"""The infinite alleles model on a Wright-Fisher population, with its exact
homozygosity recursion and the Hoppe urn for samples.

The population has 2N gene copies in discrete generations. Each copy of the
next generation copies a parent copy chosen uniformly, and then, with
probability u, mutates to an allele that has never been seen before. Alleles
are labels: only the partition of the copies into allele classes matters.

theta = 4 N u is the scaled mutation rate. Functions that take two_n use the
number of copies 2N.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Dict, Iterator, List, Sequence, Tuple


def simulate(rng, two_n: int, u: float, generations: int,
             start: Sequence[int] | None = None) -> List[int]:
    """The allele labels of the 2N copies after the given number of
    generations. The start is all copies of allele 0 unless given."""
    if two_n < 1 or not 0.0 <= u <= 1.0 or generations < 0:
        raise ValueError("need two_n >= 1, 0 <= u <= 1, generations >= 0")
    pop = list(start) if start is not None else [0] * two_n  # @line L1
    if len(pop) != two_n:
        raise ValueError("start must have two_n labels")
    fresh = max(pop) + 1
    for _ in range(generations):  # @line L2
        nxt = []
        for _ in range(two_n):
            parent = pop[rng.randrange(two_n)]  # @line L3
            if rng.random() < u:  # @line L4
                nxt.append(fresh)  # @line L4
                fresh += 1
            else:
                nxt.append(parent)  # @line L4
        pop = nxt  # @line L5
    return pop  # @line L6


def allele_counts(labels: Sequence[int]) -> List[int]:
    """The sizes of the allele classes, largest first."""
    counts: Dict[int, int] = {}
    for x in labels:
        counts[x] = counts.get(x, 0) + 1
    return sorted(counts.values(), reverse=True)


def homozygosity(labels: Sequence[int]) -> float:
    """The share of pairs of distinct copies that carry the same allele."""
    n = len(labels)
    if n < 2:
        raise ValueError("need at least two copies")
    return sum(c * (c - 1) for c in allele_counts(labels)) / (n * (n - 1))


def homozygosity_step(F, two_n: int, u):
    """F' = (1 - u)^2 (1/(2N) + (1 - 1/(2N)) F): two copies of the next
    generation are identical if neither mutates and their parents are the
    same copy or identical distinct copies."""
    return (1 - u) ** 2 * (Fraction(1, two_n) + (1 - Fraction(1, two_n)) * F)


def homozygosity_after(two_n: int, u, generations: int, F0=Fraction(1)):
    """The expected homozygosity after the given number of generations."""
    F = F0
    for _ in range(generations):
        F = homozygosity_step(F, two_n, u)
    return F


def homozygosity_equilibrium(two_n: int, u):
    """The fixed point F* = (1 - u)^2 / (2N - (2N - 1)(1 - u)^2), which is
    about 1 / (1 + theta) with theta = 4 N u = 2 two_n u."""
    r = (1 - u) ** 2
    return r / (two_n - (two_n - 1) * r)


def hoppe_urn(rng, n: int, theta: float) -> List[int]:
    """Allele labels of a sample of n genes drawn by the Hoppe urn: gene k + 1
    is a new allele with probability theta / (theta + k), else a copy of one
    of the k earlier genes chosen uniformly."""
    if n < 1 or theta <= 0:
        raise ValueError("need n >= 1 and theta > 0")
    labels: List[int] = []
    fresh = 0
    for k in range(n):
        if rng.random() * (theta + k) < theta:
            labels.append(fresh)
            fresh += 1
        else:
            labels.append(labels[rng.randrange(k)])
    return labels


def allele_profile(counts: Sequence[int], n: int) -> Tuple[int, ...]:
    """(a_1, ..., a_n): a_j is the number of alleles with exactly j copies."""
    a = [0] * n
    for c in counts:
        a[c - 1] += 1
    return tuple(a)


def rising(theta, n: int):
    """theta (theta + 1) ... (theta + n - 1)."""
    out = theta ** 0
    for i in range(n):
        out *= theta + i
    return out


def ewens_probability(a: Sequence[int], theta) -> Fraction:
    """The Ewens sampling formula n! / theta^(n rising) prod (theta/j)^a_j / a_j!.
    Exact for Fraction or integer theta."""
    n = sum((j + 1) * x for j, x in enumerate(a))
    p = Fraction(1)
    for i in range(1, n + 1):
        p *= i
    p /= rising(Fraction(theta), n)
    for j, x in enumerate(a, start=1):
        for k in range(1, x + 1):
            p *= Fraction(theta) / j / k
    return p


def partitions(n: int, largest: int | None = None) -> Iterator[List[int]]:
    """The partitions of n as lists of parts, largest first."""
    if largest is None:
        largest = n
    if n == 0:
        yield []
        return
    for first in range(min(n, largest), 0, -1):
        for rest in partitions(n - first, first):
            yield [first] + rest


def expected_alleles(n: int, theta):
    """E[K] = sum over i = 0..n-1 of theta / (theta + i) in a sample of n."""
    return sum(Fraction(theta) / (Fraction(theta) + i) for i in range(n))
