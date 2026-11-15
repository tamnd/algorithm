# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tiered-index/. The authors are listed in prov/J6839A.jsonl.

import random
from fractions import Fraction

import irtoy
from tiered_index import bm25_index, build, exhaustive_top_k, search


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


def test_toy_tiers():
    index = toy_index()
    taus = [1.5, 1.0]
    tiers = build(index, taus)
    assert tiers[0]["list"] == [4] and tiers[0]["rank"] == [7]
    assert "search" not in tiers[0] and tiers[1]["search"] == [1, 7]
    assert tiers[2]["sorted"] == [1, 2, 4, 8] and tiers[2]["array"] == [1, 2, 8]
    q1 = irtoy.tokenize(irtoy.QUERIES["q1"])
    # k = 1: after tier 2 the best score 3.0283 is at least 3 * 1.0.
    got, stats = search(index, tiers, taus, q1, 1)
    assert [d for d, _ in got] == [1] and stats.tiers == 2 and stats.scored == 2
    # k = 2: the approximate rule stops after tier 2 with d1 and d7, and
    # misses d2. The safe rule reads tier 3 and finds d2.
    got, _ = search(index, tiers, taus, q1, 2, "approx")
    assert [d for d, _ in got] == [1, 7]
    got, stats = search(index, tiers, taus, q1, 2)
    assert [d for d, _ in got] == [1, 2] and stats.tiers == 3


def test_toy_safe_against_exhaustive():
    index = toy_index()
    for taus in ([1.5, 1.0], [2.0], [1.0, 0.9, 0.7], [5.0]):
        tiers = build(index, taus)
        for text in irtoy.QUERIES.values():
            q = irtoy.tokenize(text)
            for k in range(0, 10):
                got, _ = search(index, tiers, taus, q, k)
                assert got == exhaustive_top_k(index, q, k, irtoy.DOCS)


def test_edges():
    index = {"a": [(1, 3), (4, 1)], "b": [(4, 2)]}
    taus = [2]
    tiers = build(index, taus)
    assert tiers == [{"a": [1], "b": [4]}, {"a": [4]}]
    for stop in ("safe", "approx"):
        assert search(index, tiers, taus, [], 3, stop)[0] == []
        assert search(index, tiers, taus, ["a"], 0, stop)[0] == []
        assert search(index, tiers, taus, ["zz"], 3, stop)[0] == []
        assert search(index, tiers, taus, ["a", "b"], 5, stop)[0] == [(1, 3), (4, 3)]
    assert search(index, tiers, taus, ["a", "b"], 1)[0] == [(1, 3)]


def test_random():
    rng = random.Random(20251121)
    missed = 0
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8, exact=trial % 2 == 0)
        weights = sorted({w for p in index.values() for _, w in p if w > 0}, reverse=True)
        taus = sorted(rng.sample(weights, min(len(weights), rng.randint(1, 4))), reverse=True)
        tiers = build(index, taus)
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        union = {d for t in q for d, _ in index.get(t, [])}
        want = exhaustive_top_k(index, q, k, range(1, n + 1))
        true = dict(exhaustive_top_k(index, q, n, range(1, n + 1)))
        # The safe rule: the exact top k.
        got, safe = search(index, tiers, taus, q, k)
        assert got == want
        assert safe.scored <= len(union)
        # The approximate rule: min(k, matches) documents with their true
        # scores, in tie-rule order, after no more work than the safe rule.
        got, approx = search(index, tiers, taus, q, k, "approx")
        assert len(got) == min(k, len(union))
        assert all(d in union and s == true[d] for d, s in got)
        assert got == sorted(got, key=lambda p: (-p[1], p[0]))
        assert approx.scored <= safe.scored
        missed += got != want
    assert missed > 0
