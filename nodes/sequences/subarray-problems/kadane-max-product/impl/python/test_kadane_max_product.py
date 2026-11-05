# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kadane-max-product/. The authors are listed in prov/8EPB4B.jsonl.

import math
import random

import pytest

from kadane_max_product import max_product, max_product_subarray


def brute(a: list[int]) -> int:
    return max(math.prod(a[i : j + 1]) for i in range(len(a)) for j in range(i, len(a)))


def test_example() -> None:
    assert max_product([2, 3, -2, 4, -1]) == 48
    assert max_product_subarray([2, 3, -2, 4, -1]) == (48, 0, 4)
    assert max_product([2, 3, -2, 4]) == 6
    assert max_product([-2, 3, -4]) == 24


def test_edges() -> None:
    assert max_product([-3]) == -3
    assert max_product([0]) == 0
    assert max_product([-2, 0, -1]) == 0
    assert max_product([0.5, 4, 0.5]) == 4
    assert max_product([-2, -3]) == 6
    assert max_product_subarray([-2, 0, -1]) == (0, 1, 1)
    with pytest.raises(ValueError):
        max_product([])
    with pytest.raises(ValueError):
        max_product_subarray([])


def test_against_brute_force() -> None:
    rng = random.Random(20261105)
    for _ in range(3000):
        n = rng.randrange(1, 14)
        a = [rng.randrange(-4, 5) for _ in range(n)]
        expected = brute(a)
        assert max_product(a) == expected
        best, i, j = max_product_subarray(a)
        assert best == expected
        assert 0 <= i <= j < n
        assert math.prod(a[i : j + 1]) == best
