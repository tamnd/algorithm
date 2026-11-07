# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-fft/. The authors are listed in prov/37TN4K.jsonl.

import cmath
import random

import pytest

from iterative_fft import bit_reverse, cyclic_convolution, dif_stages, dit_stages, iterative_fft, twiddles

# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]
U = 2.0**-53


def naive_dft(x: list, w, p: int | None = None) -> list:
    n = len(x)
    if p is None:
        return [sum(x[j] * w ** (j * k) for j in range(n)) for k in range(n)]
    return [sum(x[j] * pow(w, j * k, p) for j in range(n)) % p for k in range(n)]


def naive_conv(a: list, b: list, p: int | None = None) -> list:
    n = len(a)
    c = [sum(a[j] * b[(m - j) % n] for j in range(n)) for m in range(n)]
    return c if p is None else [v % p for v in c]


def rev(j: int, t: int) -> int:
    return int(format(j, f"0{t}b")[::-1], 2) if t else 0


def root_mod(n: int, p: int, g: int) -> int:
    assert (p - 1) % n == 0
    return pow(g, (p - 1) // n, p)


def root_c(n: int) -> complex:
    return cmath.exp(-2j * cmath.pi / n)


def norm(v: list) -> float:
    return sum(abs(c) ** 2 for c in v) ** 0.5


def close(a: list, b: list, scale: float = 1.0) -> bool:
    n = max(len(a), 1)
    tol = 64 * (n.bit_length() + 1) * U * max(norm(b), scale, 1.0)
    return norm([u - v for u, v in zip(a, b)]) <= tol


def test_examples() -> None:
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    dif_stages(x, twiddles(2, 8, 17), 17)
    assert x == [2, 13, 14, 12, 8, 3, 6, 1]
    bit_reverse(x)
    assert x == [2, 8, 14, 6, 13, 3, 12, 1]
    assert cyclic_convolution([1, 2, 0, 0], [3, 4, 0, 0], 4, 17) == [3, 10, 8, 0]
    assert cyclic_convolution([1, 2, 3, 4], [1, 1, 0, 0], 4, 17) == [5, 3, 5, 7]
    z: list[complex] = [1, 2, 3, 4]
    iterative_fft(z, root_c(4))
    assert z == [10, -2 + 2j, -2, -2 - 2j]


def test_orders() -> None:
    # DIF writes X[rev(i)] at position i; DIT stages read that order.
    rng = random.Random(4)
    for p, g in PRIMES:
        for t in range(0, 5):
            n = 1 << t
            w = root_mod(n, p, g)
            x = [rng.randrange(p) for _ in range(n)]
            ref = naive_dft(x, w, p)
            y = list(x)
            dif_stages(y, twiddles(w, n, p), p)
            assert y == [ref[rev(i, t)] for i in range(n)]
            z = [x[rev(i, t)] for i in range(n)]
            dit_stages(z, twiddles(w, n, p), p)
            assert z == ref


def test_edges() -> None:
    for p, g in PRIMES:
        for t in range(0, 5):
            n = 1 << t
            w = root_mod(n, p, g)
            zeros = [0] * n
            iterative_fft(zeros, w, p)
            assert zeros == [0] * n
            for pos in range(n):
                imp = [int(j == pos) for j in range(n)]
                iterative_fft(imp, w, p)
                assert imp == [pow(w, pos * k, p) for k in range(n)]
            const = [7] * n
            iterative_fft(const, w, p)
            assert const == [7 * n % p] + [0] * (n - 1)
            delta = [1] + [0] * (n - 1)
            b = [rng_val % p for rng_val in range(3, 3 + n)]
            assert cyclic_convolution(delta, b, w, p) == b
    for n in (1, 2, 4, 8):
        c: list[complex] = [1] + [0] * (n - 1)
        iterative_fft(c, root_c(n))
        assert close(c, [1] * n)


def test_not_power_of_two() -> None:
    for n in (0, 3, 6, 10):
        with pytest.raises(ValueError):
            iterative_fft([1] * n, 1, 17)
    with pytest.raises(ValueError):
        cyclic_convolution([1, 2], [1, 2, 3, 4], 4, 17)


def test_random_mod() -> None:
    rng = random.Random(1965)
    for _ in range(500):
        p, g = PRIMES[rng.randrange(len(PRIMES))]
        t = rng.randint(0, 6 if p > 97 else (5 if p == 97 else 4))
        n = 1 << t
        w = root_mod(n, p, g)
        x = [rng.randrange(p) for _ in range(n)]
        y = list(x)
        iterative_fft(y, w, p)
        assert y == naive_dft(x, w, p)
        b = [rng.randrange(p) for _ in range(n)]
        assert cyclic_convolution(x, b, w, p) == naive_conv(x, b, p)


def test_random_complex() -> None:
    rng = random.Random(1966)
    for _ in range(300):
        n = 1 << rng.randint(0, 6)
        s = rng.choice([1.0, 1e3, 1e-3])
        x = [complex(rng.uniform(-s, s), rng.uniform(-s, s)) for _ in range(n)]
        w = root_c(n)
        y = list(x)
        iterative_fft(y, w)
        assert close(y, naive_dft(x, w))
        b = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        c = cyclic_convolution(x, b, w)
        assert close(c, naive_conv(x, b), norm(x) * norm(b))


def test_integer_product() -> None:
    # Polynomial product with zero padding, exact modulo 998244353.
    p, g = 998244353, 3
    rng = random.Random(30)
    for _ in range(40):
        da, db = rng.randint(0, 30), rng.randint(0, 30)
        a = [rng.randrange(1000) for _ in range(da + 1)]
        b = [rng.randrange(1000) for _ in range(db + 1)]
        n = 1
        while n < da + db + 1:
            n *= 2
        c = cyclic_convolution(a + [0] * (n - len(a)), b + [0] * (n - len(b)), root_mod(n, p, g), p)
        ref = [0] * (da + db + 1)
        for i, u in enumerate(a):
            for j, v in enumerate(b):
                ref[i + j] += u * v
        assert c[: da + db + 1] == ref and all(v == 0 for v in c[da + db + 1 :])
