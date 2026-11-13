# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overlap-add-method/. The authors are listed in prov/H1GGYR.jsonl.

import cmath
import random
from fractions import Fraction

import pytest

from overlap_add_method import fft, overlap_add, overlap_add_exact


def direct(x, h):
    """The defining sum y[n] = sum_k h[k] x[n - k], exact on Fractions."""
    y = [Fraction(0)] * (len(x) + len(h) - 1)
    for i, xi in enumerate(x):
        for k, hk in enumerate(h):
            y[i + k] += xi * hk
    return y


def rand_seq(rng, n):
    return [Fraction(rng.randint(-20, 20), rng.randint(1, 6)) for _ in range(n)]


def test_example() -> None:
    x = [1, 2, 3, 4, 5, 6, 7]
    h = [1, 1, 1]
    assert overlap_add_exact(x, h, 4) == [1, 3, 6, 9, 12, 15, 18, 13, 7]


def test_exact_equals_direct_for_many_block_sizes() -> None:
    rng = random.Random(7301)
    for _ in range(60):
        length, m = rng.randint(1, 40), rng.randint(1, 9)
        x, h = rand_seq(rng, length), rand_seq(rng, m)
        want = direct(x, h)
        for n in range(m, m + 8):
            assert overlap_add_exact(x, h, n) == want


def test_fft_matches_direct_dft() -> None:
    rng = random.Random(7302)
    for n in (1, 2, 4, 8, 16):
        a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        want = [sum(a[t] * cmath.exp(-2j * cmath.pi * k * t / n) for t in range(n)) for k in range(n)]
        for p, q in zip(fft(a), want):
            assert abs(p - q) < 1e-12
    with pytest.raises(ValueError):
        fft([1, 2, 3])


def test_float_fft_version_within_tolerance() -> None:
    # tolerance: 1e-9 * (1 + max|x| * sum|h|); the largest error on these inputs is about 1.1e-12
    rng = random.Random(7303)
    for _ in range(60):
        length, m = rng.randint(1, 200), rng.randint(1, 33)
        x = [rng.randint(-9, 9) for _ in range(length)]
        h = [rng.randint(-9, 9) for _ in range(m)]
        want = direct([Fraction(v) for v in x], [Fraction(v) for v in h])
        tol = 1e-9 * (1 + max(map(abs, x)) * sum(map(abs, h)))
        for n in (16, 32, 64, 128):
            if n < m:
                continue
            got = overlap_add(x, h, n)
            assert len(got) == len(want)
            assert max(abs(g - float(w)) for g, w in zip(got, want)) <= tol


def test_complex_inputs() -> None:
    x = [1 + 1j, 2, -1j, 3]
    h = [1j, 1]
    got = overlap_add(x, h, 4)
    want = [(1 + 1j) * 1j, (1 + 1j) + 2j, 2 + 1, -1j + 3j, 3]
    for g, w in zip(got, want):
        assert abs(g - w) < 1e-12


def test_edges() -> None:
    assert overlap_add_exact([], [1, 2], 4) == []
    assert overlap_add_exact([5], [2], 1) == [10]
    # input shorter than the filter, and a block longer than the input
    assert overlap_add_exact([1, 2], [1, 0, 0, 1], 8) == [1, 2, 0, 1, 2]
    with pytest.raises(ValueError):
        overlap_add_exact([1, 2, 3], [1, 2, 3], 2)
