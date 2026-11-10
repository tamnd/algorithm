# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-matrix-transpose/. The authors are listed in prov/A6Y79E.jsonl.

import random

from parallel_matrix_transpose import ceil_lg, lru_misses, transpose, transpose_rows


def oracle(a: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*a)]


def test_example() -> None:
    a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    cost, swaps = transpose(a)
    assert a == [[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15], [4, 8, 12, 16]]
    assert (cost.work, cost.span, swaps) == (19, 5, 6)


def test_powers_of_two_closed_forms() -> None:
    for big_l in range(0, 8):
        n = 2**big_l
        a = [[i * n + j for j in range(n)] for i in range(n)]
        want = oracle(a)
        cost, swaps = transpose(a)
        assert a == want
        assert cost.work == n * n + n - 1
        assert cost.span == 2 * big_l + 1
        assert swaps == n * (n - 1) // 2


def test_random_any_size() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n = rng.randint(0, 40)
        a = [[rng.randint(-99, 99) for _ in range(n)] for _ in range(n)]
        want = oracle(a)
        cost, swaps = transpose(a)
        assert a == want
        assert swaps == n * (n - 1) // 2
        if n >= 1:
            assert cost.work == n * n + n - 1
            assert cost.span <= 2 * ceil_lg(n) + 1
        b = [row[:] for row in want]
        transpose_rows(b)
        assert oracle(b) == want


def test_cache_misses_are_exactly_n2_over_b() -> None:
    # a fully associative LRU cache with 2B lines of B words (so M = 2 B^2 words)
    for n in (16, 32, 64, 128):
        for b in (2, 4, 8):
            if b > n:
                continue
            trace: list[tuple[int, int]] = []
            transpose([[0] * n for _ in range(n)], trace)
            assert lru_misses(trace, n, 2 * b, b) == n * n // b


def test_row_loop_misses_more() -> None:
    n, b = 128, 8
    rec: list[tuple[int, int]] = []
    rows: list[tuple[int, int]] = []
    transpose([[0] * n for _ in range(n)], rec)
    transpose_rows([[0] * n for _ in range(n)], rows)
    assert lru_misses(rows, n, 2 * b, b) > 4 * lru_misses(rec, n, 2 * b, b)
