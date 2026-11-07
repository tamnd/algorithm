# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/convolution-via-fft/. The authors are listed in prov/XX6TKR.jsonl.

import cmath
import random

import pytest

from convolution_via_fft import _fft, convolve_complex, convolve_mod

# (prime, primitive root, largest power of two dividing p - 1)
PRIMES = [(17, 3, 16), (97, 5, 32), (998244353, 3, 1 << 23)]


def naive_conv(a: list, b: list) -> list:
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def naive_dft_mod(x: list[int], w: int, p: int) -> list[int]:
    n = len(x)
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def close(u: list, v: list, scale: float) -> bool:
    n = max(len(u), 1)
    tol = 1e-12 * n * max(n.bit_length(), 1) * max(scale, 1.0)
    return len(u) == len(v) and all(abs(x - y) <= tol for x, y in zip(u, v))


def test_examples() -> None:
    p = 998244353
    assert convolve_mod([1, 2, 3], [4, 5], p, 3) == [4, 13, 22, 15]
    assert convolve_mod([1, 2, 3, 4], [5, 6, 7, 8], p, 3) == [5, 16, 34, 60, 61, 52, 32]
    die = [0, 1, 1, 1, 1, 1, 1]
    assert convolve_mod(die, die, 17, 3) == [0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
    assert convolve_mod([3, 2, 1], [5, 4], 97, 5) == [15, 22, 13, 4]
    c = convolve_complex([1, 2, 3], [4, 5])
    assert [round(v.real) for v in c] == [4, 13, 22, 15]


def test_internal_fft_against_naive_dft() -> None:
    rng = random.Random(30)
    for p, g, top in PRIMES:
        for t in range(0, 5):
            n = 1 << t
            w = pow(g, (p - 1) // n, p)
            for _ in range(10):
                x = [rng.randrange(p) for _ in range(n)]
                y = list(x)
                _fft(y, w, lambda v: v % p)
                assert y == naive_dft_mod(x, w, p)


def test_edges() -> None:
    p = 97
    assert convolve_mod([7], [5], p, 5) == [35]
    assert convolve_mod([0, 0, 0], [0, 0], p, 5) == [0, 0, 0, 0]
    a = [3, 1, 4, 1, 5, 9, 2, 6]
    assert convolve_mod(a, [1], p, 5) == a
    assert convolve_mod(a, [0, 0, 1], p, 5) == [0, 0] + a
    assert convolve_mod([2] * 5, [3] * 4, p, 5) == [v % p for v in naive_conv([2] * 5, [3] * 4)]
    assert close(convolve_complex([2.5], [-4]), [-10], 10)
    assert close(convolve_complex([0, 0], [0]), [0, 0], 1)


def test_errors() -> None:
    with pytest.raises(ValueError):
        convolve_mod([], [1], 17, 3)
    with pytest.raises(ValueError):
        convolve_complex([1], [])
    with pytest.raises(ValueError):
        convolve_mod([1] * 10, [1] * 10, 17, 3)  # needs N = 32, which does not divide 16


def test_random_mod_against_naive() -> None:
    rng = random.Random(1966)
    for _ in range(600):
        p, g, top = PRIMES[rng.randrange(len(PRIMES))]
        limit = min(top, 64)
        m = rng.randint(1, limit // 2)
        l = rng.randint(1, limit - m + 1)
        a = [rng.randrange(p) for _ in range(m)]
        b = [rng.randrange(p) for _ in range(l)]
        assert convolve_mod(a, b, p, g) == [v % p for v in naive_conv(a, b)]


def test_random_complex_against_naive() -> None:
    rng = random.Random(1970)
    for _ in range(500):
        m, l = rng.randint(1, 40), rng.randint(1, 40)
        scale = rng.choice([1.0, 100.0])
        a = [complex(rng.uniform(-scale, scale), rng.uniform(-scale, scale)) for _ in range(m)]
        b = [complex(rng.uniform(-scale, scale), rng.uniform(-scale, scale)) for _ in range(l)]
        assert close(convolve_complex(a, b), naive_conv(a, b), scale * scale * (m + l))


def test_integer_rounding_exact() -> None:
    rng = random.Random(1971)
    for _ in range(100):
        m, l = rng.randint(1, 200), rng.randint(1, 200)
        a = [rng.randint(-999, 999) for _ in range(m)]
        b = [rng.randint(-999, 999) for _ in range(l)]
        c = convolve_complex(a, b)
        assert [round(v.real) for v in c] == naive_conv(a, b)


def test_complex_impulse_and_constant() -> None:
    n = 16
    w = cmath.exp(-2j * cmath.pi / n)
    imp = [1 + 0j] + [0j] * (n - 1)
    _fft(imp, w, lambda v: v)
    assert close(imp, [1] * n, 1)
    c = convolve_complex([1] * 6, [1] * 6)
    assert close(c, [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], 36)
