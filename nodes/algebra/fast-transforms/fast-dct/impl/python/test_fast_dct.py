# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-dct/. The authors are listed in prov/EWEX4W.jsonl.

import cmath
import math
import random

import pytest

from fast_dct import _fft, fast_dct, inverse_fast_dct


def naive_dct(x: list[float]) -> list[float]:
    n = len(x)
    return [
        sum(x[j] * math.cos(math.pi * (2 * j + 1) * k / (2 * n)) for j in range(n))
        for k in range(n)
    ]


def naive_dft(x: list[complex]) -> list[complex]:
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def close(a: list, b: list, scale: float) -> bool:
    n = max(len(a), 1)
    tol = 1e-12 * n * max(n.bit_length(), 1) * max(scale, 1.0)
    return len(a) == len(b) and all(abs(u - v) <= tol for u, v in zip(a, b))


def test_examples() -> None:
    c, s = math.cos(math.pi / 8), math.sin(math.pi / 8)
    assert close(fast_dct([1, 2, 3, 4]), [10, -3 * c - s, 0, -3 * s + c], 4)
    assert all(abs(u - v) < 1e-4 for u, v in zip(fast_dct([1, 2, 3, 4]), [10, -3.1543, 0, -0.2242]))
    out = fast_dct([1, 2, 3, 4, 5, 6, 7, 8])
    assert abs(out[0] - 36) < 1e-12
    assert all(abs(out[k]) < 1e-12 for k in (2, 4, 6))
    assert close(out, naive_dct([1, 2, 3, 4, 5, 6, 7, 8]), 8)


def test_internal_fft_against_naive_dft() -> None:
    rng = random.Random(4)
    for t in range(0, 7):
        n = 1 << t
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        y = list(x)
        _fft(y)
        assert close(y, naive_dft(x), n)
        _fft(y, inverse=True)
        assert close(y, x, 1)


def test_edges() -> None:
    assert fast_dct([2.5]) == [2.5]
    assert inverse_fast_dct([2.5]) == [2.5]
    assert close(fast_dct([1, 1]), [2, 0], 2)
    assert close(fast_dct([1, -1]), [0, math.sqrt(2)], 2)
    for t in range(0, 7):
        n = 1 << t
        assert close(fast_dct([0.0] * n), [0.0] * n, 1)
        assert close(fast_dct([3.0] * n), [3.0 * n] + [0.0] * (n - 1), 3 * n)
        for pos in (0, n - 1):
            imp = [0.0] * n
            imp[pos] = 1.0
            assert close(fast_dct(imp), naive_dct(imp), 1)


def test_not_power_of_two() -> None:
    for n in (0, 3, 6, 10):
        with pytest.raises(ValueError):
            fast_dct([1.0] * n)
        with pytest.raises(ValueError):
            inverse_fast_dct([1.0] * n)


def test_random_against_naive() -> None:
    rng = random.Random(1974)
    for _ in range(600):
        n = 1 << rng.randint(0, 6)
        scale = rng.choice([1.0, 1e3])
        x = [rng.uniform(-scale, scale) for _ in range(n)]
        out = fast_dct(x)
        assert close(out, naive_dct(x), scale * n)
        assert close(inverse_fast_dct(out), x, scale)


def test_inverse_of_naive() -> None:
    rng = random.Random(1980)
    for _ in range(100):
        n = 1 << rng.randint(1, 6)
        x = [rng.uniform(-1, 1) for _ in range(n)]
        assert close(inverse_fast_dct(naive_dct(x)), x, n)
