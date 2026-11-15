# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combmnz/. The authors are listed in prov/HTFVCS.jsonl.

import math
import random
import statistics

import irtoy
from combmnz import comb, comb_scores, normalize


def bm25_q1():
    """BM25 with k1 = 1.2, b = 0.75 and the Lucene idf on q1 of the toy collection."""
    q = irtoy.tokenize(irtoy.QUERIES["q1"])
    out = {}
    for d in irtoy.DOCS:
        s = 0.0
        for t in q:
            f = irtoy.tf(t, d)
            if f:
                idf = math.log(1 + (irtoy.N - irtoy.df(t) + 0.5) / (irtoy.df(t) + 0.5))
                bd = 1 - 0.75 + 0.75 * irtoy.doc_len(d) / irtoy.avgdl()
                s += idf * f * 2.2 / (f + 1.2 * bd)
        if s:
            out[d] = s
    return out


def random_runs(rng):
    runs = []
    for _ in range(rng.randint(1, 5)):
        docs = rng.sample(range(1, 11), rng.randint(1, 10))
        runs.append({d: round(rng.uniform(-5, 20), 3) for d in docs})
    return runs


def close(a, b):
    return abs(a - b) < 1e-9


def test_normalizations():
    rng = random.Random(1)
    for _ in range(300):
        run = random_runs(rng)[0]
        mm = normalize(run, "minmax")
        lo, hi = min(run.values()), max(run.values())
        for d in run:
            want = (run[d] - lo) / (hi - lo) if hi > lo else 1.0
            assert close(mm[d], want)
        sm = normalize(run, "sum")
        assert close(sum(sm.values()), 1.0)
        z = normalize(run, "zmuv")
        if len(set(run.values())) > 1:
            assert close(statistics.fmean(z.values()), 0.0)
            assert close(statistics.pstdev(z.values()), 1.0)
        assert normalize(run, "none") == run


def test_rules_match_the_formulas():
    rng = random.Random(2)
    for _ in range(300):
        runs = random_runs(rng)
        norm = rng.choice(["minmax", "sum", "zmuv", "none"])
        normed = [normalize(r, norm) for r in runs]
        union = {d for r in runs for d in r}
        for rule in ("SUM", "MNZ", "ANZ", "MAX", "MIN", "MED"):
            s = comb_scores(runs, rule, norm)
            assert set(s) == union
            for d in union:
                vals = [r[d] for r in normed if d in r]
                h = len(vals)
                want = {
                    "SUM": sum(vals),
                    "MNZ": h * sum(vals),
                    "ANZ": sum(vals) / h,
                    "MAX": max(vals),
                    "MIN": min(vals),
                    "MED": statistics.median(vals),
                }[rule]
                assert close(s[d], want)
            assert comb(runs, rule, norm) == sorted(union, key=lambda d: (-s[d], d))


def test_minmax_makes_fusion_blind_to_scale_and_shift():
    rng = random.Random(3)
    for _ in range(200):
        runs = random_runs(rng)
        a, b = rng.uniform(0.1, 10), rng.uniform(-50, 50)
        moved = [{d: a * s + b for d, s in runs[0].items()}] + runs[1:]
        for rule in ("SUM", "MNZ"):
            s1 = comb_scores(runs, rule, "minmax")
            s2 = comb_scores(moved, rule, "minmax")
            for d in s1:
                assert abs(s1[d] - s2[d]) < 1e-6


def test_toy_runs():
    a = bm25_q1()
    b = irtoy.RUN["q1"]
    s = comb_scores([a, b], "SUM")
    lo, hi = 0.6896, 3.0283
    assert abs(s[1] - 2.0) < 1e-9 and abs(s[6] - 1.0) < 1e-9
    assert abs(s[8] - ((1.6292 - lo) / (hi - lo) + 0.5)) < 1e-3
    assert abs(s[2] - (1.8893 - lo) / (hi - lo)) < 1e-3
    assert s[4] == 0.0
    assert comb([a, b], "SUM") == [1, 6, 8, 2, 7, 4]
    m = comb_scores([a, b], "MNZ")
    assert abs(m[1] - 4.0) < 1e-9 and abs(m[8] - 2 * s[8]) < 1e-12 and abs(m[2] - 2 * s[2]) < 1e-12
    assert comb([a, b], "MNZ") == [1, 8, 2, 6, 7, 4]
    # Without normalization, document 4 rises above 6 and 7 on its raw scores 0.69 and 1.0.
    assert comb([a, b], "SUM", "none") == [1, 8, 2, 6, 4, 7]
    # With z-scores, MNZ multiplies a negative sum by h = 2, so document 4 falls further.
    z = comb_scores([a, b], "MNZ", "zmuv")
    assert z[4] < 0 and z[4] == min(z.values())


def test_edge_cases():
    assert comb([]) == []
    assert comb([{}]) == []
    assert comb([{5: 3.0}], "MNZ") == [5]
    assert comb_scores([{1: 2.0, 2: 2.0}], "SUM") == {1: 1.0, 2: 1.0}
