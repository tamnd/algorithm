# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chinese-remainder-theorem-fft/. The authors are listed in prov/XHJRTQ.jsonl.

import cmath
import math
import random

import pytest

from chinese_remainder_theorem_fft import good_thomas, inverse_good_thomas

P = 998244353
PRIMES = {17: 3, 97: 5, P: 3}


def naive_dft(x: list, w, p: int | None = None) -> list:
    n = len(x)
    if p is not None:
        table = [pow(w, m, p) for m in range(n)]
        return [sum(x[j] * table[(j * k) % n] for j in range(n)) % p for k in range(n)]
    return [sum(x[j] * w ** ((j * k) % n) for j in range(n)) for k in range(n)]


def root(n: int, p: int) -> int:
    assert (p - 1) % n == 0
    return pow(PRIMES[p], (p - 1) // n, p)


def close(a: list, b: list, scale: float) -> bool:
    n = max(len(a), 1)
    tol = 1e-12 * n * max(scale, 1.0)
    return len(a) == len(b) and all(abs(u - v) <= tol for u, v in zip(a, b))


def test_worked_example() -> None:
    x = [1, 2, 3, 4, 5, 6]
    assert good_thomas(x, [2, 3], 3, 7) == [0, 3, 6, 4, 2, 5] == naive_dft(x, 3, 7)
    assert inverse_good_thomas([0, 3, 6, 4, 2, 5], [2, 3], 3, 7) == x


MOD_SHAPES = {
    17: [[16], [1, 16], [2], [1], [4, 1]],
    97: [[3, 2], [3, 4], [3, 8], [3, 32], [32, 3], [1, 3]],
    P: [[7, 8], [8, 7], [7, 16], [17, 8], [7, 17], [4, 7, 17], [7, 17, 2], [1, 1, 7]],
}


def test_modular_against_oracle() -> None:
    rng = random.Random(1958)
    cases = 0
    for p, shapes in MOD_SHAPES.items():
        for shape in shapes:
            n = math.prod(shape)
            w = root(n, p)
            for _ in range(40 if n <= 64 else 5):
                x = [rng.randrange(p) for _ in range(n)]
                y = good_thomas(x, shape, w, p)
                assert y == naive_dft(x, w, p)
                assert inverse_good_thomas(y, shape, w, p) == x
                cases += 1
    assert cases >= 450


COMPLEX_SHAPES = [[2, 3], [3, 2], [2, 5], [3, 4], [4, 3], [3, 5], [5, 7], [2, 3, 5], [3, 5, 7], [4, 9], [5, 8, 9], [11], [2, 3, 5, 7]]


def test_complex_against_oracle() -> None:
    rng = random.Random(1963)
    cases = 0
    for shape in COMPLEX_SHAPES:
        n = math.prod(shape)
        w = cmath.exp(-2j * math.pi / n)
        for _ in range(20 if n <= 40 else 3):
            x = [complex(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(n)]
            y = good_thomas(x, shape, w)
            scale = 5 * math.sqrt(n) * len(shape)
            assert close(y, naive_dft(x, w), scale)
            assert close(inverse_good_thomas(y, shape, w), x, scale)
            cases += 1
    assert cases >= 150


def test_edge_cases() -> None:
    assert good_thomas([5], [1], 1, 17) == [5]
    assert good_thomas([3, 4], [2], 16, 17) == [7, 16]
    for p, shape in ((97, [3, 4]), (P, [7, 8]), (17, [16])):
        n = math.prod(shape)
        w = root(n, p)
        assert good_thomas([0] * n, shape, w, p) == [0] * n
        assert good_thomas([1] + [0] * (n - 1), shape, w, p) == [1] * n
        assert good_thomas([2] * n, shape, w, p) == [2 * n % p] + [0] * (n - 1)
        for s in range(n):
            imp = [0] * n
            imp[s] = 1
            assert good_thomas(imp, shape, w, p) == naive_dft(imp, w, p)
    w = cmath.exp(-2j * math.pi / 15)
    assert close(good_thomas([1.0] * 15, [3, 5], w), [15.0] + [0.0] * 14, 15)


def test_index_maps_are_bijections() -> None:
    for shape in ([2, 3], [3, 5, 7], [4, 9], [5, 8, 9]):
        n = math.prod(shape)
        big = [n // m for m in shape]
        e = [pow(b, -1, m) for b, m in zip(big, shape)]
        ins = set()
        outs = set()
        for flat in range(n):
            digits, rest = [], flat
            for m in reversed(shape):
                digits.append(rest % m)
                rest //= m
            digits.reverse()
            ins.add(sum(b * d for b, d in zip(big, digits)) % n)
            k = sum(b * f * d for b, f, d in zip(big, e, digits)) % n
            assert all(k % m == d for m, d in zip(shape, digits))
            outs.add(k)
        assert ins == outs == set(range(n))


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        good_thomas([1, 2, 3, 4], [2, 2], 13, 17)
    with pytest.raises(ValueError):
        good_thomas([1, 2, 3], [2, 3], 1, 17)
