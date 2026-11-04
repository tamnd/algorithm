# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hat-trie/. The authors are listed in prov/HZ5P9K.jsonl.

import random

import pytest

from hat_trie import Container, HatTrie, Node

WORDS = ["cab", "cat", "car", "cart", "dog", "do", "cats"]


def test_example() -> None:
    t: HatTrie[int] = HatTrie(r=128, limit=3, slots=4)
    for w in WORDS[:3]:
        t.put(w, len(w))
    assert t.bursts == 0 and isinstance(t.root.child[ord("c")], Container)
    t.put("cart", 4)
    t.check_invariant()
    assert t.bursts == 7
    c = t.root.child[ord("c")]
    assert isinstance(c, Node)
    ca = c.child[ord("a")]
    assert isinstance(ca, Node)
    for w in WORDS[4:]:
        t.put(w, len(w))
        t.check_invariant()
    assert t.bursts == 8
    leaf = ca.child[ord("t")]
    assert isinstance(leaf, Container) and not leaf.pure
    assert sorted(k for k, _ in leaf.items()) == ["t", "ts"]
    assert t.keys() == sorted(WORDS)
    assert t.get("cart") == 4 and t.get("ca") is None and t.get("cats") == 4
    assert t.get("dot") is None and t.size() == 7


def test_edges() -> None:
    t: HatTrie[int] = HatTrie(r=128, limit=2, slots=2)
    t.put("", 0)
    for k in range(1, 40):
        t.put("a" * k, k)
        t.check_invariant()
    assert t.get("") == 0 and t.get("a" * 39) == 39 and t.get("a" * 40) is None
    assert t.keys() == ["a" * k for k in range(40)]
    t.put("a", 100)
    assert t.get("a") == 100 and t.size() == 40
    with pytest.raises(ValueError):
        t.put("é", 1)
    with pytest.raises(ValueError):
        t.put("x", None)  # type: ignore[arg-type]


def test_random_against_dict() -> None:
    rng = random.Random(2007)
    for _ in range(500):
        t: HatTrie[int] = HatTrie(r=128, limit=rng.randint(1, 6), slots=rng.choice([1, 2, 4, 8]))
        model: dict[str, int] = {}
        alpha = rng.choice(["ab", "abc", "abcdefgh"])
        for _ in range(rng.randint(0, 60)):
            k = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 6)))
            v = rng.randint(0, 99)
            t.put(k, v)
            model[k] = v
            assert t.get(k) == v
        t.check_invariant()
        assert t.size() == len(model) and t.keys() == sorted(model)
        for _ in range(5):
            k = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 6)))
            assert t.get(k) == model.get(k)
