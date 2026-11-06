# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pepin-test/. The authors are listed in prov/SM5V45.jsonl.

import random

import pytest

from pepin_test import is_fermat_number_prime, pepin_residue, pepin_test, reduce_fermat

LIMIT = 100_000
# A known prime factor of F_k for 5 <= k <= 13.
KNOWN_FACTORS = {
    5: 641,
    6: 274177,
    7: 59649589127497217,
    8: 1238926361552897,
    9: 2424833,
    10: 45592577,
    11: 319489,
    12: 114689,
    13: 2710954639361,
}


def trial_division_is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def fermat(k: int) -> int:
    return (1 << (1 << k)) + 1


def test_example_f3() -> None:
    f = 257
    seq = [3]
    for _ in range(7):
        seq.append(seq[-1] * seq[-1] % f)
    assert seq == [3, 9, 81, 136, 249, 64, 241, 256]
    assert pepin_residue(3) == 256 and pepin_test(3) is True
    assert pepin_residue(5) == 10324303 and pepin_test(5) is False
    assert fermat(5) == 641 * 6700417


def test_reduce_fermat() -> None:
    rng = random.Random(1)
    for e in [1, 2, 4, 8, 16, 32, 64, 256]:
        f = (1 << e) + 1
        for x in [0, 1, f - 1, f, f + 1, (f - 1) ** 2, f * f, 5 * f * f + 3]:
            assert reduce_fermat(x, e) == x % f
        for _ in range(200):
            x = rng.randrange(0, f**3)
            assert reduce_fermat(x, e) == x % f


def test_all_fermat_numbers_up_to_limit_against_trial_division() -> None:
    fermat_numbers = set()
    k = 0
    while fermat(k) <= LIMIT:
        fermat_numbers.add(fermat(k))
        k += 1
    assert sorted(fermat_numbers) == [3, 5, 17, 257, 65537]
    for n in range(LIMIT + 1):
        if n in fermat_numbers:
            assert is_fermat_number_prime(n) == trial_division_is_prime(n) is True
        else:
            with pytest.raises(ValueError):
                is_fermat_number_prime(n)


def test_base_three_criterion_on_small_odd_numbers() -> None:
    # The criterion 3^((n-1)/2) = -1 (mod n) never accepts a composite n = 2^m + 1
    # nor any composite below the limit with n - 1 a power of 2.
    for m in range(1, 17):
        n = (1 << m) + 1
        holds = pow(3, (n - 1) // 2, n) == n - 1
        assert holds == (trial_division_is_prime(n) and n > 3)


def test_known_status_up_to_k13() -> None:
    for k in range(0, 14):
        want = k <= 4
        assert pepin_test(k) is want, k
        if k in KNOWN_FACTORS:
            assert fermat(k) % KNOWN_FACTORS[k] == 0
    assert pepin_test(14) is False  # composite; no factor of F_14 is used here


def test_composite_fermat_numbers_are_base_2_pseudoprimes() -> None:
    for k in range(5, 12):
        f = fermat(k)
        assert pow(2, f - 1, f) == 1  # the Fermat test with base 2 is fooled
        assert pepin_residue(k) != f - 1  # Pepin's test is not


def test_other_bases() -> None:
    for k in range(2, 12):
        f = fermat(k)
        for base in (5, 10):
            assert (pepin_residue(k, base) == f - 1) == (k <= 4)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        pepin_test(-1)
    for n in (0, 1, 2, 4, 9, 2**3 + 1, 2**6 + 1, 2**12 + 1):
        with pytest.raises(ValueError):
            is_fermat_number_prime(n)
