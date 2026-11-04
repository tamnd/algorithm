# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burst-trie/. The authors are listed in prov/4A6NMB.jsonl.

import random

import pytest

from burst_trie import BurstTrie, _Access, _Container

WORDS = "she sells sea shells by the sea shore".split()


def test_example() -> None:
    t: BurstTrie[int] = BurstTrie(limit=3)
    for i, w in enumerate(WORDS):
        t.put(w, i)
        t.check_invariant()
    root = t.root
    s = root.slots["s"]
    assert isinstance(s, _Access) and isinstance(s.slots["h"], _Container)
    assert s.slots["h"].suffixes == ["e", "ells", "ore"]
    assert s.slots["e"].suffixes == ["a", "lls"]
    assert t.shape() == (2, 4)
    assert t.get("sea") == 6 and t.get("shore") == 7 and t.get("sh") is None
    assert t.keys() == ["by", "sea", "sells", "she", "shells", "shore", "the"]
    t.put("shy", 8)
    t.check_invariant()
    assert t.shape() == (3, 6)
    assert [k for k, _ in t.items_with_prefix("sh")] == ["she", "shells", "shore", "shy"]


def test_edges() -> None:
    t: BurstTrie[int] = BurstTrie(limit=1)
    assert t.get("") is None and t.keys() == []
    t.put("", 0)
    for w in ["a", "aa", "aaa", "aaaa"]:
        t.put(w, len(w))
        t.check_invariant()
    assert t.keys() == ["", "a", "aa", "aaa", "aaaa"]
    for w in ["aaaa", "a", "", "aa", "aaa", "zz"]:
        t.delete(w)
        t.check_invariant()
    assert len(t) == 0 and t.keys() == []
    with pytest.raises(ValueError):
        BurstTrie(limit=0)


def test_random_against_dict() -> None:
    rng = random.Random(8080)
    for trial in range(500):
        t: BurstTrie[int] = BurstTrie(limit=rng.randint(1, 6))
        model: dict[str, int] = {}
        for _ in range(rng.randint(0, 60)):
            k = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
            if rng.random() < 0.65:
                v = rng.randint(0, 99)
                t.put(k, v)
                model[k] = v
            else:
                t.delete(k)
                model.pop(k, None)
            assert t.get(k) == model.get(k)
        t.check_invariant()
        assert len(t) == len(model)
        assert t.items_with_prefix("") == sorted(model.items())
        p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 3)))
        assert t.items_with_prefix(p) == sorted((k, v) for k, v in model.items() if k.startswith(p))
