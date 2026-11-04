# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-dimensional-fenwick-tree/. The authors are listed in prov/RNZB8E.jsonl.

import random

import pytest

from two_dimensional_fenwick_tree import FenwickTree2D

M = [[2, 1, 4, 3], [0, 5, 2, 1], [3, 1, 6, 2], [1, 4, 0, 5]]


def brute(mat: list[list[int]], r1: int, c1: int, r2: int, c2: int) -> int:
    return sum(mat[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))


def test_example() -> None:
    ft = FenwickTree2D(M)
    assert ft.f[1][1:] == [2, 3, 4, 10]
    assert ft.f[2][1:] == [2, 8, 6, 18]
    assert ft.f[3][1:] == [3, 4, 6, 12]
    assert ft.f[4][1:] == [6, 17, 12, 40]
    assert ft.prefix(3, 4) == 30
    assert ft.query(1, 1, 2, 3) == 17
    assert ft.query(0, 0, 3, 3) == 40
    assert ft.query(2, 0, 3, 1) == 9
    ft.add(2, 1, 3)
    assert ft.f[3][1:] == [3, 7, 6, 15]
    assert ft.f[4][1:] == [6, 20, 12, 43]
    assert ft.query(1, 1, 2, 3) == 20
    ft.check_invariant()


def test_single_cell_and_empty() -> None:
    ft = FenwickTree2D([[7]])
    assert ft.query(0, 0, 0, 0) == 7
    assert ft.query(0, 0, -1, 0) == 0
    ft.add(0, 0, -10)
    assert ft.query(0, 0, 0, 0) == -3
    empty = FenwickTree2D([])
    assert empty.prefix(0, 0) == 0


def test_one_row_and_one_column() -> None:
    row = FenwickTree2D([[5, 2, 8, 1, 9, 3, 7, 4]])
    assert row.query(0, 2, 0, 6) == 28
    col = FenwickTree2D([[5], [2], [8], [1], [9], [3], [7], [4]])
    assert col.query(2, 0, 6, 0) == 28
    row.check_invariant()
    col.check_invariant()


def test_errors() -> None:
    ft = FenwickTree2D(M)
    with pytest.raises(IndexError):
        ft.add(4, 0, 1)
    with pytest.raises(IndexError):
        ft.query(0, 0, 4, 0)
    with pytest.raises(ValueError):
        FenwickTree2D([[1, 2], [3]])


def test_random_against_brute_force() -> None:
    rng = random.Random(20261104)
    for _ in range(60):
        n, m = rng.randint(1, 9), rng.randint(1, 9)
        mat = [[rng.randint(-20, 20) for _ in range(m)] for _ in range(n)]
        ft = FenwickTree2D(mat)
        ft.check_invariant()
        for _ in range(30):
            if rng.random() < 0.4:
                r, c, d = rng.randrange(n), rng.randrange(m), rng.randint(-9, 9)
                mat[r][c] += d
                ft.add(r, c, d)
            else:
                r1, r2 = sorted((rng.randrange(n), rng.randrange(n)))
                c1, c2 = sorted((rng.randrange(m), rng.randrange(m)))
                assert ft.query(r1, c1, r2, c2) == brute(mat, r1, c1, r2, c2)
        ft.check_invariant()
        assert ft.to_matrix() == mat
