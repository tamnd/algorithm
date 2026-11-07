# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-fourier-transform/. The authors are listed in prov/14CJHC.jsonl.

import cmath
import random

import pytest

from fast_fourier_transform import fft, inverse_fft

# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]


def naive_dft(x: list, w, p: int | None = None) -> list:
    n = len(x)
    if p is None:
        return [sum(x[j] * w ** (j * k) for j in range(n)) for k in range(n)]
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def root_mod(n: int, p: int, g: int) -> int:
    assert (p - 1) % n == 0
    return pow(g, (p - 1) // n, p)


def root_c(n: int) -> complex:
    return cmath.exp(-2j * cmath.pi / n)


def close(a: list, b: list, scale: float) -> bool:
    n = max(len(a), 1)
    tol = 1e-12 * n * max(n.bit_length(), 1) * max(scale, 1.0)
    return all(abs(u - v) <= tol for u, v in zip(a, b))


def test_examples() -> None:
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    fft(x, 2, 17)
    assert x == [2, 8, 14, 6, 13, 3, 12, 1]
    y = [1, 2, 3, 4]
    fft(y, 4, 17)
    assert y == [10, 7, 15, 6]
    z: list[complex] = [1, 2, 3, 4]
    fft(z, root_c(4))
    assert close(z, [10, -2 + 2j, -2, -2 - 2j], 4)


def test_edges_mod() -> None:
    for p, g in PRIMES:
        for t in range(0, 5):
            n = 1 << t
            if (p - 1) % n:
                continue
            w = root_mod(n, p, g)
            zeros = [0] * n
            fft(zeros, w, p)
            assert zeros == [0] * n
            for pos in range(n):
                imp = [0] * n
                imp[pos] = 1
                fft(imp, w, p)
                assert imp == [pow(w, pos * k, p) for k in range(n)]
            const = [5] * n
            fft(const, w, p)
            assert const == [5 * n % p] + [0] * (n - 1)


def test_edges_complex() -> None:
    for n in (1, 2, 4, 8):
        w = root_c(n)
        imp: list[complex] = [1] + [0] * (n - 1)
        fft(imp, w)
        assert close(imp, [1] * n, 1)
        const: list[complex] = [3] * n
        fft(const, w)
        assert close(const, [3 * n] + [0] * (n - 1), 3 * n)


def test_not_power_of_two() -> None:
    for n in (0, 3, 6, 12):
        with pytest.raises(ValueError):
            fft([1] * n, 1, 17)


def test_random_mod_against_naive() -> None:
    rng = random.Random(1965)
    for _ in range(600):
        p, g = PRIMES[rng.randrange(len(PRIMES))]
        t = rng.randint(0, 6 if p > 97 else 4)
        n = 1 << t
        w = root_mod(n, p, g)
        x = [rng.randrange(p) for _ in range(n)]
        y = list(x)
        fft(y, w, p)
        assert y == naive_dft(x, w, p)
        inverse_fft(y, w, p)
        assert y == x


def test_random_complex_against_naive() -> None:
    rng = random.Random(1805)
    for _ in range(500):
        n = 1 << rng.randint(0, 6)
        scale = rng.choice([1.0, 1e3])
        x = [complex(rng.uniform(-scale, scale), rng.uniform(-scale, scale)) for _ in range(n)]
        w = root_c(n)
        y = list(x)
        fft(y, w)
        assert close(y, naive_dft(x, w), scale * n)
        inverse_fft(y, w)
        assert close(y, x, scale)


def test_conjugate_root() -> None:
    rng = random.Random(7)
    for _ in range(50):
        n = 1 << rng.randint(1, 5)
        x = [complex(rng.random(), rng.random()) for _ in range(n)]
        w = root_c(n).conjugate()
        y = list(x)
        fft(y, w)
        assert close(y, naive_dft(x, w), n)


def test_large_mod() -> None:
    p, g = 998244353, 3
    rng = random.Random(23)
    n = 1 << 10
    w = root_mod(n, p, g)
    x = [rng.randrange(p) for _ in range(n)]
    y = list(x)
    fft(y, w, p)
    for k in rng.sample(range(n), 8):
        assert y[k] == sum(x[j] * pow(w, j * k, p) for j in range(n)) % p
    inverse_fft(y, w, p)
    assert y == x
