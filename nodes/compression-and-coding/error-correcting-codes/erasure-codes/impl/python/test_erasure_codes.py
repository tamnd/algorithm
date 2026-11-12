# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/erasure-codes/. The authors are listed in prov/KSMYGE.jsonl.

import itertools
import random

from erasure_codes import (EXP, bit_matrix, cauchy_decode, cauchy_encode, cauchy_matrix, gpow, inv,
                           invert, mul, mul_by_bits, raid6_recover, raid6_syndromes)


def det(a):
    a = [list(r) for r in a]
    n, d = len(a), 1
    for c in range(n):
        p = next((r for r in range(c, n) if a[r][c]), None)
        if p is None:
            return 0
        a[c], a[p] = a[p], a[c]
        d = mul(d, a[c][c])
        f = inv(a[c][c])
        for r in range(c + 1, n):
            if a[r][c]:
                t = mul(a[r][c], f)
                a[r] = [x ^ mul(t, y) for x, y in zip(a[r], a[c])]
    return d


def test_field_facts_from_anvin():
    assert gpow(8) == 0x1D  # {02}^8 = {1d} because the polynomial is 0x11D
    assert len(set(EXP[:255])) == 255  # {02} generates all 255 nonzero elements
    for a in range(1, 256):
        assert mul(a, inv(a)) == 1
    rng = random.Random(1)
    for _ in range(500):
        a, b, c = (rng.randrange(256) for _ in range(3))
        assert mul(a, b ^ c) == mul(a, b) ^ mul(a, c)


def test_raid6_every_one_or_two_lost_blocks():
    rng = random.Random(2)
    n, size = 6, 5
    data = [[rng.randrange(256) for _ in range(size)] for _ in range(n)]
    p, q = raid6_syndromes(data)
    names = list(range(n)) + ["P", "Q"]
    for r in (1, 2):
        for lost in itertools.combinations(names, r):
            d = [None if i in lost else list(data[i]) for i in range(n)]
            dd, pp, qq = raid6_recover(d, None if "P" in lost else p, None if "Q" in lost else q)
            assert (dd, pp, qq) == (data, p, q)


def test_raid6_needs_the_generator_for_two_data_disks():
    # g^(y - x) + {01} must be nonzero, so the two data indices must differ modulo 255.
    for x in range(10):
        for y in range(x + 1, 255):
            assert gpow(y - x) ^ 1 != 0
    assert gpow(255) ^ 1 == 0  # with 256 data disks, disks 0 and 255 would clash


def test_cauchy_every_square_submatrix_is_invertible():
    c = cauchy_matrix(3, 5)
    for r in (1, 2, 3):
        for rows in itertools.combinations(range(3), r):
            for cols in itertools.combinations(range(5), r):
                assert det([[c[i][j] for j in cols] for i in rows]) != 0


def test_cauchy_rs_recovers_from_every_k_subset():
    rng = random.Random(3)
    for k, m in ((3, 2), (4, 3), (5, 2)):
        data = [[rng.randrange(256) for _ in range(4)] for _ in range(k)]
        blocks = data + cauchy_encode(data, m)
        for keep in itertools.combinations(range(k + m), k):
            assert cauchy_decode({i: blocks[i] for i in keep}, k, m) == data


def test_k_minus_one_blocks_never_determine_the_data():
    # MDS: k - 1 blocks are consistent with q choices of a missing data block.
    rng = random.Random(4)
    k, m = 3, 2
    data = [[rng.randrange(256)] for _ in range(k)]
    blocks = data + cauchy_encode(data, m)
    c = cauchy_matrix(m, k)[0]  # block 3 is the first parity block
    seen = set()
    for v in range(256):
        # keep blocks 1 and 3; set data block 0 to v and solve block 3 for data block 2
        rest = blocks[3][0] ^ mul(c[0], v) ^ mul(c[1], data[1][0])
        other = [[v], list(data[1]), [mul(inv(c[2]), rest)]]
        assert other[1] == blocks[1] and cauchy_encode(other, m)[0] == blocks[3]
        seen.add((v, other[2][0]))
    assert len(seen) == 256


def test_xor_form_equals_table_form():
    for e in range(256):
        for v in (0, 1, 2, 0x80, 0x55, 0xFF, 0x1D):
            assert mul_by_bits(e, v) == mul(e, v)
    assert bit_matrix(1) == [[int(i == j) for j in range(8)] for i in range(8)]


def test_invert():
    rng = random.Random(5)
    for _ in range(50):
        a = [[rng.randrange(256) for _ in range(4)] for _ in range(4)]
        if det(a) == 0:
            continue
        b = invert(a)
        prod = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                for t in range(4):
                    prod[i][j] ^= mul(a[i][t], b[t][j])
        assert prod == [[int(i == j) for j in range(4)] for i in range(4)]
