# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-array-trie/. The authors are listed in prov/8PV0JP.jsonl.

import random

from double_array_trie import DoubleArrayTrie


def test_example() -> None:
    t = DoubleArrayTrie({"ab": 0, "ac": 1, "b": 2, "bc": 3})
    t.check_invariant()
    assert t.code == {"a": 1, "b": 2, "c": 3}
    assert t.base == [1, -1, 2, 6, 1, 7, -3, -2, -4, 8]
    assert t.check == [-2, 4, 0, 0, 2, 2, 3, 5, 9, 3]
    assert t.get("ab") == 0 and t.get("bc") == 3 and t.get("a") is None and t.get("abc") is None
    assert t.keys_with_prefix("") == ["ab", "ac", "b", "bc"]
    assert t.prefixes_of("bcd") == ["b", "bc"]


def test_edges() -> None:
    e: DoubleArrayTrie[int] = DoubleArrayTrie({})
    assert e.get("") is None and e.keys_with_prefix("") == []
    t = DoubleArrayTrie({"": 0, "z": 1})
    t.check_invariant()
    assert t.get("") == 0 and t.get("z") == 1 and t.get("q") is None
    assert t.prefixes_of("zz") == ["", "z"]


def test_random_against_dict() -> None:
    rng = random.Random(3030)
    for _ in range(500):
        alpha = rng.choice(["ab", "abc", "abcdefgh"])
        model = {
            "".join(rng.choice(alpha) for _ in range(rng.randint(0, 6))): rng.randint(0, 99)
            for _ in range(rng.randint(0, 25))
        }
        t = DoubleArrayTrie(model)
        t.check_invariant()
        for _ in range(20):
            q = "".join(rng.choice(alpha + "x") for _ in range(rng.randint(0, 6)))
            assert t.get(q) == model.get(q)
            assert t.prefixes_of(q) == sorted((k for k in model if q.startswith(k)), key=len)
        for k, v in model.items():
            assert t.get(k) == v
        p = "".join(rng.choice(alpha) for _ in range(rng.randint(0, 2)))
        assert t.keys_with_prefix(p) == sorted(k for k in model if k.startswith(p))
