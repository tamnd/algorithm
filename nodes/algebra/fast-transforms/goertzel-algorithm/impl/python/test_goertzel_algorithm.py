# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goertzel-algorithm/. The authors are listed in prov/R480RJ.jsonl.

import cmath
import math
import random

import pytest

from goertzel_algorithm import goertzel

U = 2.0**-53
# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]


def naive_mod(x, k, w, p):
    return sum(xj * pow(w, j * k, p) for j, xj in enumerate(x)) % p


def naive_complex(x, k):
    n = len(x)
    re = math.fsum((xj * cmath.exp(-2j * math.pi * ((j * k) % n) / n)).real for j, xj in enumerate(x))
    im = math.fsum((xj * cmath.exp(-2j * math.pi * ((j * k) % n) / n)).imag for j, xj in enumerate(x))
    return complex(re, im)


def tolerance(x, k):
    """The proved first-order bound (13u + eta + mu)(n + 2) M ||x||_1, with eta + mu <= 7u."""
    n = len(x)
    s = abs(math.sin(2 * math.pi * (k % n) / n))
    m = n if s == 0 else min(n, 1 / s)
    return 20 * U * (n + 2) * m * max(sum(abs(t) for t in x), 1e-300)


def root(p, g, n):
    assert (p - 1) % n == 0
    return pow(g, (p - 1) // n, p)


def test_example_mod_17():
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    assert goertzel(x, 1, 2, 17) == 8
    assert [goertzel(x, k, 2, 17) for k in range(8)] == [2, 8, 14, 6, 13, 3, 12, 1]


def test_example_complex():
    assert abs(goertzel([1, 2, 3, 4], 1) - (-2 + 2j)) < 1e-12


def test_edges_complex():
    assert goertzel([5.0], 0) == 5
    assert abs(goertzel([3.0, 4.0], 1) - (-1)) < 1e-15
    for n in [1, 2, 3, 7, 8, 12]:
        for k in range(n):
            assert goertzel([0.0] * n, k) == 0
            assert abs(goertzel([1.0] + [0.0] * (n - 1), k) - 1) < 1e-12
            want = n * 2.5 if k == 0 else 0
            assert abs(goertzel([2.5] * n, k) - want) < 1e-12 * n


def test_errors():
    with pytest.raises(ValueError):
        goertzel([], 0)
    with pytest.raises(ValueError):
        goertzel([1, 2, 3], 1, 2, 17)


def test_random_mod():
    rng = random.Random(20261107)
    for p, g in PRIMES:
        lengths = [n for n in range(1, 50) if (p - 1) % n == 0]
        for n in lengths:
            w = root(p, g, n)
            for _ in range(5):
                x = [rng.randrange(p) for _ in range(n)]
                for k in range(n):
                    assert goertzel(x, k, w, p) == naive_mod(x, k, w, p)
                    assert goertzel(x, k + 3 * n, w, p) == goertzel(x, k, w, p)


def test_inverse_mod():
    rng = random.Random(5)
    for p, g in PRIMES:
        for n in [n for n in (1, 2, 3, 4, 6, 8, 12, 16) if (p - 1) % n == 0]:
            w = root(p, g, n)
            x = [rng.randrange(p) for _ in range(n)]
            y = [goertzel(x, k, w, p) for k in range(n)]
            ninv = pow(n, -1, p)
            back = [goertzel(y, j, pow(w, -1, p), p) * ninv % p for j in range(n)]
            assert back == x


def test_random_complex_any_length():
    rng = random.Random(77)
    for n in list(range(1, 40)) + [97, 128, 255, 256, 331]:
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        for k in rng.sample(range(n), min(n, 6)) + [0, n - 1]:
            assert abs(goertzel(x, k) - naive_complex(x, k)) <= tolerance(x, k)
        y = [goertzel(x, k) for k in range(n)] if n <= 64 else None
        if y is not None:
            back = [goertzel([v.conjugate() for v in y], j).conjugate() / n for j in range(n)]
            assert max(abs(a - b) for a, b in zip(back, x)) <= 1e-12 * n


def test_large_real():
    rng = random.Random(3)
    n = 4096
    x = [rng.uniform(-1, 1) for _ in range(n)]
    for k in [0, 1, 2, n // 4, n // 2 - 1, n // 2, n - 1]:
        assert abs(goertzel(x, k) - naive_complex(x, k)) <= tolerance(x, k)
