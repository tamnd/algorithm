# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/griesmer-bound/. The authors are listed in prov/9D53Y5.jsonl.

import random

from griesmer_bound import (
    binary_min_length, cyclic_generator, griesmer_length, min_distance, paley_code, rank, residual_code,
    simplex_generator, span, weight,
)

# Ternary Golay code: g(x) = x^5 + x^4 - x^3 + x^2 - 1, low degree first, over GF(3).
TERNARY_GOLAY_G = [2, 0, 1, 2, 1, 1]
# Binary Golay code: g(x) = x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1.
BINARY_GOLAY_G = [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]


def test_formula() -> None:
    assert griesmer_length(4, 3) == 7
    assert griesmer_length(5, 3) == 8
    assert griesmer_length(5, 8) == 16
    assert griesmer_length(12, 7) == 22
    assert griesmer_length(12, 8) == 23
    assert griesmer_length(6, 5, 3) == 11
    # each term is at least 1, so the bound implies the Singleton bound n >= d + k - 1
    for k in range(1, 8):
        for d in range(1, 20):
            assert griesmer_length(k, d) >= d + k - 1


def test_simplex_codes_meet_it() -> None:
    for q, kmax in ((2, 4), (3, 3), (5, 2)):
        for k in range(1, kmax + 1):
            gen = simplex_generator(k, q)
            words = span(gen, q)
            n = len(gen[0])
            assert n == (q ** k - 1) // (q - 1)
            assert {weight(w) for w in words if any(w)} == {q ** (k - 1)}
            assert n == griesmer_length(k, q ** (k - 1), q)


def test_simplex_minus_subspace_meets_it() -> None:
    # Delete the nonzero points of a u-dimensional subspace from the binary simplex code
    # of dimension 4: an [15 - (2^u - 1), 4, 8 - 2^(u-1)] code at the Griesmer length.
    gen = simplex_generator(4, 2)
    cols = [tuple(row[j] for row in gen) for j in range(15)]
    for u in (1, 2, 3):
        sub = {tuple((v >> i) & 1 for i in range(4)) for v in range(1, 2 ** u)}
        keep = [j for j, c in enumerate(cols) if c not in sub]
        g2 = [tuple(row[j] for j in keep) for row in gen]
        n, d = len(keep), min_distance(span(g2, 2))
        assert (n, d) == (15 - (2 ** u - 1), 8 - 2 ** (u - 1))
        assert n == griesmer_length(4, d)


def test_golay_codes() -> None:
    t = span(cyclic_generator(TERNARY_GOLAY_G, 11), 3)
    assert len(t) == 729 and min_distance(t) == 5
    assert griesmer_length(6, 5, 3) == 11  # the ternary Golay code meets the bound
    b = span(cyclic_generator(BINARY_GOLAY_G, 23), 2)
    assert min_distance(b) == 7
    assert griesmer_length(12, 7) == 22 < 23  # the binary Golay code does not


def test_residual_code_step() -> None:
    rng = random.Random(1960)
    for _ in range(60):
        q = rng.choice([2, 3])
        k = rng.randint(2, 4)
        n = rng.randint(k + 2, 9)
        gen = [tuple(rng.randrange(q) for _ in range(n)) for _ in range(k)]
        if rank(gen, q) < k:
            continue
        words = span(gen, q)
        d = min_distance(words)
        c = next(w for w in words if weight(w) == d)
        res = residual_code(words, c)
        assert len(res) == q ** (k - 1)  # dimension k - 1
        assert min_distance(res) >= -(-d // q)
        assert n >= griesmer_length(k, d, q)


def test_shortest_binary_codes_small_dimension() -> None:
    # Exhaustive: for k <= 3 the shortest binary linear code has the Griesmer length.
    for k in (1, 2, 3):
        for d in range(1, 9):
            g = griesmer_length(k, d)
            assert binary_min_length(k, d, g + 1) == g
    for d in (1, 2, 3, 4):
        assert binary_min_length(4, d, 9) == griesmer_length(4, d)


def test_nonlinear_code_breaks_it() -> None:
    # A nonlinear (19, 20, 10) code: any 16 of its words have 2^4 words at length 19,
    # but a linear [n, 4, 10] code needs n >= 10 + 5 + 3 + 2 = 20.
    words = paley_code(19)
    assert len(set(words)) == 20
    dists = [sum(a != b for a, b in zip(u, v)) for i, u in enumerate(words) for v in words[i + 1:]]
    assert min(dists) == 10
    assert griesmer_length(4, 10) == 20 > 19


def test_bound_not_always_met() -> None:
    # k = 5, d = 3: the Griesmer length is 8, but 2^5 (1 + 8) = 288 > 2^8 violates the
    # Hamming bound, so the shortest code has length 9 (a shortened Hamming code).
    assert griesmer_length(5, 3) == 8
    assert 2 ** 5 * (1 + 8) > 2 ** 8
    hamming15 = [tuple((j >> i) & 1 for j in range(1, 16)) for i in range(4)]  # H of [15, 11, 3]
    keep = [j for j in range(15) if sum(hamming15[i][j] for i in range(4)) >= 2][:9]
    # the 9 columns of weight >= 2 kept form the parity-check matrix of a [9, 5, 3] code
    h = [tuple(row[j] for j in keep) for row in hamming15]
    assert rank(h, 2) == 4
    cols = {tuple(row[j] for row in h) for j in range(9)}
    assert len(cols) == 9 and all(any(c) for c in cols)  # distinct nonzero columns: d >= 3
