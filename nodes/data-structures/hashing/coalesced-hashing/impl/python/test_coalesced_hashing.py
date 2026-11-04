# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coalesced-hashing/. The authors are listed in prov/E023N7.jsonl.

import random

import pytest

from coalesced_hashing import CoalescedHashTable


def test_page_example() -> None:
    t = CoalescedHashTable(11)
    for k in [27, 18, 29, 28, 39, 13, 16, 38, 21]:
        t.insert(k, str(k))
        t.check_invariant()
    keys = [None if not isinstance(x, int) else x for x in t.key]
    assert keys == [None, None, 13, 21, 38, 27, 28, 18, 16, 39, 29]
    assert t.next == [None, None, None, None, None, 8, 9, 10, 4, None, 3]
    assert t.r == 3
    assert t.search(21) == "21"  # probes 10, 3
    assert t.search(40) is None  # probes 7, 10, 3
    assert t.search(33) is None  # home slot 0 is empty


def test_edges() -> None:
    t = CoalescedHashTable(1)
    assert t.search(0) is None and not t.delete(0)
    t.insert(0, "a")
    t.insert(0, "b")
    assert len(t) == 1 and t.search(0) == "b"
    with pytest.raises(OverflowError):
        t.insert(1, "c")
    assert t.delete(0)
    t.insert(1, "c")
    assert t.search(1) == "c" and t.search(0) is None
    t.check_invariant()
    u = CoalescedHashTable(5, h=lambda k: 0)
    for k in range(5):
        u.insert(k, k)
        u.check_invariant()
    assert [u.search(k) for k in range(5)] == [0, 1, 2, 3, 4]
    with pytest.raises(OverflowError):
        u.insert(9, 9)


def test_random_against_dict() -> None:
    rng = random.Random(5150)
    for _ in range(600):
        m = rng.randint(1, 15)
        t = CoalescedHashTable(m)
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 40)):
            k = rng.randint(-25, 25)
            r = rng.random()
            if r < 0.5:
                v = rng.randint(0, 9)
                if k in model or len(model) < m:
                    t.insert(k, v)
                    model[k] = v
                else:
                    with pytest.raises(OverflowError):
                        t.insert(k, v)
            elif r < 0.65:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.search(k) == model.get(k)
            t.check_invariant()
            assert len(t) == len(model)
        assert sorted(t.keys()) == sorted(model)
