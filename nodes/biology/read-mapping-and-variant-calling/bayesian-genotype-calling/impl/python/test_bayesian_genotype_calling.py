# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-genotype-calling/. The authors are listed in prov/YB8C7J.jsonl.

import itertools
import math
import random

from bioseq import random_dna, revcomp, simulate_reads, phred_to_prob
from biostoch import binom_pmf
from bayesian_genotype_calling import (base_prob, call_genotype, call_site, log_likelihoods,
                                       prior_hwe, prior_theta)

EXAMPLE = [("A", 30), ("A", 30), ("A", 20), ("G", 30), ("G", 20), ("G", 10)]


def brute_posterior(pileup, ref, alt, prior):
    """P(g | D) by a sum over every way to assign each read to one of the two chromosomes."""
    joint = []
    for g in range(3):
        chroms = [(ref, ref), (ref, alt), (alt, alt)][g]
        lik = 0.0
        for origin in itertools.product((0, 1), repeat=len(pileup)):
            term = 0.5 ** len(pileup)
            for (b, q), c in zip(pileup, origin):
                term *= base_prob(b, chroms[c], phred_to_prob(q))
            lik += term
        joint.append(prior[g] * lik)
    s = sum(joint)
    return [x / s for x in joint]


def test_page_example():
    ll = log_likelihoods(EXAMPLE, "A", "G")
    pl = [round(-10 * (x - max(ll)) / math.log(10)) for x in ll]
    assert pl == [56, 0, 76]
    c = call_genotype(EXAMPLE, "A", "G", prior_theta(0.001))
    assert c.genotype == 1
    assert abs(c.posterior[1] - 0.997462) < 1e-6
    assert abs(c.gq - 25.955) < 1e-3 and abs(c.qual - 25.955) < 1e-3
    c = call_genotype(EXAMPLE, "A", "G", prior_hwe(0.3))
    assert c.genotype == 1 and abs(c.gq - 55.261) < 1e-3


def test_two_reads_and_one_of_ten():
    c = call_genotype([("G", 30)] * 2, "A", "G", prior_theta(0.001))
    assert c.genotype == 2
    assert abs(c.posterior[1] - 0.333432) < 1e-6 and abs(c.posterior[2] - 0.666420) < 1e-6
    c = call_genotype([("G", 30)] + [("A", 30)] * 9, "A", "G", prior_theta(0.001))
    assert c.genotype == 0 and abs(c.posterior[1] - 0.002932) < 1e-6


def test_against_brute_force():
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(0, 8)
        pile = [(rng.choice("AAGGC"), rng.choice((5, 10, 20, 30, 40))) for _ in range(n)]
        prior = prior_theta(rng.choice((0.001, 0.01, 0.1))) if rng.random() < 0.5 else prior_hwe(rng.random())
        c = call_genotype(pile, "A", "G", prior)
        brute = brute_posterior(pile, "A", "G", prior)
        for g in range(3):
            assert abs(c.posterior[g] - brute[g]) < 1e-9
        assert c.genotype == max(range(3), key=lambda g: (brute[g], -g)) or \
            abs(brute[c.genotype] - max(brute)) < 1e-12


def test_equal_qualities_match_binomial():
    e = phred_to_prob(20)
    for n in range(0, 12):
        for k in range(n + 1):
            pile = [("G", 20)] * k + [("A", 20)] * (n - k)
            ll = log_likelihoods(pile, "A", "G")
            for g in range(3):
                pa = (g / 2) * (1 - e) + (1 - g / 2) * (e / 3)
                pr = (g / 2) * (e / 3) + (1 - g / 2) * (1 - e)
                # pa^k pr^(n-k) = (pa + pr)^n t^k (1 - t)^(n-k) with t = pa / (pa + pr).
                expect = (pa + pr) ** n * binom_pmf(k, n, pa / (pa + pr)) / math.comb(n, k)
                assert abs(math.exp(ll[g]) - expect) <= 1e-12 * max(1.0, expect)


def test_no_reads_gives_prior_and_deep_pileup_is_finite():
    prior = prior_theta(0.001)
    c = call_genotype([], "A", "G", prior)
    assert all(abs(a - b) < 1e-15 for a, b in zip(c.posterior, prior))
    deep = [("A", 40)] * 3000 + [("G", 40)] * 3000
    c = call_genotype(deep, "A", "G", prior)
    assert c.genotype == 1 and math.isfinite(c.qual) and c.qual > 1000


def test_priors_sum_to_one():
    for t in (0.0, 0.001, 0.5):
        assert abs(sum(prior_theta(t)) - 1) < 1e-15
    for f in (0.0, 0.2, 1.0):
        assert abs(sum(prior_hwe(f)) - 1) < 1e-15


def test_recovers_simulated_variants():
    rng = random.Random(2024)
    g_len, read_len, q = 3000, 100, 20
    genome = random_dna(rng, g_len)
    sites = rng.sample(range(50, g_len - 50), 24)
    truth = {}
    hap = [list(genome), list(genome)]
    for i, s in enumerate(sites):
        alt = rng.choice([b for b in "ACGT" if b != genome[s]])
        g = 2 if i % 4 == 0 else 1
        truth[s] = (alt, g)
        hap[0][s] = alt
        if g == 2:
            hap[1][s] = alt
    piles = [[] for _ in range(g_len)]
    for h in hap:
        for r in simulate_reads(rng, "".join(h), 450, read_len, phred_to_prob(q)):
            fwd = r.read if r.strand == "+" else revcomp(r.read)
            for j, b in enumerate(fwd):
                piles[r.pos + j].append((b, q))
    called = {}
    for s in range(g_len):
        c = call_site(genome[s], piles[s], prior_theta(0.001))
        if c.genotype > 0:
            called[s] = (c.alt, c.genotype)
    assert called == truth
