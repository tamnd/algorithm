# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/em-haplotype-frequency-estimation/. The authors are listed in prov/5PQV9Z.jsonl.
"""EM estimation of haplotype frequencies from unphased genotypes
(Excoffier and Slatkin 1995).

Input: n diploid genotypes at m biallelic sites. A genotype is a tuple of
m values in {0, 1, 2}, the number of copies of allele 1 at each site. A
haplotype is a tuple of m values in {0, 1}.

Model: the two haplotypes of each individual are drawn independently from
the haplotype frequencies p (Hardy-Weinberg proportions for haplotypes).
The probability of a genotype g is the sum, over the unordered haplotype
pairs {h, h'} that are compatible with g, of w p_h p_h', where w = 2 if
h != h' and w = 1 if h = h'.

EM: the E-step splits each individual over its compatible pairs in
proportion to w p_h p_h'; the M-step sets p_h to the expected number of
copies of h divided by 2n. The log-likelihood never decreases.
"""

from __future__ import annotations

import math
from itertools import product

Genotype = tuple[int, ...]
Haplotype = tuple[int, ...]


def compatible_pairs(g: Genotype) -> list[tuple[Haplotype, Haplotype]]:
    """The unordered haplotype pairs that give genotype g.

    With h heterozygous sites there are 2^(h-1) pairs (1 pair when h = 0).
    The allele of the first heterozygous site is fixed to 0 on the first
    haplotype of each pair, so that each unordered pair appears once.
    """
    het = [j for j, x in enumerate(g) if x == 1]
    for x in g:
        if x not in (0, 1, 2):
            raise ValueError("a genotype value must be 0, 1 or 2")
    base = [1 if x == 2 else 0 for x in g]
    if not het:
        h = tuple(base)
        return [(h, h)]
    pairs = []
    for bits in product((0, 1), repeat=len(het) - 1):
        a = list(base)
        b = list(base)
        a[het[0]], b[het[0]] = 0, 1
        for j, bit in zip(het[1:], bits):
            a[j], b[j] = bit, 1 - bit
        pairs.append((tuple(a), tuple(b)))
    return pairs


def genotype_prob(pairs: list[tuple[Haplotype, Haplotype]], p: dict[Haplotype, float]) -> float:
    """P(g) = sum over compatible pairs of w p_h p_h'."""
    total = 0.0
    for h, k in pairs:
        w = 1.0 if h == k else 2.0
        total += w * p.get(h, 0.0) * p.get(k, 0.0)
    return total


def log_likelihood(genotypes: list[Genotype], p: dict[Haplotype, float]) -> float:
    """The log-likelihood of the haplotype frequencies p for the genotypes."""
    s = 0.0
    for g in genotypes:
        q = genotype_prob(compatible_pairs(g), p)
        if q <= 0.0:
            return -math.inf
        s += math.log(q)
    return s


def em_haplotype_frequencies(genotypes: list[Genotype], max_iter: int = 1000, tol: float = 1e-10,
                             init: dict[Haplotype, float] | None = None
                             ) -> tuple[dict[Haplotype, float], list[float]]:
    """Run EM. Return the frequencies and the log-likelihood after each step.

    The start is uniform over the haplotypes that occur in some compatible
    pair, unless init is given. EM stops when the log-likelihood gains less
    than tol in one step, or after max_iter steps.
    """
    n = len(genotypes)
    if n == 0:
        raise ValueError("need at least one genotype")
    s = [compatible_pairs(g) for g in genotypes]  # @line L1
    hap_set = sorted({h for pairs in s for pair in pairs for h in pair})  # @line L2
    if init is None:
        p = {h: 1.0 / len(hap_set) for h in hap_set}
    else:
        p = {h: init.get(h, 0.0) for h in hap_set}
        z = sum(p.values())
        p = {h: v / z for h, v in p.items()}
    trace = [log_likelihood(genotypes, p)]
    for _ in range(max_iter):  # @line L3
        c = {h: 0.0 for h in hap_set}  # @line L4
        for pairs in s:  # @line L5
            weights = [(1.0 if h == k else 2.0) * p[h] * p[k] for h, k in pairs]
            total = sum(weights)  # @line L6
            for (h, k), w in zip(pairs, weights):  # @line L7
                e = w / total
                c[h] += e
                c[k] += e
        p = {h: c[h] / (2 * n) for h in hap_set}  # @line L8
        trace.append(log_likelihood(genotypes, p))
        if trace[-1] - trace[-2] < tol:  # @line L9
            break
    return p, trace  # @line L10


def gene_count(haplotype_pairs: list[tuple[Haplotype, Haplotype]]) -> dict[Haplotype, float]:
    """Haplotype frequencies by direct counting when the phase is known."""
    c: dict[Haplotype, float] = {}
    for h, k in haplotype_pairs:
        c[h] = c.get(h, 0.0) + 1.0
        c[k] = c.get(k, 0.0) + 1.0
    total = 2.0 * len(haplotype_pairs)
    return {h: v / total for h, v in c.items()}


def two_site_ld(p: dict[Haplotype, float]) -> tuple[float, float, float]:
    """D, D' and r^2 from two-site haplotype frequencies (allele 1 at each site)."""
    p11 = p.get((1, 1), 0.0)
    pa = p11 + p.get((1, 0), 0.0)
    pb = p11 + p.get((0, 1), 0.0)
    d = p11 - pa * pb
    if d >= 0:
        dmax = min(pa * (1 - pb), (1 - pa) * pb)
    else:
        dmax = min(pa * pb, (1 - pa) * (1 - pb))
    dprime = d / dmax if dmax > 0 else 0.0
    den = pa * (1 - pa) * pb * (1 - pb)
    r2 = d * d / den if den > 0 else 0.0
    return d, dprime, r2
