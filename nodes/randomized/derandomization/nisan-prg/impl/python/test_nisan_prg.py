# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nisan-prg/. The authors are listed in prov/AGXJ9C.jsonl.

import random
from collections import Counter
from fractions import Fraction
from itertools import product

from nisan_prg import (
    IRREDUCIBLE,
    apply_hash,
    gf_mul,
    nisan_bits,
    nisan_blocks,
    output_length,
    seed_length,
)


def poly_mod(a, m):
    dm = m.bit_length() - 1
    while a and a.bit_length() - 1 >= dm:
        a ^= m << (a.bit_length() - 1 - dm)
    return a


def is_irreducible(poly):
    k = poly.bit_length() - 1
    for d in range(1, k // 2 + 1):
        for low in range(1 << d):
            if poly_mod(poly, (1 << d) | low) == 0:
                return False
    return True


def recursive_oracle(x, hs, k, poly):
    """G_0(x) = x and G_i(x) = G_(i-1)(x) followed by G_(i-1)(h_i(x))."""
    if not hs:
        return [x]
    *lower, top = hs
    return recursive_oracle(x, lower, k, poly) + recursive_oracle(apply_hash(top, x, k, poly), lower, k, poly)


def test_polynomials_are_irreducible() -> None:
    for k, poly in IRREDUCIBLE.items():
        assert poly.bit_length() - 1 == k
        assert is_irreducible(poly)


def test_field_axioms_small() -> None:
    for k in range(1, 5):
        poly = IRREDUCIBLE[k]
        size = 1 << k
        for a in range(1, size):
            assert sum(gf_mul(a, b, k, poly) == 1 for b in range(size)) == 1
        for a, b, c in product(range(size), repeat=3):
            assert gf_mul(a, b ^ c, k, poly) == gf_mul(a, b, k, poly) ^ gf_mul(a, c, k, poly)


def test_example_on_page() -> None:
    k, poly = 2, IRREDUCIBLE[2]
    blocks = nisan_blocks(1, [(2, 1), (3, 0), (2, 2)], k, poly)
    assert blocks == [1, 3, 3, 0, 0, 1, 0, 1]
    assert blocks == recursive_oracle(1, [(2, 1), (3, 0), (2, 2)], k, poly)


def test_matches_recursive_definition() -> None:
    rng = random.Random(1)
    for _ in range(600):
        k = rng.randrange(1, 9)
        ell = rng.randrange(0, 6)
        poly = IRREDUCIBLE[k]
        x = rng.randrange(1 << k)
        hs = [(rng.randrange(1 << k), rng.randrange(1 << k)) for _ in range(ell)]
        assert nisan_blocks(x, hs, k, poly) == recursive_oracle(x, hs, k, poly)


def test_lengths() -> None:
    rng = random.Random(2)
    for _ in range(100):
        k = rng.randrange(1, 9)
        ell = rng.randrange(0, 6)
        hs = [(rng.randrange(1 << k), rng.randrange(1 << k)) for _ in range(ell)]
        bits = nisan_bits(rng.randrange(1 << k), hs, k, IRREDUCIBLE[k])
        assert len(bits) == output_length(k, ell) == k * 2**ell
        assert set(bits) <= {0, 1}
        assert seed_length(k, ell) == k + 2 * k * ell


def test_wide_test_relation_holds_on_every_seed() -> None:
    rng = random.Random(4)
    for _ in range(500):
        k = rng.randrange(1, 9)
        poly = IRREDUCIBLE[k]
        hs = [(rng.randrange(1 << k), rng.randrange(1 << k)) for _ in range(3)]
        b = nisan_blocks(rng.randrange(1 << k), hs, k, poly)
        left = gf_mul(b[1] ^ b[3], b[4] ^ b[6], k, poly)
        right = gf_mul(b[5] ^ b[7], b[0] ^ b[2], k, poly)
        assert left == right


def test_each_block_is_exactly_uniform() -> None:
    k, ell = 2, 2
    poly = IRREDUCIBLE[k]
    size = 1 << k
    counts = [Counter() for _ in range(1 << ell)]
    for x in range(size):
        for flat in product(range(size), repeat=2 * ell):
            hs = [(flat[2 * i], flat[2 * i + 1]) for i in range(ell)]
            for j, block in enumerate(nisan_blocks(x, hs, k, poly)):
                counts[j][block] += 1
    total = size ** (2 * ell + 1)
    for c in counts:
        assert sorted(c) == list(range(size))
        assert all(v * size == total for v in c.values())


def test_hash_family_is_pairwise_independent() -> None:
    for k in (1, 2, 3):
        poly = IRREDUCIBLE[k]
        size = 1 << k
        for x1 in range(size):
            for x2 in range(size):
                if x1 == x2:
                    continue
                pairs = Counter(
                    (apply_hash((a, b), x1, k, poly), apply_hash((a, b), x2, k, poly))
                    for a in range(size)
                    for b in range(size)
                )
                assert len(pairs) == size * size and set(pairs.values()) == {1}


def test_mixing_lemma_mean_and_variance_exact() -> None:
    rng = random.Random(3)
    k = 3
    poly = IRREDUCIBLE[k]
    size = 1 << k
    for _ in range(200):
        a_set = {x for x in range(size) if rng.randrange(2)}
        b_set = {y for y in range(size) if rng.randrange(2)}
        alpha = Fraction(len(a_set), size)
        beta = Fraction(len(b_set), size)
        values = []
        for a in range(size):
            for b in range(size):
                hits = sum(1 for x in a_set if apply_hash((a, b), x, k, poly) in b_set)
                values.append(Fraction(hits, size))
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        assert mean == alpha * beta
        assert var == alpha * beta * (1 - beta) / size
