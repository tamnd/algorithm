# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/real-valued-fft/. The authors are listed in prov/C9SKTZ.jsonl.

import cmath
import math
import random

import pytest

from real_valued_fft import GaussMod, inverse_real_fft, real_fft

U = 2.0**-53
# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
# All three are 1 mod 4; 127 is 3 mod 4, where Z_p[i] is the field of p^2 elements.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]


def gauss_root(p, g, n):
    """An element of Z_p[i] of order n with w * conj(w) = 1, for p = 1 mod 4 and n | p - 1."""
    s = pow(g, (p - 1) // 4, p)  # a square root of -1
    a = pow(g, (p - 1) // n, p)
    u, v = a, pow(a, -1, p)  # the images of w under Z_p[i] -> Z_p x Z_p
    re = (u + v) * pow(2, -1, p) % p
    im = (u - v) * pow(2 * s, -1, p) % p
    return GaussMod(re, im, p)


def gauss_root_3mod4(p, n):
    """An element of order n in the norm-one subgroup of the field Z_p[i], n | p + 1."""
    for a in range(1, p):
        z = GaussMod(a, 1, p) ** (p - 1)
        w = z ** ((p + 1) // n)
        if n == 1 or w ** (n // 2) == GaussMod(-1, 0, p):
            return w
    raise AssertionError


def naive(x, w, p):
    n = len(x)
    one = GaussMod(1, 0, p)
    out = []
    for k in range(n // 2 + 1):
        acc = GaussMod(0, 0, p)
        for j, v in enumerate(x):
            acc = acc + (one * v) * (w ** (j * k % n))
        out.append(acc)
    return out


def naive_complex(x):
    n = len(x)
    return [sum(v * cmath.exp(-2j * math.pi * ((j * k) % n) / n) for j, v in enumerate(x)) for k in range(n // 2 + 1)]


def norm(v):
    return math.sqrt(sum(abs(t) ** 2 for t in v))


def tol(n, ref):
    return 64 * (n.bit_length() + 1) * U * max(norm(ref), 1.0)


def test_example():
    y = real_fft([1.0, 2.0, 3.0, 4.0])
    assert y == [10, -2 + 2j, -2]
    assert inverse_real_fft(y) == [1, 2, 3, 4]


def test_edges():
    assert real_fft([5.0]) == [5]
    assert real_fft([3.0, 5.0]) == [8, -2]
    for n in [1, 2, 4, 8, 16]:
        assert all(v == 0 for v in real_fft([0.0] * n))
        assert all(abs(v - 1) < 1e-12 for v in real_fft([1.0] + [0.0] * (n - 1)))
        y = real_fft([3.0] * n)
        assert abs(y[0] - 3 * n) < 1e-12 and all(abs(v) < 1e-12 * n for v in y[1:])
    with pytest.raises(ValueError):
        real_fft([1.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        real_fft([])


def test_exact_mod_primes():
    rng = random.Random(20261107)
    for p, g in PRIMES:
        n = 1
        while (p - 1) % n == 0 and n <= 64:
            w = gauss_root(p, g, n)
            for _ in range(6):
                x = [rng.randrange(p) for _ in range(n)]
                y = real_fft(x, w)
                assert y == naive(x, w, p)
                assert inverse_real_fft(y, w) == x
            n *= 2


def test_exact_3_mod_4():
    rng = random.Random(4)
    p = 127
    for n in [1, 2, 4, 8, 16, 32, 64, 128]:
        w = gauss_root_3mod4(p, n)
        for _ in range(4):
            x = [rng.randrange(p) for _ in range(n)]
            y = real_fft(x, w)
            assert y == naive(x, w, p)
            assert inverse_real_fft(y, w) == x


def test_bad_root():
    with pytest.raises(ValueError):
        real_fft([1, 2, 3, 4], GaussMod(4, 0, 17))  # 4 has order 4 but 4 * conj(4) = 16


def test_random_complex():
    rng = random.Random(77)
    for t in range(0, 11):
        n = 2**t
        for _ in range(3):
            x = [rng.uniform(-1, 1) for _ in range(n)]
            ref = naive_complex(x)
            y = real_fft(x)
            assert norm([a - b for a, b in zip(y, ref)]) <= tol(n, ref)
            back = inverse_real_fft(y)
            assert norm([a - b for a, b in zip(back, x)]) <= tol(n, x)


def test_large():
    rng = random.Random(3)
    n = 2**14
    x = [rng.gauss(0, 1) for _ in range(n)]
    y = real_fft(x)
    back = inverse_real_fft(y)
    assert norm([a - b for a, b in zip(back, x)]) <= tol(n, x)
    full = y + [v.conjugate() for v in y[-2:0:-1]]
    assert abs(norm(full) ** 2 - n * norm(x) ** 2) <= 1e-9 * n * norm(x) ** 2
