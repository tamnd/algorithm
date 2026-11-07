# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-hartley-transform/. The authors are listed in prov/JPR6KM.jsonl.

import cmath
import math
import random

import pytest

from fast_hartley_transform import dft_from_dht, fht, inverse_fht, real_cyclic_convolution


def naive_dht(x: list[float]) -> list[float]:
    n = len(x)
    return [
        sum(x[j] * (math.cos(2 * math.pi * j * k / n) + math.sin(2 * math.pi * j * k / n)) for j in range(n))
        for k in range(n)
    ]


def naive_dft(x: list[float]) -> list[complex]:
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def close(a: list, b: list, scale: float) -> bool:
    n = max(len(a), 1)
    tol = 1e-13 * n * max(n.bit_length(), 1) * max(scale, 1.0)
    return len(a) == len(b) and all(abs(u - v) <= tol for u, v in zip(a, b))


def transformed(x: list[float]) -> list[float]:
    y = [float(v) for v in x]
    fht(y)
    return y


def test_examples() -> None:
    assert close(transformed([1, 2, 3, 4]), [10, -4, -2, 0], 4)
    r = 4 * math.sqrt(2)
    assert close(transformed([1, 2, 3, 4, 5, 6, 7, 8]), [36, -8 - r, -8, -r, -4, -8 + r, 0, r], 8)
    assert close(dft_from_dht([10, -4, -2, 0]), [10, -2 + 2j, -2, -2 - 2j], 4)
    assert close(real_cyclic_convolution([1, 2, 3, 4], [1, 1, 0, 0]), [5, 3, 5, 7], 10)


def test_edge_cases() -> None:
    assert transformed([2.5]) == [2.5]
    assert transformed([3, 5]) == [8, -2]
    for n in (1, 2, 4, 8, 16, 32, 64):
        assert transformed([0.0] * n) == [0.0] * n
        assert close(transformed([1.0] + [0.0] * (n - 1)), [1.0] * n, 1)
        c = transformed([2.0] * n)
        assert close(c, [2.0 * n] + [0.0] * (n - 1), 2 * n)
        for p in range(n):
            imp = [0.0] * n
            imp[p] = 1.0
            assert close(transformed(imp), naive_dht(imp), 1)


def test_random_against_oracle() -> None:
    rng = random.Random(1984)
    for case in range(600):
        n = 1 << rng.randint(0, 6)
        x = [rng.uniform(-10, 10) for _ in range(n)]
        scale = 10 * math.sqrt(n)
        y = transformed(x)
        assert close(y, naive_dht(x), scale)
        assert close(dft_from_dht(y), naive_dft(x), scale)
        back = list(y)
        inverse_fht(back)
        assert close(back, x, 10)
        if case % 3 == 0:
            b = [rng.uniform(-10, 10) for _ in range(n)]
            want = [sum(x[i] * b[(k - i) % n] for i in range(n)) for k in range(n)]
            assert close(real_cyclic_convolution(x, b), want, 100 * n)


def test_involution_large() -> None:
    rng = random.Random(7)
    for n in (256, 1024, 4096):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        y = transformed(x)
        assert abs(sum(v * v for v in y) - n * sum(v * v for v in x)) < 1e-9 * n * n
        inverse_fht(y)
        assert close(y, x, 1)


def test_bad_length() -> None:
    with pytest.raises(ValueError):
        fht([1.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        real_cyclic_convolution([1.0, 2.0], [1.0])
