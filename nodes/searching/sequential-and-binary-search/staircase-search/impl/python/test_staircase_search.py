# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/staircase-search/. The authors are listed in prov/0A4NQ0.jsonl.

import random

from staircase_search import count_at_most, staircase_search

M = [
    [1, 4, 7, 11, 15],
    [2, 5, 8, 12, 19],
    [3, 6, 9, 16, 22],
    [10, 13, 14, 17, 24],
]


def oracle(mat: list[list[int]], x: int) -> tuple[int, int] | None:
    for i, row in enumerate(mat):
        cols = [j for j, v in enumerate(row) if v == x]
        if cols:
            return (i, max(cols))
    return None


def random_matrix(rng: random.Random, m: int, n: int) -> list[list[int]]:
    mat = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            up = mat[i - 1][j] if i > 0 else -5
            left = mat[i][j - 1] if j > 0 else -5
            mat[i][j] = max(up, left) + rng.randint(0, 3)
    return mat


def test_example() -> None:
    assert staircase_search(M, 9) == (2, 2)
    assert staircase_search(M, 20) is None
    assert staircase_search(M, 15) == (0, 4)
    assert staircase_search(M, 10) == (3, 0)
    assert staircase_search(M, 1) == (0, 0)
    assert staircase_search(M, 24) == (3, 4)
    assert staircase_search(M, 0) is None
    assert staircase_search(M, 25) is None


def test_edges() -> None:
    assert staircase_search([], 1) is None
    assert staircase_search([[]], 1) is None
    assert staircase_search([[], []], 1) is None
    assert staircase_search([[5]], 5) == (0, 0)
    assert staircase_search([[5]], 4) is None
    assert staircase_search([[5]], 6) is None
    assert staircase_search([[1, 2, 3]], 3) == (0, 2)
    assert staircase_search([[1], [2], [3]], 1) == (0, 0)
    assert staircase_search([[7, 7], [7, 7]], 7) == (0, 1)


def test_corners_and_band() -> None:
    # Two anti-diagonals of value 2n - 2 and 2n + 2 around x = 2n - 1:
    # any single band cell may hold x.
    for n in range(1, 9):
        base = [[2 * (i + j) + (2 if i + j >= n else 0) for j in range(n)] for i in range(n)]
        assert staircase_search(base, 2 * n - 1) is None
        for i in range(n):
            for j in range(n):
                if i + j in (n - 1, n):
                    mat = [row[:] for row in base]
                    mat[i][j] = 2 * n - 1
                    assert staircase_search(mat, 2 * n - 1) == (i, j)


def test_read_bound() -> None:
    class Cell:
        reads = 0

        def __init__(self, v: int) -> None:
            self.v = v

        def __eq__(self, other: object) -> bool:
            Cell.reads += 1
            return isinstance(other, Cell) and self.v == other.v

        def __lt__(self, other: "Cell") -> bool:
            return self.v < other.v

    for m, n in [(1, 1), (1, 7), (7, 1), (4, 5), (10, 10), (3, 30)]:
        mat = [[Cell(2 * (i * n + j)) for j in range(n)] for i in range(m)]
        worst = 0
        for v in range(-1, 2 * m * n + 1):
            Cell.reads = 0
            staircase_search(mat, Cell(v))
            worst = max(worst, Cell.reads)
        assert worst == m + n - 1


def test_random_against_scan() -> None:
    rng = random.Random(4417)
    for _ in range(3000):
        m, n = rng.randint(0, 7), rng.randint(0, 7)
        mat = random_matrix(rng, m, n) if n > 0 else [[] for _ in range(m)]
        x = rng.randint(-6, 30)
        assert staircase_search(mat, x) == oracle(mat, x)
        assert count_at_most(mat, x) == sum(v <= x for row in mat for v in row)


def test_strings() -> None:
    mat = [["ant", "bee", "cow"], ["bat", "cat", "dog"], ["cod", "eel", "fox"]]
    assert staircase_search(mat, "eel") == (2, 1)
    assert staircase_search(mat, "elk") is None
