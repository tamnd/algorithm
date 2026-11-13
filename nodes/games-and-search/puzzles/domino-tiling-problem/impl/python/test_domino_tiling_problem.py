# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/domino-tiling-problem/. The authors are listed in prov/YTYE25.jsonl.

import random

from domino_tiling_problem import (brute_force, colour_balance, count_kasteleyn, count_region,
                                   count_transfer, has_tiling, kasteleyn_product, rectangle)


def test_rectangles_three_ways() -> None:
    for m in range(1, 9):
        for n in range(1, 9):
            t = count_transfer(m, n)
            assert t == round(kasteleyn_product(m, n)), (m, n)
            assert t == count_kasteleyn(rectangle(m, n)), (m, n)
            assert t == count_region(rectangle(m, n)), (m, n)


def test_known_values() -> None:
    assert count_transfer(8, 8) == 12988816 == 3604 ** 2
    assert [count_transfer(2, n) for n in range(1, 11)] == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    assert count_transfer(3, 4) == 11 and count_transfer(4, 4) == 36 and count_transfer(6, 6) == 6728


def test_brute_force_small() -> None:
    for m in range(1, 5):
        for n in range(1, 6):
            assert brute_force(rectangle(m, n)) == count_transfer(m, n)


def test_mutilated_board() -> None:
    board = rectangle(8, 8) - {(0, 0), (7, 7)}
    assert colour_balance(board) == -2
    assert count_region(board) == 0
    assert not has_tiling(board)


def test_gomory() -> None:
    board = rectangle(8, 8)
    black = [x for x in board if sum(x) % 2 == 0]
    white = [x for x in board if sum(x) % 2 == 1]
    rng = random.Random(1)
    for _ in range(60):
        b, w = rng.choice(black), rng.choice(white)
        assert has_tiling(board - {b, w})


def aztec(n):
    return {(r, c) for r in range(-n, n) for c in range(-n, n) if abs(2 * r + 1) + abs(2 * c + 1) <= 2 * n}


def test_aztec_diamond() -> None:
    for n in range(1, 6):
        assert count_region(aztec(n)) == 2 ** (n * (n + 1) // 2)
        assert count_kasteleyn(aztec(n)) == 2 ** (n * (n + 1) // 2)


def test_random_regions() -> None:
    rng = random.Random(7)
    for _ in range(300):
        region = {(r, c) for r in range(5) for c in range(6) if rng.random() < 0.8}
        count = count_region(region)
        assert has_tiling(region) == (count > 0)
        assert count == brute_force(region)
