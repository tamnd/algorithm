# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-genotype-calling/. The authors are listed in prov/YB8C7J.jsonl.
"""Bayesian genotype calling at one biallelic site of a diploid sample.

A pileup is a list of (base, quality) pairs: the base that each read shows
at the site and its Phred base quality. The genotype g is the number of
copies of the alternate allele, 0, 1 or 2. The error model is the usual one
of the genotype likelihood page: a base is read correctly with probability
1 - e, and as each of the three other bases with probability e / 3, where
e = 10^(-Q/10). Reads are independent given the genotype, and each read
comes from either chromosome with probability 1/2.

All sums are in log space, so a deep pileup does not underflow.
"""

from __future__ import annotations

import math
from collections import namedtuple
from typing import List, Sequence, Tuple

from biostoch import logsumexp

Call = namedtuple("Call", ["genotype", "posterior", "gq", "qual", "alt"])

_LN10 = math.log(10.0)


def base_prob(base: str, allele: str, e: float) -> float:
    """P(read shows base | the read comes from a chromosome with allele)."""
    return 1.0 - e if base == allele else e / 3.0


def prior_theta(theta: float) -> List[float]:
    """The prior (1 - 3 theta / 2, theta, theta / 2) from the population mutation rate."""
    if not 0.0 <= theta <= 2.0 / 3.0:
        raise ValueError("need 0 <= theta <= 2/3")
    return [1.0 - 1.5 * theta, theta, theta / 2.0]


def prior_hwe(f: float) -> List[float]:
    """The Hardy-Weinberg prior ((1 - f)^2, 2 f (1 - f), f^2) for alternate allele frequency f."""
    if not 0.0 <= f <= 1.0:
        raise ValueError("need 0 <= f <= 1")
    return [(1.0 - f) ** 2, 2.0 * f * (1.0 - f), f * f]


def log_likelihoods(pileup: Sequence[Tuple[str, float]], ref: str, alt: str) -> List[float]:
    """ln P(D | g) for g = 0, 1, 2."""
    ll = [0.0, 0.0, 0.0]
    for b, q in pileup:
        e = 10.0 ** (-q / 10.0)
        pr, pa = base_prob(b, ref, e), base_prob(b, alt, e)
        for g in range(3):
            ll[g] += math.log((g / 2.0) * pa + (1.0 - g / 2.0) * pr)
    return ll


def call_genotype(pileup: Sequence[Tuple[str, float]], ref: str, alt: str,
                  prior: Sequence[float]) -> Call:
    """The maximum a posteriori genotype, its posterior, GQ and QUAL.

    GQ is -10 log10 of the posterior probability that the called genotype is
    wrong. QUAL is -10 log10 P(g = 0 | D), the Phred-scaled probability that
    the site is not variant. Ties in the posterior go to the smaller g.
    """
    if alt == ref:
        raise ValueError("alt must differ from ref")
    lp = [math.log(p) if p > 0 else -math.inf for p in prior]  # @line L1
    for b, q in pileup:  # @line L2
        e = 10.0 ** (-q / 10.0)  # @line L3
        pr, pa = base_prob(b, ref, e), base_prob(b, alt, e)
        for g in range(3):  # @line L4
            lp[g] += math.log((g / 2.0) * pa + (1.0 - g / 2.0) * pr)  # @line L5
    z = logsumexp(lp)  # @line L6
    post = [math.exp(x - z) for x in lp]  # @line L7
    best = max(range(3), key=lambda g: (lp[g], -g))  # @line L8
    wrong = logsumexp([lp[g] for g in range(3) if g != best]) - z  # @line L9
    gq = -10.0 * wrong / _LN10 if wrong > -math.inf else math.inf
    qual = -10.0 * (lp[0] - z) / _LN10 if lp[0] > -math.inf else math.inf
    return Call(best, post, gq, qual, alt)  # @line L10


def call_site(ref: str, pileup: Sequence[Tuple[str, float]], prior: Sequence[float]) -> Call:
    """Call one site, with the most common non-reference base as the alternate allele.

    Ties between non-reference bases go to the first in ACGT order, so a site
    with no non-reference base is tested against the first other base.
    """
    others = [b for b in "ACGT" if b != ref]
    counts = {b: 0 for b in others}
    for b, _ in pileup:
        if b in counts:
            counts[b] += 1
    alt = max(others, key=lambda b: (counts[b], -others.index(b)))
    return call_genotype(pileup, ref, alt, prior)
