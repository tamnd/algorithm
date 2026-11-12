# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-code/. The authors are listed in prov/NYBA8H.jsonl.

import random
from itertools import combinations, product
from math import comb

from hamming_code import (
    data_positions,
    decode,
    decode_secded,
    encode,
    encode_extended,
    message_of,
    parity_check_matrix,
    qary_decode,
    qary_parity_check,
    syndrome_position,
)


def weight(v):
    return sum(1 for x in v if x)


def qary_code(h, q):
    """All v with H v^T = 0: free values on the non-unit columns, then solve the unit columns."""
    r, n = len(h), len(h[0])
    unit = [next(j for j in range(n) if all(h[x][j] == (x == i) for x in range(r))) for i in range(r)]
    free = [j for j in range(n) if j not in unit]
    out = []
    for vals in product(range(q), repeat=len(free)):
        v = [0] * n
        for j, a in zip(free, vals):
            v[j] = a
        for i in range(r):
            v[unit[i]] = -sum(h[i][j] * v[j] for j in free) % q
        assert all(sum(a * b for a, b in zip(row, v)) % q == 0 for row in h)
        out.append(tuple(v))
    return out


def test_page_example():
    c = encode((1, 0, 1, 1), 3)
    assert c == (0, 1, 1, 0, 0, 1, 1)
    r = list(c)
    r[4] ^= 1  # position 5
    assert syndrome_position(tuple(r)) == 5
    assert decode(tuple(r)) == c
    assert parity_check_matrix(3) == [[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]]


def test_codewords_satisfy_h_and_d3():
    for r in (2, 3, 4):
        h = parity_check_matrix(r)
        k = (1 << r) - 1 - r
        words = [encode(m, r) for m in product(range(2), repeat=k)]
        assert len(set(words)) == 2**k
        for c in words:
            assert all(sum(a * b for a, b in zip(row, c)) % 2 == 0 for row in h)
        assert min(weight(c) for c in words if any(c)) == 3


def test_perfect_sphere_packing():
    for r in range(2, 6):
        n = (1 << r) - 1
        k = n - r
        assert 2**k * (1 + n) == 2**n
    for q, r in [(3, 2), (3, 3), (5, 2), (7, 2)]:
        n = (q**r - 1) // (q - 1)
        assert 2 <= n and q ** (n - r) * (1 + n * (q - 1)) == q**n


def test_spheres_partition_space():
    for r in (2, 3, 4):
        n = (1 << r) - 1
        k = n - r
        seen = set()
        for m in product(range(2), repeat=k):
            c = encode(m, r)
            ball = [c] + [tuple(b ^ (i == j) for j, b in enumerate(c)) for i in range(n)]
            for v in ball:
                assert v not in seen
                seen.add(v)
        assert len(seen) == 2**n


def test_single_errors_exhaustive():
    for r in (2, 3, 4):
        n = (1 << r) - 1
        k = n - r
        for m in product(range(2), repeat=k):
            c = encode(m, r)
            assert decode(c) == c and message_of(c, r) == m
            for i in range(n):
                y = list(c)
                y[i] ^= 1
                assert syndrome_position(tuple(y)) == i + 1
                assert decode(tuple(y)) == c


def test_r5_random_messages_all_positions():
    rng = random.Random(3)
    for _ in range(200):
        m = tuple(rng.randrange(2) for _ in range(26))
        c = encode(m, 5)
        assert message_of(c, 5) == m
        for i in range(31):
            y = list(c)
            y[i] ^= 1
            assert decode(tuple(y)) == c


def test_two_errors_are_miscorrected():
    c = encode((0, 0, 0, 0), 3)
    for i, j in combinations(range(7), 2):
        y = list(c)
        y[i] ^= 1
        y[j] ^= 1
        out = decode(tuple(y))
        assert out != c and weight(out) == 3


def test_secded_exhaustive():
    for r in (3, 4):
        n = 1 << r
        k = n - 1 - r
        words = [encode_extended(m, r) for m in product(range(2), repeat=k)]
        assert min(weight(c) for c in words if any(c)) == 4
        for c in words:
            assert decode_secded(c) == ("ok", c)
            for i in range(n):
                y = list(c)
                y[i] ^= 1
                assert decode_secded(tuple(y)) == ("corrected", c)
            for i, j in combinations(range(n), 2):
                y = list(c)
                y[i] ^= 1
                y[j] ^= 1
                assert decode_secded(tuple(y))[0] == "double"


def test_qary_hamming():
    for q, r in [(3, 2), (3, 3), (5, 2)]:
        h = qary_parity_check(r, q)
        n = len(h[0])
        assert n == (q**r - 1) // (q - 1)
        code = qary_code(h, q)
        assert len(code) == q ** (n - r)
        assert min(weight(c) for c in code if any(c)) == 3
        rng = random.Random(q * 10 + r)
        sample = code if len(code) <= 30 else rng.sample(code, 30)
        for c in sample:
            for i in range(n):
                for a in range(1, q):
                    y = list(c)
                    y[i] = (y[i] + a) % q
                    assert qary_decode(h, tuple(y), q) == c


def test_ternary_example():
    h = qary_parity_check(2, 3)
    assert h == [[0, 1, 1, 1], [1, 0, 1, 2]]
    assert data_positions(3) == [3, 5, 6, 7]
    assert comb(7, 1) + 1 == 8
