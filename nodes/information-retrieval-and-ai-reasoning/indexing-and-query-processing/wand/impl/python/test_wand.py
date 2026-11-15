# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wand/. The authors are listed in prov/F02PAM.jsonl.

import random
from fractions import Fraction

import irtoy
from wand import bm25_index, daat_scored, exhaustive_top_k, wand


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
    q1 = irtoy.tokenize(irtoy.QUERIES["q1"])
    got, stats = wand(index, q1, 5)
    assert [d for d, _ in got] == [1, 2, 8, 7, 4]
    want = [3.0283, 1.8893, 1.6292, 1.2743, 0.6896]
    assert all(abs(s - w) < 5e-5 for (_, s), w in zip(got, want))
    assert stats.scored == 5
    # k = 1: after d1 the threshold is 3.0283, and no prefix of bounds
    # (at most 0.9497 + 0.98 + 1.3291) exceeds it.
    got, stats = wand(index, q1, 1)
    assert [d for d, _ in got] == [1] and stats.scored == 1
    got, _ = wand(index, irtoy.tokenize(irtoy.QUERIES["q2"]), 3)
    assert [d for d, _ in got] == [4, 3, 5]
    assert wand(index, irtoy.tokenize(irtoy.QUERIES["q4"]), 5)[0] == []


def test_toy_against_exhaustive():
    index = toy_index()
    for text in irtoy.QUERIES.values():
        q = irtoy.tokenize(text)
        for k in range(0, 10):
            got, stats = wand(index, q, k)
            assert got == exhaustive_top_k(index, q, k, irtoy.DOCS)
            assert stats.scored <= daat_scored(index, q)


def test_edges():
    index = {"a": [(1, 3), (4, 1)], "b": [(4, 2)]}
    assert wand(index, [], 3)[0] == []
    assert wand(index, ["a"], 0)[0] == []
    assert wand(index, ["zz"], 3)[0] == []
    assert wand(index, ["a", "b"], 1)[0] == [(1, 3)]
    assert wand(index, ["a", "b"], 5)[0] == [(1, 3), (4, 3)]
    assert wand({"a": [(1, 3), (2, 3), (3, 3)]}, ["a"], 2)[0] == [(1, 3), (2, 3)]


def test_factor_above_one_is_unsafe():
    # The true top 1 is d2 with score 2. After d1 the threshold is 1, and
    # with factor 2 the bound sum 2 at d2 is not greater than 2.
    index = {"a": [(1, 1), (2, 1)], "b": [(2, 1)]}
    assert wand(index, ["a", "b"], 1)[0] == [(2, 2)]
    assert wand(index, ["a", "b"], 1, factor=2)[0] == [(1, 1)]


def test_random_against_exhaustive():
    rng = random.Random(20251117)
    total_wand = total_daat = 0
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8, exact=trial % 2 == 0)
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        got, stats = wand(index, q, k)
        assert got == exhaustive_top_k(index, q, k, range(1, n + 1))
        assert stats.scored <= daat_scored(index, q)
        total_wand += stats.scored
        total_daat += daat_scored(index, q)
    assert total_wand < total_daat
