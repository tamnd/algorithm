# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-hashing/. The authors are listed in prov/PMZJW6.jsonl.

import random

import pytest

from double_hashing import DELETED, DoubleHashTable


def layout(t: DoubleHashTable) -> list:
    return [None if s is None else ("D" if s is DELETED else s[0]) for s in t.slots]


def test_page_example() -> None:
    t = DoubleHashTable(13, h1=lambda k: k % 13, h2=lambda k: 1 + k % 11)
    for k in [18, 41, 22, 44, 59, 32, 31, 73]:
        t.insert(k, -k)
        t.check_invariant()
    assert layout(t) == [None, None, 41, None, 32, 18, 44, 59, 73, 22, None, None, 31]
    assert t.delete(44)
    assert t.search(32) == -32  # probes slot 6 (DELETED), then slot 4
    assert t.search(57) is None
    t.insert(19, -19)  # path 6 (DELETED), 2, 11 (EMPTY): reuses slot 6
    assert t.slots[6] == [19, -19]
    t.check_invariant()


def test_default_hashes_match_example() -> None:
    t = DoubleHashTable(13)
    for k in [18, 41, 22, 44, 59, 32, 31, 73]:
        t.insert(k, k)
    assert layout(t) == [None, None, 41, None, 32, 18, 44, 59, 73, 22, None, None, 31]


def test_edges() -> None:
    with pytest.raises(ValueError):
        DoubleHashTable(12)
    t = DoubleHashTable(2)
    assert t.search(5) is None and not t.delete(5)
    t.insert(5, "a")
    t.insert(5, "b")
    assert len(t) == 1 and t.search(5) == "b"
    t.insert(6, "c")
    with pytest.raises(OverflowError):
        t.insert(7, "d")
    assert t.delete(5)
    t.insert(7, "d")  # reuses the DELETED slot of a full table
    assert t.search(7) == "d" and t.search(6) == "c" and t.search(5) is None
    t.check_invariant()


def test_fill_every_slot() -> None:
    t = DoubleHashTable(31)
    for k in range(31):
        t.insert(k * 1000, k)
    t.check_invariant()
    assert all(t.search(k * 1000) == k for k in range(31))


def test_random_against_dict() -> None:
    rng = random.Random(7331)
    for _ in range(600):
        m = rng.choice([2, 3, 5, 7, 11, 13, 17])
        t = DoubleHashTable(m)
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 50)):
            k = rng.randint(-30, 30)
            r = rng.random()
            if r < 0.45:
                v = rng.randint(0, 9)
                if k in model or len(t) < m:
                    try:
                        t.insert(k, v)
                        model[k] = v
                    except OverflowError:
                        assert k not in model and all(s is not None and s is not DELETED for s in t.slots)
            elif r < 0.75:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.search(k) == model.get(k)
            t.check_invariant()
            assert len(t) == len(model)
        assert sorted(t.keys()) == sorted(model)
