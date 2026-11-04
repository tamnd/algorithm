# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trie/. The authors are listed in prov/SJRBA7.jsonl.

import random
import re

from trie import Trie

WORDS = "she sells sea shells by the sea shore".split()


def build() -> Trie[int]:
    t: Trie[int] = Trie()
    for i, w in enumerate(WORDS):
        t.put(w, i)
        t.check_invariant()
    return t


def test_example() -> None:
    t = build()
    assert t.size() == 7
    assert t.node_count() == 20
    assert t.get("shells") == 3
    assert t.get("sea") == 6
    assert t.get("shell") is None
    assert t.get("shy") is None
    assert t.keys_with_prefix("sh") == ["she", "shells", "shore"]
    assert t.keys() == ["by", "sea", "sells", "she", "shells", "shore", "the"]
    assert t.longest_prefix_of("shellsort") == "shells"
    assert t.longest_prefix_of("shelter") == "she"
    assert t.longest_prefix_of("xyz") is None
    assert t.keys_that_match(".he") == ["she", "the"]
    t.delete("shells")
    t.check_invariant()
    assert t.node_count() == 17
    assert t.get("she") == 0


def test_edges() -> None:
    t: Trie[int] = Trie()
    assert t.get("") is None and t.keys() == [] and t.longest_prefix_of("a") is None
    t.put("", 1)
    assert t.get("") == 1 and t.longest_prefix_of("abc") == ""
    t.delete("x")
    t.delete("")
    t.check_invariant()
    assert t.size() == 0 and t.node_count() == 1
    t.put("a", 1)
    t.put("ab", 2)
    t.delete("a")
    t.check_invariant()
    assert t.get("ab") == 2 and t.node_count() == 3


def test_random_against_dict() -> None:
    rng = random.Random(4417)
    for _ in range(500):
        t: Trie[int] = Trie()
        model: dict[str, int] = {}
        for _ in range(rng.randint(0, 40)):
            k = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
            op = rng.random()
            if op < 0.6:
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
        prefixes = {k[:i] for k in model for i in range(len(k) + 1)}
        assert t.node_count() == len(prefixes | {""})
        p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 2)))
        assert t.keys_with_prefix(p) == sorted(k for k in model if k.startswith(p))
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
        cands = [k for k in model if s.startswith(k)]
        assert t.longest_prefix_of(s) == (max(cands, key=len) if cands else None)
        q = "".join(rng.choice("ab.") for _ in range(rng.randint(0, 3)))
        rx = re.compile(q)
        assert t.keys_that_match(q) == sorted(k for k in model if rx.fullmatch(k))
