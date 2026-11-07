# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mixed-radix-fft/. The authors are listed in prov/FR88CY.jsonl.

import cmath
import math
import random

import pytest

from mixed_radix_fft import mixed_radix_fft, prime_factors

U = 2.0**-53
# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]


def naive_mod(x, w, p):
    n = len(x)
    return [sum(v * pow(w, j * k, p) for j, v in enumerate(x)) % p for k in range(n)]


def naive_complex(x):
    n = len(x)
    return [sum(v * cmath.exp(-2j * math.pi * ((j * k) % n) / n) for j, v in enumerate(x)) for k in range(n)]


def norm(v):
    return math.sqrt(sum(abs(t) ** 2 for t in v))


def tol(rad, ref):
    """64 (r_1 + ... + r_t + 1) u ||ref||_2: a stage of radix r is a direct DFT of length r."""
    return 64 * (sum(rad) + 1) * U * max(norm(ref), 1.0)


def root(p, g, n):
    return pow(g, (p - 1) // n, p)


def factorizations(n, limit=6):
    """Some orderings of radices with product n."""
    f = prime_factors(n)
    out = [f, f[::-1]]
    if n % 4 == 0:
        out.append([4] * (n.bit_length() - 1 if n & (n - 1) == 0 else 0) or [4, n // 4])
    if n > 1 and len(f) > 1:
        out.append([f[0], n // f[0]])
        out.append([n])
    seen, res = set(), []
    for r in out:
        if math.prod(r) == n and tuple(r) not in seen:
            seen.add(tuple(r))
            res.append(r)
    return res[:limit]


def test_example_mod_97():
    w = pow(5, 16, 97)
    assert w == 36
    x = [1, 2, 3, 4, 5, 6]
    assert mixed_radix_fft(x, [2, 3], w, 97) == [21, 75, 23, 94, 68, 16]
    assert mixed_radix_fft(x, [3, 2], w, 97) == [21, 75, 23, 94, 68, 16]


def test_edges():
    assert mixed_radix_fft([7], [], 1, 97) == [7]
    assert mixed_radix_fft([3, 5], [2], 96, 97) == [8, 95]
    for n in [1, 2, 3, 5, 6, 9, 12]:
        assert max(map(abs, mixed_radix_fft([0j] * n))) == 0
        assert all(abs(v - 1) < 1e-12 for v in mixed_radix_fft([1] + [0] * (n - 1)))
        y = mixed_radix_fft([2.0] * n)
        assert abs(y[0] - 2 * n) < 1e-12 and all(abs(v) < 1e-12 * n for v in y[1:])


def test_errors():
    with pytest.raises(ValueError):
        mixed_radix_fft([])
    with pytest.raises(ValueError):
        mixed_radix_fft([1, 2, 3, 4], [3])
    with pytest.raises(ValueError):
        mixed_radix_fft([1, 2, 3, 4], [4, 1])
    with pytest.raises(ValueError):
        mixed_radix_fft([1, 2, 3, 4], None, 16, 17)  # 16 has order 2, not 4


def test_random_mod_all_orders():
    rng = random.Random(20261107)
    for p, g in PRIMES:
        lengths = [n for n in range(1, 130) if (p - 1) % n == 0]
        for n in lengths:
            w = root(p, g, n)
            for rad in factorizations(n):
                for _ in range(2):
                    x = [rng.randrange(p) for _ in range(n)]
                    y = mixed_radix_fft(x, rad, w, p)
                    assert y == naive_mod(x, w, p)
                    assert mixed_radix_fft(y, rad[::-1], w, p, inverse=True) == x


def test_large_mod_lengths():
    rng = random.Random(9)
    p, g = 998244353, 3
    for n in [7 * 17, 4 * 7 * 17]:
        w = root(p, g, n)
        x = [rng.randrange(p) for _ in range(n)]
        assert mixed_radix_fft(x, None, w, p) == naive_mod(x, w, p)


def test_random_complex_any_length():
    rng = random.Random(77)
    for n in list(range(1, 65)) + [96, 100, 210, 243, 360]:
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        ref = naive_complex(x)
        for rad in factorizations(n, 3):
            y = mixed_radix_fft(x, rad)
            assert norm([a - b for a, b in zip(y, ref)]) <= tol(rad, ref)
            back = mixed_radix_fft(y, rad, inverse=True)
            assert norm([a - b for a, b in zip(back, x)]) <= 2 * tol(rad, x)


def test_large_complex():
    rng = random.Random(3)
    n = 2**6 * 3**3 * 5  # 8640
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    y = mixed_radix_fft(x)
    back = mixed_radix_fft(y, inverse=True)
    assert norm([a - b for a, b in zip(back, x)]) <= 2 * tol(prime_factors(n), x)
    # Parseval as an independent check on the forward transform.
    assert abs(norm(y) ** 2 - n * norm(x) ** 2) <= 1e-9 * n * norm(x) ** 2
