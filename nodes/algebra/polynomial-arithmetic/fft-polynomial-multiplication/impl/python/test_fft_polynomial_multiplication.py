# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fft-polynomial-multiplication/. The authors are listed in prov/WT2CHV.jsonl.

import random
from fractions import Fraction

import pytest

from fft_polynomial_multiplication import (
    multiply_complex,
    multiply_fraction,
    multiply_int,
    multiply_mod,
    multiply_mod_any,
    ntt,
)


def school(a, b):
    """The schoolbook product, normalized: the reference."""
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    while c and c[-1] == 0:
        c.pop()
    return c


def strip(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def school_mod(a, b, m):
    return strip([x % m for x in school(a, b)])


def test_example():
    # (1 + 2x)(3 - x) over Z/17Z with N = 4 and omega = 4 (4^2 = -1 mod 17)
    a = [1, 2, 0, 0]
    ntt(a, 4, 17)
    assert a == [3, 9, 16, 10]
    b = [3, 16, 0, 0]
    ntt(b, 4, 17)
    assert b == [2, 16, 4, 7]
    c = [x * y % 17 for x, y in zip(a, b)]
    assert c == [6, 8, 13, 2]
    ntt(c, 13, 17)  # 13 = 4^-1 mod 17
    inv4 = pow(4, -1, 17)
    assert [x * inv4 % 17 for x in c] == [3, 5, 15, 0]  # 3 + 5x - 2x^2
    assert multiply_int([1, 2], [3, -1]) == [3, 5, -2]
    assert multiply_mod([1, 1, 0, 3], [2, 998244352]) == [2, 1, 998244352, 6, 998244350]


def test_dft_is_evaluation():
    p, g = 998244353, 3
    rng = random.Random(3)
    for k in range(0, 7):
        size = 1 << k
        a = [rng.randrange(p) for _ in range(size)]
        w = pow(g, (p - 1) // size, p)
        got = list(a)
        ntt(got, w, p)
        want = [sum(a[j] * pow(w, i * j, p) for j in range(size)) % p for i in range(size)]
        assert got == want


def test_edges():
    assert multiply_int([], [1, 2]) == [] and multiply_int([3], []) == []
    assert multiply_int([5], [7]) == [35] and multiply_int([0, 1], [0, 1]) == [0, 0, 1]
    assert multiply_int([2], [0, 0, 1]) == [0, 0, 2]
    # products that cancel at the top over Z/pZ
    assert multiply_mod_any([1, 2], [1, 2], 4) == [1]
    assert multiply_mod_any([1, 1], [1, 1], 2) == [1, 0, 1]
    assert multiply_mod_any([2], [3], 6) == []
    # negative and large coefficients
    big = 10**30
    assert multiply_int([big, -big], [big, big]) == school([big, -big], [big, big])
    # very different degrees
    rng = random.Random(9)
    long = [rng.randint(-10**6, 10**6) for _ in range(700)] + [1]
    assert multiply_int(long, [3, -1]) == school(long, [3, -1])
    assert multiply_fraction([Fraction(1, 2)], [Fraction(2, 3), Fraction(0)]) == [Fraction(1, 3)]
    with pytest.raises(ValueError):
        multiply_mod([1] * 10, [1] * 10, 7, 3)


def test_random_over_z():
    rng = random.Random(1)
    for _ in range(600):
        a = strip([rng.randint(-100, 100) for _ in range(rng.randint(0, 20))])
        b = strip([rng.randint(-100, 100) for _ in range(rng.randint(0, 20))])
        assert multiply_int(a, b) == school(a, b)
    for _ in range(40):
        a = strip([rng.randint(-10**40, 10**40) for _ in range(rng.randint(1, 30))])
        b = strip([rng.randint(-10**20, 10**20) for _ in range(rng.randint(1, 30))])
        assert multiply_int(a, b) == school(a, b)


@pytest.mark.parametrize("m", [2, 3, 7, 998244353, 10**9 + 7, 4, 12])
def test_random_mod(m):
    rng = random.Random(m)
    for _ in range(500):
        a = strip([rng.randrange(m) for _ in range(rng.randint(0, 16))])
        b = strip([rng.randrange(m) for _ in range(rng.randint(0, 16))])
        assert multiply_mod_any(a, b, m) == school_mod(a, b, m)
        if m == 998244353:
            assert multiply_mod(a, b) == school_mod(a, b, m)


def test_random_ntt_primes():
    rng = random.Random(4)
    from fft_polynomial_multiplication import NTT_PRIMES

    for p, g in NTT_PRIMES:
        for _ in range(150):
            a = strip([rng.randrange(p) for _ in range(rng.randint(0, 40))])
            b = strip([rng.randrange(p) for _ in range(rng.randint(0, 40))])
            assert multiply_mod(a, b, p, g) == school_mod(a, b, p)


def test_random_over_q():
    rng = random.Random(2)
    for _ in range(500):
        a = strip([Fraction(rng.randint(-9, 9), rng.randint(1, 6)) for _ in range(rng.randint(0, 10))])
        b = strip([Fraction(rng.randint(-9, 9), rng.randint(1, 6)) for _ in range(rng.randint(0, 10))])
        assert multiply_fraction(a, b) == school(a, b)


def test_complex_fft_small_coefficients():
    rng = random.Random(6)
    for _ in range(500):
        a = strip([rng.randint(-50, 50) for _ in range(rng.randint(0, 30))])
        b = strip([rng.randint(-50, 50) for _ in range(rng.randint(0, 30))])
        assert multiply_complex(a, b) == school(a, b)


def test_larger_sizes():
    rng = random.Random(8)
    a = [rng.randint(-1000, 1000) for _ in range(2000)] + [1]
    b = [rng.randint(-1000, 1000) for _ in range(1500)] + [1]
    c = multiply_int(a, b)
    # check by evaluation at a few points instead of a slow schoolbook product
    for u in (1, -1, 2, 3):
        def ev(p):
            s = 0
            for x in reversed(p):
                s = s * u + x
            return s
        assert ev(c) == ev(a) * ev(b)
