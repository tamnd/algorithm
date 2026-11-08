# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blum-blum-shub/. The authors are listed in prov/QDNJTG.jsonl.

import math
import random

import pytest

from blum_blum_shub import (
    BBS,
    brute_period,
    carmichael_lambda,
    carmichael_lambda_pq,
    direct_state,
    is_blum_prime,
    is_prime,
    multiplicative_order,
    predicted_period,
    previous_state,
    quadratic_residues,
    random_blum_prime,
    states,
)

SMALL_BLUM = [(7, 11), (11, 23), (7, 19), (23, 47), (11, 19), (19, 43), (31, 43)]


def test_worked_example_n_253():
    g = BBS(253, 3)
    assert g.x == 9
    xs = states(253, 9, 6)
    assert xs == [9, 81, 236, 36, 31, 202, 71]
    assert g.bits(6) == [1, 0, 0, 1, 0, 1]
    assert brute_period(253, 9) == 20 == predicted_period(11, 23, 9)


def test_three_bits_per_step():
    g = BBS(253, 3, j=3)
    # x_1 = 81 = 1010001, x_2 = 236 = 11101100: low 3 bits, least significant first
    assert g.bits(6) == [1, 0, 0, 0, 0, 1]


def test_is_prime_against_trial_division():
    def trial(n):
        return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))
    assert all(is_prime(n) == trial(n) for n in range(5000))
    assert is_prime(2 ** 61 - 1) and not is_prime(2 ** 61 + 1)


def test_squaring_permutes_quadratic_residues_of_blum_integers():
    for p, q in SMALL_BLUM:
        n = p * q
        qr = quadratic_residues(n)
        assert len(qr) == (p - 1) * (q - 1) // 4
        assert sorted(x * x % n for x in qr) == qr
    # for n = 5 * 13 (5 = 1 mod 4) squaring is not injective on the residues
    qr = quadratic_residues(65)
    assert len(set(x * x % 65 for x in qr)) < len(qr)


def test_period_formula_exhaustive():
    for p, q in SMALL_BLUM:
        n = p * q
        ll = carmichael_lambda(carmichael_lambda(n))
        periods = []
        for x0 in quadratic_residues(n):
            per = brute_period(n, x0)
            assert per == predicted_period(p, q, x0)
            assert ll % per == 0
            periods.append(per)
        if (p, q) == (23, 47):
            assert max(periods) == ll == 110
        assert min(periods) == 1  # x_0 = 1 is a fixed point


def test_lambda_helpers():
    assert carmichael_lambda(253) == carmichael_lambda_pq(11, 23) == 110
    assert carmichael_lambda(110) == 20
    assert multiplicative_order(2, 55) == 20
    assert carmichael_lambda(8) == 2 and carmichael_lambda(16) == 4


def test_direct_access_and_backward_step_with_factors():
    rng = random.Random(11)
    p, q = random_blum_prime(40, rng), random_blum_prime(40, rng)
    n = p * q
    s = rng.randrange(2, n)
    x0 = s * s % n
    xs = states(n, x0, 200)
    for i in (0, 1, 2, 57, 200):
        assert direct_state(p, q, x0, i) == xs[i]
    for i in range(1, 200):
        assert previous_state(p, q, xs[i]) == xs[i - 1]


def test_full_state_predicts_everything():
    rng = random.Random(5)
    p, q = random_blum_prime(32, rng), random_blum_prime(32, rng)
    g = BBS(p * q, 123456789)
    for _ in range(10):
        g.next_word()
    leaked = g.x
    future = g.bits(64)
    h = BBS(p * q, 1)
    h.x = leaked
    assert h.bits(64) == future


def test_blum_prime_generation():
    rng = random.Random(2)
    for bits in (8, 16, 64):
        p = random_blum_prime(bits, rng)
        assert p % 4 == 3 and is_prime(p) and p.bit_length() == bits
    assert is_blum_prime(7) and not is_blum_prime(13) and not is_blum_prime(15)


def test_invalid_parameters():
    with pytest.raises(ValueError):
        BBS(253, 11)  # gcd(11, 253) = 11
    with pytest.raises(ValueError):
        BBS(254, 3)
    with pytest.raises(ValueError):
        BBS(253, 3, j=0)
    with pytest.raises(ValueError):
        random_blum_prime(2, random.Random(0))


def test_chi_square_on_nibbles():
    # 40000 parity bits from a 124-bit Blum integer; 15 degrees of freedom, 1% point 30.58
    rng = random.Random(2024)
    p, q = random_blum_prime(62, rng), random_blum_prime(62, rng)
    g = BBS(p * q, rng.randrange(2, p * q))
    bits = g.bits(40000)
    counts = [0] * 16
    for i in range(0, 40000, 4):
        counts[bits[i] | bits[i + 1] << 1 | bits[i + 2] << 2 | bits[i + 3] << 3] += 1
    exp = 10000 / 16
    chi2 = sum((c - exp) ** 2 / exp for c in counts)
    assert chi2 < 30.58
    ones = sum(bits)
    assert abs(ones - 20000) < 4 * math.sqrt(40000) / 2  # within 4 standard deviations (sd 100)
