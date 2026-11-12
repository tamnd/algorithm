# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/repetition-code/. The authors are listed in prov/8TYFGD.jsonl.

import itertools
import math
import random

from repetition_code import (
    chernoff_bound, decode, encode, error_probability, majority, shortest_length, simulate,
)


def test_encode_decode() -> None:
    assert encode([1, 0], 3) == [1, 1, 1, 0, 0, 0]
    assert decode([1, 0, 1, 0, 0, 1], 3) == [1, 0]
    assert decode(list("abccca"), 3) == [None, "c"]  # "abc" is a three-way tie, no generator
    assert majority(list("abbab")) == "b"


def test_corrects_up_to_half_exhaustive() -> None:
    for n in (1, 3, 5, 7, 9):
        t = (n - 1) // 2
        for b in (0, 1):
            for y in itertools.product((0, 1), repeat=n):
                flips = sum(1 for v in y if v != b)
                out = decode(list(y), n)[0]
                if flips <= t:
                    assert out == b
                else:
                    assert out == 1 - b


def test_exact_error_matches_enumeration() -> None:
    p = 0.13
    for n in range(1, 11):
        rng_free = 0.0
        for e in itertools.product((0, 1), repeat=n):
            w = sum(e)
            pr = p ** w * (1 - p) ** (n - w)
            if 2 * w > n:
                rng_free += pr
            elif 2 * w == n:
                rng_free += pr / 2
        assert math.isclose(error_probability(n, p), rng_free)


def test_values_and_even_lengths() -> None:
    assert math.isclose(error_probability(3, 0.1), 0.028)
    assert math.isclose(error_probability(3, 0.1), 3 * 0.1 ** 2 - 2 * 0.1 ** 3)
    # an even length 2k is no better than 2k - 1
    for k in range(1, 8):
        assert math.isclose(error_probability(2 * k, 0.2), error_probability(2 * k - 1, 0.2))
    assert shortest_length(0.1, 1e-15) == 63


def test_decreasing_and_bounded() -> None:
    p = 0.1
    vals = [error_probability(n, p) for n in range(1, 60, 2)]
    assert all(a > b for a, b in zip(vals, vals[1:]))
    for n in range(1, 60, 2):
        assert error_probability(n, p) <= chernoff_bound(n, p)
    # the error falls exponentially, at the rate D(1/2 || p) bits per symbol
    d = 0.5 * math.log2(0.5 / p) + 0.5 * math.log2(0.5 / (1 - p))
    n = 401
    assert abs(-math.log2(error_probability(n, p)) / n - d) < 0.02


def test_perfect_code() -> None:
    # odd n: the two balls of radius (n - 1)/2 fill the whole space
    for n in range(1, 16, 2):
        assert 2 * sum(math.comb(n, i) for i in range((n - 1) // 2 + 1)) == 2 ** n


def test_simulation() -> None:
    est = simulate(5, 0.2, 40000, seed=3)
    exact = error_probability(5, 0.2)
    assert abs(est - exact) < 4 * math.sqrt(exact * (1 - exact) / 40000)


def test_random_tie_break() -> None:
    rng = random.Random(1)
    outs = {decode([0, 1], 2, rng)[0] for _ in range(50)}
    assert outs == {0, 1}
