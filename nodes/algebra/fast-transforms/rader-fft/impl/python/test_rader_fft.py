# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rader-fft/. The authors are listed in prov/8K6AGB.jsonl.

import cmath
import math
import random

import pytest

from rader_fft import cyclic_convolution, is_prime, primitive_root, rader_fft

U = 2.0**-53
# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]


def naive_mod(x, w, P):
    n = len(x)
    return [sum(v * pow(w, j * k, P) for j, v in enumerate(x)) % P for k in range(n)]


def naive_complex(x):
    n = len(x)
    return [sum(v * cmath.exp(-2j * math.pi * ((j * k) % n) / n) for j, v in enumerate(x)) for k in range(n)]


def norm(v):
    return math.sqrt(sum(abs(t) ** 2 for t in v))


def conv_length(n):
    L = 1
    while L < 2 * n - 3:
        L *= 2
    return L


def modulus_for(n):
    """A prime P = 1 mod n with P - 1 divisible by the inner convolution length."""
    step = n * conv_length(n) // math.gcd(n, conv_length(n))
    P = step + 1
    while not is_prime(P):
        P += step
    return P


def test_example_mod_41():
    assert primitive_root(41) == 6 and primitive_root(5) == 2
    w = pow(6, 8, 41)
    assert w == 10
    assert cyclic_convolution([2, 3, 5, 4], [10, 16, 37, 18], 41) == [36, 13, 39, 21]
    assert rader_fft([1, 2, 3, 4, 5], w, 41) == [15, 37, 22, 14, 40]


def test_given_primes():
    rng = random.Random(20261107)
    for P, g in PRIMES:
        for n in [q for q in range(2, 40) if is_prime(q) and (P - 1) % q == 0 and (P - 1) % conv_length(q) == 0]:
            w = pow(g, (P - 1) // n, P)
            for _ in range(5):
                x = [rng.randrange(P) for _ in range(n)]
                y = rader_fft(x, w, P)
                assert y == naive_mod(x, w, P)
                assert rader_fft(y, w, P, inverse=True) == x


def test_many_prime_lengths_exact():
    rng = random.Random(11)
    for n in [q for q in range(2, 140) if is_prime(q)]:
        P = modulus_for(n)
        w = pow(primitive_root(P), (P - 1) // n, P)
        for _ in range(2):
            x = [rng.randrange(P) for _ in range(n)]
            y = rader_fft(x, w, P)
            assert y == naive_mod(x, w, P)
            assert rader_fft(y, w, P, inverse=True) == x


def test_edges():
    assert rader_fft([3, 5], 16, 17) == [8, 15]
    for n in [2, 3, 5, 7, 11, 13]:
        assert max(map(abs, rader_fft([0j] * n))) == 0
        assert all(abs(v - 1) < 1e-12 for v in rader_fft([1.0] + [0.0] * (n - 1)))
        y = rader_fft([2.0] * n)
        assert abs(y[0] - 2 * n) < 1e-12 and all(abs(v) < 1e-12 * n for v in y[1:])


def test_errors():
    with pytest.raises(ValueError):
        rader_fft([1.0, 2.0, 3.0, 4.0])
    with pytest.raises(ValueError):
        rader_fft([1.0])
    with pytest.raises(ValueError):
        rader_fft([1, 2, 3], 1, 97)


def test_random_complex():
    rng = random.Random(77)
    for n in [q for q in range(2, 400) if is_prime(q)]:
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        ref = naive_complex(x) if n < 200 else None
        y = rader_fft(x)
        tol = 64 * (n.bit_length() + 2) * U
        if ref is not None:
            assert norm([a - b for a, b in zip(y, ref)]) <= tol * norm(ref)
        back = rader_fft(y, inverse=True)
        assert norm([a - b for a, b in zip(back, x)]) <= tol * norm(x)


def test_large_complex():
    rng = random.Random(3)
    n = 8191  # a Mersenne prime; the inner length is 16384
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    y = rader_fft(x)
    back = rader_fft(y, inverse=True)
    assert norm([a - b for a, b in zip(back, x)]) <= 64 * (n.bit_length() + 2) * U * norm(x)
    assert abs(norm(y) ** 2 - n * norm(x) ** 2) <= 1e-9 * n * norm(x) ** 2
