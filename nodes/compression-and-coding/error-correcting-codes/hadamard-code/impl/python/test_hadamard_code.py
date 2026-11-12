# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadamard-code/. The authors are listed in prov/AJ00FE.jsonl.

import random
from itertools import combinations

from hadamard_code import (
    decode_fwht, decode_linear, encode, encode_augmented, fwht, is_hadamard, local_decode,
    local_decode_majority, min_distance, paley, paley_code, sylvester,
)


def test_sylvester_matrices() -> None:
    for r in range(6):
        h = sylvester(r)
        assert is_hadamard(h)
        n = 1 << r
        # entry (a, x) is (-1)^(a . x)
        assert all(h[a][x] == (-1) ** ((a & x).bit_count()) for a in range(n) for x in range(n))


def test_code_parameters() -> None:
    for r in range(1, 7):
        n = 1 << r
        lin = [encode(x, r) for x in range(n)]
        assert len(set(map(tuple, lin))) == n
        # every nonzero codeword has weight exactly 2^(r-1): the code is equidistant
        assert all(sum(c) == n // 2 for c in lin[1:])
        aug = [encode_augmented(x, b, r) for x in range(n) for b in (0, 1)]
        weights = sorted({sum(c) for c in aug})
        assert weights == ([0, n // 2, n] if r > 0 else [0, 1])
        assert min_distance([tuple(c) for c in aug]) == n // 2
        # the augmented code is the rows of H and -H read as bits (+1 -> 0, -1 -> 1)
        h = sylvester(r)
        rows = {tuple(0 if v == 1 else 1 for v in row) for row in h}
        rows |= {tuple(1 - b for b in row) for row in rows}
        assert rows == {tuple(c) for c in aug}


def test_fwht_matches_definition() -> None:
    rng = random.Random(3)
    for r in range(6):
        n = 1 << r
        v = [rng.randint(-5, 5) for _ in range(n)]
        h = sylvester(r)
        assert fwht(v) == [sum(h[a][x] * v[x] for x in range(n)) for a in range(n)]


def test_fwht_decoder_corrects_up_to_radius() -> None:
    r = 4
    n = 1 << r
    t = n // 4 - 1  # 3 errors: below half the distance 8
    rng = random.Random(1969)
    for x, b in [(0, 0), (5, 1), (rng.randrange(n), rng.randrange(2))]:
        c = encode_augmented(x, b, r)
        for w in range(t + 1):
            for pos in combinations(range(n), w):
                y = list(c)
                for p in pos:
                    y[p] ^= 1
                assert decode_fwht(y) == (x, b)


def test_fwht_decoder_is_maximum_likelihood() -> None:
    rng = random.Random(1966)
    for r in (3, 5):
        n = 1 << r
        code = {(x, b): encode_augmented(x, b, r) for x in range(n) for b in (0, 1)}
        for _ in range(300):
            y = [rng.randrange(2) for _ in range(n)]
            best = min(sum(u != v for u, v in zip(c, y)) for c in code.values())
            got = code[decode_fwht(y)]
            assert sum(u != v for u, v in zip(got, y)) == best
            # the linear code alone: nearest codeword among b = 0
            best_lin = min(sum(u != v for u, v in zip(code[(x, 0)], y)) for x in range(n))
            assert sum(u != v for u, v in zip(code[(decode_linear(y), 0)], y)) == best_lin


def test_local_decoding() -> None:
    rng = random.Random(1991)
    r = 8
    n = 1 << r
    x = rng.randrange(n)
    c = encode(x, r)
    y = list(c)
    for p in rng.sample(range(n), n // 10):  # 10 percent of the positions are wrong
        y[p] ^= 1
    # one 2-query decode is right with probability at least 0.8
    for i in range(r):
        hits = sum(local_decode(y, i, rng) == (x >> i) & 1 for _ in range(2000))
        assert hits >= 0.75 * 2000
    # a majority of 31 such decodes recovers every message bit
    assert sum(local_decode_majority(y, i, 31, rng) << i for i in range(r)) == x


def test_paley_codes_are_nonlinear_hadamard_codes() -> None:
    for q in (3, 7, 11, 19, 23):
        h = paley(q)
        assert is_hadamard(h)
        words = paley_code(q)
        n = q + 1
        assert len(set(words)) == 2 * n
        assert min_distance(words) == n // 2
    # order 12 is not a power of 2, so this (12, 24, 6) code cannot be linear
    words = set(paley_code(11))
    u, v = sorted(words)[1:3]
    assert tuple(a ^ b for a, b in zip(u, v)) not in words
