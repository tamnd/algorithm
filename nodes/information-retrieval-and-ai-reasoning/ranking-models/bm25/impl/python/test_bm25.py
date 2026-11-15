# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bm25/. The authors are listed in prov/T2NA0M.jsonl.

import math
import random

import irtoy
from bm25 import BM25, idf_lucene, idf_rsj

# Scores are compared to the 4 decimals printed on the page.
TOL4 = 5e-5
# Two ways of computing the same float sum are compared with this tolerance.
TOL = 1e-9

DOCS = {d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()}


def q(name: str) -> list:
    return irtoy.tokenize(irtoy.QUERIES[name])


def close(got: list, want: list, tol: float = TOL4) -> None:
    assert [d for d, _ in got] == [d for d, _ in want], (got, want)
    for (_, s), (_, t) in zip(got, want):
        assert abs(s - t) <= tol, (got, want)


def brute_score(docs: dict, query: list, d, k1: float, b: float, idf: str) -> float:
    """The BM25 formula written out directly, for one document, with qtf counted linearly."""
    n = len(docs)
    avgdl = sum(len(t) for t in docs.values()) / n
    total = 0.0
    for t in sorted(set(query)):
        df = sum(1 for toks in docs.values() if t in toks)
        tf = docs[d].count(t)
        if df == 0 or tf == 0:
            continue
        w = math.log(1 + (n - df + 0.5) / (df + 0.5)) if idf == "lucene" else math.log((n - df + 0.5) / (df + 0.5))
        big_k = k1 * (1 - b + b * len(docs[d]) / avgdl)
        total += query.count(t) * w * tf * (k1 + 1) / (tf + big_k)
    return total


def test_check_values_q1_lucene() -> None:
    m = BM25(DOCS, k1=1.2, b=0.75)
    close(m.rank(q("q1")), [(1, 3.0283), (2, 1.8893), (8, 1.6292), (7, 1.2743), (4, 0.6896)])


def test_hand_computation_of_d2() -> None:
    m = BM25(DOCS)
    assert abs(m.avgdl - 9.875) <= TOL
    assert abs(m.length_factor(1) - 0.933544) <= 1e-6
    assert abs(m.length_factor(2) - 1.009494) <= 1e-6
    assert abs(m.tf_part(2, 2) - 1.370122) <= 1e-6
    assert abs(m.tf_part(1, 2) - 0.994848) <= 1e-6
    d2 = m.idf("sorted") * m.tf_part(2, 2) + m.idf("array") * m.tf_part(1, 2)
    assert abs(d2 - 1.8893) <= TOL4


def test_rsj_idf_of_sorted_is_zero() -> None:
    assert irtoy.df("sorted") == 4 and irtoy.N == 8
    assert idf_rsj(8, 4) == 0.0
    assert abs(idf_lucene(8, 4) - math.log(2)) <= TOL
    m = BM25(DOCS, idf="rsj")
    close(m.rank(q("q1")), [(1, 1.4604), (7, 0.9506), (2, 0.4497), (8, 0.4497), (4, 0.0)])


def test_rsj_idf_is_negative_above_half() -> None:
    assert idf_rsj(8, 5) < 0 < idf_lucene(8, 5)
    assert idf_rsj(8, 3) > 0


def test_q2_tie_broken_by_id() -> None:
    got = BM25(DOCS).rank(q("q2"))
    close(got, [(4, 2.6946), (3, 2.2139), (5, 2.2139), (2, 1.2743)])
    assert got[1][1] == got[2][1]
    assert [d for d, _ in got[1:3]] == [3, 5]


def test_q3_and_empty_q4() -> None:
    close(BM25(DOCS).rank(q("q3")), [(7, 3.5651)])
    assert BM25(DOCS).rank(q("q4")) == []
    assert BM25(DOCS).rank([]) == []


def test_top_k_is_a_prefix() -> None:
    m = BM25(DOCS)
    full = m.rank(q("q1"))
    for k in range(0, 7):
        assert m.rank(q("q1"), k) == full[:k]


def test_saturation_bound_and_monotone_tf() -> None:
    m = BM25(DOCS)
    prev = 0.0
    for tf in range(1, 200):
        cur = m.tf_part(tf, 2)
        assert prev < cur < m.k1 + 1
        prev = cur
    assert m.tf_part(0, 2) == 0.0


def test_b_zero_ignores_length() -> None:
    docs = {1: ["x", "y"], 2: ["x"] + ["z"] * 30, 3: ["w"]}
    got = BM25(docs, b=0.0).rank(["x"])
    assert got[0][1] == got[1][1]
    got = BM25(docs, b=0.75).rank(["x"])
    assert got[0][0] == 1 and got[0][1] > got[1][1]


def test_k1_zero_is_binary() -> None:
    m = BM25(DOCS, k1=0.0)
    for d, s in m.rank(q("q1")):
        want = sum(m.idf(t) for t in set(q("q1")) if t in DOCS[d])
        assert abs(s - want) <= TOL


def test_k3_query_term_frequency() -> None:
    m_lin = BM25(DOCS)
    m_bin = BM25(DOCS, k3=0.0)
    m_k3 = BM25(DOCS, k3=7.0)
    s1 = dict(m_lin.rank(["sorted"]))
    s2 = dict(m_lin.rank(["sorted", "sorted"]))
    assert all(abs(s2[d] - 2 * s1[d]) <= TOL for d in s1)
    assert dict(m_bin.rank(["sorted", "sorted"])) == dict(m_bin.rank(["sorted"]))
    s3 = dict(m_k3.rank(["sorted", "sorted"]))
    assert all(abs(s3[d] - s1[d] * 8 * 2 / 9) <= TOL for d in s1)


def test_dropping_the_k1_plus_1_factor_keeps_the_order() -> None:
    m = BM25(DOCS)
    for name in irtoy.QUERIES:
        query = q(name)
        alt = {}
        for d, _ in m.rank(query):
            alt[d] = sum(m.idf(t) * DOCS[d].count(t) / (DOCS[d].count(t) + m.k1 * m.length_factor(d))
                         for t in set(query))
        order = sorted(alt, key=lambda d: (-alt[d], d))
        assert order == [d for d, _ in m.rank(query)]


def test_random_collections_against_the_formula() -> None:
    rng = random.Random(20261115)
    vocab = [f"t{i}" for i in range(12)]
    for _ in range(300):
        n = rng.randint(1, 15)
        ids = rng.sample(range(100), n)
        docs = {d: [rng.choice(vocab[: rng.randint(1, 12)]) for _ in range(rng.randint(1, 25))] for d in ids}
        k1 = rng.choice([0.0, 0.5, 1.2, 2.0])
        b = rng.choice([0.0, 0.3, 0.75, 1.0])
        idf = rng.choice(["lucene", "rsj"])
        m = BM25(docs, k1=k1, b=b, idf=idf)
        query = [rng.choice(vocab + ["absent"]) for _ in range(rng.randint(0, 5))]
        got = m.rank(query)
        matching = sorted(d for d in docs if any(t in docs[d] for t in query))
        assert sorted(d for d, _ in got) == matching
        for d, s in got:
            assert abs(s - brute_score(docs, query, d, k1, b, idf)) <= TOL
        keys = [(-s, d) for d, s in got]
        assert keys == sorted(keys)


def test_bad_parameters() -> None:
    for kw in ({"k1": -1.0}, {"b": 1.5}, {"b": -0.1}):
        try:
            BM25(DOCS, **kw)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted {kw}")
