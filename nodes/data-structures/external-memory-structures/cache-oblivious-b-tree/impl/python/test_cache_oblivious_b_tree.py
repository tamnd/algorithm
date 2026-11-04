# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cache-oblivious-b-tree/. The authors are listed in prov/KRJ5HP.jsonl.

import math
import random

from cache_oblivious_b_tree import CacheObliviousBTree, veb_pos


def show(t: CacheObliviousBTree[int]) -> str:
    return " ".join("_" if x is None else str(x) for x in t.slots)


def test_example() -> None:
    t: CacheObliviousBTree[int] = CacheObliviousBTree()
    for k in [50, 20, 80, 10, 60, 30, 70, 40]:
        t.insert(k)
        t.check_invariant()
    assert (t.cap, t.S, t.H) == (32, 4, 3)
    assert show(t).startswith("10 _ _ _ 20 _ _ _ 30 _ 40 _ _ 50 _ _ _ _ 60")
    # the index in van Emde Boas order: root, its two children, then the
    # four bottom trees of three nodes each
    assert t.index == [10, 10, 60, 10, 10, 20, 30, 30, 50, 60, 60, 70, 80, 80, None]
    assert t.pos[3] == [4, 5, 7, 8, 10, 11, 13, 14]
    touched: list[int] = []
    s, p = t._search(45, touched)
    assert [-1 - q for q in touched if q < 0] == [2, 6, 8]  # mins 60, 30, 50
    assert s == 2 and t.slots[p] == 40
    assert t.predecessor(45) == 40 and t.predecessor(5) is None
    assert t.range(15, 60) == [20, 30, 40, 50, 60]
    t.delete(30)
    t.check_invariant()
    assert 30 not in t and t.index[t.pos[3][2]] == 40


def test_edges() -> None:
    t: CacheObliviousBTree[int] = CacheObliviousBTree()
    assert t.predecessor(3) is None and 3 not in t and t.range(0, 9) == []
    t.delete(3)
    t.insert(3)
    t.insert(3)
    assert list(t) == [3] and t.predecessor(100) == 3
    t.delete(3)
    assert list(t) == [] and len(t) == 0
    t.check_invariant()
    assert veb_pos(4, 3, 5) == 11


def test_against_set() -> None:
    rng = random.Random(41)
    for _ in range(500):
        t: CacheObliviousBTree[int] = CacheObliviousBTree()
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
            below = [x for x in ref if x <= k]
            assert t.predecessor(k) == (max(below) if below else None)
            if i % 23 == 0:
                t.check_invariant()
        t.check_invariant()
        assert list(t) == sorted(ref)


def test_search_blocks() -> None:
    N = 4096
    t: CacheObliviousBTree[int] = CacheObliviousBTree()
    for k in random.Random(5).sample(range(10 * N), N):
        t.insert(k)
    t.check_invariant()
    queries = random.Random(6).sample(range(10 * N), 200)
    for B in (4, 16, 64, 256):
        worst = max(t.blocks_touched(q, B) for q in queries)
        assert worst <= 4 * math.log(t.cap, B) + 4
    assert t.moves <= N * math.log2(N) ** 2 / 2
