# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-suffix-tree/. The authors are listed in prov/WSA7VT.jsonl.

import random

import pytest

from sparse_suffix_tree import SparseSuffixTree


def occurrences(t: str, p: str) -> list[int]:
    return [i for i in range(len(t) - len(p) + 1) if t.startswith(p, i)]


def test_example() -> None:
    x = SparseSuffixTree("abracadabra", [0, 3, 6, 9])
    x.check_invariant()
    assert x.node_count() == 6
    assert sorted(x.root.children) == ["a", "d", "r"]
    assert x.sampled_occurrences("a") == [0, 3]
    assert x.sampled_occurrences("abra") == [0]
    assert x.all_occurrences("abra", 3) == [0, 7]
    assert x.all_occurrences("bra", 3) == [1, 8]
    assert x.all_occurrences("cad", 3) == [4]


def test_edges() -> None:
    x = SparseSuffixTree("abc", [])
    x.check_invariant()
    assert x.sampled_occurrences("a") == [] and x.node_count() == 1
    t = "mississippi"
    full = SparseSuffixTree(t, list(range(len(t))))
    full.check_invariant()
    assert full.sampled_occurrences("ssi") == [2, 5]
    assert full.all_occurrences("i", 1) == occurrences(t, "i")
    with pytest.raises(ValueError):
        full.all_occurrences("ss", 3)
    with pytest.raises(ValueError):
        SparseSuffixTree("a\0", [0])


def test_random_against_scan() -> None:
    rng = random.Random(1996)
    for _ in range(600):
        t = "".join(rng.choice("ab" if rng.random() < 0.5 else "abc") for _ in range(rng.randint(1, 30)))
        sample = [i for i in range(len(t)) if rng.random() < 0.4]
        x = SparseSuffixTree(t, sample)
        x.check_invariant()
        k = rng.randint(1, 4)
        y = SparseSuffixTree(t, list(range(0, len(t), k)))
        y.check_invariant()
        for _ in range(3):
            p = "".join(rng.choice("abc") for _ in range(rng.randint(1, 6)))
            assert x.sampled_occurrences(p) == [i for i in occurrences(t, p) if i in sample]
            if len(p) >= k:
                assert y.all_occurrences(p, k) == occurrences(t, p)
