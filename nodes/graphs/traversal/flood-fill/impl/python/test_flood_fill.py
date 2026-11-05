# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flood-fill/. The authors are listed in prov/M5TTW9.jsonl.

import random

import pytest

from flood_fill import flood_fill


def oracle(grid: list[list[int]], row: int, col: int, color: int) -> list[list[int]]:
    """Independent oracle: grow the region to a fixed point, then recolor it."""
    rows, cols = len(grid), len(grid[0])
    old = grid[row][col]
    region = {(row, col)}
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if (r, c) in region or grid[r][c] != old:
                    continue
                if any((r + dr, c + dc) in region for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    region.add((r, c))
                    changed = True
    return [[color if (r, c) in region else grid[r][c] for c in range(cols)] for r in range(rows)]


def test_example() -> None:
    grid = [
        [1, 1, 1, 2, 2, 2],
        [1, 2, 1, 2, 1, 2],
        [1, 2, 1, 1, 1, 2],
        [2, 2, 2, 2, 1, 1],
        [1, 1, 2, 1, 1, 2],
    ]
    assert flood_fill(grid, 0, 0, 3) == 14
    assert grid == [
        [3, 3, 3, 2, 2, 2],
        [3, 2, 3, 2, 3, 2],
        [3, 2, 3, 3, 3, 2],
        [2, 2, 2, 2, 3, 3],
        [1, 1, 2, 3, 3, 2],
    ]


def test_same_color_does_nothing() -> None:
    grid = [[5, 5], [5, 5]]
    assert flood_fill(grid, 1, 1, 5) == 0
    assert grid == [[5, 5], [5, 5]]


def test_single_cell_and_isolated_seed() -> None:
    grid = [[0]]
    assert flood_fill(grid, 0, 0, 7) == 1 and grid == [[7]]
    grid = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
    assert flood_fill(grid, 1, 1, 9) == 1
    assert grid == [[1, 0, 1], [0, 9, 0], [1, 0, 1]]


def test_diagonal_is_not_connected() -> None:
    grid = [[1, 0], [0, 1]]
    assert flood_fill(grid, 0, 0, 2) == 1
    assert grid == [[2, 0], [0, 1]]


def test_seed_outside() -> None:
    with pytest.raises(IndexError):
        flood_fill([[0]], 1, 0, 1)


def test_long_snake() -> None:
    # A single row of 100000 cells: the region is a path of 100000 vertices.
    grid = [[0] * 100000]
    assert flood_fill(grid, 0, 50000, 1) == 100000
    assert all(x == 1 for x in grid[0])
    # A serpentine path inside a 301 x 301 grid.
    n = 301
    grid = [[1 if r % 2 == 0 else 0 for _ in range(n)] for r in range(n)]
    for r in range(1, n, 2):
        grid[r][n - 1 if r % 4 == 1 else 0] = 1
    total = sum(map(sum, grid))
    assert flood_fill(grid, 0, 0, 2) == total
    assert all(x != 1 for row in grid for x in row)


def test_random_against_oracle() -> None:
    rng = random.Random(4421)
    for _ in range(600):
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        k = rng.randint(1, 3)
        grid = [[rng.randrange(k) for _ in range(cols)] for _ in range(rows)]
        r, c = rng.randrange(rows), rng.randrange(cols)
        color = rng.randrange(k + 1)
        want = oracle(grid, r, c, color)
        before = [row[:] for row in grid]
        got = flood_fill(grid, r, c, color)
        assert grid == want
        assert got == sum(before[i][j] != want[i][j] for i in range(rows) for j in range(cols))
