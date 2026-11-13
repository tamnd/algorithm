# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lifting-scheme/. The authors are listed in prov/8YF7JV.jsonl.

import math
import random
from fractions import Fraction

import pytest

from lifting_scheme import (
    HAAR_STEPS,
    LEGALL_53_OFFSETS,
    LEGALL_53_STEPS,
    daubechies4_steps,
    lift_forward,
    lift_forward_int,
    lift_inverse,
    lift_inverse_int,
    multilevel,
)


def conv_level(x, ht, gt):
    """Reference: the convolution (filter bank) form of one level, s[i] = sum_l ht[l] x[2i + l]."""
    m = len(x)
    s = [sum((c * x[(2 * i + l) % m] for l, c in ht.items()), 0) for i in range(m // 2)]
    d = [sum((c * x[(2 * i + l) % m] for l, c in gt.items()), 0) for i in range(m // 2)]
    return s, d


F = Fraction
HAAR_CONV = ({0: F(1, 2), 1: F(1, 2)}, {0: F(-1), 1: F(1)})
LEGALL_CONV = (
    {-2: F(-1, 8), -1: F(1, 4), 0: F(3, 4), 1: F(1, 4), 2: F(-1, 8)},
    {0: F(-1, 2), 1: F(1), 2: F(-1, 2)},
)


def test_example() -> None:
    s, d = lift_forward([1, 2, 3, 4, 5, 6, 7, 8], LEGALL_53_STEPS)
    assert d == [0, 0, 0, 4]
    assert s == [2, 3, 5, 8]
    s, d = lift_forward_int([4, 6, 10, 12, 8, 6, 5, 5], LEGALL_53_STEPS, LEGALL_53_OFFSETS)
    assert d == [-1, 3, 0, 1]
    assert s == [4, 11, 9, 5]
    s, d = lift_forward([4, 6, 10, 12, 8, 6, 5, 5], LEGALL_53_STEPS)
    assert d == [-1, 3, F(-1, 2), F(1, 2)]
    assert s == [F(31, 8), F(21, 2), F(69, 8), 5]


@pytest.mark.parametrize("steps,conv", [(HAAR_STEPS, HAAR_CONV), (LEGALL_53_STEPS, LEGALL_CONV)])
def test_same_as_convolution_exact(steps, conv) -> None:
    rng = random.Random(2)
    for n in (2, 4, 6, 8, 16, 30):
        for _ in range(20):
            x = [F(rng.randint(-99, 99), rng.randint(1, 7)) for _ in range(n)]
            assert lift_forward(x, steps) == conv_level(x, *conv)
            s, d = lift_forward(x, steps)
            assert lift_inverse(s, d, steps) == x


def test_daubechies4_same_as_convolution() -> None:
    r3, r2 = math.sqrt(3), math.sqrt(2)
    h = [(1 + r3) / (4 * r2), (3 + r3) / (4 * r2), (3 - r3) / (4 * r2), (1 - r3) / (4 * r2)]
    lo = {l: h[l] for l in range(4)}
    # The lifted high-pass is the usual g_l = (-1)^l h_(3-l), negated and shifted by one output.
    hi = {-2: -h[3], -1: h[2], 0: -h[1], 1: h[0]}
    steps, scale, inv = daubechies4_steps()
    rng = random.Random(4)
    for n in (4, 8, 16, 64):
        x = [rng.uniform(-1, 1) for _ in range(n)]
        s, d = lift_forward(x, steps, scale)
        cs, cd = conv_level(x, lo, hi)
        assert max(abs(p - q) for p, q in zip(s + d, cs + cd)) < 1e-12
        assert abs(sum(v * v for v in s + d) - sum(v * v for v in x)) < 1e-12 * n
        back = lift_inverse(s, d, steps, inv)
        assert max(abs(p - q) for p, q in zip(back, x)) < 1e-12


def jpeg2000_53(x):
    """Reference: the reversible 5/3 formulas written out directly (periodic indices)."""
    h = len(x) // 2
    e, o = x[0::2], x[1::2]
    d = [o[i] - (e[i] + e[(i + 1) % h]) // 2 for i in range(h)]
    s = [e[i] + (d[i - 1] + d[i] + 2) // 4 for i in range(h)]
    return s, d


def test_integer_to_integer() -> None:
    rng = random.Random(9)
    for n in (2, 4, 8, 10, 64):
        for _ in range(200):
            x = [rng.randint(-1000, 1000) for _ in range(n)]
            s, d = lift_forward_int(x, LEGALL_53_STEPS, LEGALL_53_OFFSETS)
            assert all(isinstance(v, int) for v in s + d)
            assert (s, d) == jpeg2000_53(x)
            assert lift_inverse_int(s, d, LEGALL_53_STEPS, LEGALL_53_OFFSETS) == x
            hs, hd = lift_forward_int(x, HAAR_STEPS, [F(0), F(0)])
            assert hd == [x[2 * i + 1] - x[2 * i] for i in range(n // 2)]
            assert lift_inverse_int(hs, hd, HAAR_STEPS, [F(0), F(0)]) == x


def test_integer_close_to_exact() -> None:
    # The rounded transform stays within a fixed distance of the exact one.
    rng = random.Random(13)
    for _ in range(200):
        x = [rng.randint(0, 255) for _ in range(16)]
        si, di = lift_forward_int(x, LEGALL_53_STEPS, LEGALL_53_OFFSETS)
        se, de = lift_forward(x, LEGALL_53_STEPS)
        assert max(abs(a - b) for a, b in zip(di, de)) <= F(1, 2)
        assert max(abs(a - b) for a, b in zip(si, se)) <= F(3, 4)


def test_multilevel_mean() -> None:
    a, ds = multilevel([1, 2, 3, 4, 5, 6, 7, 8], LEGALL_53_STEPS, (1, 1), 3)
    assert a == [F(9, 2)] and ds[0] == [0, 0, 0, 4]


def test_odd_length() -> None:
    with pytest.raises(ValueError):
        lift_forward([1, 2, 3], HAAR_STEPS)
    with pytest.raises(ValueError):
        lift_forward_int([1, 2, 3], HAAR_STEPS, [F(0), F(0)])
