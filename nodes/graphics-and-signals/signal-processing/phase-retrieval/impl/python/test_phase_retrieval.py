# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phase-retrieval/. The authors are listed in prov/YZ4Y3G.jsonl.

import cmath
import math
import random
from fractions import Fraction

from phase_retrieval import (
    autocorrelation,
    brute_force_same_magnitude,
    c,
    conjugate_flip,
    error_reduction,
    flip_zeros,
    from_zeros,
    global_phase,
    same_magnitude,
    shift,
    trim,
    trivial_class,
)


def dtft_mag2(x, w):
    return abs(sum(complex(v) * cmath.exp(-1j * w * n) for n, v in enumerate(x))) ** 2


def to_complex(x):
    return [complex(float(v[0]), float(v[1])) for v in x]


def random_gaussian_integer_signal(rng, n):
    return [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]


def test_autocorrelation_gives_the_magnitude() -> None:
    rng = random.Random(1)
    for _ in range(20):
        x = random_gaussian_integer_signal(rng, rng.randint(1, 7))
        x[0] = (1, 0)
        x[-1] = (2, -1)
        r = autocorrelation(x)
        n = len(x)
        for t in range(9):
            w = -math.pi + 2 * math.pi * t / 8
            via_r = sum(complex(float(v[0]), float(v[1])) * cmath.exp(-1j * w * k) for k, v in zip(range(-(n - 1), n), r))
            assert abs(via_r.imag) < 1e-9
            assert abs(via_r.real - dtft_mag2(to_complex([c(*v) for v in x]), w)) < 1e-9


def test_trivial_ambiguities_are_exact() -> None:
    rng = random.Random(7)
    units = [(1, 0), (-1, 0), (0, 1), (Fraction(3, 5), Fraction(4, 5)), (Fraction(-5, 13), Fraction(12, 13))]
    for _ in range(50):
        x = random_gaussian_integer_signal(rng, rng.randint(1, 8))
        for n0 in (1, 3):
            assert same_magnitude(x, shift(x, n0))
        assert same_magnitude(x, conjugate_flip(x))
        for u in units:
            assert same_magnitude(x, global_phase(x, u))
        both = global_phase(shift(conjugate_flip(x), 2), units[3])
        assert same_magnitude(x, both)


def test_plain_reversal_is_not_an_ambiguity_for_complex_signals() -> None:
    x = [(1, 0), (0, 1)]
    y = list(reversed(x))
    assert not same_magnitude(x, y)
    assert same_magnitude(x, conjugate_flip(x))


def test_zero_flipping_keeps_the_magnitude() -> None:
    rng = random.Random(3)
    for _ in range(10):
        k = rng.randint(1, 4)
        zeros = [(Fraction(rng.randint(-9, 9), rng.randint(1, 4)), Fraction(rng.randint(-9, 9), rng.randint(1, 4))) for _ in range(k)]
        base = flip_zeros((1, 0), zeros, 0)
        assert base == from_zeros((1, 0), zeros)
        for mask in range(1 << k):
            assert same_magnitude(base, flip_zeros((1, 0), zeros, mask))


def test_worked_example_and_brute_force() -> None:
    x = from_zeros((1, 0), [(-2, 0), (-3, 0)])
    assert [v[0] for v in x] == [1, 5, 6]
    y = flip_zeros((1, 0), [(-2, 0), (-3, 0)], 1)
    assert [v[0] for v in y] == [2, 7, 3]
    assert [v[0] for v in autocorrelation([1, 5, 6])] == [6, 35, 62, 35, 6]
    assert same_magnitude([1, 5, 6], [2, 7, 3])
    assert [2, 7, 3] not in [list(t) for t in trivial_class([1, 5, 6])]
    found = set(brute_force_same_magnitude([1, 5, 6], 7))
    want = trivial_class([1, 5, 6]) | trivial_class([2, 7, 3])
    assert found == want and len(found) == 8


def test_trim_removes_the_shift() -> None:
    assert trim(shift([1, 2], 3)) == [c(1), c(2)]


def test_error_reduction_never_increases() -> None:
    for seed in (1, 2, 3, 4):
        rng = random.Random(seed)
        support, size = 6, 16
        x = [rng.uniform(-1, 1) for _ in range(support)]
        padded = x + [0.0] * (size - support)
        mag = [abs(sum(padded[j] * cmath.exp(-2j * math.pi * j * k / size) for j in range(size))) for k in range(size)]
        start = [rng.uniform(-1, 1) for _ in range(support)]
        _, hist = error_reduction(mag, support, start, 60)
        assert all(b <= a + 1e-12 for a, b in zip(hist, hist[1:]))
