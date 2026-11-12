# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kingman-coalescent/. The authors are listed in prov/6QE1Y8.jsonl.
"""The Kingman coalescent: exact moments and a simulator.

Time is in coalescent units: 2N generations for a diploid population of N
individuals, or N generations for a haploid population of N gene copies.
While k lineages remain, the waiting time to the next merge is exponential
with rate k(k - 1)/2, and the pair that merges is uniform among the
k(k - 1)/2 pairs. Mutations fall on each lineage at rate theta/2 per unit,
with theta = 4 N mu (diploid) or 2 N mu (haploid).
"""

import random
from fractions import Fraction


def harmonic(m: int) -> Fraction:
    """a = 1 + 1/2 + ... + 1/m, exactly (0 for m = 0)."""
    return sum((Fraction(1, i) for i in range(1, m + 1)), Fraction(0))


def expected_tmrca(n: int) -> Fraction:
    """E[T_MRCA] as the sum of the means 2/(k(k-1)) of the waiting times."""
    return sum((Fraction(2, k * (k - 1)) for k in range(2, n + 1)), Fraction(0))


def expected_total_length(n: int) -> Fraction:
    """E[L], where L is the sum of the branch lengths: k lineages for time T_k."""
    return sum((k * Fraction(2, k * (k - 1)) for k in range(2, n + 1)), Fraction(0))


def var_tmrca(n: int) -> Fraction:
    """Var[T_MRCA]; the T_k are independent with variance (2/(k(k-1)))^2."""
    return sum((Fraction(2, k * (k - 1)) ** 2 for k in range(2, n + 1)), Fraction(0))


def var_total_length(n: int) -> Fraction:
    """Var[L] = sum over k of k^2 Var[T_k] = 4 (1 + 1/4 + ... + 1/(n-1)^2)."""
    return sum((Fraction(k * k) * Fraction(2, k * (k - 1)) ** 2 for k in range(2, n + 1)), Fraction(0))


def watterson_estimator(s: int, n: int) -> Fraction:
    """theta_W = S / a_n with a_n = 1 + 1/2 + ... + 1/(n-1)."""
    return Fraction(s) / harmonic(n - 1)


def simulate(n: int, rng: random.Random):
    """Run the coalescent on a sample of n >= 1 labeled lineages 0..n-1.

    Returns (times, tree): times[k] is the waiting time while k lineages remain
    (k = n down to 2), and tree is the genealogy as nested pairs of labels.
    """
    lineages = list(range(n))  # @line L1
    times = {}
    for k in range(n, 1, -1):  # @line L2
        times[k] = rng.expovariate(k * (k - 1) / 2)  # @line L3
        i, j = rng.sample(range(k), 2)  # @line L4
        if i > j:
            i, j = j, i
        merged = (lineages[i], lineages[j])  # @line L5
        lineages[j] = lineages[-1]
        lineages.pop()
        lineages[i] = merged
    return times, lineages[0]  # @line L6


def tmrca_and_length(times: dict) -> tuple:
    """T_MRCA and the total branch length L from the waiting times."""
    return sum(times.values()), sum(k * t for k, t in times.items())


def poisson(mean: float, rng: random.Random) -> int:
    """A Poisson count: the number of rate-1 arrivals in [0, mean]."""
    count, clock = 0, rng.expovariate(1.0)
    while clock <= mean:
        count += 1
        clock += rng.expovariate(1.0)
    return count


def segregating_sites(n: int, theta: float, rng: random.Random) -> int:
    """S under the infinite-sites model: Poisson with mean (theta/2) L."""
    times, _ = simulate(n, rng)
    return poisson(theta / 2 * tmrca_and_length(times)[1], rng)


def root_split(tree) -> int:
    """The number of sample labels on the left side of the root."""
    if not isinstance(tree, tuple):
        return 1
    stack, count = [tree[0]], 0
    while stack:
        x = stack.pop()
        if isinstance(x, tuple):
            stack.extend(x)
        else:
            count += 1
    return count


def wright_fisher_pair_time(pop: int, rng: random.Random) -> int:
    """Generations back until two gene copies in a haploid Wright-Fisher
    population of size pop pick the same parent."""
    g = 1
    while rng.randrange(pop) != rng.randrange(pop):
        g += 1
    return g
