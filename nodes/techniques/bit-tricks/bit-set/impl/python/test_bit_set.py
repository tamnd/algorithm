# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bit-set/. The authors are listed in prov/C0Q5CB.jsonl.

import random

import pytest

from bit_set import BitSet


def test_page_example() -> None:
    s = BitSet(10, w=4)
    assert s.words == [0, 0, 0]
    s.insert(1)
    s.insert(6)
    s.insert(9)
    assert s.words == [0b0010, 0b0100, 0b0010]
    assert s.contains(6)
    s.delete(1)
    assert not s.contains(1)
    s.insert(4)
    assert s.words == [0b0000, 0b0101, 0b0010]
    assert s.count() == 3
    assert s.next_member(5) == 6
    assert s.next_member(7) == 9
    assert s.next_member(10) is None
    s.complement()
    s.check_invariant()
    assert s.words == [0b1111, 0b1010, 0b0001]
    assert s.members() == [0, 1, 2, 3, 5, 7, 8]


def test_empty_and_edges() -> None:
    s = BitSet()
    assert s.count() == 0 and s.members() == [] and s.next_member(0) is None
    s.complement()
    s.check_invariant()
    t = BitSet(64)
    t.complement()
    t.check_invariant()
    assert t.count() == 64 and t.words == [2**64 - 1]
    t.delete(63)
    assert t.next_member(63) is None and t.next_member(62) == 62
    with pytest.raises(IndexError):
        t.insert(64)
    with pytest.raises(IndexError):
        t.contains(-1)


def test_delete_absent_and_insert_twice() -> None:
    s = BitSet(5, w=8)
    s.delete(3)
    s.insert(3)
    s.insert(3)
    assert s.members() == [3] and s.count() == 1


def test_random_against_set() -> None:
    rng = random.Random(1999)
    for _ in range(60):
        n = rng.randrange(0, 200)
        w = rng.choice([1, 3, 4, 8, 64])
        s, t = BitSet(n, w), BitSet(n, w)
        model, model_t = set(), set()
        for _ in range(300):
            op = rng.randrange(7)
            i = rng.randrange(n) if n else 0
            if op == 0 and n:
                s.insert(i)
                model.add(i)
            elif op == 1 and n:
                s.delete(i)
                model.discard(i)
            elif op == 2 and n:
                assert s.contains(i) == (i in model)
            elif op == 3:
                assert s.count() == len(model)
            elif op == 4:
                k = rng.randrange(n + 2)
                bigger = [x for x in model if x >= k]
                assert s.next_member(k) == (min(bigger) if bigger else None)
            elif op == 5:
                s.complement()
                model = set(range(n)) - model
            elif n:
                t.insert(i)
                model_t.add(i)
                s.union(t)
                model |= model_t
            s.check_invariant()
            assert s.members() == sorted(model)
