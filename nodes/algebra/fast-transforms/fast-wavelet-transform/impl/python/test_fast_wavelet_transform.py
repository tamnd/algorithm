# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-wavelet-transform/. The authors are listed in prov/H8RGV6.jsonl.

import math
import random

import pytest

from fast_wavelet_transform import DAUBECHIES4, HAAR, fwt, inverse_fwt

S2 = math.sqrt(2.0)
FILTERS = [HAAR, DAUBECHIES4]


def level_matrix(m: int, h: list[float]) -> list[list[float]]:
    """The m x m one-level analysis matrix, built from its definition."""
    big_l = len(h)
    g = [(-1) ** l * h[big_l - 1 - l] for l in range(big_l)]
    w = [[0.0] * m for _ in range(m)]
    for i in range(m // 2):
        for l in range(big_l):
            w[i][(2 * i + l) % m] += h[l]
            w[m // 2 + i][(2 * i + l) % m] += g[l]
    return w


def naive_fwt(x: list[float], h: list[float], levels: int) -> list[float]:
    """O(n^2) oracle: multiply the leading block by the dense level matrix."""
    y = [float(v) for v in x]
    m = len(x)
    for _ in range(levels):
        w = level_matrix(m, h)
        head = [sum(w[r][c] * y[c] for c in range(m)) for r in range(m)]
        y[0:m] = head
        m //= 2
    return y


def close(a: list[float], b: list[float], scale: float) -> bool:
    n = max(len(a), 1)
    tol = 1e-13 * n * max(scale, 1.0)
    return len(a) == len(b) and all(abs(u - v) <= tol for u, v in zip(a, b))


def norm(v: list[float]) -> float:
    return math.sqrt(sum(t * t for t in v))


def test_filters_are_orthonormal() -> None:
    for h in FILTERS:
        big_l = len(h)
        for s in range(big_l // 2):
            dot = sum(h[l] * h[l + 2 * s] for l in range(big_l - 2 * s))
            assert abs(dot - (1.0 if s == 0 else 0.0)) < 1e-15


def test_haar_example() -> None:
    x = [4, 6, 10, 12, 8, 6, 5, 5]
    want = [14 * S2, 2 * S2, -6, 2, -S2, -S2, S2, 0]
    assert close(fwt(x, HAAR, 3), want, 30)
    assert close(inverse_fwt(want, HAAR, 3), [float(v) for v in x], 30)
    assert close(fwt(x, HAAR, 1), [10 / S2, 22 / S2, 14 / S2, 10 / S2, -S2, -S2, S2, 0], 30)


def test_daubechies4_kills_linear_data() -> None:
    x = list(range(8))
    y = fwt(x, DAUBECHIES4, 1)
    assert all(abs(t) < 1e-12 for t in y[4:7])
    assert abs(y[7]) > 1


def test_edge_cases() -> None:
    for h in FILTERS:
        assert fwt([3.5], h, 0) == [3.5]
        assert inverse_fwt([3.5], h, 0) == [3.5]
        assert close(fwt([1, 3], h, 1), naive_fwt([1, 3], h, 1), 4)
        assert close(inverse_fwt(fwt([1, 3], h, 1), h, 1), [1.0, 3.0], 4)
        for n in (2, 4, 8, 16, 32):
            j = n.bit_length() - 1
            assert fwt([0.0] * n, h, j) == [0.0] * n
            const = fwt([2.0] * n, h, j)
            assert abs(const[0] - 2.0 * math.sqrt(n)) < 1e-12
            assert all(abs(t) < 1e-12 for t in const[1:])
            for p in range(n):
                imp = [0.0] * n
                imp[p] = 1.0
                y = fwt(imp, h, j)
                assert close(y, naive_fwt(imp, h, j), 1)
                assert abs(norm(y) - 1.0) < 1e-12
                assert close(inverse_fwt(y, h, j), imp, 1)


def test_haar_basis_inner_products() -> None:
    n = 16
    rng = random.Random(7)
    x = [rng.uniform(-1, 1) for _ in range(n)]
    y = fwt(x, HAAR, 4)
    assert abs(y[0] - sum(x) / 4) < 1e-12
    for level in range(1, 5):
        width = 1 << level
        start = n >> level
        for i in range(n >> level):
            seg = x[i * width:(i + 1) * width]
            want = (sum(seg[: width // 2]) - sum(seg[width // 2:])) / math.sqrt(width)
            assert abs(y[start + i] - want) < 1e-12


def test_random_against_oracle() -> None:
    rng = random.Random(20261107)
    cases = 0
    for _ in range(300):
        h = rng.choice(FILTERS)
        m0 = rng.choice([1, 1, 2, 3, 5])
        levels = rng.randint(0, 5)
        n = m0 << levels
        if n > 96:
            continue
        x = [rng.uniform(-100, 100) for _ in range(n)]
        y = fwt(x, h, levels)
        assert close(y, naive_fwt(x, h, levels), 100)
        assert close(inverse_fwt(y, h, levels), x, 100)
        assert abs(norm(y) - norm(x)) <= 1e-12 * max(1, n) * max(norm(x), 1)
        cases += 1
    for _ in range(400):
        h = rng.choice(FILTERS)
        levels = rng.randint(0, 7)
        n = rng.choice([1, 2, 3]) << levels
        x = [rng.uniform(-1, 1) for _ in range(n)]
        y = fwt(x, h, levels)
        assert close(inverse_fwt(y, h, levels), x, 1)
        assert abs(norm(y) - norm(x)) <= 1e-13 * n * max(norm(x), 1)
        cases += 1
    assert cases >= 500


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        fwt([1.0, 2.0, 3.0], HAAR, 1)
    with pytest.raises(ValueError):
        fwt([1.0, 2.0], [1.0, 2.0, 3.0], 1)
