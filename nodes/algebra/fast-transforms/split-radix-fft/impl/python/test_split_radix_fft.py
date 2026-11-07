# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/split-radix-fft/. The authors are listed in prov/7Q1636.jsonl.

import cmath
import math
import random

import pytest

from split_radix_fft import split_radix_core, split_radix_fft

U = 2.0**-53


def dft_mod(x, w, p):
    n = len(x)
    return [sum(v * pow(w, j * k, p) for j, v in enumerate(x)) % p for k in range(n)]


def dft_c(x):
    n = len(x)
    return [sum(v * cmath.exp(-2j * math.pi * ((j * k) % n) / n) for j, v in enumerate(x)) for k in range(n)]


def root(p, g, n):
    return pow(g, (p - 1) // n, p)


def norm(v):
    return math.sqrt(sum(abs(t) ** 2 for t in v))


def tol(n, x):
    return 64 * (n.bit_length() + 1) * U * math.sqrt(n) * max(norm(x), 1.0)


MODS = [(17, 3, 16), (97, 5, 32), (998244353, 3, 2**23)]


@pytest.mark.parametrize("p,g,nmax", MODS)
def test_exact_mod_p(p, g, nmax):
    rng = random.Random(p)
    n = 1
    while n <= min(nmax, 256):
        w = root(p, g, n)
        for _ in range(5):
            x = [rng.randrange(p) for _ in range(n)]
            X = split_radix_fft(x, w, p)
            assert X == dft_mod(x, w, p)
            assert split_radix_fft(X, w, p, inverse=True) == x
        n *= 2


def test_example_mod_17():
    assert split_radix_fft([1, 2, 3, 4, 5, 6, 7, 8], 2, 17) == [2, 8, 14, 6, 13, 3, 12, 1]


def test_large_mod_p_round_trip():
    p, g = 998244353, 3
    rng = random.Random(7)
    n = 2**12
    w = root(p, g, n)
    x = [rng.randrange(p) for _ in range(n)]
    X = split_radix_fft(x, w, p)
    assert split_radix_fft(X, w, p, inverse=True) == x
    k = rng.randrange(n)
    assert X[k] == sum(v * pow(w, j * k, p) for j, v in enumerate(x)) % p


def test_integer_ring():
    # Over Z[i], with w = -i for n = 4 and exact Gaussian integers as complex numbers.
    rng = random.Random(3)
    for _ in range(50):
        x = [rng.randint(-100, 100) for _ in range(4)]
        assert split_radix_fft(x) == [complex(round(v.real), round(v.imag)) for v in dft_c(x)]


def test_complex_against_direct():
    rng = random.Random(11)
    for L in range(0, 9):
        n = 2**L
        for _ in range(4):
            x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
            X = split_radix_fft(x)
            R = dft_c(x)
            assert norm([a - b for a, b in zip(X, R)]) <= tol(n, x)


def test_complex_round_trip_large():
    rng = random.Random(13)
    for L in (10, 12, 14):
        n = 2**L
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        y = split_radix_fft(split_radix_fft(x), inverse=True)
        assert norm([a - b for a, b in zip(x, y)]) <= tol(n, x)


def test_edge_cases():
    assert split_radix_fft([5]) == [5]
    assert split_radix_fft([3, 1], 16, 17) == [4, 2]
    for n in (1, 2, 4, 8, 64):
        assert split_radix_fft([0] * n) == [0] * n
        imp = [1] + [0] * (n - 1)
        assert split_radix_fft(imp) == [1] * n
        const = split_radix_fft([2.5] * n)
        assert abs(const[0] - 2.5 * n) <= tol(n, [2.5] * n)
        assert norm(const[1:]) <= tol(n, [2.5] * n)
    with pytest.raises(ValueError):
        split_radix_fft([1, 2, 3])
    with pytest.raises(ValueError):
        split_radix_fft([1, 2, 3, 4], 2, 17)  # 2 has order 8, not 4


C = {"a": 0, "m": 0}


class Count:
    def __init__(self, v):
        self.v = v

    def __add__(self, o):
        C["a"] += 1
        return Count(self.v + o.v)

    def __sub__(self, o):
        C["a"] += 1
        return Count(self.v - o.v)

    def __mul__(self, o):
        C["m"] += 1
        return Count(self.v * o.v)


def test_operation_counts():
    for L in range(0, 13):
        n = 2**L
        C["a"] = C["m"] = 0
        split_radix_core([Count(1)] * n, [Count(1)] * n)
        assert C["a"] == n * L
        assert 2 * C["m"] == n * L - 2 * n + 2
