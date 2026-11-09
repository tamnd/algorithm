# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pascal-triangle-dp/. The authors are listed in prov/RACQ8D.jsonl.

import itertools
import math
import random

from pascal_triangle_dp import count_additions, pascal_binomial, pascal_triangle


def brute_count(n: int, k: int) -> int:
    """Count the k-subsets of range(n) by listing them."""
    if k < 0 or k > n:
        return 0
    return sum(1 for _ in itertools.combinations(range(n), k))


def test_page_examples() -> None:
    assert pascal_binomial(6, 3) == 20
    assert pascal_binomial(6, 3, 7) == 6
    assert pascal_binomial(100, 50) == 100891344545564193334812497256
    assert pascal_binomial(100, 50, 10**9) == 812497256
    assert count_additions(6, 3) == 15
    assert count_additions(100, 50) == 3775
    assert pascal_triangle(10)[10] == [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]


def test_edge_cases() -> None:
    assert pascal_binomial(0, 0) == 1
    assert pascal_binomial(0, 0, 1) == 0
    assert pascal_binomial(0, 1) == 0
    assert pascal_binomial(0, -1) == 0
    for n in range(12):
        assert pascal_binomial(n, 0) == 1
        assert pascal_binomial(n, n) == 1
        assert pascal_binomial(n, n + 1) == 0
        assert pascal_binomial(n, n + 5) == 0
        assert pascal_binomial(n, -1) == 0
        assert pascal_binomial(n, 0, 1) == 0
    for bad in ((-1, 0, None), (3, 1, 0)):
        try:
            pascal_binomial(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"no ValueError for {bad}")


def test_against_brute_force_small() -> None:
    for n in range(0, 15):
        for k in range(-2, n + 3):
            want = brute_count(n, k)
            assert pascal_binomial(n, k) == want
            for m in (1, 2, 6, 7, 12):
                assert pascal_binomial(n, k, m) == want % m


def test_random_against_math_comb() -> None:
    rng = random.Random(20261109)
    for _ in range(600):
        n = rng.randrange(0, 120)
        k = rng.randrange(-3, n + 4)
        want = math.comb(n, k) if 0 <= k <= n else 0
        assert pascal_binomial(n, k) == want
        m = rng.choice([1, 2, 3, 4, 10, 97, 1000, 10**9 + 7, rng.randrange(1, 10**6)])
        assert pascal_binomial(n, k, m) == want % m


def test_triangle_rows() -> None:
    rows = pascal_triangle(40)
    for i, row in enumerate(rows):
        assert len(row) == i + 1
        assert sum(row) == 2**i
        assert row == [math.comb(i, j) for j in range(i + 1)]
    rows7 = pascal_triangle(40, 7)
    for i in range(41):
        assert rows7[i] == [x % 7 for x in rows[i]]
    assert pascal_triangle(0, 1) == [[0]]


def test_addition_count_formula() -> None:
    for n in range(0, 60):
        for k in range(0, n + 1):
            kk = min(k, n - k)
            assert count_additions(n, k) == n * kk - kk * (kk - 1) // 2
