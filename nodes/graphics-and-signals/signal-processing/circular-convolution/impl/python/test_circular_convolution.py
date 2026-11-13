# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circular-convolution/. The authors are listed in prov/KFMA92.jsonl.

import random
from fractions import Fraction

import pytest

from circular_convolution import circular_convolve, circular_convolve_dft, time_alias


def linear(x, h):
    """The defining double sum of the linear convolution, exact."""
    y = [Fraction(0)] * (len(x) + len(h) - 1)
    for i in range(len(x)):
        for k in range(len(h)):
            y[i + k] += x[i] * h[k]
    return y


def rand_seq(rng, n):
    return [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]


def test_example() -> None:
    assert circular_convolve([1, 2, 3, 4], [1, 1, 0, 0], 4) == [5, 3, 5, 7]
    assert circular_convolve([1, 2, 3], [4, 5], 3) == [19, 13, 22]


def test_equals_linear_iff_long_enough() -> None:
    rng = random.Random(7201)
    for _ in range(200):
        n, m = rng.randint(1, 8), rng.randint(1, 8)
        x, h = rand_seq(rng, n), rand_seq(rng, m)
        y = linear(x, h)
        for length in range(max(n, m), n + m + 4):
            c = circular_convolve(x, h, length)
            # c is always the time-aliased linear convolution
            assert c == time_alias(y, length)
            if length >= n + m - 1:
                assert c == y + [0] * (length - len(y))


def test_one_short_is_wrong_when_the_ends_do_not_cancel() -> None:
    rng = random.Random(7202)
    for _ in range(200):
        n, m = rng.randint(2, 8), rng.randint(2, 8)
        x, h = rand_seq(rng, n), rand_seq(rng, m)
        x[0] = x[-1] = Fraction(rng.randint(1, 9))
        h[0] = h[-1] = Fraction(rng.randint(1, 9))
        y = linear(x, h)
        length = n + m - 2
        c = circular_convolve(x, h, length)
        # the last output wraps onto index 0: c[0] = y[0] + y[L]
        assert c[0] == y[0] + y[length] and y[length] == x[-1] * h[-1] != 0
        assert c != y[:length]
        assert c[1:] == y[1:length]


def test_dft_product_matches() -> None:
    rng = random.Random(7203)
    for _ in range(40):
        n, m = rng.randint(1, 9), rng.randint(1, 9)
        x = [rng.randint(-9, 9) for _ in range(n)]
        h = [rng.randint(-9, 9) for _ in range(m)]
        length = rng.randint(max(n, m), n + m + 2)
        exact = circular_convolve(x, h, length)
        approx = circular_convolve_dft(x, h, length)
        for a, b in zip(exact, approx):
            assert abs(a - b) < 1e-9


def test_commutative_and_identity() -> None:
    rng = random.Random(7204)
    for _ in range(50):
        length = rng.randint(1, 8)
        x, h = rand_seq(rng, length), rand_seq(rng, length)
        assert circular_convolve(x, h, length) == circular_convolve(h, x, length)
        assert circular_convolve(x, [1], length) == x
        # a cyclic shift of h by one shifts the result by one
        shifted = [h[-1]] + h[:-1]
        c = circular_convolve(x, h, length)
        assert circular_convolve(x, shifted, length) == [c[-1]] + c[:-1]


def test_too_long_input() -> None:
    with pytest.raises(ValueError):
        circular_convolve([1, 2, 3], [1], 2)
