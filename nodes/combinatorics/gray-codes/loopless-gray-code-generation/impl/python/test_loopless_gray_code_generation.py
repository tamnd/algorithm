# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loopless-gray-code-generation/. The authors are listed in prov/32MDEZ.jsonl.

import random

import pytest

from loopless_gray_code_generation import gray_codes, gray_delta_sequence, loopless_gray


def reflect(n: int) -> list[int]:
    """Reference: the reflected Gray code from its recursive definition."""
    lst = [0]
    for i in range(n):
        lst = lst + [x | (1 << i) for x in reversed(lst)]
    return lst


def ruler(k: int) -> int:
    r = 0
    while k % 2 == 0:
        k //= 2
        r += 1
    return r


def test_example() -> None:
    assert gray_codes(3) == [0, 1, 3, 2, 6, 7, 5, 4]
    assert gray_delta_sequence(3) == [0, 1, 0, 2, 0, 1, 0]
    assert gray_delta_sequence(4) == [0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0]


def test_edges() -> None:
    assert [a[:] for a in loopless_gray(0)] == [[]]
    assert [a[:] for a in loopless_gray(1)] == [[0], [1]]
    assert gray_delta_sequence(0) == []
    with pytest.raises(ValueError):
        list(loopless_gray(-1))


def test_matches_reflected_code() -> None:
    for n in range(0, 13):
        assert gray_codes(n) == reflect(n)


def test_delta_is_ruler() -> None:
    for n in range(1, 12):
        d = gray_delta_sequence(n)
        assert d == [ruler(k) for k in range(1, 1 << n)]


def test_same_object_in_place() -> None:
    gen = loopless_gray(5)
    first = next(gen)
    second = next(gen)
    assert first is second


def test_random_prefix() -> None:
    rng = random.Random(7)
    for _ in range(50):
        n = rng.randrange(1, 40)
        steps = min(rng.randrange(1, 3000), 1 << n)
        gen = loopless_gray(n)
        for k in range(steps):
            a = next(gen)
            value = sum(bit << j for j, bit in enumerate(a))
            assert value == k ^ (k >> 1)
