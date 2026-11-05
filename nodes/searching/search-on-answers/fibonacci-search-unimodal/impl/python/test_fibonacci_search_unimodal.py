# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-search-unimodal/. The authors are listed in prov/FM952M.jsonl.

import random

from fibonacci_search_unimodal import fibonacci_search_max


def budget(n: int) -> int:
    a, b, big_n = 1, 2, 1  # F(N + 1), F(N + 2) for N = 1
    while b - 1 < n:
        a, b = b, a + b
        big_n += 1
    return big_n


def run(values):
    calls = []

    def f(i):
        calls.append(i)
        return values[i - 1]

    return fibonacci_search_max(f, len(values)), calls


def test_example() -> None:
    values = [2, 5, 9, 14, 20, 23, 21, 18, 11, 8, 4, 1]
    mode, calls = run(values)
    assert mode == 6
    assert calls == [5, 8, 3, 6, 7]


def test_small() -> None:
    assert run([7])[0] == 1
    assert run([1, 2])[0] == 2
    assert run([2, 1])[0] == 1
    assert run([1, 3, 2])[0] == 2


def test_budget_values() -> None:
    assert [budget(n) for n in (1, 2, 4, 7, 10, 12, 13, 100, 1000, 10 ** 6)] == [1, 2, 3, 4, 5, 5, 6, 10, 15, 29]


def test_every_mode_exact_count() -> None:
    for n in range(1, 90):
        for m in range(1, n + 1):
            values = [-(abs(i - m)) for i in range(1, n + 1)]
            mode, calls = run(values)
            assert mode == m
            assert len(calls) <= budget(n)
            assert all(1 <= c <= n for c in calls)
            assert len(set(calls)) == len(calls)


def test_random_unimodal() -> None:
    rng = random.Random(11)
    for _ in range(3000):
        n = rng.randrange(1, 200)
        m = rng.randrange(1, n + 1)
        left = sorted(rng.sample(range(-10 ** 6, 10 ** 6), m - 1))
        right = sorted(rng.sample(range(-10 ** 6, 10 ** 6), n - m), reverse=True)
        top = max(left + right + [0]) + 1
        values = left + [top] + right
        mode, calls = run(values)
        assert mode == m
        assert len(calls) <= budget(n)
