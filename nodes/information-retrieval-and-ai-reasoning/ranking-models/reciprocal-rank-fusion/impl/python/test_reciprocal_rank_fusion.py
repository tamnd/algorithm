# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reciprocal-rank-fusion/. The authors are listed in prov/552S8S.jsonl.

import random
from fractions import Fraction

import irtoy
from reciprocal_rank_fusion import rrf, rrf_scores, to_ranking


def random_profile(rng, n, m, partial):
    items = list(range(1, n + 1))
    out = []
    for _ in range(m):
        r = items[:]
        rng.shuffle(r)
        if partial:
            r = r[: rng.randint(0, n)]
        out.append(r)
    return out


def bm25_q1():
    """BM25 with k1 = 1.2, b = 0.75 and the Lucene idf on q1 of the toy collection."""
    q = irtoy.tokenize(irtoy.QUERIES["q1"])
    import math

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


def test_scores_match_the_formula():
    rng = random.Random(1)
    for _ in range(300):
        prof = random_profile(rng, rng.randint(1, 8), rng.randint(1, 5), partial=True)
        k = rng.choice([0, 1, 5, 60, 1000])
        if k == 0 and any(len(r) == 0 for r in prof):
            continue
        s = rrf_scores(prof, k, exact=True)
        union = {d for r in prof for d in r}
        assert set(s) == union
        for d in union:
            want = sum((Fraction(1, k + r.index(d) + 1) for r in prof if d in r), Fraction(0))
            assert s[d] == want
        got = rrf(prof, k)
        assert got == sorted(union, key=lambda d: (-s[d], d))
        f = rrf_scores(prof, k)
        for d in union:
            assert abs(f[d] - float(s[d])) < 1e-12


def test_large_k_gives_the_order_of_the_total_rank():
    rng = random.Random(2)
    for _ in range(300):
        n, m = rng.randint(1, 7), rng.randint(1, 5)
        prof = random_profile(rng, n, m, partial=False)
        k = m * n * n + 1
        s = rrf_scores(prof, k, exact=True)
        total = {d: sum(r.index(d) + 1 for r in prof) for d in range(1, n + 1)}
        for x in total:
            for y in total:
                if total[x] < total[y]:
                    assert s[x] > s[y]


def test_one_top_rank_beats_a_better_total_at_k_60():
    # x has ranks 1 and 41 (total 42), y has ranks 20 and 20 (total 40).
    a = ["x"] + [f"a{i}" for i in range(18)] + ["y"] + [f"b{i}" for i in range(21)]
    b = [f"c{i}" for i in range(19)] + ["y"] + [f"d{i}" for i in range(20)] + ["x"]
    assert a.index("x") + 1 == 1 and b.index("x") + 1 == 41
    assert a.index("y") + 1 == 20 and b.index("y") + 1 == 20
    s = rrf_scores([a, b], 60, exact=True)
    assert s["x"] == Fraction(1, 61) + Fraction(1, 101)
    assert s["y"] == Fraction(2, 80)
    assert s["x"] > s["y"]


def test_toy_runs():
    run_a = to_ranking(bm25_q1())
    run_b = to_ranking(irtoy.RUN["q1"])
    assert run_a == [1, 2, 8, 7, 4]
    assert run_b == [1, 6, 8, 2, 4]
    s = rrf_scores([run_a, run_b], 60, exact=True)
    assert s == {
        1: Fraction(2, 61),
        2: Fraction(1, 62) + Fraction(1, 64),
        8: Fraction(2, 63),
        6: Fraction(1, 62),
        7: Fraction(1, 64),
        4: Fraction(2, 65),
    }
    assert rrf([run_a, run_b]) == [1, 2, 8, 4, 6, 7]
    # Cut to depth 2: only documents 1, 2 and 6 are left, and 2 ties with 6.
    assert rrf([run_a, run_b], depth=2) == [1, 2, 6]


def test_edge_cases():
    assert rrf([]) == []
    assert rrf([[], []]) == []
    assert rrf([[3, 1, 2]]) == [3, 1, 2]
