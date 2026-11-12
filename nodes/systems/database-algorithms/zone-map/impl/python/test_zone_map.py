# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zone-map/. The authors are listed in prov/BKMHC8.jsonl.

import itertools
import random

from zone_map import ZoneMap, skip_probability

UNSORTED = [5, 12, 1, 16, 9, 3, 14, 7, 2, 11, 15, 6, 13, 4, 10, 8]


def scan(column, lo, hi):
    return [r for r, v in enumerate(column) if lo <= v <= hi]


def qualifying_blocks(column, b, lo, hi):
    return {r // b for r in scan(column, lo, hi)}


def test_example():
    z = ZoneMap.build(UNSORTED, 4)
    assert (z.lo, z.hi) == ([1, 3, 2, 4], [16, 14, 15, 13])
    assert z.scan(6, 9) == [4, 7, 11, 15]
    assert (z.blocks_read, z.blocks_skipped) == (4, 0)
    s = ZoneMap.build(sorted(UNSORTED), 4)
    assert (s.lo, s.hi) == ([1, 5, 9, 13], [4, 8, 12, 16])
    assert s.scan(6, 9) == [5, 6, 7, 8]
    assert (s.blocks_read, s.blocks_skipped) == (2, 2)


def test_edges():
    z = ZoneMap.build([], 3)
    assert z.scan(0, 10) == [] and z.num_blocks() == 0
    z = ZoneMap.build([7], 3)
    assert z.scan(7, 7) == [0] and z.scan(8, 9) == [] and z.blocks_skipped == 1
    z = ZoneMap.build([4, 4, 4, 4, 4], 2)
    assert z.scan(4, 4) == [0, 1, 2, 3, 4] and z.blocks_read == 3
    assert z.scan(5, 3) == []


def test_never_skips_a_qualifying_block():
    rng = random.Random(1998)
    for _ in range(500):
        n = rng.randint(0, 60)
        b = rng.randint(1, 8)
        column = [rng.randint(-20, 20) for _ in range(n)]
        if rng.random() < 0.5:
            column.sort()
        z = ZoneMap.build(column, b)
        z.check_invariant()
        for _ in range(5):
            lo = rng.randint(-25, 25)
            hi = rng.randint(lo - 2, 25)
            assert z.scan(lo, hi) == scan(column, lo, hi)
            assert z.blocks_read >= len(qualifying_blocks(column, b, lo, hi))
            assert z.blocks_read + z.blocks_skipped == z.num_blocks()


def test_updates_keep_bounds_valid():
    rng = random.Random(476)
    column = [rng.randint(0, 100) for _ in range(200)]
    z = ZoneMap.build(column, 10)
    for _ in range(500):
        r, x = rng.randrange(200), rng.randint(-50, 150)
        z.update(r, x)
        column[r] = x
        if rng.random() < 0.1:
            z.recompute(rng.randrange(z.num_blocks()))
        z.check_invariant()
        lo = rng.randint(-60, 160)
        hi = rng.randint(lo, 170)
        assert z.scan(lo, hi) == scan(column, lo, hi)


def test_sorted_reads_only_qualifying_blocks_plus_at_most_one():
    rng = random.Random(487)
    for _ in range(500):
        n = rng.randint(1, 80)
        b = rng.randint(1, 9)
        column = sorted(rng.randint(0, 40) for _ in range(n))
        z = ZoneMap.build(column, b)
        lo = rng.randint(-5, 45)
        hi = rng.randint(lo, 50)
        res = z.scan(lo, hi)
        q = qualifying_blocks(column, b, lo, hi)
        m = len(res)
        if m > 0:
            assert z.blocks_read == len(q)
            assert z.blocks_read <= (m + b - 1 + b - 1) // b
        else:
            assert z.blocks_read <= 1


def test_sorted_against_random_counts():
    rng = random.Random(2)
    column = [rng.randrange(10 ** 6) for _ in range(10000)]
    z = ZoneMap.build(column, 100)
    s = ZoneMap.build(sorted(column), 100)
    assert len(z.scan(500000, 509999)) == 98
    assert (z.blocks_read, z.blocks_skipped) == (100, 0)
    assert len(s.scan(500000, 509999)) == 98
    assert (s.blocks_read, s.blocks_skipped) == (2, 98)
    assert len(z.scan(0, 9999)) == 113
    assert (z.blocks_read, z.blocks_skipped) == (68, 32)
    assert (s.scan(0, 9999), s.blocks_read) == (list(range(113)), 2)


def test_skip_probability_by_enumeration():
    for total in range(1, 6):
        for lo in range(total + 1):
            for hi in range(lo - 1, total):
                below, above = lo, total - 1 - hi
                for b in range(1, 4):
                    skipped = sum(
                        1 for blk in itertools.product(range(total), repeat=b)
                        if max(blk) < lo or min(blk) > hi
                    )
                    num, den = skip_probability(below, above, total, b)
                    if hi >= lo:
                        assert (num, den) == (skipped, total ** b)
