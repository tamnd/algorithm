# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impact-ordered-index/. The authors are listed in prov/BBYS9T.jsonl.

import random

import irtoy
from impact_ordered_index import bm25_index, build, exhaustive_top_k, saat, to_document_order


def toy_index():
    return bm25_index({d: irtoy.tokenize(t) for d, t in irtoy.DOCS.items()})


def random_index(rng, n, vocab):
    """A random index on docids 1..n with integer impacts 1..9."""
    index = {}
    for t in range(vocab):
        density = rng.random() ** 2
        ids = [d for d in range(1, n + 1) if rng.random() < density]
        index[f"t{t}"] = [(d, rng.randint(1, 9)) for d in ids]
    return index


def test_toy_quantized():
    index = toy_index()
    q1 = irtoy.tokenize(irtoy.QUERIES["q1"])
    q2 = irtoy.tokenize(irtoy.QUERIES["q2"])
    imp = build(index, 8)
    assert imp["search"] == [(6, [1]), (5, [7])]
    assert imp["sorted"] == [(4, [2]), (3, [1, 4, 8])]
    got, stats = saat(imp, q1, 5)
    assert got == [(1, 13), (2, 8), (8, 7), (7, 5), (4, 3)]
    assert stats.postings == 9 and stats.scored == 5
    # With 8 levels the ranking of q1 and q2 is the BM25 ranking.
    for q in (q1, q2):
        assert [d for d, _ in saat(imp, q, 5)[0]] == [d for d, _ in exhaustive_top_k(index, q, 5, irtoy.DOCS)]
    # With 4 levels d3, d4 and d5 all get 5 for q2, so d3 ranks first,
    # though d4 has the best BM25 score.
    assert saat(build(index, 4), q2, 1)[0] == [(3, 5)]


def test_safe_stop_example():
    imp = {"a": [(9, [1]), (1, [2, 3])], "b": [(8, [1]), (2, [4])]}
    got, stats = saat(imp, ["a", "b"], 1, stop="safe")
    # After two segments d1 has 17, and any document can still gain at most
    # 1 + 2 = 3.
    assert got == [(1, 17)] and stats.postings == 2
    assert saat(imp, ["a", "b"], 1)[0] == [(1, 17)]
    assert saat(imp, ["a", "b"], 3)[0] == [(1, 17), (4, 2), (2, 1)]


def test_build_rejects_bad_impacts():
    for bad in (0, 2.5):
        try:
            build({"a": [(1, bad)]})
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")


def test_edges():
    imp = {"a": [(3, [1]), (1, [4])], "b": [(2, [4])]}
    for stop in ("none", "safe"):
        assert saat(imp, [], 3, stop)[0] == []
        assert saat(imp, ["a"], 0, stop)[0] == []
        assert saat(imp, ["zz"], 3, stop)[0] == []
        assert saat(imp, ["a", "b"], 1, stop)[0] == [(1, 3)]
        assert saat(imp, ["a", "b"], 5, stop)[0] == [(1, 3), (4, 3)]
    assert saat(imp, ["a", "b"], 5, "budget", 0)[0] == []


def test_random():
    rng = random.Random(20251120)
    saved = 0
    for trial in range(300):
        n = rng.randint(1, 200)
        index = random_index(rng, n, 8)
        imp = build(index)
        assert to_document_order(imp) == index
        q = rng.sample(sorted(index), rng.randint(1, 5))
        if rng.random() < 0.2:
            q.append("missing")
        k = rng.randint(1, 12)
        total = sum(len(index.get(t, [])) for t in q)
        union = len({d for t in q for d, _ in index.get(t, [])})
        want = exhaustive_top_k(index, q, k, range(1, n + 1))
        true = dict(exhaustive_top_k(index, q, n, range(1, n + 1)))
        # Run to the end: safe and exact.
        got, stats = saat(imp, q, k)
        assert got == want
        assert stats.postings == total and stats.scored == union
        # Safe early stop: exact docids in exact order, lower-bound scores.
        got, stats = saat(imp, q, k, "safe")
        assert [d for d, _ in got] == [d for d, _ in want]
        assert all(s <= true[d] for d, s in got)
        assert stats.postings <= total and stats.scored <= union
        saved += total - stats.postings
        # Budget stop: approximate; each score is at most the true score.
        budget = rng.randint(0, total)
        got, stats = saat(imp, q, k, "budget", budget)
        assert stats.postings == budget
        assert len(got) <= k and all(s <= true[d] for d, s in got)
        assert saat(imp, q, k, "budget", total)[0] == want
    assert saved > 0
