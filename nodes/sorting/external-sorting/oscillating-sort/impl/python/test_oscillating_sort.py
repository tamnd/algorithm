# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oscillating-sort/. The authors are listed in prov/P385WS.jsonl.

import random

import pytest

from oscillating_sort import oscillating_sort


def ceil_log(s: int, p: int) -> int:
    k, q = 0, 1
    while q < s:
        q *= p
        k += 1
    return k


def test_example() -> None:
    f = [5, 2, 7, 1, 8, 3, 6, 4]
    assert oscillating_sort(f, 2, 4) == 2
    assert f == list(range(1, 9))


def test_edges() -> None:
    a: list[int] = []
    assert oscillating_sort(a) == 0 and a == []
    a = [1]
    assert oscillating_sort(a) == 0 and a == [1]
    a = [3, 1, 2]
    assert oscillating_sort(a, 3, 4) == 0 and a == [1, 2, 3]
    a = [5] * 9
    oscillating_sort(a, 2, 4)
    assert a == [5] * 9
    a = list(range(50, 0, -1))
    assert oscillating_sort(a, 1, 5) == 4 and a == list(range(1, 51))
    with pytest.raises(ValueError):
        oscillating_sort([1], 2, 3)


def test_random_against_sorted() -> None:
    rng = random.Random(1962)
    for _ in range(600):
        n = rng.randint(0, 120)
        m = rng.randint(1, 6)
        t = rng.randint(4, 9)
        f = [rng.randint(-40, 40) for _ in range(n)]
        want = sorted(f)
        levels = oscillating_sort(f, m, t)
        assert f == want
        assert levels == ceil_log(-(-n // m), t - 2)
