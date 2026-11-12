# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arena-allocation/. The authors are listed in prov/WB0SXP.jsonl.

import random

from arena_allocation import Arena, ChunkPool


def test_worked_example() -> None:
    pool = ChunkPool(k=64)
    a = Arena(pool)
    assert a.alloc(10) == 0  # new chunk [0, 80): 16 + 64 bytes
    assert a.alloc(20) == 16  # rounded to 24
    assert a.alloc(50) == 80  # needs 56, 40 left: a new chunk [80, 200)
    assert a.chunks == [(0, 80), (80, 200)]
    assert a.alloc(30) == 136
    assert a.alloc(40) == 200  # 32 left in [80, 200): a third chunk
    assert a.chunks == [(0, 80), (80, 200), (200, 304)]
    a.free_all()
    assert pool.free == [(200, 304), (80, 200), (0, 80)]
    b = Arena(pool)  # a later arena reuses the chunks
    assert b.alloc(100) == 80  # (0, 80) is too small, so b also takes (80, 200)
    assert b.chunks == [(0, 80), (80, 200)]
    assert b.alloc(8) == 184
    assert pool.system.chunks == 3


def test_random() -> None:
    rng = random.Random(1990)
    pool = ChunkPool(k=256)
    for _ in range(40):
        arenas = [Arena(pool) for _ in range(3)]
        live: list[tuple[int, int, int]] = []  # (arena, start, end)
        for _ in range(150):
            i = rng.randrange(3)
            n = rng.choice([0, 1, 7, 8, 24, 100, rng.randrange(1, 600)])
            p = arenas[i].alloc(n)
            e = p + n
            assert p % 8 == 0
            assert n == 0 or any(s <= p and e <= t for s, t in arenas[i].chunks)
            for _, q, f in live:
                assert e <= q or f <= p or n == 0  # no overlap with live blocks
            live.append((i, p, e))
            if rng.random() < 0.03:
                j = rng.randrange(3)
                arenas[j].free_all()
                live = [b for b in live if b[0] != j]
        for a in arenas:
            a.free_all()
    # every chunk the system gave is now free, once
    assert len(pool.free) == pool.system.chunks
    assert len(set(pool.free)) == len(pool.free)
