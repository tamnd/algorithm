# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maxscore/. The authors are listed in prov/ZNWK20.jsonl.

import random
from fractions import Fraction

import irtoy
from maxscore import bm25_index, daat_scored, exhaustive_top_k, maxscore


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
    q1 = irtoy.tokenize(irtoy.QUERIES["q1"])
    got, stats = maxscore(index, q1, 5)
    assert [d for d, _ in got] == [1, 2, 8, 7, 4]
    want = [3.0283, 1.8893, 1.6292, 1.2743, 0.6896]
    assert all(abs(s - w) < 5e-5 for (_, s), w in zip(got, want))
    assert stats.scored == 5
    got, _ = maxscore(index, irtoy.tokenize(irtoy.QUERIES["q2"]), 3)
    assert [d for d, _ in got] == [4, 3, 5]
    assert maxscore(index, irtoy.tokenize(irtoy.QUERIES["q4"]), 5)[0] == []


def test_toy_nonessential():
    # q1 with k = 2: after d1 and d2 the threshold is 1.8893. The bounds in
    # increasing order are 0.9497 (sorted), 0.98 (array) and 1.3291
    # (search), with prefix sums 0.9497 and 1.9297, so "sorted" becomes
    # nonessential. d4 contains only "sorted" and is never a candidate.
    # d7 is scored fully. For d8 the partial score 0.9396 of "array" plus
    # the bound 0.9497 of "sorted" equals the threshold, so the probe of
    # "sorted" is skipped and d8 is not scored fully.
    index = toy_index()
    got, stats = maxscore(index, irtoy.tokenize(irtoy.QUERIES["q1"]), 2)
    assert [d for d, _ in got] == [1, 2]
    assert stats.scored == 3


def test_toy_against_exhaustive():
    index = toy_index()
    for text in irtoy.QUERIES.values():
        q = irtoy.tokenize(text)
        for k in range(0, 10):
            got, stats = maxscore(index, q, k)
            assert close(got, exhaustive_top_k(index, q, k, irtoy.DOCS))
            assert stats.scored <= daat_scored(index, q)


def test_edges():
    index = {"a": [(1, 3), (4, 1)], "b": [(4, 2)]}
    assert maxscore(index, [], 3)[0] == []
    assert maxscore(index, ["a"], 0)[0] == []
    assert maxscore(index, ["zz"], 3)[0] == []
    assert maxscore(index, ["a", "b"], 1)[0] == [(1, 3)]
    assert maxscore(index, ["a", "b"], 5)[0] == [(1, 3), (4, 3)]
    assert maxscore({"a": [(1, 3), (2, 3), (3, 3)]}, ["a"], 2)[0] == [(1, 3), (2, 3)]


def test_random_against_exhaustive():
    rng = random.Random(20251119)
    total_ms = total_daat = 0
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8, exact=trial % 2 == 0)
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        got, stats = maxscore(index, q, k)
        assert got == exhaustive_top_k(index, q, k, range(1, n + 1))
        assert stats.scored <= daat_scored(index, q)
        total_ms += stats.scored
        total_daat += daat_scored(index, q)
    assert total_ms < total_daat
