# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hopscotch-hashing/. The authors are listed in prov/W6T3BN.jsonl.

import random

import pytest

from hopscotch_hashing import HopscotchHashTable, _EMPTY


def layout(t: HopscotchHashTable) -> list[object]:
    return [None if x is _EMPTY else x for x in t.key]


def test_page_example() -> None:
    t = HopscotchHashTable(10, 3)
    for k in [20, 31, 41, 13, 22, 15]:
        t.insert(k, str(k))
        t.check_invariant()
    assert layout(t) == [20, 31, 41, 13, 22, 15, None, None, None, None]
    t.insert(52, "52")
    t.check_invariant()
    assert layout(t) == [20, 31, 41, 52, 22, 13, 15, None, None, None]
    assert t.hop[2] == 0b110 and t.hop[3] == 0b100 and t.hop[5] == 0b010
    t.insert(62, "62")
    t.check_invariant()
    assert t.m == 20 and len(t) == 8
    want: list[object] = [None] * 20
    for s, k in [(0, 20), (1, 41), (2, 22), (3, 62), (11, 31), (12, 52), (13, 13), (15, 15)]:
        want[s] = k
    assert layout(t) == want
    assert t.search(13) == "13" and t.search(42) is None
    assert t.delete(41) and not t.delete(41)
    assert len(t) == 7 and t.search(41) is None
    t.check_invariant()


def test_place_fails_without_resize() -> None:
    t = HopscotchHashTable(10, 3)
    for k in [20, 31, 41, 13, 22, 15, 52]:
        t.insert(k, k)
    before = sorted(t.keys())
    assert not t._place(62, 62)
    t.check_invariant()
    assert sorted(t.keys()) == before


def test_edges() -> None:
    t = HopscotchHashTable(1, 1)
    assert t.search("a") is None and not t.delete("a") and len(t) == 0
    t.insert("a", 1)
    t.insert("a", 2)
    assert len(t) == 1 and t.search("a") == 2
    t.insert("b", None)
    assert t.contains("b") and t.search("b") is None
    assert t.delete("a") and not t.delete("a")
    t.check_invariant()
    with pytest.raises(ValueError):
        HopscotchHashTable(4, 5)


def test_too_many_equal_hashes() -> None:
    t = HopscotchHashTable(8, 3, h=lambda k: 0)
    for k in range(3):
        t.insert(k, k)
    t.check_invariant()
    with pytest.raises(OverflowError):
        t.insert(3, 3)
    assert sorted(t.keys()) == [0, 1, 2]


def test_full_neighbourhoods() -> None:
    t = HopscotchHashTable(4, 4, h=lambda k: 7)
    for k in range(4):
        t.insert(k, k)
    assert t.m == 4 and len(t) == 4
    t.check_invariant()
    assert all(t.search(k) == k for k in range(4))


def test_random_against_dict() -> None:
    rng = random.Random(9091)
    for _ in range(600):
        H = rng.randint(1, 6)
        t = HopscotchHashTable(rng.randint(H, 16), H)
        ref: dict[int, int] = {}
        hi = rng.choice([20, 60, 200])
        for _ in range(rng.randint(1, 80)):
            k = rng.randrange(hi)
            op = rng.random()
            if op < 0.55:
                v = rng.randrange(1000)
                t.insert(k, v)
                ref[k] = v
            elif op < 0.8:
                assert t.delete(k) == (k in ref)
                ref.pop(k, None)
            else:
                assert t.search(k) == ref.get(k)
        t.check_invariant()
        assert len(t) == len(ref)
        assert sorted(t.keys()) == sorted(ref)
        for k in range(hi):
            assert t.search(k) == ref.get(k)
