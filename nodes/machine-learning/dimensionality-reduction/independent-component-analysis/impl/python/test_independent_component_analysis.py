# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-component-analysis/. The authors are listed in prov/RPTZE3.jsonl.

import math
import random
from fractions import Fraction

import pytest

from independent_component_analysis import (
    amari_index,
    best_angle,
    contrast,
    ica_jacobi,
    kurtosis,
    whiten,
)


def laplace(rng: random.Random) -> float:
    u = rng.random() - 0.5
    return -math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u)) / math.sqrt(2.0)


def uniform(rng: random.Random) -> float:
    return rng.uniform(-math.sqrt(3.0), math.sqrt(3.0))


def mixtures(rng: random.Random, n: int, makers: list, a: list) -> tuple[list, list]:
    srcs = [[mk(rng) for mk in makers] for _ in range(n)]
    xs = [[sum(a[i][j] * s[j] for j in range(len(makers))) for i in range(len(a))] for s in srcs]
    return srcs, xs


def matmul(p: list, q: list) -> list:
    return [[sum(p[i][k] * q[k][j] for k in range(len(q))) for j in range(len(q[0]))] for i in range(len(p))]


def test_whitening_gives_identity_covariance() -> None:
    rng = random.Random(1)
    _, xs = mixtures(rng, 500, [uniform, laplace, uniform], [[1, 2, 0], [0.5, 1, 1], [2, 0, 1]])
    z, _, _ = whiten(xs)
    n = len(xs)
    for i in range(3):
        assert sum(z[i]) / n == pytest.approx(0.0, abs=1e-12)
        for j in range(3):
            assert sum(a * b for a, b in zip(z[i], z[j])) / n == pytest.approx(1.0 if i == j else 0.0, abs=1e-10)


def test_recovers_uniform_and_laplace_sources() -> None:
    rng = random.Random(2)
    a = [[1.0, 0.6], [0.4, 1.0]]
    srcs, xs = mixtures(rng, 4000, [uniform, laplace], a)
    unmix, ys, _ = ica_jacobi(xs)
    p = matmul(unmix, a)
    assert amari_index(p) < 0.05
    # Each estimate matches one source up to sign: |corr| close to 1.
    for i in range(2):
        cors = []
        for j in range(2):
            col = [s[j] for s in srcs]
            mu = sum(col) / len(col)
            sd = math.sqrt(sum((c - mu) ** 2 for c in col) / len(col))
            cors.append(abs(sum(y * (c - mu) for y, c in zip(ys[i], col)) / len(col) / sd))
        assert max(cors) > 0.99 and min(cors) < 0.1


def test_three_sources_and_monotone_contrast() -> None:
    rng = random.Random(3)
    a = [[1.0, 2.0, 0.5], [0.3, 1.0, 1.0], [1.5, 0.2, 1.0]]
    _, xs = mixtures(rng, 3000, [uniform, laplace, lambda r: r.choice([-1.0, 1.0])], a)
    unmix, _, history = ica_jacobi(xs)
    assert all(b >= a_ - 1e-9 for a_, b in zip(history, history[1:]))
    assert amari_index(matmul(unmix, a)) < 0.05


def test_best_angle_never_decreases_pair_contrast() -> None:
    rng = random.Random(4)
    for _ in range(5):
        _, xs = mixtures(rng, 400, [uniform, laplace], [[rng.uniform(-1, 1) for _ in range(2)] for _ in range(2)])
        z, _, _ = whiten(xs)
        t, f_new, f_old = best_angle(z[0], z[1])
        assert 0.0 <= t < math.pi / 2 + 1e-9
        assert f_new >= f_old
        c, s = math.cos(t), math.sin(t)
        y1 = [c * a + s * b for a, b in zip(z[0], z[1])]
        y2 = [-s * a + c * b for a, b in zip(z[0], z[1])]
        assert contrast([y1, y2]) == pytest.approx(f_new, rel=1e-9)


def test_kurtosis_is_additive_with_fourth_powers() -> None:
    # Exact check on a product distribution: s1 uniform on {-1, 1}, s2 uniform on {-2, 0, 0, 2}.
    s1 = [Fraction(-1), Fraction(1)]
    s2 = [Fraction(-2), Fraction(0), Fraction(0), Fraction(2)]

    def cum4(vals: list) -> Fraction:
        n = len(vals)
        m2 = sum(v * v for v in vals) / n
        m4 = sum(v ** 4 for v in vals) / n
        return m4 - 3 * m2 * m2

    k1, k2 = cum4(s1), cum4(s2)
    for a, b in [(Fraction(1), Fraction(1)), (Fraction(3, 5), Fraction(4, 5)), (Fraction(2), Fraction(-1, 3))]:
        mix = [a * u + b * v for u in s1 for v in s2]
        assert cum4(mix) == a ** 4 * k1 + b ** 4 * k2


def test_gaussian_kurtosis_is_near_zero_and_page_numbers() -> None:
    rng = random.Random(5)
    g = [rng.gauss(0, 1) for _ in range(40000)]
    assert abs(kurtosis(g)) < 0.1
    # Page example: unit-variance uniform has kurtosis -1.2 and Laplace has 3.
    # At 45 degrees each mixture has kurtosis (-1.2 + 3) / 4 = 0.45.
    k_u, k_l = -1.2, 3.0
    assert (k_u + k_l) / 4 == pytest.approx(0.45)
    assert 2 * 0.45 ** 2 == pytest.approx(0.405)
    assert k_u ** 2 + k_l ** 2 == pytest.approx(10.44)


def test_singular_covariance_raises() -> None:
    xs = [[float(i), 2.0 * i] for i in range(10)]
    with pytest.raises(ValueError):
        ica_jacobi(xs)
