# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/document-at-a-time-evaluation/. The authors are listed in prov/CR25E3.jsonl.

import random
from fractions import Fraction

import irtoy
from document_at_a_time_evaluation import bm25_index, daat, exhaustive_top_k


def toy_index():
    return bm25_index({d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()})


def random_index(rng, n, vocab, exact):
    """A random index on docids 1..n with nonnegative weights.

    exact selects Fraction weights; else small integers, which give many
    ties.
    """
    index = {}
    for t in range(vocab):
        density = rng.random() ** 2
        ids = [d for d in range(1, n + 1) if rng.random() < density]
        if exact:
            index[f"t{t}"] = [(d, Fraction(rng.randint(0, 40), rng.randint(1, 6))) for d in ids]
        else:
            index[f"t{t}"] = [(d, rng.randint(0, 5)) for d in ids]
    return index


def test_toy_check_values():
    index = toy_index()
    got, stats = daat(index, irtoy.tokenize(irtoy.QUERIES["q1"]), 5)
    assert [d for d, _ in got] == [1, 2, 8, 7, 4]
    want = [3.0283, 1.8893, 1.6292, 1.2743, 0.6896]
    assert all(abs(s - w) < 5e-5 for (_, s), w in zip(got, want))
    assert stats.scored == 5 and stats.postings == 9
    # q2: d3 and d5 tie at 2.2139; the smaller docid ranks first.
    got, _ = daat(index, irtoy.tokenize(irtoy.QUERIES["q2"]), 3)
    assert [d for d, _ in got] == [4, 3, 5]
    assert got[1][1] == got[2][1]
    # q4: no query term occurs in the collection.
    assert daat(index, irtoy.tokenize(irtoy.QUERIES["q4"]), 5)[0] == []


def test_toy_against_exhaustive():
    index = toy_index()
    for text in irtoy.QUERIES.values():
        q = irtoy.tokenize(text)
        for k in range(0, 10):
            got, _ = daat(index, q, k)
            assert got == exhaustive_top_k(index, q, k, irtoy.DOCS)


def test_edges():
    index = {"a": [(1, 3), (4, 1)], "b": [(4, 2)]}
    assert daat(index, [], 3)[0] == []
    assert daat(index, ["a"], 0)[0] == []
    assert daat(index, ["zz"], 3)[0] == []
    # d1 and d4 both score 3, so d1 ranks first.
    assert daat(index, ["a", "b"], 1)[0] == [(1, 3)]
    assert daat(index, ["a", "b"], 5)[0] == [(1, 3), (4, 3)]
    # Equal scores: the smaller docid wins the last place.
    assert daat({"a": [(1, 3), (2, 3), (3, 3)]}, ["a"], 2)[0] == [(1, 3), (2, 3)]


def test_random_against_exhaustive():
    rng = random.Random(20251115)
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8, exact=trial % 2 == 0)
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        got, stats = daat(index, q, k)
        assert got == exhaustive_top_k(index, q, k, range(1, n + 1))
        union = set()
        for t in q:
            union.update(d for d, _ in index.get(t, []))
        # DAAT scores every matching document once and reads every posting.
        assert stats.scored == len(union)
        assert stats.postings == sum(len(index.get(t, [])) for t in q)
