# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gene-set-enrichment-analysis/. The authors are listed in prov/W39J2F.jsonl.

import math
import random

import pytest

from gene_set_enrichment_analysis import enrichment_score, gsea, leading_edge, signal_to_noise

GENES = ["g%d" % i for i in range(1, 9)]
SCORES = [2.0, 1.5, 1.0, 0.5, -0.2, -0.6, -1.2, -2.5]


def brute_es(genes, scores, members, p):
    """For each cut i, hit(i) - miss(i) from the definition, and the value farthest from 0."""
    order = sorted(range(len(genes)), key=lambda i: -scores[i])
    hits = [i for i in order if genes[i] in members]
    nr = sum(abs(scores[i]) ** p for i in hits)
    miss_total = len(genes) - len(hits)
    devs = [0.0]
    for cut in range(1, len(order) + 1):
        top = order[:cut]
        hit = sum(abs(scores[i]) ** p for i in top if genes[i] in members) / nr
        miss = sum(1 for i in top if genes[i] not in members) / miss_total
        devs.append(hit - miss)
    return max(devs), min(devs)


def agrees(es, extremes):
    """ES is the extreme deviation; when the largest and the smallest have equal size, either sign is right."""
    hi, lo = extremes
    if math.isclose(hi, -lo, rel_tol=1e-9, abs_tol=1e-12):
        return math.isclose(abs(es), hi, rel_tol=1e-9, abs_tol=1e-12)
    want = hi if hi > -lo else lo
    return math.isclose(es, want, rel_tol=1e-9, abs_tol=1e-12)


def ks_statistic(sample_a, sample_b):
    """The signed two-sample Kolmogorov-Smirnov statistic sup (F_a - F_b), by the empirical cdfs."""
    devs = [0.0]
    for x in sorted(set(sample_a) | set(sample_b)):
        fa = sum(v <= x for v in sample_a) / len(sample_a)
        fb = sum(v <= x for v in sample_b) / len(sample_b)
        devs.append(fa - fb)
    return max(devs), min(devs)


def test_page_example():
    s = {"g1", "g3", "g6"}
    es, path = enrichment_score(GENES, SCORES, s, p=1)
    assert math.isclose(es, 5 / 6 - 0.2, rel_tol=1e-12)
    expected = [5 / 9, 5 / 9 - 0.2, 5 / 6 - 0.2, 5 / 6 - 0.4, 5 / 6 - 0.6, 0.4, 0.2, 0.0]
    for a, b in zip(path, expected):
        assert math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)
    assert leading_edge(GENES, SCORES, s) == ["g1", "g3"]
    es0, _ = enrichment_score(GENES, SCORES, s, p=0)
    assert math.isclose(es0, 2 / 3 - 0.2, rel_tol=1e-12)


def test_matches_brute_force():
    rng = random.Random(61)
    for _ in range(200):
        n = rng.randint(2, 30)
        genes = list(range(n))
        scores = [rng.gauss(0, 1) for _ in range(n)]
        k = rng.randint(1, n - 1)
        members = set(rng.sample(genes, k))
        for p in (0, 1, 2):
            assert agrees(enrichment_score(genes, scores, members, p)[0],
                          brute_es(genes, scores, members, p))


def test_p_zero_is_the_kolmogorov_smirnov_statistic():
    rng = random.Random(62)
    for _ in range(100):
        n = rng.randint(2, 25)
        genes = list(range(n))
        scores = [rng.random() for _ in range(n)]
        members = set(rng.sample(genes, rng.randint(1, n - 1)))
        order = sorted(range(n), key=lambda i: -scores[i])
        pos_in = [r for r, i in enumerate(order) if i in members]
        pos_out = [r for r, i in enumerate(order) if i not in members]
        es = enrichment_score(genes, scores, members, p=0)[0]
        assert agrees(es, ks_statistic(pos_in, pos_out))


def test_extremes_and_end_of_walk():
    genes = list(range(10))
    scores = [10 - i for i in range(10)]
    assert enrichment_score(genes, scores, {0, 1, 2}, p=0)[0] == pytest.approx(1.0)
    assert enrichment_score(genes, scores, {7, 8, 9}, p=0)[0] == pytest.approx(-1.0)
    assert abs(enrichment_score(genes, scores, {2, 5, 7}, p=1)[1][-1]) < 1e-12
    with pytest.raises(ValueError):
        enrichment_score(genes, scores, set(), p=1)
    with pytest.raises(ValueError):
        enrichment_score(genes, scores, set(genes), p=1)


def test_signal_to_noise():
    assert math.isclose(signal_to_noise([1, 3, 6, 10], [1, 1, 0, 0]), (2 - 8) / (math.sqrt(2) + math.sqrt(8)))
    with pytest.raises(ValueError):
        signal_to_noise([1, 2, 3], [1, 0, 0])


def make_data(rng, genes, shift_genes, shift, labels):
    expr = []
    for g in range(genes):
        row = [rng.gauss(0, 1) for _ in labels]
        if g in shift_genes:
            row = [x + shift * c for x, c in zip(row, labels)]
        expr.append(row)
    return expr


def test_permutation_results_and_determinism():
    rng = random.Random(63)
    labels = [1] * 5 + [0] * 5
    expr = make_data(rng, 60, set(range(10)), 2.0, labels)
    genes = list(range(60))
    sets = {"up": list(range(10)), "random": list(range(30, 40))}
    a = gsea(expr, genes, labels, sets, rng=random.Random(7), n_perm=200)
    b = gsea(expr, genes, labels, sets, rng=random.Random(7), n_perm=200)
    assert a == b
    assert a["up"]["es"] > 0 and a["up"]["nes"] > 1
    assert a["up"]["p_abs"] < 0.05 and a["up"]["p_sign"] < 0.05
    for v in a.values():
        assert 0 < v["p_abs"] <= 1 and 0 < v["p_sign"] <= 1
        assert (v["nes"] >= 0) == (v["es"] >= 0)
    with pytest.raises(ValueError):
        gsea(expr, genes, labels, sets)


def test_exact_enumeration_p_value_is_valid_under_the_null():
    # Under the null every one of the C(6, 3) = 20 label assignments is equally
    # likely, so P(p_abs <= u) <= u. Checked at u = 0.1 and 0.25 over 300 null data sets,
    # with the binomial tolerance 4 sqrt(u (1 - u) / 300).
    rng = random.Random(64)
    labels = [1, 1, 1, 0, 0, 0]
    genes = list(range(12))
    sets = {"S": [0, 1, 2, 3]}
    ps = []
    for _ in range(300):
        expr = make_data(rng, 12, set(), 0.0, labels)
        res = gsea(expr, genes, labels, sets, exact=True)
        ps.append(res["S"]["p_abs"])
    assert min(ps) >= 1 / 20
    for u in (0.1, 0.25):
        frac = sum(p <= u for p in ps) / len(ps)
        assert frac <= u + 4 * math.sqrt(u * (1 - u) / len(ps))
