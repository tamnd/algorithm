# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucy-hedgehog-prime-counting/. The authors are listed in prov/KWQ8J3.jsonl.

import random

from lucy_hedgehog_prime_counting import lucy_hedgehog_prime_counting, lucy_prime_sum


def is_prime_by_trial_division(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


LIMIT = 400000
PI = [0] * (LIMIT + 1)
SUM = [0] * (LIMIT + 1)


def _fill() -> None:
    flags = bytearray([1]) * (LIMIT + 1)
    flags[0] = flags[1] = 0
    p = 2
    while p * p <= LIMIT:
        if flags[p]:
            flags[p * p :: p] = bytes(len(range(p * p, LIMIT + 1, p)))
        p += 1
    c = s = 0
    for i in range(LIMIT + 1):
        if flags[i]:
            c += 1
            s += i
        PI[i] = c
        SUM[i] = s


_fill()


def test_table_against_trial_division() -> None:
    c = 0
    for m in range(5001):
        c += is_prime_by_trial_division(m)
        assert PI[m] == c


def test_every_x_up_to_2000() -> None:
    for x in range(-3, 2001):
        assert lucy_hedgehog_prime_counting(x) == PI[max(x, 0)]
        assert lucy_prime_sum(x) == SUM[max(x, 0)]


def test_squares_of_primes_and_neighbours() -> None:
    for q in (2, 3, 5, 7, 11, 13, 31, 97, 101, 211, 307, 541, 631):
        for x in (q * q - 1, q * q, q * q + 1, q**4 - 1, q**4, q**4 + 1):
            if 0 <= x <= LIMIT:
                assert lucy_hedgehog_prime_counting(x) == PI[x]
                assert lucy_prime_sum(x) == SUM[x]


def test_random() -> None:
    rng = random.Random(2013)
    for _ in range(80):
        x = rng.randint(2001, LIMIT)
        assert lucy_hedgehog_prime_counting(x) == PI[x]
        assert lucy_prime_sum(x) == SUM[x]


def test_known_values() -> None:
    assert lucy_hedgehog_prime_counting(100) == 25
    assert lucy_hedgehog_prime_counting(10**6) == 78498
    assert lucy_hedgehog_prime_counting(10**8) == 5761455
    assert lucy_hedgehog_prime_counting(10**9) == 50847534
    assert lucy_prime_sum(2 * 10**6) == 142913828922
