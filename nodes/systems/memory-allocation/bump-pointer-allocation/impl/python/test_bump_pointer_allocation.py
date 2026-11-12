# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bump-pointer-allocation/. The authors are listed in prov/Q000WF.jsonl.

import random

import pytest

from bump_pointer_allocation import BumpAllocator


def test_worked_example() -> None:
    z = BumpAllocator(0, 64)
    assert z.alloc(5) == 0
    assert z.alloc(8, 8) == 8  # 3 bytes of padding
    assert z.alloc(3) == 16
    assert z.alloc(4, 4) == 20
    assert z.top == 24
    assert z.alloc(50) is None  # 24 + 50 > 64
    assert z.top == 24  # a failed call changes nothing
    assert z.alloc(40) == 24
    z.reset()
    assert z.alloc(50) == 0


def test_errors() -> None:
    z = BumpAllocator(0, 8)
    with pytest.raises(ValueError):
        z.alloc(1, 3)
    with pytest.raises(ValueError):
        z.alloc(-1)
    with pytest.raises(ValueError):
        BumpAllocator(5, 4)


def test_random() -> None:
    rng = random.Random(1987)
    for _ in range(200):
        base = rng.randrange(0, 100)
        limit = base + rng.randrange(0, 500)
        z = BumpAllocator(base, limit)
        blocks: list[tuple[int, int]] = []
        for _ in range(60):
            if rng.random() < 0.05:
                z.reset()
                blocks.clear()
                continue
            n = rng.randrange(0, 40)
            a = 1 << rng.randrange(0, 5)
            top = z.top
            p = z.alloc(n, a)
            want = -(-top // a) * a  # the least multiple of a that is >= top
            if want + n > limit:
                assert p is None and z.top == top
                continue
            assert p == want and p % a == 0 and base <= p and p + n <= limit
            assert all(p >= q + m for q, m in blocks)  # above every live block
            blocks.append((p, n))
            assert z.top == p + n
