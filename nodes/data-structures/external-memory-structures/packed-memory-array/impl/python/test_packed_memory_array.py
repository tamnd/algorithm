# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/packed-memory-array/. The authors are listed in prov/A555C0.jsonl.

import math
import random

from packed_memory_array import PackedMemoryArray


def show(t: PackedMemoryArray[int]) -> str:
    return " ".join("_" if x is None else str(x) for x in t.slots)


def test_example() -> None:
    t: PackedMemoryArray[int] = PackedMemoryArray()
    assert (t.cap, t.S, t.H) == (8, 2, 2)
    for k in [50, 20, 80]:
        t.insert(k)
    assert show(t) == "20 50 80 _ _ _ _ _"
    t.insert(10)  # segment and its pair are too dense, so the whole array is spread
    assert show(t) == "10 _ 20 _ 50 _ 80 _"
    t.insert(60)
    t.insert(30)
    assert show(t) == "10 _ 20 30 50 60 80 _"
    t.insert(70)  # every window is too dense: the array grows to 32 slots
    assert (t.cap, t.S, t.H) == (32, 4, 3)
    assert show(t) == (
        "10 _ _ _ 20 _ _ _ _ 30 _ _ _ 50 _ _ _ _ 60 _ _ _ 70 _ _ _ _ 80 _ _ _ _"
    )
    t.insert(40)  # fits in its segment
    assert show(t)[: len("10 _ _ _ 20 _ _ _ 30 _ 40 _")] == "10 _ _ _ 20 _ _ _ 30 _ 40 _"
    assert t.moves == 19
    assert t.range(15, 60) == [20, 30, 40, 50, 60]
    assert t.predecessor(45) == 40 and t.predecessor(5) is None
    t.delete(30)
    assert 30 not in t and 40 in t and len(t) == 7
    t.check_invariant()


def test_edges() -> None:
    t: PackedMemoryArray[int] = PackedMemoryArray()
    assert t.predecessor(1) is None and 1 not in t and t.range(0, 9) == []
    t.delete(1)
    t.insert(1)
    t.insert(1)
    assert list(t) == [1]
    t.delete(1)
    assert list(t) == [] and len(t) == 0
    t.check_invariant()


def test_against_set() -> None:
    rng = random.Random(23)
    for _ in range(500):
        t: PackedMemoryArray[int] = PackedMemoryArray()
        ref: set[int] = set()
        for i in range(rng.randrange(1, 250)):
            k = rng.randrange(150)
            r = rng.random()
            if r < 0.35:
                t.delete(k)
                ref.discard(k)
            elif r < 0.85:
                t.insert(k)
                ref.add(k)
            else:
                lo, hi = sorted((k, rng.randrange(150)))
                assert t.range(lo, hi) == sorted(x for x in ref if lo <= x <= hi)
            assert (k in t) == (k in ref)
            if i % 19 == 0:
                t.check_invariant()
        t.check_invariant()
        assert list(t) == sorted(ref)


def test_moves_bound() -> None:
    N = 4096
    for keys in (list(range(N)), list(range(N, 0, -1)), random.Random(3).sample(range(10 * N), N)):
        t: PackedMemoryArray[int] = PackedMemoryArray()
        for k in keys:
            t.insert(k)
        # O(log^2 N) amortized moves per insert, with a small constant
        assert t.moves <= N * math.log2(N) ** 2 / 2
        assert t.cap <= 8 * N
        t.check_invariant()
