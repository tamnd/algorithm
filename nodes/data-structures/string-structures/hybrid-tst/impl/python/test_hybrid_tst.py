# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-tst/. The authors are listed in prov/EHWQ99.jsonl.

import random

import pytest

from hybrid_tst import HybridTST

WORDS = "she sells sea shells by the sea shore".split()


def test_example() -> None:
    t: HybridTST[int] = HybridTST("abcdefghijklmnopqrstuvwxyz")
    for i, w in enumerate(WORDS):
        t.put(w, i)
        t.check_invariant()
    assert t.size() == 7 and t.tst_node_count() == 12
    assert t.get("by") == 4 and t.get("shore") == 7 and t.get("sh") is None
    assert t.keys() == ["by", "sea", "sells", "she", "shells", "shore", "the"]
    assert t.keys_with_prefix("s") == ["sea", "sells", "she", "shells", "shore"]
    assert t.keys_with_prefix("sh") == ["she", "shells", "shore"]
    assert t.keys_with_prefix("shel") == ["shells"]
    assert t.longest_prefix_of("shellsort") == "shells"
    assert t.longest_prefix_of("byte") == "by"
    t.delete("by")
    t.check_invariant()
    assert t.get("by") is None and t.table[1 * 26 + 24] is None


def test_edges() -> None:
    t: HybridTST[int] = HybridTST()
    t.put("", 0)
    t.put("a", 1)
    t.put("ab", 2)
    t.put("abc", 3)
    t.check_invariant()
    assert t.keys() == ["", "a", "ab", "abc"]
    assert t.longest_prefix_of("abcd") == "abc"
    for k in ["abc", "ab", "a", ""]:
        t.delete(k)
        t.check_invariant()
    assert t.size() == 0 and t.keys() == []
    with pytest.raises(ValueError):
        t.put("\u4e2d\u6587", 1)


def test_random_against_dict() -> None:
    rng = random.Random(5521)
    for _ in range(500):
        t: HybridTST[int] = HybridTST("abc")
        model: dict[str, int] = {}
        for _ in range(rng.randint(0, 40)):
            k = "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
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
        p = "".join(rng.choice("abc") for _ in range(rng.randint(0, 3)))
        assert t.keys_with_prefix(p) == sorted(k for k in model if k.startswith(p))
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 6)))
        cands = [k for k in model if s.startswith(k)]
        assert t.longest_prefix_of(s) == (max(cands, key=len) if cands else None)
