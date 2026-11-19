# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rotary-position-embedding/. The authors are listed in prov/XBK70H.jsonl.

import cmath
import math
import random

import pytest

from rotary_position_embedding import rope, rope_half, rope_score


def rand_vec(rng, d):
    return [rng.gauss(0, 1) for _ in range(d)]


def complex_oracle(x, pos, base=10000.0):
    """Each pair as the complex number x[2i] + i x[2i+1], multiplied by exp(i pos theta_i)."""
    d = len(x)
    out = []
    for i in range(d // 2):
        z = complex(x[2 * i], x[2 * i + 1]) * cmath.exp(1j * pos * base ** (-2 * i / d))
        out += [z.real, z.imag]
    return out


def close(u, v, tol=1e-9):
    return all(abs(a - b) <= tol * (1 + abs(b)) for a, b in zip(u, v))


def test_worked_example():
    assert round(rope_score([1.0, 0.0], 3, [1.0, 0.0], 1), 6) == -0.416147
    assert round(math.cos(2), 6) == -0.416147
    assert close(rope([1.0, 0.0], 3), [math.cos(3), math.sin(3)])


@pytest.mark.parametrize("seed", range(10))
def test_against_complex_oracle(seed):
    rng = random.Random(seed)
    d = 2 * rng.randint(1, 12)
    x = rand_vec(rng, d)
    pos = rng.randint(-100, 3000)
    assert close(rope(x, pos), complex_oracle(x, pos))


@pytest.mark.parametrize("seed", range(15))
def test_score_depends_only_on_offset(seed):
    rng = random.Random(100 + seed)
    d = 2 * rng.randint(1, 10)
    q, k = rand_vec(rng, d), rand_vec(rng, d)
    m, n = rng.randint(0, 500), rng.randint(0, 500)
    t = rng.randint(-200, 200)
    s = rope_score(q, m, k, n)
    assert rope_score(q, m + t, k, n + t) == pytest.approx(s, abs=1e-9)
    # and it equals q . R_(n - m) k
    assert math.fsum(a * b for a, b in zip(q, rope(k, n - m))) == pytest.approx(s, abs=1e-9)


@pytest.mark.parametrize("seed", range(5))
def test_norm_is_kept_and_position_zero_is_identity(seed):
    rng = random.Random(200 + seed)
    x = rand_vec(rng, 8)
    y = rope(x, rng.randint(1, 1000))
    assert math.hypot(*y) == pytest.approx(math.hypot(*x))
    assert rope(x, 0) == x
    # rotations compose: R_a R_b = R_(a + b)
    a, b = rng.randint(0, 50), rng.randint(0, 50)
    assert close(rope(rope(x, a), b), rope(x, a + b))


@pytest.mark.parametrize("seed", range(5))
def test_half_layout_is_a_permutation(seed):
    rng = random.Random(300 + seed)
    d = 2 * rng.randint(1, 8)
    h = d // 2
    x = rand_vec(rng, d)
    pos = rng.randint(0, 500)
    # interleave the halves: (x_0, x_h, x_1, x_(h+1), ...)
    perm = [v for i in range(h) for v in (i, i + h)]
    inter = rope([x[p] for p in perm], pos)
    half = rope_half(x, pos)
    assert close([half[p] for p in perm], inter)
    # mixing the layouts is a different function
    if d >= 4:
        assert not close(rope(x, pos + 1), rope_half(x, pos + 1), 1e-6)


def test_errors():
    with pytest.raises(ValueError):
        rope([1.0, 2.0, 3.0], 1)
    with pytest.raises(ValueError):
        rope_score([1.0, 0.0], 0, [1.0, 0.0, 0.0, 0.0], 0)
    with pytest.raises(ValueError):
        rope([1.0, 0.0], 1, base=0.5)
