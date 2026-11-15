# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/block-max-wand/. The authors are listed in prov/MB0KJQ.jsonl.

import random
from fractions import Fraction

import irtoy
from block_max_wand import bm25_index, block_max_wand, daat_scored, exhaustive_top_k


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
    got, stats = block_max_wand(index, q1, 5, b=2)
    assert [d for d, _ in got] == [1, 2, 8, 7, 4]
    want = [3.0283, 1.8893, 1.6292, 1.2743, 0.6896]
    assert all(abs(s - w) < 5e-5 for (_, s), w in zip(got, want))
    assert stats.scored == 5
    got, _ = block_max_wand(index, irtoy.tokenize(irtoy.QUERIES["q2"]), 3, b=2)
    assert [d for d, _ in got] == [4, 3, 5]
    assert block_max_wand(index, irtoy.tokenize(irtoy.QUERIES["q4"]), 5)[0] == []


def test_block_check_skips():
    # "a" has a block max of 9 only in its first block. With k = 1 the
    # threshold after d1 is 10. Every later pivot has a list bound sum of
    # 9 + 2 = 11 > 10, so WAND scores d3, d4 and d5, but the block maxes
    # 1 + 2 = 3 are not greater than 10, so BMW skips them.
    index = {"a": [(1, 9), (2, 1), (3, 1), (4, 1), (5, 1)], "b": [(1, 1), (3, 2), (4, 2), (5, 2)]}
    got, stats = block_max_wand(index, ["a", "b"], 1, b=2)
    assert got == [(1, 10)]
    assert stats.scored == 1


def test_toy_against_exhaustive():
    index = toy_index()
    for text in irtoy.QUERIES.values():
        q = irtoy.tokenize(text)
        for b in (1, 2, 3, 64):
            for k in range(0, 10):
                got, stats = block_max_wand(index, q, k, b)
                assert got == exhaustive_top_k(index, q, k, irtoy.DOCS)
                assert stats.scored <= daat_scored(index, q)


def test_edges():
    index = {"a": [(1, 3), (4, 1)], "b": [(4, 2)]}
    for b in (1, 2):
        assert block_max_wand(index, [], 3, b)[0] == []
        assert block_max_wand(index, ["a"], 0, b)[0] == []
        assert block_max_wand(index, ["zz"], 3, b)[0] == []
        assert block_max_wand(index, ["a", "b"], 1, b)[0] == [(1, 3)]
        assert block_max_wand(index, ["a", "b"], 5, b)[0] == [(1, 3), (4, 3)]
        assert block_max_wand({"a": [(1, 3), (2, 3), (3, 3)]}, ["a"], 2, b)[0] == [(1, 3), (2, 3)]


def test_random_against_exhaustive():
    rng = random.Random(20251118)
    total_bmw = total_daat = 0
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8, exact=trial % 2 == 0)
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        b = rng.randint(1, 8)
        got, stats = block_max_wand(index, q, k, b)
        assert got == exhaustive_top_k(index, q, k, range(1, n + 1))
        assert stats.scored <= daat_scored(index, q)
        total_bmw += stats.scored
        total_daat += daat_scored(index, q)
    assert total_bmw < total_daat
