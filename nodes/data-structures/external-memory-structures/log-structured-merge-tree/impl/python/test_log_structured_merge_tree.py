# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/log-structured-merge-tree/. The authors are listed in prov/T0A3TV.jsonl.

import math
import random

import pytest

from log_structured_merge_tree import TOMB, LSMTree


def show(t: LSMTree[int, str]) -> str:
    def f(k: int, v: object) -> str:
        return ("-" if v is TOMB else "") + str(k)

    mem = "mem{" + " ".join(f(k, v) for k, v in sorted(t.mem.items())) + "}"
    lv = [
        "L%d[%s]" % (i + 1, " ".join(f(k, v) for k, v in zip(r.keys, r.vals)))
        for i, r in enumerate(t.levels)
    ]
    return " ".join([mem, *lv])


def test_example() -> None:
    t: LSMTree[int, str] = LSMTree(block_size=2, memtable_size=2, ratio=2)
    for k in [50, 20, 80, 10]:
        t.put(k, str(k))
    assert show(t) == "mem{} L1[10 20 50 80]"
    t.put(60, "60")
    t.delete(20)
    # the tombstone reaches the last level and is dropped with the key
    assert show(t) == "mem{} L1[10 50 60 80]"
    t.put(30, "30")
    t.put(70, "70")
    # level 1 would hold 6 > 4 entries, so the merge goes on into level 2
    assert show(t) == "mem{} L1[] L2[10 30 50 60 70 80]"
    t.put(40, "40")
    t.delete(80)
    t.put(90, "90")
    t.put(25, "25")
    assert show(t) == "mem{} L1[25 40 -80 90] L2[10 30 50 60 70 80]"
    assert t.ios == 20
    # 80 is still in level 2, but the newer tombstone in level 1 hides it
    assert t.get(80) is None and t.get(20) is None
    assert t.get(60) == "60" and t.get(25) == "25"
    assert t.range(20, 60) == [(25, "25"), (30, "30"), (40, "40"), (50, "50"), (60, "60")]
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        LSMTree(2, 2, 1)
    t: LSMTree[int, int] = LSMTree(1, 1, 2)
    assert t.get(3) is None and len(t) == 0
    t.delete(3)
    t.put(3, 1)
    t.put(3, 2)
    assert t.get(3) == 2 and list(t) == [3]
    t.delete(3)
    assert t.get(3) is None and t.items() == []
    t.check_invariant()


def test_against_dict() -> None:
    rng = random.Random(13)
    for _ in range(500):
        t: LSMTree[int, int] = LSMTree(rng.randrange(1, 4), rng.randrange(1, 6), rng.randrange(2, 5))
        d: dict[int, int] = {}
        for i in range(rng.randrange(1, 300)):
            k = rng.randrange(100)
            r = rng.random()
            if r < 0.25:
                t.delete(k)
                d.pop(k, None)
            elif r < 0.75:
                t.put(k, i)
                d[k] = i
            elif r < 0.9:
                assert t.get(k) == d.get(k)
            else:
                lo, hi = sorted((k, rng.randrange(100)))
                assert t.range(lo, hi) == sorted((a, b) for a, b in d.items() if lo <= a <= hi)
            if i % 23 == 0:
                t.check_invariant()
        t.check_invariant()
        assert t.items() == sorted(d.items())


def test_io_bound() -> None:
    B, C0, T = 64, 256, 4
    t: LSMTree[int, int] = LSMTree(B, C0, T)
    rng = random.Random(2)
    N = 40000
    for k in rng.sample(range(10 * N), N):
        t.put(k, k)
    levels = len(t.levels)
    assert levels <= 1 + math.log(N / C0, T)
    # each entry is rewritten at most about T + 1 times per level
    assert t.ios <= (T + 1) * levels * N / B * 1.5
    assert t.ios < N / 4
    t.ios = 0
    for k in rng.sample(range(10 * N), 500):
        t.get(k)
    assert t.ios <= 500 * levels
