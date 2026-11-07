# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-fft/. The authors are listed in prov/BWBTC5.jsonl.

import cmath
import random

import pytest

from inverse_fft import forward_fft, inverse_fft

# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]
U = 2.0**-53


def naive_dft(x: list, w, p: int | None = None) -> list:
    n = len(x)
    if p is None:
        return [sum(x[j] * w ** (j * k) for j in range(n)) for k in range(n)]
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def naive_idft(y: list, w, p: int | None = None) -> list:
    """The O(n^2) reference: x[j] = (1/n) sum of y[k] w^(-jk)."""
    n = len(y)
    if p is None:
        return [sum(y[k] * w ** (-j * k) for k in range(n)) / n for j in range(n)]
    w_inv, n_inv = pow(w, -1, p), pow(n, -1, p)
    return [sum(y[k] * pow(w_inv, j * k, p) for k in range(n)) * n_inv % p for j in range(n)]


def root_mod(n: int, p: int, g: int) -> int:
    assert (p - 1) % n == 0
    return pow(g, (p - 1) // n, p)


def root_c(n: int) -> complex:
    return cmath.exp(-2j * cmath.pi / n)


def norm(v: list) -> float:
    return sum(abs(c) ** 2 for c in v) ** 0.5


def close(a: list, b: list) -> bool:
    """2-norm error within a tolerance scaled by lg n, as the bound predicts."""
    n = max(len(a), 1)
    tol = 64 * (n.bit_length() + 1) * U * max(norm(b), 1.0)
    return norm([u - v for u, v in zip(a, b)]) <= tol


def test_examples() -> None:
    # The worked example: n = 8 modulo 17 with w = 2.
    y = [2, 8, 14, 6, 13, 3, 12, 1]
    inverse_fft(y, 2, 17)
    assert y == [1, 2, 3, 4, 5, 6, 7, 8]
    z = [2, 8, 14, 6, 13, 3, 12, 1]
    inverse_fft(z, 2, 17, scale=False)
    assert z == [8 * v % 17 for v in range(1, 9)]
    q = [10, 7, 15, 6]
    inverse_fft(q, 4, 17)
    assert q == [1, 2, 3, 4]
    c: list[complex] = [10, -2 + 2j, -2, -2 - 2j]
    inverse_fft(c, root_c(4))
    assert close(c, [1, 2, 3, 4])


def test_edges_mod() -> None:
    for p, g in PRIMES:
        for t in range(0, 5):
            n = 1 << t
            w = root_mod(n, p, g)
            zeros = [0] * n
            inverse_fft(zeros, w, p)
            assert zeros == [0] * n
            # A spike at frequency k comes from the wave w^(-jk)/n.
            for k in range(n):
                spike = [0] * n
                spike[k] = 1
                inverse_fft(spike, w, p)
                assert spike == naive_idft([int(i == k) for i in range(n)], w, p)
            ones = [1] * n
            inverse_fft(ones, w, p)
            assert ones == [1] + [0] * (n - 1)
            const = [n % p] + [0] * (n - 1)
            inverse_fft(const, w, p)
            assert const == [1] * n


def test_edges_complex() -> None:
    for n in (1, 2, 4, 8):
        w = root_c(n)
        ones: list[complex] = [1] * n
        inverse_fft(ones, w)
        assert close(ones, [1] + [0] * (n - 1))
        spike: list[complex] = [n] + [0] * (n - 1)
        inverse_fft(spike, w)
        assert close(spike, [1] * n)
        zeros: list[complex] = [0] * n
        inverse_fft(zeros, w)
        assert zeros == [0] * n


def test_small_exact_complex() -> None:
    # For n <= 4 all twiddle factors are 1 or -i or i, so integer data stays exact.
    for n, w in ((1, 1 + 0j), (2, -1 + 0j), (4, -1j)):
        rng = random.Random(n)
        for _ in range(50):
            x = [complex(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(n)]
            y = naive_dft(x, w)
            inverse_fft(y, w)
            assert y == x


def test_not_power_of_two() -> None:
    for n in (0, 3, 5, 6, 12):
        with pytest.raises(ValueError):
            inverse_fft([1] * n, 1, 17)


def test_random_mod_against_naive() -> None:
    rng = random.Random(1966)
    for _ in range(600):
        p, g = PRIMES[rng.randrange(len(PRIMES))]
        t = rng.randint(0, 6 if p > 97 else (5 if p == 97 else 4))
        n = 1 << t
        w = root_mod(n, p, g)
        y = [rng.randrange(p) for _ in range(n)]
        x = list(y)
        inverse_fft(x, w, p)
        assert x == naive_idft(y, w, p)
        forward_fft(x, w, p)
        assert x == y
        z = list(y)
        inverse_fft(z, w, p, scale=False)
        assert z == [v * n % p for v in naive_idft(y, w, p)]


def test_random_complex_against_naive() -> None:
    rng = random.Random(1805)
    for _ in range(400):
        n = 1 << rng.randint(0, 6)
        s = rng.choice([1.0, 1e3, 1e-3])
        y = [complex(rng.uniform(-s, s), rng.uniform(-s, s)) for _ in range(n)]
        w = root_c(n)
        x = list(y)
        inverse_fft(x, w)
        assert close(x, naive_idft(y, w))
        forward_fft(x, w)
        assert close(x, y)


def test_large() -> None:
    p, g = 998244353, 3
    rng = random.Random(23)
    n = 1 << 12
    w = root_mod(n, p, g)
    x = [rng.randrange(p) for _ in range(n)]
    y = list(x)
    forward_fft(y, w, p)
    for k in rng.sample(range(n), 4):
        assert y[k] == sum(x[j] * pow(w, j * k, p) for j in range(n)) % p
    inverse_fft(y, w, p)
    assert y == x
    xs = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
    ys = list(xs)
    forward_fft(ys, root_c(n))
    inverse_fft(ys, root_c(n))
    assert close(ys, xs)
