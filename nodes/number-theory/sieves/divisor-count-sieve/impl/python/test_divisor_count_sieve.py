# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divisor-count-sieve/. The authors are listed in prov/VFD6YZ.jsonl.

import random

from divisor_count_sieve import divisor_count_sieve, divisor_power_sum_sieve


def divisors_by_definition(m: int) -> list[int]:
    return [e for e in range(1, m + 1) if m % e == 0]


def divisors_by_trial_division(m: int) -> list[int]:
    small, large, e = [], [], 1
    while e * e <= m:
        if m % e == 0:
            small.append(e)
            if e * e != m:
                large.append(m // e)
        e += 1
    return small + large[::-1]


def test_example() -> None:
    assert divisor_count_sieve(12) == [0, 1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6]
    assert divisor_power_sum_sieve(12) == [0, 1, 3, 4, 7, 6, 12, 8, 15, 13, 18, 12, 28]
    assert sum(divisor_count_sieve(12)) == 35


def test_edges() -> None:
    assert divisor_count_sieve(0) == [0]
    assert divisor_count_sieve(1) == [0, 1]
    assert divisor_count_sieve(2) == [0, 1, 2]
    assert divisor_power_sum_sieve(0, 2) == [0]
    assert divisor_power_sum_sieve(1, 0) == [0, 1]


def test_against_definition_up_to_800() -> None:
    d = divisor_count_sieve(800)
    s1 = divisor_power_sum_sieve(800, 1)
    s2 = divisor_power_sum_sieve(800, 2)
    for m in range(1, 801):
        divs = divisors_by_definition(m)
        assert d[m] == len(divs)
        assert s1[m] == sum(divs)
        assert s2[m] == sum(e * e for e in divs)


def test_every_n_up_to_2000() -> None:
    full = [0] + [len(divisors_by_trial_division(m)) for m in range(1, 2001)]
    for n in range(0, 2001, 7):
        assert divisor_count_sieve(n) == full[: n + 1]
    for n in range(1990, 2001):
        assert divisor_count_sieve(n) == full[: n + 1]


def test_random_larger_n() -> None:
    rng = random.Random(1849)
    for _ in range(4):
        n = rng.randint(2001, 50000)
        d = divisor_count_sieve(n)
        s = divisor_power_sum_sieve(n)
        for m in rng.sample(range(1, n + 1), 300) + [n]:
            divs = divisors_by_trial_division(m)
            assert d[m] == len(divs)
            assert s[m] == sum(divs)


def test_summatory_value() -> None:
    assert sum(divisor_count_sieve(10**4)) == 93668
