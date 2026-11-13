# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/josephus-problem/. The authors are listed in prov/8ZZ2XW.jsonl.

import random

from josephus_problem import (order_fenwick, rotate_left, simulate, survivor_concrete,
                              survivor_fast, survivor_k2, survivor_recurrence)


def test_all_methods_agree_with_simulation() -> None:
    for n in range(1, 501):
        for k in range(1, 11):
            last = simulate(n, k)[-1]
            assert survivor_recurrence(n, k) == last, (n, k)
            assert survivor_fast(n, k) == last, (n, k)
            if k >= 2:
                assert survivor_concrete(n, k) == last, (n, k)
            if k == 2:
                assert survivor_k2(n) == last == rotate_left(n), n


def test_fenwick_order() -> None:
    for n in range(1, 120):
        for k in range(1, 12):
            assert order_fenwick(n, k) == simulate(n, k)
    rng = random.Random(3)
    for _ in range(20):
        n, k = rng.randint(1, 2000), rng.randint(1, 3000)
        assert order_fenwick(n, k) == simulate(n, k)


def test_worked_values() -> None:
    assert simulate(10, 2) == [2, 4, 6, 8, 10, 3, 7, 1, 9, 5]
    assert simulate(7, 3) == [3, 6, 2, 7, 5, 1, 4]
    assert simulate(41, 3)[-2:] == [16, 31]
    assert survivor_k2(100) == 73 and survivor_recurrence(100, 3) == 91
    assert survivor_k2(2 ** 20) == 1


def test_k2_fixed_points_and_iteration() -> None:
    for n in range(1, 5000):
        assert (survivor_k2(n) == n) == ((n + 1) & n == 0)
        x = n
        while survivor_k2(x) != x:
            x = survivor_k2(x)
        assert x == 2 ** bin(n).count("1") - 1


def test_large_k2() -> None:
    n = 10 ** 18 + 12345
    assert survivor_k2(n) == rotate_left(n)
    assert survivor_fast(10 ** 6, 2) == survivor_k2(10 ** 6)
