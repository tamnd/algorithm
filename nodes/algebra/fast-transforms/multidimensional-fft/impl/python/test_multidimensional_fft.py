# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multidimensional-fft/. The authors are listed in prov/98S7CV.jsonl.

import cmath
import itertools
import random
from math import prod

import pytest

from multidimensional_fft import multidimensional_fft

# (prime, primitive root): 3 is a primitive root of 17 and 998244353, 5 of 97.
PRIMES = [(17, 3), (97, 5), (998244353, 3)]
U = 2.0**-53


def index(j: tuple, shape: list[int]) -> int:
    r = 0
    for ja, na in zip(j, shape):
        r = r * na + ja
    return r


def naive(x: list, shape: list[int], roots: list, p: int | None = None) -> list:
    """The O(N^2) d-dimensional DFT, straight from the definition."""
    pts = list(itertools.product(*[range(n) for n in shape]))
    out = [0] * len(x)
    for k in pts:
        acc = 0
        for j in pts:
            w = 1
            for a, (ja, ka) in enumerate(zip(j, k)):
                w = w * (pow(roots[a], ja * ka, p) if p else roots[a] ** (ja * ka))
                if p:
                    w %= p
            acc += x[index(j, shape)] * w
        out[index(k, shape)] = acc % p if p else acc
    return out


def mod_roots(shape: list[int], p: int, g: int) -> list[int]:
    return [pow(g, (p - 1) // n, p) for n in shape]


def c_roots(shape: list[int]) -> list[complex]:
    return [cmath.exp(-2j * cmath.pi / n) for n in shape]


def norm(v: list) -> float:
    return sum(abs(c) ** 2 for c in v) ** 0.5


def close(a: list, b: list) -> bool:
    n = max(len(a), 1)
    tol = 64 * (n.bit_length() + 1) * U * max(norm(b), 1.0)
    return norm([u - v for u, v in zip(a, b)]) <= tol


def inverse(y: list, shape: list[int], roots: list, p: int | None = None) -> list:
    x = list(y)
    n = prod(shape)
    if p is None:
        multidimensional_fft(x, shape, [1 / w for w in roots])
        return [v / n for v in x]
    multidimensional_fft(x, shape, [pow(w, -1, p) for w in roots], p)
    n_inv = pow(n, -1, p)
    return [v * n_inv % p for v in x]


SHAPES = [[1], [2], [8], [1, 1], [2, 4], [4, 2], [4, 4], [2, 1, 4], [2, 2, 2], [1, 8, 2], [2, 2, 2, 2]]


def test_example() -> None:
    x = [1, 2, 3, 4, 5, 6, 7, 8]
    multidimensional_fft(x, [2, 4], [16, 13], 17)
    assert x == [36 % 17, (-4 - 4 * 13) % 17, (-4) % 17, (-4 + 4 * 13) % 17, (-16) % 17, 0, 0, 0]
    assert x == [2, 12, 13, 14, 1, 0, 0, 0]


def test_edges() -> None:
    for p, g in PRIMES:
        for shape in SHAPES:
            n = prod(shape)
            roots = mod_roots(shape, p, g)
            zeros = [0] * n
            multidimensional_fft(zeros, shape, roots, p)
            assert zeros == [0] * n
            const = [5] * n
            multidimensional_fft(const, shape, roots, p)
            assert const == [5 * n % p] + [0] * (n - 1)
            imp = [1] + [0] * (n - 1)
            multidimensional_fft(imp, shape, roots, p)
            assert imp == [1] * n


def test_errors() -> None:
    with pytest.raises(ValueError):
        multidimensional_fft([1] * 6, [2, 3], [16, 1], 17)
    with pytest.raises(ValueError):
        multidimensional_fft([1] * 4, [2, 4], [16, 13], 17)
    with pytest.raises(ValueError):
        multidimensional_fft([1] * 8, [2, 4], [16], 17)


def test_random_mod() -> None:
    rng = random.Random(1977)
    for _ in range(150):
        p, g = PRIMES[rng.randrange(len(PRIMES))]
        shape = rng.choice(SHAPES)
        roots = mod_roots(shape, p, g)
        x = [rng.randrange(p) for _ in range(prod(shape))]
        y = list(x)
        multidimensional_fft(y, shape, roots, p)
        assert y == naive(x, shape, roots, p)
        assert inverse(y, shape, roots, p) == x


def test_random_complex() -> None:
    rng = random.Random(1984)
    for _ in range(100):
        shape = rng.choice(SHAPES)
        roots = c_roots(shape)
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(prod(shape))]
        y = list(x)
        multidimensional_fft(y, shape, roots)
        assert close(y, naive(x, shape, roots))
        assert close(inverse(y, shape, roots), x)


def test_separable_and_larger() -> None:
    # The DFT of an outer product is the outer product of the 1D DFTs.
    p, g = 998244353, 3
    rng = random.Random(5)
    shape = [16, 32]
    roots = mod_roots(shape, p, g)
    u = [rng.randrange(p) for _ in range(16)]
    v = [rng.randrange(p) for _ in range(32)]
    x = [a * b % p for a in u for b in v]
    multidimensional_fft(x, shape, roots, p)
    fu = [sum(u[j] * pow(roots[0], j * k, p) for j in range(16)) % p for k in range(16)]
    fv = [sum(v[j] * pow(roots[1], j * k, p) for j in range(32)) % p for k in range(32)]
    assert x == [a * b % p for a in fu for b in fv]
