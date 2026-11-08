# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-micali/. The authors are listed in prov/01DETK.jsonl.

import random

import pytest

from blum_micali import (
    BlumMicali,
    cycle_lengths,
    dlog_table,
    dlog_with_oracle,
    half_predicate,
    is_primitive_root,
    sqrt_mod,
)


def test_worked_example_p_23():
    g = BlumMicali(23, 5, 10)
    states = [g.x]
    bits = []
    for _ in range(12):
        bits.append(g.next_bit())
        states.append(g.x)
    assert states == [10, 9, 11, 22, 1, 5, 20, 12, 18, 6, 8, 16, 3]
    assert bits == [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0]


def test_map_is_a_permutation_and_cycles():
    assert cycle_lengths(23, 5) == [1, 1, 3, 4, 13]
    for p, g in [(23, 5), (1019, 2), (2039, 7)]:
        assert sum(cycle_lengths(p, g)) == p - 1
        assert sorted(pow(g, x, p) for x in range(1, p)) == list(range(1, p))


def test_half_predicate_is_balanced_and_pairs_square_roots():
    for p, g in [(23, 5), (1019, 2), (1907, 2)]:
        assert sum(half_predicate(x, p) for x in range(1, p)) == (p - 1) // 2
        h = (p - 1) // 2
        for x in range(1, h + 1):
            # g^x and g^(x + h) are the two square roots of g^(2x); B separates them
            r, r2 = pow(g, x, p), pow(g, x + h, p)
            assert r2 == p - r and r * r % p == r2 * r2 % p == pow(g, 2 * x, p)
            assert half_predicate(x, p) == 1 and half_predicate(x + h, p) == 0


def test_sqrt_mod():
    for p in (23, 1019, 1033, 2039, 7681):  # 1033 and 7681 are 1 mod 4 and 1 mod 8
        for a in range(1, p):
            if pow(a, (p - 1) // 2, p) == 1:
                r = sqrt_mod(a, p)
                assert r * r % p == a
    with pytest.raises(ValueError):
        sqrt_mod(5, 23)  # 5 is a non-residue mod 23


def test_perfect_predictor_gives_discrete_logarithm():
    for p, g in [(23, 5), (1019, 2), (1033, 5), (7681, 17)]:
        assert is_primitive_root(g, p)
        table = dlog_table(p, g)
        oracle = lambda z: half_predicate(table[z], p)
        for y in range(1, p):
            assert dlog_with_oracle(y, p, g, oracle) == table[y]


def test_previous_bit_is_the_predicate_of_the_preimage():
    # b_i = B(x_i) and x_(i+1) = g^(x_i): predicting b_i from x_(i+1) is computing B(log x_(i+1))
    p, g = 2039, 7
    table = dlog_table(p, g)
    gen = BlumMicali(p, g, 1234)
    for _ in range(200):
        x = gen.x
        b = gen.next_bit()
        assert b == half_predicate(table[gen.x], p) and table[gen.x] == x


def test_invalid_parameters():
    with pytest.raises(ValueError):
        BlumMicali(23, 2, 5)  # 2 has order 11 mod 23
    with pytest.raises(ValueError):
        BlumMicali(23, 5, 0)
    with pytest.raises(ValueError):
        BlumMicali(22, 5, 3)
    with pytest.raises(ValueError):
        dlog_with_oracle(0, 23, 5, lambda z: 0)


def test_chi_square_on_pairs():
    # 20000 bits with a 61-bit prime: pairs of bits, 3 degrees of freedom, 1% point 11.34
    p = 2 ** 61 - 1
    g = 37
    assert is_primitive_root(g, p)
    gen = BlumMicali(p, g, 123456789)
    bits = gen.bits(20000)
    counts = [0] * 4
    for i in range(0, 20000, 2):
        counts[bits[i] * 2 + bits[i + 1]] += 1
    chi2 = sum((c - 2500) ** 2 / 2500 for c in counts)
    assert chi2 < 11.34
