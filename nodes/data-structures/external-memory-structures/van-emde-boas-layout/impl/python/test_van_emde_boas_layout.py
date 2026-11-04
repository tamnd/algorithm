# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/van-emde-boas-layout/. The authors are listed in prov/VCF4TV.jsonl.

import bisect
import math
import random

import pytest

from van_emde_boas_layout import VEBLayout, veb_pos


def test_example() -> None:
    t = VEBLayout(list(range(1, 16)))
    assert t.h == 4
    # top tree of 2 levels, then 4 bottom trees of 2 levels, left to right
    assert t.slots == [8, 4, 12, 2, 1, 3, 6, 5, 7, 10, 9, 11, 14, 13, 15]
    assert t.path(11) == [0, 2, 9, 11]
    assert t.predecessor(11) == 11 and 11 in t
    t2 = VEBLayout([10 * k for k in range(1, 16)])
    assert t2.predecessor(105) == 100 and 105 not in t2
    assert t2.predecessor(5) is None and t2.predecessor(999) == 150
    t.check_invariant()


def test_paper_example_blocks() -> None:
    # N = 2^16 - 1 keys and B = 16, as on the cache-oblivious model page
    n, B = 2**16 - 1, 16
    t = VEBLayout(list(range(n)))
    keys = range(0, n, 7)
    assert max(t.blocks_touched(k, B) for k in keys) <= 7
    assert max(t.blocks_touched(k, B, 5) for k in keys) <= 8
    assert max(t.blocks_touched(k, B) for k in range(n)) == 7

    def bfs_blocks(k: int) -> int:
        d, x, seen = 0, 0, set()
        while d < 16:
            seen.add(((1 << d) - 1 + x) // B)
            r = x * (1 << (16 - d)) + (1 << (15 - d)) - 1
            if r == k:
                break
            x = 2 * x + (1 if r < k else 0)
            d += 1
        return len(seen)

    assert max(bfs_blocks(k) for k in keys) == 13


def test_edges() -> None:
    with pytest.raises(ValueError):
        VEBLayout([2, 1])
    e: VEBLayout[int] = VEBLayout([])
    assert e.predecessor(3) is None and 3 not in e and len(e) == 0
    e.check_invariant()
    one = VEBLayout([5])
    assert one.predecessor(5) == 5 and one.predecessor(4) is None
    one.check_invariant()


def test_against_bisect() -> None:
    rng = random.Random(17)
    for _ in range(500):
        n = rng.randrange(0, 200)
        keys = sorted(rng.sample(range(1000), n))
        t = VEBLayout(keys)
        t.check_invariant()
        assert t.inorder() == keys
        for _ in range(20):
            q = rng.randrange(-5, 1005)
            i = bisect.bisect_right(keys, q)
            want = keys[i - 1] if i else None
            assert t.predecessor(q) == want
            assert (q in t) == (q in keys)


def test_log_b_bound() -> None:
    for h in (10, 14):
        n = 2**h - 1
        t = VEBLayout(list(range(n)))
        rng = random.Random(h)
        for B in (2, 4, 8, 32, 64, 256):
            worst = max(t.blocks_touched(rng.randrange(n), B, rng.randrange(B)) for _ in range(300))
            assert worst <= max(2, 8 * math.log2(n + 1) / math.log2(B + 1))
    assert sorted(veb_pos(5, d, x) for d in range(5) for x in range(1 << d)) == list(range(31))
