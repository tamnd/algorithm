# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-reflected-gray-code/. The authors are listed in prov/73K11Q.jsonl.

import random

import pytest

from binary_reflected_gray_code import as_strings, binary_reflected_gray_code


def reflect(n: int) -> list[str]:
    """Reference: the recursive definition on strings."""
    lst = [""]
    for _ in range(n):
        lst = ["0" + x for x in lst] + ["1" + x for x in reversed(lst)]
    return lst


def test_examples() -> None:
    assert binary_reflected_gray_code(3) == [0, 1, 3, 2, 6, 7, 5, 4]
    assert as_strings(binary_reflected_gray_code(4), 4) == (
        "0000 0001 0011 0010 0110 0111 0101 0100 "
        "1100 1101 1111 1110 1010 1011 1001 1000"
    ).split()


def test_edges() -> None:
    assert binary_reflected_gray_code(0) == [0]
    assert as_strings(binary_reflected_gray_code(0), 0) == [""]
    assert binary_reflected_gray_code(1) == [0, 1]
    with pytest.raises(ValueError):
        binary_reflected_gray_code(-1)


def test_against_definition() -> None:
    for n in range(0, 12):
        g = binary_reflected_gray_code(n)
        assert as_strings(g, n) == reflect(n)
        assert g == [k ^ (k >> 1) for k in range(1 << n)]


def test_gray_cycle_properties() -> None:
    for n in range(1, 14):
        g = binary_reflected_gray_code(n)
        assert len(g) == 1 << n
        assert sorted(g) == list(range(1 << n))
        for k in range(1, len(g)):
            d = g[k] ^ g[k - 1]
            assert d == k & -k  # bit rho(k) changes
        assert g[-1] ^ g[0] == 1 << (n - 1)


def test_random_ranks() -> None:
    rng = random.Random(7)
    g = binary_reflected_gray_code(16)
    for _ in range(2000):
        k = rng.randrange(1 << 16)
        assert g[k] == k ^ (k >> 1)
        assert g[(1 << 16) - 1 - k] == g[k] ^ (1 << 15)
