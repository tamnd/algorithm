# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-walsh-hadamard-transform/. The authors are listed in prov/E3XY86.jsonl.

import random

import pytest

from fast_walsh_hadamard_transform import fwht, inverse_fwht, xor_convolution

PRIMES = [17, 97, 998244353]


def naive_wht(x: list, p: int | None = None) -> list:
    n = len(x)
    y = [sum(x[j] * (-1) ** bin(j & k).count("1") for j in range(n)) for k in range(n)]
    return y if p is None else [v % p for v in y]


def naive_xor_conv(a: list[int], b: list[int]) -> list[int]:
    n = len(a)
    c = [0] * n
    for i in range(n):
        for j in range(n):
            c[i ^ j] += a[i] * b[j]
    return c


def test_examples() -> None:
    x = [1, 2, 3, 4]
    fwht(x)
    assert x == [10, -2, -4, 0]
    y = [3, 1, 4, 1, 5, 9, 2, 6]
    fwht(y)
    assert y == [31, -3, 5, -1, -13, 13, -7, -1]
    inverse_fwht(y)
    assert y == [3, 1, 4, 1, 5, 9, 2, 6]
    assert xor_convolution([1, 2, 3, 4], [5, 6, 7, 8]) == [70, 68, 62, 60]
    assert xor_convolution([1, 2, 3, 4], [5, 6, 7, 8], 17) == [70 % 17, 68 % 17, 62 % 17, 60 % 17]


def test_edges() -> None:
    for t in range(0, 6):
        n = 1 << t
        z = [0] * n
        fwht(z)
        assert z == [0] * n
        for pos in range(n):
            imp = [0] * n
            imp[pos] = 1
            fwht(imp)
            assert imp == [(-1) ** bin(pos & k).count("1") for k in range(n)]
        c = [7] * n
        fwht(c)
        assert c == [7 * n] + [0] * (n - 1)
    one = [5]
    fwht(one)
    assert one == [5]
    two = [5, 2]
    fwht(two)
    assert two == [7, 3]


def test_not_power_of_two() -> None:
    for n in (0, 3, 5, 12):
        with pytest.raises(ValueError):
            fwht([1] * n)


def test_random_int_against_naive() -> None:
    rng = random.Random(1923)
    for _ in range(600):
        n = 1 << rng.randint(0, 6)
        x = [rng.randint(-1000, 1000) for _ in range(n)]
        y = list(x)
        fwht(y)
        assert y == naive_wht(x)
        z = list(y)
        fwht(z)
        assert z == [n * v for v in x]
        inverse_fwht(y)
        assert y == x


def test_random_mod_against_naive() -> None:
    rng = random.Random(1976)
    for _ in range(300):
        p = PRIMES[rng.randrange(len(PRIMES))]
        n = 1 << rng.randint(0, 6)
        x = [rng.randrange(p) for _ in range(n)]
        y = list(x)
        fwht(y, p)
        assert y == naive_wht(x, p)
        inverse_fwht(y, p)
        assert y == x


def test_random_float() -> None:
    rng = random.Random(1867)
    for _ in range(200):
        n = 1 << rng.randint(0, 7)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        y = list(x)
        fwht(y)
        ref = naive_wht(x)
        tol = 1e-13 * n * max(n.bit_length(), 1)
        assert all(abs(u - v) <= tol for u, v in zip(y, ref))
        inverse_fwht(y)
        assert all(abs(u - v) <= tol for u, v in zip(y, x))


def test_xor_convolution_random() -> None:
    rng = random.Random(23)
    for _ in range(300):
        n = 1 << rng.randint(0, 5)
        a = [rng.randint(-50, 50) for _ in range(n)]
        b = [rng.randint(-50, 50) for _ in range(n)]
        assert xor_convolution(a, b) == naive_xor_conv(a, b)
        p = PRIMES[rng.randrange(len(PRIMES))]
        assert xor_convolution(a, b, p) == [v % p for v in naive_xor_conv(a, b)]
