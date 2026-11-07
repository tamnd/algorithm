# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bluestein-fft/. The authors are listed in prov/GDR6AH.jsonl.

import cmath
import math
import random

import pytest

from bluestein_fft import bluestein, inverse_bluestein

P = 998244353
ROOTS = {17: 3, 97: 5, P: 3}
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]


def naive_dft(x: list, p: int | None = None) -> list:
    n = len(x)
    if p is None:
        table = [cmath.exp(-2j * math.pi * m / n) for m in range(n)]
        return [sum(x[j] * table[j * k % n] for j in range(n)) for k in range(n)]
    w = pow(ROOTS[p], (p - 1) // n, p)
    table = [pow(w, m, p) for m in range(n)]
    return [sum(x[j] * table[j * k % n] for j in range(n)) % p for k in range(n)]


def close(a: list, b: list, scale: float) -> bool:
    n = max(len(a), 1)
    tol = 1e-13 * n * max(scale, 1.0)
    return len(a) == len(b) and all(abs(u - v) <= tol for u, v in zip(a, b))


def valid_lengths(p: int, limit: int) -> list[int]:
    out = []
    for n in range(1, limit + 1):
        m = 1
        while m < 2 * n - 1:
            m *= 2
        if (p - 1) % (2 * n) == 0 and (p - 1) % m == 0:
            out.append(n)
    return out


def test_worked_example() -> None:
    assert bluestein([1, 2, 3], 97, 5) == [6, 60, 34] == naive_dft([1, 2, 3], 97)
    assert inverse_bluestein([6, 60, 34], 97, 5) == [1, 2, 3]
    h = math.sqrt(3) / 2
    assert close(bluestein([1, 2, 3]), [6, complex(-1.5, h), complex(-1.5, -h)], 6)


def test_valid_lengths() -> None:
    assert valid_lengths(17, 200) == [1, 2, 4, 8]
    assert valid_lengths(97, 200) == [1, 2, 3, 4, 6, 8, 12, 16]
    assert valid_lengths(P, 200) == [1, 2, 4, 7, 8, 14, 16, 17, 28, 32, 34, 56, 64, 68, 112, 119, 128, 136]


def test_modular_against_oracle() -> None:
    rng = random.Random(1970)
    cases = 0
    for p in (17, 97, P):
        for n in valid_lengths(p, 140):
            for _ in range(25 if n <= 40 else 3):
                x = [rng.randrange(p) for _ in range(n)]
                y = bluestein(x, p, ROOTS[p])
                assert y == naive_dft(x, p)
                assert inverse_bluestein(y, p, ROOTS[p]) == x
                cases += 1
    assert cases >= 500


def test_complex_primes() -> None:
    rng = random.Random(1968)
    for n in PRIMES:
        for _ in range(3):
            x = [complex(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(n)]
            y = bluestein(x)
            scale = 5 * math.sqrt(n)
            assert close(y, naive_dft(x), scale)
            assert close(inverse_bluestein(y), x, 5)


def test_complex_random_lengths() -> None:
    rng = random.Random(1969)
    for _ in range(500):
        n = rng.randint(1, 40)
        x = [complex(rng.uniform(-10, 10), rng.uniform(-10, 10)) for _ in range(n)]
        y = bluestein(x)
        scale = 10 * math.sqrt(n)
        assert close(y, naive_dft(x), scale)
        assert close(inverse_bluestein(y), x, 10)


def test_edge_cases() -> None:
    assert bluestein([5], 97, 5) == [5]
    assert bluestein([3, 4], 17, 3) == [7, 16]
    assert close(bluestein([2.5]), [2.5], 1)
    assert close(bluestein([3, 4]), [7, -1], 4)
    for n in (1, 2, 3, 5, 6, 7, 10, 12, 31, 64, 100):
        assert close(bluestein([0.0] * n), [0.0] * n, 1)
        assert close(bluestein([1.0] + [0.0] * (n - 1)), [1.0] * n, 1)
        assert close(bluestein([2.0] * n), [2.0 * n] + [0.0] * (n - 1), 2 * n)
        for s in (0, n // 2, n - 1):
            imp = [0.0] * n
            imp[s] = 1.0
            assert close(bluestein(imp), naive_dft(imp), 1)
    for p in (17, 97, P):
        for n in valid_lengths(p, 20):
            assert bluestein([0] * n, p, ROOTS[p]) == [0] * n
            assert bluestein([1] + [0] * (n - 1), p, ROOTS[p]) == [1] * n
            assert bluestein([2] * n, p, ROOTS[p]) == [2 * n % p] + [0] * (n - 1)


def test_larger_lengths() -> None:
    rng = random.Random(2)
    for n in (127, 251, 509, 1000):
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        y = bluestein(x)
        energy = sum(abs(v) ** 2 for v in y)
        assert abs(energy - n * sum(abs(v) ** 2 for v in x)) < 1e-9 * n * n
        assert close(inverse_bluestein(y), x, 1)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        bluestein([])
    with pytest.raises(ValueError):
        bluestein([1, 2, 3], 17, 3)
    with pytest.raises(ValueError):
        bluestein([1] * 5, 97, 5)
