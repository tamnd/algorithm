# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blocked-sort-based-indexing/. The authors are listed in prov/7YJRVM.jsonl.

import math
import random

import irtoy
from blocked_sort_based_indexing import bsbi, invert


def direct_index(docs: list[tuple[int, list[str]]]) -> dict[str, list[tuple[int, int]]]:
    """The reference: one dictionary of dictionaries, built in memory."""
    m: dict[str, dict[int, int]] = {}
    for d, tokens in docs:
        for w in tokens:
            m.setdefault(w, {})
            m[w][d] = m[w].get(d, 0) + 1
    return {w: sorted(p.items()) for w, p in m.items()}


def toy_docs() -> list[tuple[int, list[str]]]:
    return [(d, irtoy.tokenize(t)) for d, t in sorted(irtoy.DOCS.items())]


def check_runs(runs: list[list[tuple[int, int, int]]], tokens: int, m: int) -> None:
    assert len(runs) == math.ceil(tokens / m)
    for run in runs:
        keys = [(t, d) for t, d, _ in run]
        assert keys == sorted(set(keys))
        assert sum(f for _, _, f in run) <= m


def test_toy_collection_block_16() -> None:
    docs = toy_docs()
    index, runs = bsbi(docs, 16)
    assert index == direct_index(docs)
    assert [len(r) for r in runs] == [15, 16, 16, 15, 15]
    assert sum(len(r) for r in runs) == 77
    assert len(index) == 50 and sum(len(p) for p in index.values()) == 74
    assert index["sorted"] == [(1, 1), (2, 2), (4, 1), (8, 1)]
    assert index["a"] == [(1, 2), (3, 1), (4, 2), (6, 2), (7, 1)]
    check_runs(runs, 79, 16)


def test_toy_collection_every_block_size() -> None:
    docs = toy_docs()
    want = direct_index(docs)
    for m in range(1, 90):
        index, runs = bsbi(docs, m)
        assert index == want
        check_runs(runs, 79, m)


def test_invert_groups_pairs() -> None:
    assert invert([(2, 5), (1, 7), (2, 5), (1, 3)]) == [(1, 3, 1), (1, 7, 1), (2, 5, 2)]
    assert invert([]) == []


def test_edge_cases() -> None:
    assert bsbi([], 3) == ({}, [])
    assert bsbi([(1, []), (2, [])], 3) == ({}, [])
    index, runs = bsbi([(4, ["x", "x", "x"])], 1)
    assert index == {"x": [(4, 3)]} and len(runs) == 3
    try:
        bsbi([(1, ["x"])], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("block size 0 was accepted")


def test_random_collections() -> None:
    rng = random.Random(20261115)
    for _ in range(600):
        vocab = [f"w{i}" for i in range(rng.randint(1, 30))]
        docs = []
        d = 0
        for _ in range(rng.randint(0, 12)):
            d += rng.randint(1, 4)
            docs.append((d, [rng.choice(vocab) for _ in range(rng.randint(0, 15))]))
        tokens = sum(len(t) for _, t in docs)
        m = rng.randint(1, 12)
        index, runs = bsbi(docs, m)
        assert index == direct_index(docs)
        check_runs(runs, tokens, m)
