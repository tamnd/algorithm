# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meissel-lehmer-algorithm/. The authors are listed in prov/2SPPAE.jsonl.

import random

from meissel_lehmer_algorithm import icbrt, meissel_lehmer


def is_prime_by_trial_division(m: int) -> bool:
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


LIMIT = 300000
PI = [0] * (LIMIT + 1)


def _fill() -> None:
    flags = bytearray([1]) * (LIMIT + 1)
    flags[0] = flags[1] = 0
    p = 2
    while p * p <= LIMIT:
        if flags[p]:
            flags[p * p :: p] = bytes(len(range(p * p, LIMIT + 1, p)))
        p += 1
    c = 0
    for i in range(LIMIT + 1):
        c += flags[i]
        PI[i] = c


_fill()


def test_sieve_table_against_trial_division() -> None:
    c = 0
    for m in range(5001):
        c += is_prime_by_trial_division(m)
        assert PI[m] == c


def test_every_x_up_to_2000() -> None:
    for x in range(-3, 2001):
        assert meissel_lehmer(x) == PI[max(x, 0)]


def test_cube_root() -> None:
    for x in range(0, 30000):
        y = icbrt(x)
        assert y**3 <= x < (y + 1) ** 3
    for y in (10**5, 10**6 - 1, 2**21):
        for x in (y**3 - 1, y**3, y**3 + 1):
            c = icbrt(x)
            assert c**3 <= x < (c + 1) ** 3


def test_cubes_and_squares_of_primes() -> None:
    for q in (2, 3, 5, 7, 11, 13, 17, 31, 47, 61, 67):
        for base in (q**3, q * q, (q + 1) ** 3):
            for x in (base - 1, base, base + 1):
                if x <= LIMIT:
                    assert meissel_lehmer(x) == PI[x]
    for q in (101, 211, 307, 401, 541):
        assert meissel_lehmer(q * q) == PI[q * q]


def test_random() -> None:
    rng = random.Random(1959)
    for _ in range(60):
        x = rng.randint(2001, LIMIT)
        assert meissel_lehmer(x) == PI[x]


def test_known_values() -> None:
    assert meissel_lehmer(100) == 25
    assert meissel_lehmer(1000) == 168
    assert meissel_lehmer(10**6) == 78498
    assert meissel_lehmer(10**7) == 664579
    assert meissel_lehmer(10**8) == 5761455
