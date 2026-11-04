# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-radix-tree/. The authors are listed in prov/1RJXRZ.jsonl.

import random

import pytest

from adaptive_radix_tree import AdaptiveRadixTree, _Inner

WORDS = [b"tree", b"trie", b"tries", b"trip", b"trot", b"try"]


def test_example() -> None:
    t: AdaptiveRadixTree[int] = AdaptiveRadixTree()
    for i, w in enumerate(WORDS):
        t.put(w, i)
        t.check_invariant()
    root = t.root
    assert isinstance(root, _Inner) and root.prefix == b"tr" and root.kind == 4
    assert [chr(b) for b, _ in root.items()] == ["e", "i", "o", "y"]
    assert t.node_kinds() == {4: 3, 16: 0, 48: 0, 256: 0}
    assert t.get(b"trie") == 1 and t.get(b"tri") is None and t.get(b"trees") is None
    assert t.keys() == sorted(WORDS)
    t.put(b"trunk", 6)
    assert t.root.kind == 16
    t.delete(b"trunk")
    assert t.root.kind == 16  # hysteresis: 4 children do not shrink a Node16
    t.delete(b"trot")
    assert t.root.kind == 4
    t.delete(b"trip")
    t.check_invariant()
    assert t.keys() == [b"tree", b"trie", b"tries", b"try"]


def test_edges() -> None:
    t: AdaptiveRadixTree[int] = AdaptiveRadixTree()
    assert t.get(b"") is None and t.keys() == []
    t.put(b"", 0)
    t.put(b"a", 1)
    assert t.get(b"") == 0 and t.keys() == [b"", b"a"]
    t.delete(b"")
    t.delete(b"a")
    t.delete(b"a")
    assert len(t) == 0 and t.root is None
    for b in range(1, 256):
        t.put(bytes([b]), b)
    t.check_invariant()
    assert t.root.kind == 256 and len(t) == 255
    for b in range(1, 256):
        t.delete(bytes([b]))
        t.check_invariant()
    assert t.root is None
    with pytest.raises(ValueError):
        t.put(b"a\x00b", 1)


def test_random_against_dict() -> None:
    rng = random.Random(1313)
    for trial in range(500):
        t: AdaptiveRadixTree[int] = AdaptiveRadixTree()
        model: dict[bytes, int] = {}
        span = 3 if trial % 2 else 70
        for _ in range(rng.randint(0, 120)):
            k = bytes(rng.randint(1, span) for _ in range(rng.randint(0, 4)))
            if rng.random() < 0.6:
                v = rng.randint(0, 99)
                t.put(k, v)
                model[k] = v
            else:
                t.delete(k)
                model.pop(k, None)
            assert t.get(k) == model.get(k)
        t.check_invariant()
        assert len(t) == len(model)
        assert t.items() == sorted(model.items())
