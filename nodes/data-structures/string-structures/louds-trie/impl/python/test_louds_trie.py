# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/louds-trie/. The authors are listed in prov/C20ZQR.jsonl.

import random

from louds_trie import BitVector, LoudsTrie

KEYS = ["i", "in", "inn", "tea", "ten", "to"]


def test_example() -> None:
    t = LoudsTrie(KEYS)
    t.check_invariant()
    assert "".join(map(str, t.b.bits)) == "1011010110101100000"
    assert t.label[1:] == list("itneonan")
    assert t.children_range(2) == (4, 6) and t.child(2, "o") == 5
    assert t.parent(7) == 4 and t.string_of(8) == "ten"
    assert t.keys_with_prefix("t") == ["tea", "ten", "to"]
    assert t.keys_with_prefix("") == KEYS
    assert t.contains("inn") and not t.contains("te") and not t.contains("tex")


def test_edges() -> None:
    t = LoudsTrie([])
    t.check_invariant()
    assert t.b.bits == [1, 0, 0] and not t.contains("") and t.keys_with_prefix("") == []
    t = LoudsTrie(["", "a"])
    t.check_invariant()
    assert t.contains("") and t.contains("a") and t.keys_with_prefix("") == ["", "a"]
    t = LoudsTrie(["x" * 200])
    t.check_invariant()
    assert t.contains("x" * 200) and not t.contains("x" * 199)


def test_bitvector_against_scan() -> None:
    rng = random.Random(89)
    for _ in range(200):
        bits = [rng.randint(0, 1) for _ in range(rng.randint(1, 300))]
        b = BitVector(bits)
        for i in range(len(bits) + 1):
            assert b.rank1(i) == sum(bits[:i])
        ones = [p for p, v in enumerate(bits) if v]
        zeros = [p for p, v in enumerate(bits) if not v]
        assert [b.select1(j + 1) for j in range(len(ones))] == ones
        assert [b.select0(j + 1) for j in range(len(zeros))] == zeros


def test_random_against_set() -> None:
    rng = random.Random(1989)
    for _ in range(600):
        keys = {"".join(rng.choice("abc") for _ in range(rng.randint(0, 6))) for _ in range(rng.randint(0, 25))}
        t = LoudsTrie(list(keys))
        t.check_invariant()
        assert t.keys_with_prefix("") == sorted(keys)
        for _ in range(5):
            s = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 6)))
            assert t.contains(s) == (s in keys)
            assert t.keys_with_prefix(s[:2]) == sorted(k for k in keys if k.startswith(s[:2]))
