# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/array-multiplier/. The authors are listed in prov/4XX4WG.jsonl.

import random

from array_multiplier import array_multiply, from_bits, multiply, to_bits


def test_example() -> None:
    bits, _, _ = array_multiply([1, 0, 1, 1], [1, 1, 0, 1])
    assert bits == [1, 1, 1, 1, 0, 0, 0, 1]
    assert from_bits(bits) == 143


def test_exhaustive_small() -> None:
    for n in range(1, 6):
        for x in range(1 << n):
            for y in range(1 << n):
                assert multiply(x, y, n) == x * y


def test_edges() -> None:
    for n in (1, 2, 3, 8, 16, 33):
        top = (1 << n) - 1
        assert multiply(0, 0, n) == 0
        assert multiply(top, 0, n) == 0
        assert multiply(0, top, n) == 0
        assert multiply(1, top, n) == top
        assert multiply(top, top, n) == top * top
        assert multiply(1 << (n - 1), 1 << (n - 1), n) == 1 << (2 * n - 2)


def test_cell_counts_and_depth() -> None:
    for n in range(1, 13):
        _, counts, depth = array_multiply([1] * n, [1] * n)
        assert counts.and_gates == n * n
        if n >= 2:
            assert counts.full_adders == n * n - 2 * n
            assert counts.half_adders == n
        assert depth == 2 * n - 1


def test_depth_does_not_depend_on_values() -> None:
    rng = random.Random(7)
    for n in (4, 9):
        for _ in range(20):
            x, y = rng.randrange(1 << n), rng.randrange(1 << n)
            _, _, depth = array_multiply(to_bits(x, n), to_bits(y, n))
            assert depth == 2 * n - 1


def test_random_against_python() -> None:
    rng = random.Random(4004)
    for _ in range(600):
        n = rng.randint(1, 24)
        x, y = rng.randrange(1 << n), rng.randrange(1 << n)
        assert multiply(x, y, n) == x * y


def test_bad_lengths() -> None:
    for a, b in (([], []), ([1], [1, 0])):
        try:
            array_multiply(a, b)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
