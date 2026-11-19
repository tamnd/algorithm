# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sinusoidal-positional-encoding/. The authors are listed in prov/D6ZPH5.jsonl.

import cmath
import math
import random

import pytest

from sinusoidal_positional_encoding import encoding_matrix, frequencies, positional_encoding, shift_matrix


def matvec(m, v):
    return [sum(a * b for a, b in zip(row, v)) for row in m]


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def test_worked_example():
    assert [round(x, 6) for x in positional_encoding(1, 4)] == [0.841471, 0.540302, 0.01, 0.99995]
    assert [round(x, 6) for x in positional_encoding(2, 4)] == [0.909297, -0.416147, 0.019999, 0.9998]
    assert positional_encoding(0, 4) == [0.0, 1.0, 0.0, 1.0]
    assert round(dot(positional_encoding(1, 4), positional_encoding(2, 4)), 6) == 1.540252


@pytest.mark.parametrize("seed", range(10))
def test_against_complex_exponential(seed):
    rng = random.Random(seed)
    d = 2 * rng.randint(1, 16)
    pos = rng.randint(0, 5000)
    pe = positional_encoding(pos, d)
    for i in range(d // 2):
        z = cmath.exp(1j * pos / 10000 ** (2 * i / d))
        assert pe[2 * i] == pytest.approx(z.imag, abs=1e-9)
        assert pe[2 * i + 1] == pytest.approx(z.real, abs=1e-9)


@pytest.mark.parametrize("seed", range(10))
def test_shift_is_linear_and_independent_of_position(seed):
    rng = random.Random(100 + seed)
    d = 2 * rng.randint(1, 10)
    k = rng.randint(-50, 50)
    mk = shift_matrix(k, d)
    for _ in range(5):
        pos = rng.randint(0, 1000)
        got = matvec(mk, positional_encoding(pos, d))
        want = positional_encoding(pos + k, d)
        assert all(abs(a - b) < 1e-9 for a, b in zip(got, want))


@pytest.mark.parametrize("seed", range(10))
def test_dot_product_depends_only_on_offset(seed):
    rng = random.Random(200 + seed)
    d = 2 * rng.randint(1, 10)
    k = rng.randint(0, 40)
    want = sum(math.cos(k * w) for w in frequencies(d))
    for _ in range(5):
        p = rng.randint(0, 2000)
        assert dot(positional_encoding(p, d), positional_encoding(p + k, d)) == pytest.approx(want, abs=1e-9)


def test_norm_and_frequencies():
    d = 16
    for p in (0, 3, 999):
        assert math.sqrt(dot(positional_encoding(p, d), positional_encoding(p, d))) == pytest.approx(math.sqrt(d / 2))
    w = frequencies(d)
    assert w[0] == 1.0
    ratios = [w[i + 1] / w[i] for i in range(len(w) - 1)]
    assert all(r == pytest.approx(10000 ** (-2 / d)) for r in ratios)
    assert 2 * math.pi / w[-1] < 10000 * 2 * math.pi


def test_matrix_and_errors():
    m = encoding_matrix(3, 4, start=1)
    assert m[0] == positional_encoding(1, 4)
    assert len(m) == 3
    with pytest.raises(ValueError):
        positional_encoding(1, 3)
    with pytest.raises(ValueError):
        positional_encoding(1, 4, base=1.0)
