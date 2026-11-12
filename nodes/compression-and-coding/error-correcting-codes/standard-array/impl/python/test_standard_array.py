# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/standard-array/. The authors are listed in prov/YCM9KR.jsonl.

import random
from itertools import product

from standard_array import StandardArray, weight

G52 = [[1, 0, 1, 1, 0], [0, 1, 0, 1, 1]]
G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]
G42 = [[1, 0, 1, 1], [0, 1, 1, 2]]  # ternary [4, 2, 3]


def bits(s):
    return tuple(int(x) for x in s)


def dist(a, b):
    return sum(x != y for x, y in zip(a, b))


def rank_mod(rows, q):
    m = [list(r) for r in rows]
    rank = 0
    for col in range(len(m[0]) if m else 0):
        piv = next((i for i in range(rank, len(m)) if m[i][col] % q), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = pow(m[rank][col], q - 2, q)
        m[rank] = [x * inv % q for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][col]:
                f = m[i][col]
                m[i] = [(x - f * y) % q for x, y in zip(m[i], m[rank])]
        rank += 1
    return rank


def test_page_table():
    a = StandardArray(G52)
    a.check_invariant()
    want = [
        "00000 01011 10110 11101",
        "10000 11011 00110 01101",
        "01000 00011 11110 10101",
        "00100 01111 10010 11001",
        "00010 01001 10100 11111",
        "00001 01010 10111 11100",
        "11000 10011 01110 00101",
        "10001 11010 00111 01100",
    ]
    assert [" ".join("".join(map(str, x)) for x in row) for row in a.rows] == want
    assert a.locate(bits("11100")) == (5, 3)
    assert a.decode(bits("11100")) == bits("11101")


def test_decode_is_nearest_exhaustive():
    for g, q in [(G52, 2), (G74, 2), (G42, 3)]:
        a = StandardArray(g, q)
        a.check_invariant()
        for r in product(range(q), repeat=a.n):
            c = a.decode(r)
            assert dist(r, c) == min(dist(r, x) for x in a.codewords)
            i, _ = a.locate(r)
            assert dist(r, c) == weight(a.leader(i))


def test_corrects_up_to_t():
    a = StandardArray(G74)
    for c in a.codewords:
        for i in range(7):
            r = list(c)
            r[i] ^= 1
            assert a.decode(tuple(r)) == c


def test_edge_codes():
    a = StandardArray([[1, 1, 1, 1, 1]])  # repetition code, t = 2
    a.check_invariant()
    assert len(a.rows) == 16
    assert max(weight(a.leader(i)) for i in range(16)) == 2
    b = StandardArray([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # the whole space: one row
    b.check_invariant()
    assert len(b.rows) == 1


def test_random_codes():
    rng = random.Random(5)
    done = 0
    while done < 60:
        q = rng.choice([2, 2, 2, 3])
        n = rng.randint(2, 7 if q == 2 else 4)
        k = rng.randint(1, n)
        g = [[rng.randrange(q) for _ in range(n)] for _ in range(k)]
        if rank_mod(g, q) < k:
            continue
        a = StandardArray(g, q)
        a.check_invariant()
        for _ in range(20):
            r = tuple(rng.randrange(q) for _ in range(n))
            assert dist(r, a.decode(r)) == min(dist(r, x) for x in a.codewords)
        done += 1
