# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/memory-pool/. The authors are listed in prov/K0DCNX.jsonl.

import random

import pytest

from memory_pool import NIL, MemoryPool


def test_worked_example() -> None:
    z = MemoryPool(4, 2)
    a, b, c = z.alloc(), z.alloc(), z.alloc()
    assert (a, b, c) == (0, 2, 4)
    z.free(a)
    z.free(c)
    assert z.free_list() == [4, 0]
    assert z.mem[4] == 0 and z.mem[0] == NIL
    assert z.alloc() == 4  # last in, first out
    assert z.alloc() == 0
    assert z.alloc() == 6  # a block never used before
    assert z.alloc() is None
    assert z.free_list() == []


def test_double_free_is_caught_in_check_mode() -> None:
    z = MemoryPool(2, 1, check=True)
    p = z.alloc()
    z.free(p)
    with pytest.raises(ValueError):
        z.free(p)


def test_against_model() -> None:
    rng = random.Random(42)
    for _ in range(50):
        n, b = rng.randrange(0, 20), rng.randrange(1, 4)
        z = MemoryPool(n, b, check=True)
        live: set[int] = set()
        for _ in range(300):
            if live and rng.random() < 0.5:
                p = rng.choice(sorted(live))
                live.remove(p)
                z.free(p)
            else:
                p = z.alloc()
                if p is None:
                    assert len(live) == n, "fails only when every block is in use"
                else:
                    assert p not in live and p % b == 0 and 0 <= p < n * b
                    live.add(p)
            fl = z.free_list()
            assert len(fl) == len(set(fl)), "the free list has no cycle and no repeat"
            assert set(fl).isdisjoint(live)
            assert len(fl) + len(live) + (n - z.fresh) == n, "every block is in one place"
            assert all(p < z.fresh * b for p in fl)
