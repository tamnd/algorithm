# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interpolation-search/. The authors are listed in prov/XVAMYG.jsonl.

import random

from interpolation_search import interpolation_search

A = [10, 13, 18, 22, 27, 31, 38, 40, 47, 52, 56, 61, 67, 73, 78, 85, 90, 94]


def check(a: list[float], x: float) -> None:
    r = interpolation_search(a, x)
    if x in a:
        assert 0 <= r < len(a) and a[r] == x
    else:
        assert r == -1


def test_example() -> None:
    assert interpolation_search(A, 61) == 11
    assert interpolation_search(A, 50) == -1
    assert interpolation_search(A, 10) == 0
    assert interpolation_search(A, 94) == 17
    assert interpolation_search(A, 9) == -1
    assert interpolation_search(A, 95) == -1


def test_edges() -> None:
    assert interpolation_search([], 1) == -1
    assert interpolation_search([4], 4) == 0
    assert interpolation_search([4], 5) == -1
    assert interpolation_search([4], 3) == -1
    assert interpolation_search([5, 5, 5, 5], 5) == 0
    assert interpolation_search([5, 5, 5, 5], 6) == -1


def test_bad_input_is_slow_but_correct() -> None:
    a = list(range(999)) + [10**9]
    assert interpolation_search(a, 998) == 998
    assert interpolation_search(a, 10**9) == 999
    assert interpolation_search(a, 999) == -1


def test_every_position_and_gap() -> None:
    for n in range(0, 60):
        a = [3 * i * i for i in range(n)]
        for i in range(n):
            assert interpolation_search(a, a[i]) == i
            check(a, a[i] + 1)
            check(a, a[i] - 1)


def test_duplicates() -> None:
    rng = random.Random(77)
    for _ in range(1000):
        a = sorted(rng.randint(0, 6) for _ in range(rng.randint(0, 25)))
        for x in range(-1, 8):
            check(a, x)


def test_floats() -> None:
    rng = random.Random(5)
    for _ in range(300):
        a = sorted(rng.random() for _ in range(rng.randint(1, 60)))
        for v in a:
            check(a, v)
        check(a, rng.random())
        check(a, -0.5)
        check(a, 1.5)


def test_random_against_linear_scan() -> None:
    rng = random.Random(1978)
    for _ in range(3000):
        a = sorted(rng.randint(-50, 50) for _ in range(rng.randint(0, 40)))
        check(a, rng.randint(-55, 55))
