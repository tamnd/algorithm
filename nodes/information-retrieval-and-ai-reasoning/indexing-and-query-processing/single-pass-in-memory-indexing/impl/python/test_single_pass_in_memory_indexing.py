# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/single-pass-in-memory-indexing/. The authors are listed in prov/8P8GD3.jsonl.

import math
import random

import irtoy
from single_pass_in_memory_indexing import merge_blocks, spimi


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


def check_blocks(blocks, tokens: int, m: int) -> None:
    assert len(blocks) == math.ceil(tokens / m)
    for block in blocks:
        terms = [w for w, _ in block]
        assert terms == sorted(set(terms))
        used = 0
        for _, plist in block:
            ids = [d for d, _ in plist]
            assert ids == sorted(set(ids))
            used += sum(f for _, f in plist)
        assert used <= m


def test_toy_collection_block_16() -> None:
    docs = toy_docs()
    index, blocks = spimi(docs, 16)
    assert index == direct_index(docs)
    assert [len(b) for b in blocks] == [14, 13, 15, 15, 14]
    assert [sum(len(p) for _, p in b) for b in blocks] == [15, 16, 16, 15, 15]
    assert dict(blocks[0])["sorted"] == [(1, 1), (2, 1)]
    assert dict(blocks[1])["sorted"] == [(2, 1)]
    assert index["sorted"] == [(1, 1), (2, 2), (4, 1), (8, 1)]
    assert index["list"] == [(3, 1), (4, 2)]
    check_blocks(blocks, 79, 16)


def test_toy_collection_every_block_size() -> None:
    docs = toy_docs()
    want = direct_index(docs)
    for m in range(1, 90):
        index, blocks = spimi(docs, m)
        assert index == want
        check_blocks(blocks, 79, m)


def test_merge_joins_cut_document() -> None:
    blocks = [[("x", [(1, 1), (2, 1)])], [("w", [(2, 1)]), ("x", [(2, 3), (5, 1)])]]
    assert merge_blocks(blocks) == {"w": [(2, 1)], "x": [(1, 1), (2, 4), (5, 1)]}
    assert blocks[0][0][1] == [(1, 1), (2, 1)]


def test_edge_cases() -> None:
    assert spimi([], 2) == ({}, [])
    assert spimi([(1, []), (3, [])], 2) == ({}, [])
    index, blocks = spimi([(7, ["y", "y", "y"])], 1)
    assert index == {"y": [(7, 3)]} and len(blocks) == 3
    try:
        spimi([(1, ["y"])], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("block size 0 was accepted")


def test_random_collections() -> None:
    rng = random.Random(20261116)
    for _ in range(600):
        vocab = [f"w{i}" for i in range(rng.randint(1, 30))]
        docs = []
        d = 0
        for _ in range(rng.randint(0, 12)):
            d += rng.randint(1, 4)
            docs.append((d, [rng.choice(vocab) for _ in range(rng.randint(0, 15))]))
        tokens = sum(len(t) for _, t in docs)
        m = rng.randint(1, 12)
        index, blocks = spimi(docs, m)
        assert index == direct_index(docs)
        check_blocks(blocks, tokens, m)
