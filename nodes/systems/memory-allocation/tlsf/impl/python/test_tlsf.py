# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tlsf/. The authors are listed in prov/P3XK4D.jsonl.

import random

import pytest

from tlsf import TLSF, class_low, mapping_insert, mapping_search


def check(z: TLSF, live: dict[int, int]) -> None:
    """Blocks tile the heap, free blocks are in the right lists, bitmaps match."""
    lists = z.free_lists()
    on_list = {b: c for c, xs in lists.items() for b in xs}
    a, prev, prev_free = 0, -1, False
    while a < z.h:
        assert z.prev_phys[a] == prev
        free = z.is_free[a]
        assert not (free and prev_free)  # immediate coalescing
        if free:
            assert on_list[a] == mapping_insert(z.size[a], z.j)
        else:
            assert a in live and z.size[a] >= live[a]
        prev, prev_free, a = a, free, a + z.size[a]
    assert a == z.h
    assert len(on_list) == sum(z.is_free.values())
    for fl in range(z.maxfl + 1):
        row = sum(1 << sl for (f, sl) in lists if f == fl)
        assert z.sl_bitmap[fl] == row
        assert bool((z.fl_bitmap >> fl) & 1) == (row != 0)
    assert z.fl_bitmap >> (z.maxfl + 1) == 0


def test_mapping() -> None:
    for j in range(0, 5):
        for r in range(1 << j, 3000):
            fl, sl = mapping_insert(r, j)
            assert 0 <= sl < (1 << j)
            assert class_low(fl, sl, j) <= r
            # r is below the next class's lower bound
            nfl, nsl = (fl, sl + 1) if sl + 1 < (1 << j) else (fl + 1, 0)
            assert r < class_low(nfl, nsl, j)
            # mapping_search gives the least class whose lower bound is >= r
            fs, ss = mapping_search(r, j)
            low = class_low(fs, ss, j)
            assert low >= r
            assert mapping_insert(low, j) == (fs, ss)
            if (fs, ss) != (j, 0):  # the class just below starts below r
                pfl, psl = (fs, ss - 1) if ss > 0 else (fs - 1, (1 << j) - 1)
                assert class_low(pfl, psl, j) < r


def test_worked_example() -> None:
    z = TLSF(100, 2)
    assert z.free_lists() == {(6, 2): [0]}
    assert z.malloc(13) == 0  # rounded up to 14, the start of class (3, 3)
    assert z.size[0] == 14
    assert z.malloc(20) == 14
    assert z.malloc(10) == 34
    z.free(14)
    assert z.free_lists() == {(4, 1): [14], (5, 3): [44]}
    assert z.fl_bitmap == 0b110000 and z.sl_bitmap[4] == 0b10
    assert z.malloc(11) == 14  # search class (3, 2) is empty; row 4 gives 14
    assert z.free_lists() == {(3, 0): [26], (5, 3): [44]}
    assert z.malloc(40) == 44
    z.free(0)
    z.free(34)  # merges with the free block at 26
    assert z.size[26] == 18
    assert z.free_lists() == {(3, 3): [0], (4, 0): [26, 84]}
    assert z.fl_bitmap == 0b11000
    assert z.malloc(17) is None  # good fit: blocks of 18 sit below class (4, 1)
    assert z.malloc(16) == 26
    assert z.size[26] == 18  # a rest of 2 words is too small to split off


def test_errors() -> None:
    z = TLSF(16, 2)
    with pytest.raises(ValueError):
        z.free(0)
    with pytest.raises(ValueError):
        z.malloc(0)
    assert z.malloc(17) is None
    with pytest.raises(ValueError):
        TLSF(3, 2)


def test_random() -> None:
    rng = random.Random(2004)
    for j in (0, 1, 2, 3, 4):
        h = rng.randrange(1 << j, 3000)
        z = TLSF(h, j)
        live: dict[int, int] = {}
        for _ in range(1500):
            if live and rng.random() < 0.45:
                b = rng.choice(list(live))
                del live[b]
                z.free(b)
            else:
                n = rng.randrange(1, max(2, h // 8))
                b = z.malloc(n)
                if b is None:
                    # TLSF fails only when no free block reaches the search class
                    low = class_low(*mapping_search(max(n, 1 << j), j), j)
                    assert all(z.size[a] < low for a, f in z.is_free.items() if f)
                else:
                    assert z.size[b] >= n  # the block is big enough
                    live[b] = n
            check(z, live)
        for b in list(live):
            z.free(b)
        assert z.free_lists() == {mapping_insert(h, j): [0]}
