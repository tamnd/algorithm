# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitmap-index/. The authors are listed in prov/4975XR.jsonl.

import random

from bitmap_index import (
    EQUALITY, RANGE, MAX_COUNT, BitmapIndex, _push, bit_sliced_sum,
    wah_compress, wah_decompress, wah_op,
)


def scan(column, lo, hi):
    return sum(1 << r for r, x in enumerate(column) if lo <= x <= hi)


def rows_string(bits, n):
    return "".join("1" if bits >> r & 1 else "0" for r in range(n))


EXAMPLE = [2, 0, 3, 1, 2, 0, 3, 2]


def test_example_equality_bitmaps():
    idx = BitmapIndex.build(EXAMPLE, EQUALITY)
    got = {v: rows_string(idx.bitmaps[v], 8) for v in idx.domain}
    assert got == {0: "01000100", 1: "00010000", 2: "10001001", 3: "00100010"}


def test_example_range_bitmaps():
    idx = BitmapIndex.build(EXAMPLE, RANGE)
    got = {v: rows_string(idx.bitmaps[v], 8) for v in idx.domain[:-1]}
    assert got == {0: "01000100", 1: "01010100", 2: "11011101"}
    assert 3 not in idx.bitmaps


def test_example_queries():
    for enc in (EQUALITY, RANGE):
        idx = BitmapIndex.build(EXAMPLE, enc)
        assert rows_string(idx.range_query(1, 2), 8) == "10011001"
        assert rows_string(idx.equal(2), 8) == "10001001"
    eq = BitmapIndex.build(EXAMPLE, EQUALITY)
    eq.range_query(1, 3)
    assert eq.reads == 3
    rg = BitmapIndex.build(EXAMPLE, RANGE)
    rg.range_query(1, 3)
    assert rg.reads == 1          # R[3] is all ones and is not stored
    rg.range_query(1, 2)
    assert rg.reads == 2


def test_empty_and_edges():
    for enc in (EQUALITY, RANGE):
        idx = BitmapIndex(enc)
        assert idx.range_query(0, 10) == 0
        assert idx.equal(5) == 0
        idx.append(7)
        assert idx.range_query(7, 7) == 1
        assert idx.range_query(8, 9) == 0
        assert idx.range_query(5, 4) == 0
        idx.check_invariant([7])


def test_random_against_scan():
    rng = random.Random(4975)
    for _ in range(500):
        n = rng.randint(0, 40)
        c = rng.randint(1, 8)
        column = [rng.randint(-3, -3 + c) for _ in range(n)]
        for enc in (EQUALITY, RANGE):
            idx = BitmapIndex.build(column, enc)
            idx.check_invariant(column)
            for _ in range(5):
                lo = rng.randint(-5, 7)
                hi = rng.randint(lo - 1, 8)
                assert idx.range_query(lo, hi) == scan(column, lo, hi)
                if enc == RANGE:
                    assert idx.reads <= 2
                v = rng.randint(-4, 6)
                assert idx.equal(v) == scan(column, v, v)


def test_appends_keep_invariant():
    rng = random.Random(77)
    for enc in (EQUALITY, RANGE):
        idx = BitmapIndex(enc)
        column = []
        for _ in range(300):
            v = rng.randint(0, 30)
            idx.append(v)
            column.append(v)
            if len(column) % 25 == 0:
                idx.check_invariant(column)


def test_bit_sliced_sum():
    rng = random.Random(9)
    for _ in range(300):
        column = [rng.randint(0, 100) for _ in range(rng.randint(0, 30))]
        rows = rng.getrandbits(len(column)) if column else 0
        want = sum(x for r, x in enumerate(column) if rows >> r & 1)
        assert bit_sliced_sum(column, rows) == want


def random_bitmap(rng, n):
    """Bits with long runs, so that WAH makes fills."""
    bits, r = 0, 0
    while r < n:
        length = rng.choice([1, 3, 31, 62, 100, 400])
        kind = rng.random()
        for i in range(r, min(n, r + length)):
            if kind < 0.4 or (kind < 0.8 and rng.random() < 0.5):
                bits |= 1 << i
        r += length
    return bits


def test_wah_example():
    # 200 rows: rows 0 to 61 are 0, row 62 is 1, rows 63 to 199 are 1
    n = 200
    bits = ((1 << n) - 1) ^ ((1 << 62) - 1)
    words = wah_compress(bits, n)
    # groups: 0 and 1 are zero fills, groups 2 to 5 are ones, group 6 has 14 real bits
    assert words == [0x80000002, 0xC0000004, (1 << 14) - 1]
    assert wah_decompress(words) == bits


def test_wah_roundtrip_and_ops():
    rng = random.Random(1132863)
    for _ in range(500):
        n = rng.randint(0, 1500)
        a, b = random_bitmap(rng, n), random_bitmap(rng, n)
        wa, wb = wah_compress(a, n), wah_compress(b, n)
        assert wah_decompress(wa) == a
        assert all(0 <= w < 1 << 32 for w in wa)
        assert wah_decompress(wah_op(wa, wb, "and")) == a & b
        assert wah_decompress(wah_op(wa, wb, "or")) == a | b
        assert wah_op(wa, wb, "and") == wah_compress(a & b, n)
        assert wah_op(wa, wb, "or") == wah_compress(a | b, n)


def test_wah_long_fill_splits():
    out = []
    _push(out, True, 0, MAX_COUNT + 5)
    assert out == [0x80000000 | MAX_COUNT, 0x80000005]
