# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ternary-search-tree/. The authors are listed in prov/BVWSE3.jsonl.

import random
import re

import pytest

from ternary_search_tree import TernarySearchTree

WORDS = "she sells sea shells by the sea shore".split()


def test_example() -> None:
    t: TernarySearchTree[int] = TernarySearchTree()
    for i, w in enumerate(WORDS):
        t.put(w, i)
        t.check_invariant()
    assert t.size() == 7 and t.node_count() == 19
    assert t.root is not None and t.root.c == "s"
    assert t.get("sea") == 6 and t.get("shy") is None and t.get("sh") is None
    assert t.keys() == ["by", "sea", "sells", "she", "shells", "shore", "the"]
    assert t.keys_with_prefix("sh") == ["she", "shells", "shore"]
    assert t.keys_with_prefix("she") == ["she", "shells"]
    assert t.keys_that_match(".he") == ["she", "the"]
    assert t.longest_prefix_of("shellsort") == "shells"
    t.delete("shells")
    t.check_invariant()
    assert t.node_count() == 16
    t.delete("she")
    t.check_invariant()
    assert t.keys() == ["by", "sea", "sells", "shore", "the"]


def test_edges() -> None:
    t: TernarySearchTree[int] = TernarySearchTree()
    assert t.get("a") is None and t.keys() == [] and t.longest_prefix_of("a") is None
    with pytest.raises(ValueError):
        t.put("", 1)
    t.put("a", 1)
    t.delete("a")
    t.check_invariant()
    assert t.root is None and t.size() == 0
    for w in ["m", "c", "x", "a", "e", "d"]:
        t.put(w, 0)
    t.delete("c")  # a node with two BST children
    t.check_invariant()
    assert t.keys() == ["a", "d", "e", "m", "x"]


def test_random_against_dict() -> None:
    rng = random.Random(9103)
    for _ in range(500):
        t: TernarySearchTree[int] = TernarySearchTree()
        model: dict[str, int] = {}
        for _ in range(rng.randint(0, 40)):
            k = "".join(rng.choice("abcd") for _ in range(rng.randint(1, 4)))
            if rng.random() < 0.6:
                v = rng.randint(0, 99)
                t.put(k, v)
                model[k] = v
            else:
                t.delete(k)
                model.pop(k, None)
            t.check_invariant()
            assert t.get(k) == model.get(k)
        assert t.size() == len(model)
        assert t.keys() == sorted(model)
        prefixes = {k[:i] for k in model for i in range(1, len(k) + 1)}
        assert t.node_count() == len(prefixes)
        p = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 2)))
        assert t.keys_with_prefix(p) == sorted(k for k in model if k.startswith(p))
        s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 5)))
        cands = [k for k in model if s.startswith(k)]
        assert t.longest_prefix_of(s) == (max(cands, key=len) if cands else None)
        q = "".join(rng.choice("ab.") for _ in range(rng.randint(1, 3)))
        rx = re.compile(q)
        assert t.keys_that_match(q) == sorted(k for k in model if rx.fullmatch(k))
