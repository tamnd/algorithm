# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-tree/. The authors are listed in prov/4A6SZN.jsonl.

import random

from radix_tree import RadixTree

WORDS = "she sells sea shells by the sea shore".split()


def test_example() -> None:
    t: RadixTree[int] = RadixTree()
    counts = []
    for i, w in enumerate(WORDS):
        t.put(w, i)
        t.check_invariant()
        counts.append(t.node_count())
    assert counts == [2, 4, 6, 7, 8, 9, 9, 11]
    assert t.keys() == ["by", "sea", "sells", "she", "shells", "shore", "the"]
    assert t.get("sea") == 6 and t.get("s") is None and t.get("shel") is None
    assert t.keys_with_prefix("sh") == ["she", "shells", "shore"]
    assert t.keys_with_prefix("shel") == ["shells"]
    assert t.keys_with_prefix("shx") == []
    assert t.longest_prefix_of("shellsort") == "shells"
    t.delete("she")
    t.check_invariant()
    assert t.node_count() == 10 and t.get("shells") == 3
    t.delete("sea")
    t.check_invariant()
    assert t.node_count() == 8


def test_edges() -> None:
    t: RadixTree[int] = RadixTree()
    assert t.get("") is None and t.keys() == []
    t.put("", 5)
    t.put("a", 1)
    t.put("aaa", 3)
    t.check_invariant()
    assert t.keys() == ["", "a", "aaa"]
    t.delete("a")
    t.check_invariant()
    assert t.node_count() == 2 and t.get("aaa") == 3
    t.delete("")
    t.delete("zz")
    t.check_invariant()
    assert t.size() == 1


def test_random_against_dict() -> None:
    rng = random.Random(7781)
    for _ in range(500):
        t: RadixTree[int] = RadixTree()
        model: dict[str, int] = {}
        for _ in range(rng.randint(0, 40)):
            k = "".join(rng.choice("ab") for _ in range(rng.randint(0, 5)))
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
        assert t.node_count() <= max(1, 2 * len(model))
        p = "".join(rng.choice("ab") for _ in range(rng.randint(0, 3)))
        assert t.keys_with_prefix(p) == sorted(k for k in model if k.startswith(p))
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
        cands = [k for k in model if s.startswith(k)]
        assert t.longest_prefix_of(s) == (max(cands, key=len) if cands else None)
