# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/term-at-a-time-evaluation/. The authors are listed in prov/AQAN27.jsonl.

import random
from fractions import Fraction

import irtoy
from term_at_a_time_evaluation import bm25_index, exhaustive_top_k, taat, taat_maxscore


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


def close(a, b):
    """Same docids in the same order, and scores equal within 1e-9."""
    return [d for d, _ in a] == [d for d, _ in b] and all(abs(x - y) < 1e-9 for (_, x), (_, y) in zip(a, b))


def test_toy_check_values():
    index = toy_index()
    got, stats = taat(index, irtoy.tokenize(irtoy.QUERIES["q1"]), 5)
    assert [d for d, _ in got] == [1, 2, 8, 7, 4]
    want = [3.0283, 1.8893, 1.6292, 1.2743, 0.6896]
    assert all(abs(s - w) < 5e-5 for (_, s), w in zip(got, want))
    assert stats.scored == 5 and stats.postings == 9
    got, _ = taat(index, irtoy.tokenize(irtoy.QUERIES["q2"]), 3)
    assert [d for d, _ in got] == [4, 3, 5]
    assert taat(index, irtoy.tokenize(irtoy.QUERIES["q4"]), 5)[0] == []


def test_toy_maxscore_trace():
    # q1 with k = 1: after "search" and "array" the best accumulator,
    # d1 = 2.3091, exceeds the bound 0.9497 of "sorted", so "sorted"
    # creates no accumulator for d4.
    index = toy_index()
    got, stats = taat_maxscore(index, irtoy.tokenize(irtoy.QUERIES["q1"]), 1)
    assert [d for d, _ in got] == [1] and abs(got[0][1] - 3.0283) < 5e-5
    assert stats.scored == 4 and stats.postings == 8


def test_toy_against_exhaustive():
    index = toy_index()
    for text in irtoy.QUERIES.values():
        q = irtoy.tokenize(text)
        for k in range(0, 10):
            want = exhaustive_top_k(index, q, k, irtoy.DOCS)
            assert taat(index, q, k)[0] == want
            assert close(taat_maxscore(index, q, k)[0], want)


def test_edges():
    index = {"a": [(1, 3), (4, 1)], "b": [(4, 2)]}
    for f in (taat, taat_maxscore):
        assert f(index, [], 3)[0] == []
        assert f(index, ["a"], 0)[0] == []
        assert f(index, ["zz"], 3)[0] == []
        assert f(index, ["a", "b"], 1)[0] == [(1, 3)]
        assert f({"a": [(1, 3), (2, 3), (3, 3)]}, ["a"], 2)[0] == [(1, 3), (2, 3)]


def test_random_against_exhaustive():
    rng = random.Random(20251116)
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8, exact=trial % 2 == 0)
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        want = exhaustive_top_k(index, q, k, range(1, n + 1))
        got, stats = taat(index, q, k)
        assert got == want
        got2, stats2 = taat_maxscore(index, q, k)
        assert got2 == want
        union = set()
        for t in q:
            union.update(d for d, _ in index.get(t, []))
        assert stats.scored == len(union)
        # The variant never creates more accumulators or reads more weights.
        assert stats2.scored <= stats.scored
        assert stats2.postings <= stats.postings
