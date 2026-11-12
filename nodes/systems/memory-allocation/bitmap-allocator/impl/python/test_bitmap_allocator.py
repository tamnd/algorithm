# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitmap-allocator/. The authors are listed in prov/GDECRB.jsonl.

import random

import pytest

from bitmap_allocator import BitmapAllocator, run_of_ones


class Naive:
    """One bool per unit; first fit by a plain scan."""

    def __init__(self, h: int) -> None:
        self.used = [False] * h
        self.size: dict[int, int] = {}

    def malloc(self, n: int) -> int | None:
        run = 0
        for x, u in enumerate(self.used):
            run = 0 if u else run + 1
            if run == n:
                a = x - n + 1
                for y in range(a, a + n):
                    self.used[y] = True
                self.size[a] = n
                return a
        return None

    def free(self, p: int) -> None:
        for y in range(p, p + self.size.pop(p)):
            self.used[y] = False


def test_run_of_ones() -> None:
    rng = random.Random(7)
    for _ in range(300):
        f = rng.getrandbits(64)
        n = rng.randrange(1, 65)
        r = run_of_ones(f, n)
        for j in range(64):
            want = j + n <= 64 and all((f >> k) & 1 for k in range(j, j + n))
            assert bool((r >> j) & 1) == want


def test_worked_example() -> None:
    z = BitmapAllocator(200)  # four words; units 200 .. 255 are padding
    assert z.malloc(60) == 0
    assert z.malloc(10) == 60  # crosses the border of words 0 and 1
    assert z.malloc(100) == 70
    z.free(60)
    assert z.malloc(5) == 60  # first fit: the lowest hole
    assert z.malloc(40) is None  # holes of 5 and 30 units only
    assert z.malloc(30) == 170
    z.free(0)
    z.free(60)
    z.free(70)
    z.free(170)
    assert z.malloc(200) == 0


def test_errors() -> None:
    z = BitmapAllocator(10)
    with pytest.raises(ValueError):
        z.free(3)
    with pytest.raises(ValueError):
        z.malloc(0)
    assert z.malloc(11) is None


def test_against_naive() -> None:
    rng = random.Random(1995)
    for _ in range(60):
        h = rng.randrange(1, 400)
        z, ref = BitmapAllocator(h), Naive(h)
        live: list[int] = []
        for _ in range(150):
            if live and rng.random() < 0.45:
                p = live.pop(rng.randrange(len(live)))
                z.free(p)
                ref.free(p)
            else:
                n = rng.randrange(1, max(2, h // 2))
                if rng.random() < 0.3:
                    n = rng.randrange(1, 8)
                p = z.malloc(n)
                assert p == ref.malloc(n)
                if p is not None:
                    live.append(p)
            assert [z.is_used(x) for x in range(h)] == ref.used
        for p in live:
            z.free(p)
        assert not any(z.is_used(x) for x in range(h))
