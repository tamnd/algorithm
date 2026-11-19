# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-hmm-tagging/. The authors are listed in prov/FKE3K3.jsonl.

import math
import random
from fractions import Fraction

from bayesian_hmm_tagging import (all_taggings, build_counts, conditional, exact_posterior, gibbs,
                                  log_marginal, many_to_one_accuracy, marginal, rising)


def without_position(words, tags, k, W, s, i):
    c = build_counts(words, tags, k, W)
    ts = tags[s]
    a = ts[i - 1] if i > 0 else 0
    b = ts[i + 1] if i + 1 < len(ts) else 0
    c.add_trans(a, ts[i], -1)
    c.add_trans(ts[i], b, -1)
    c.add_emit(ts[i], words[s][i], -1)
    return c, a, b


def test_rising_factorial():
    assert rising(Fraction(1, 2), 0) == 1
    assert rising(Fraction(1, 2), 3) == Fraction(1, 2) * Fraction(3, 2) * Fraction(5, 2)
    assert rising(3, 4) == math.factorial(6) // math.factorial(2)


def test_conditional_is_ratio_of_marginals():
    """The collapsed conditional equals P(t with t_i = t, w) / sum over t' of the same, exactly."""
    rng = random.Random(1)
    for _ in range(40):
        k = rng.randint(1, 3)
        W = rng.randint(1, 4)
        alpha = Fraction(rng.randint(1, 9), rng.randint(1, 9))
        beta = Fraction(rng.randint(1, 9), rng.randint(1, 9))
        words = [[rng.randrange(W) for _ in range(rng.randint(1, 4))] for _ in range(rng.randint(1, 3))]
        tags = [[rng.randint(1, k) for _ in ws] for ws in words]
        s = rng.randrange(len(words))
        i = rng.randrange(len(words[s]))
        c, a, b = without_position(words, tags, k, W, s, i)
        p = conditional(c, a, words[s][i], b, alpha, beta)
        joint = []
        for t in range(1, k + 1):
            tg = [list(ts) for ts in tags]
            tg[s][i] = t
            joint.append(marginal(words, tg, k, W, alpha, beta))
        zp = sum(p[1:])
        zj = sum(joint)
        for t in range(1, k + 1):
            assert p[t] / zp == joint[t - 1] / zj


def test_conditional_tricky_cases_same_tag_neighbours():
    """a = t = b, the case of the indicator terms, against the ratio of marginals."""
    words = [[0, 0, 0]]
    k, W = 2, 1
    alpha, beta = Fraction(1, 3), Fraction(2, 5)
    for mid in (1, 2):
        tags = [[1, mid, 1]]
        c, a, b = without_position(words, tags, k, W, 0, 1)
        p = conditional(c, a, 0, b, alpha, beta)
        m1 = marginal(words, [[1, 1, 1]], k, W, alpha, beta)
        m2 = marginal(words, [[1, 2, 1]], k, W, alpha, beta)
        assert p[1] / p[2] == m1 / m2


def test_marginal_sums_to_one_over_words():
    """Summing P(t, w) over all taggings and all word strings of fixed lengths gives P(lengths)."""
    k, W = 2, 2
    alpha, beta = Fraction(1, 2), Fraction(1, 3)
    total = Fraction(0)
    for w0 in range(W):
        for w1 in range(W):
            words = [[w0, w1]]
            total += sum(marginal(words, tg, k, W, alpha, beta) for tg in all_taggings(words, k))
    # The emission part sums to 1, so the total is P(the two-word length pattern) under the prior.
    trans_only = Fraction(0)
    for tg in all_taggings([[0, 0]], k):
        c = build_counts([[0, 0]], tg, k, 1)
        p = Fraction(1)
        for a in range(k + 1):
            for b in range(k + 1):
                p *= rising(alpha, c.trans[a][b])
            p /= rising((k + 1) * alpha, c.out[a])
        trans_only += p
    assert total == trans_only


def test_log_marginal_matches_exact():
    rng = random.Random(4)
    words = [[rng.randrange(3) for _ in range(4)] for _ in range(2)]
    tags = [[rng.randint(1, 2) for _ in ws] for ws in words]
    exact = marginal(words, tags, 2, 3, Fraction(1, 10), Fraction(1, 5))
    assert abs(log_marginal(words, tags, 2, 3, 0.1, 0.2) - math.log(exact)) < 1e-9


def test_gibbs_frequencies_match_exact_posterior():
    words = [[0, 1, 0], [1]]
    k, W = 2, 2
    alpha, beta = 0.5, 0.5
    exact = exact_posterior(words, k, W, Fraction(1, 2), Fraction(1, 2))
    _, samples = gibbs(words, k, W, alpha, beta, sweeps=20000, seed=12345)
    freq = {}
    for smp in samples[200:]:
        freq[smp] = freq.get(smp, 0) + 1
    n = len(samples) - 200
    assert len(exact) == 16
    assert sum(exact.values()) == 1
    for key, p in exact.items():
        assert abs(freq.get(key, 0) / n - float(p)) < 0.01


def test_gibbs_finds_planted_classes():
    """Two tags with disjoint vocabularies that alternate; sparse priors recover them."""
    rng = random.Random(9)
    words, gold = [], []
    for _ in range(30):
        ws, gs = [], []
        for j in range(rng.randint(2, 6)):
            if j % 2 == 0:
                ws.append(rng.randrange(0, 4))
                gs.append("D")
            else:
                ws.append(rng.randrange(4, 8))
                gs.append("N")
        words.append(ws)
        gold.append(gs)
    tags, _ = gibbs(words, 2, 8, 0.1, 0.1, sweeps=150, seed=3)
    assert many_to_one_accuracy(gold, tags) == 1.0
    assert log_marginal(words, tags, 2, 8, 0.1, 0.1) > log_marginal(words, [[1] * len(ws) for ws in words], 2, 8, 0.1, 0.1)


def test_counts_restored_after_sweeps():
    rng = random.Random(2)
    words = [[rng.randrange(5) for _ in range(rng.randint(1, 6))] for _ in range(5)]
    tags, _ = gibbs(words, 3, 5, 0.3, 0.2, sweeps=5, seed=8)
    c = build_counts(words, tags, 3, 5)
    assert sum(c.ntag) == sum(len(ws) for ws in words)
    assert c.out[0] == len(words) and sum(c.trans[a][0] for a in range(4)) == len(words)
