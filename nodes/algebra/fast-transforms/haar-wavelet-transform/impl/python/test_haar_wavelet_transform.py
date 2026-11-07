# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/haar-wavelet-transform/. The authors are listed in prov/5B1Q93.jsonl.

import math
import random
from fractions import Fraction

import pytest

from haar_wavelet_transform import AVERAGES, ORTHONORMAL, haar, inverse_haar


def direct_averages(x: list) -> list:
    """The transform by averages from its closed form, in O(n^2) time."""
    n = len(x)
    y = [Fraction(sum(x), n)]
    j = 0
    while (1 << j) < n:
        size = n >> j
        for k in range(1 << j):
            left = x[k * size : k * size + size // 2]
            right = x[k * size + size // 2 : (k + 1) * size]
            y.append((Fraction(sum(left), size // 2) - Fraction(sum(right), size // 2)) / 2)
        j += 1
    return y


def direct_orthonormal(x: list[float]) -> list[float]:
    """Inner products with the orthonormal Haar basis vectors, in O(n^2) time."""
    n = len(x)
    rows = [[1 / math.sqrt(n)] * n]
    j = 0
    while (1 << j) < n:
        size = n >> j
        for k in range(1 << j):
            row = [0.0] * n
            for i in range(k * size, (k + 1) * size):
                row[i] = (1 if i < k * size + size // 2 else -1) / math.sqrt(size)
            rows.append(row)
        j += 1
    return [sum(r[i] * x[i] for i in range(n)) for r in rows]


def close(a: list[float], b: list[float], norm: float) -> bool:
    n = len(a)
    # the proved bound of the fast form is about 3 lg(n) u; the direct sums add about n u
    tol = 4 * (n + n.bit_length()) * 2.0**-52 * max(norm, 1.0)
    return math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b))) <= tol


def test_example() -> None:
    x = [Fraction(v) for v in (4, 6, 10, 12, 8, 6, 5, 5)]
    haar(x, AVERAGES)
    assert x == [7, 1, -3, 1, -1, -1, 1, 0]
    y = [4.0, 6.0, 10.0, 12.0, 8.0, 6.0, 5.0, 5.0]
    haar(y, ORTHONORMAL)
    s = math.sqrt(2)
    assert close(y, [14 * s, 2 * s, -6, 2, -s, -s, s, 0], 30)
    assert abs(sum(v * v for v in y) - 446) < 1e-9


def test_edges() -> None:
    for n in (1, 2, 4, 8, 16):
        zeros = [Fraction(0)] * n
        haar(zeros, AVERAGES)
        assert zeros == [0] * n
        const = [Fraction(5)] * n
        haar(const, AVERAGES)
        assert const == [5] + [0] * (n - 1)
        for pos in range(n):
            imp = [Fraction(0)] * n
            imp[pos] = Fraction(1)
            expect = direct_averages(imp)
            haar(imp, AVERAGES)
            assert imp == expect
            back = list(imp)
            inverse_haar(back, AVERAGES)
            assert back == [1 if i == pos else 0 for i in range(n)]
    one = [Fraction(3)]
    haar(one, AVERAGES)
    assert one == [3]
    two = [Fraction(3), Fraction(1)]
    haar(two, AVERAGES)
    assert two == [2, 1]


def test_not_power_of_two() -> None:
    for n in (0, 3, 6, 12):
        with pytest.raises(ValueError):
            haar([Fraction(1)] * n, AVERAGES)
        with pytest.raises(ValueError):
            inverse_haar([1.0] * n, ORTHONORMAL)


def test_random_exact() -> None:
    rng = random.Random(1910)
    for _ in range(400):
        n = 1 << rng.randint(0, 6)
        x = [Fraction(rng.randint(-100, 100)) for _ in range(n)]
        y = list(x)
        haar(y, AVERAGES)
        assert y == direct_averages(x)
        inverse_haar(y, AVERAGES)
        assert y == x


def test_random_float() -> None:
    rng = random.Random(3711)
    for _ in range(200):
        n = 1 << rng.randint(0, 7)
        x = [rng.uniform(-1e3, 1e3) for _ in range(n)]
        norm = math.sqrt(sum(v * v for v in x))
        y = list(x)
        haar(y, ORTHONORMAL)
        assert close(y, direct_orthonormal(x), norm)
        assert abs(math.sqrt(sum(v * v for v in y)) - norm) <= 1e-12 * max(norm, 1.0) * n
        inverse_haar(y, ORTHONORMAL)
        assert close(y, x, norm)
