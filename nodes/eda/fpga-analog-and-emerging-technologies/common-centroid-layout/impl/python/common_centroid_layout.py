# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-centroid-layout/. The authors are listed in prov/JQ9ZE3.jsonl.

"""Common-centroid arrays of unit cells, and the mismatch that a gradient leaves.

The array has rows x cols unit cells. Cell (i, j) has its center at
(j + 1/2, i + 1/2), in units of the cell pitch. A pattern is a list of rows,
and each entry is the index of the device that owns the cell.
"""

from fractions import Fraction


def common_centroid_pattern(rows: int, cols: int, counts: list) -> list:
    """Give each device counts[d] cells so that each device has its centroid at
    the center of the array. Each cell is paired with its point reflection
    through the center, and both cells of a pair go to the same device."""
    n = rows * cols
    if sum(counts) != n or any(k < 0 for k in counts):
        raise ValueError("the counts must be nonnegative and fill the array")
    odd = [d for d, k in enumerate(counts) if k % 2]
    if len(odd) != n % 2:
        raise ValueError("no common-centroid pattern: wrong number of odd counts")
    grid = [[-1] * cols for _ in range(rows)]
    left = [k // 2 for k in counts]  # pairs still to place
    if n % 2:  # the center cell is its own reflection
        grid[rows // 2][cols // 2] = odd[0]
    for i in range(rows):
        for j in range(cols):
            mi, mj = rows - 1 - i, cols - 1 - j
            if (i, j) >= (mi, mj):
                continue  # each pair once, from its first cell
            # spread the devices: take the one with the largest share of pairs left
            d = max(range(len(counts)), key=lambda e: (Fraction(left[e], max(counts[e], 1)), -e))
            left[d] -= 1
            grid[i][j] = grid[mi][mj] = d
    return grid


def cells_of(grid: list) -> dict:
    out: dict = {}
    for i, row in enumerate(grid):
        for j, d in enumerate(row):
            out.setdefault(d, []).append((Fraction(2 * j + 1, 2), Fraction(2 * i + 1, 2)))
    return out


def centroids(grid: list) -> dict:
    return {d: (sum(x for x, _ in c) / len(c), sum(y for _, y in c) / len(c)) for d, c in cells_of(grid).items()}


def device_means(grid: list, p) -> dict:
    """The mean of a parameter field p(x, y) over the cells of each device."""
    return {d: sum(Fraction(p(x, y)) for x, y in c) / len(c) for d, c in cells_of(grid).items()}


def second_moments(grid: list) -> dict:
    """For each device, the mean of (dx^2, dx dy, dy^2) about the array center."""
    cx, cy = Fraction(len(grid[0]), 2), Fraction(len(grid), 2)
    out = {}
    for d, c in cells_of(grid).items():
        k = len(c)
        out[d] = (
            sum((x - cx) ** 2 for x, _ in c) / k,
            sum((x - cx) * (y - cy) for x, y in c) / k,
            sum((y - cy) ** 2 for _, y in c) / k,
        )
    return out
