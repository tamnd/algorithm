# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hadlock-algorithm/. The authors are listed in prov/Q7C4F1.jsonl.

import random

from hadlock_algorithm import hadlock_algorithm, hadlock_search, manhattan


def bfs_dist(grid: list[str], s: tuple[int, int]) -> dict[tuple[int, int], int]:
    """Plain breadth-first search over all free cells, written apart from the router."""
    rows, cols = len(grid), len(grid[0])
    dist = {s: 0}
    frontier = [s]
    while frontier:
        nxt = []
        for r, c in frontier:
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    nxt.append((nr, nc))
        frontier = nxt
    return dist


def is_path(grid: list[str], path: list[tuple[int, int]], s: tuple[int, int], t: tuple[int, int]) -> bool:
    if path[0] != s or path[-1] != t:
        return False
    if any(grid[r][c] != "." for r, c in path):
        return False
    return all(manhattan(a, b) == 1 for a, b in zip(path, path[1:]))


def random_grid(rng: random.Random, rows: int, cols: int, density: float) -> list[str]:
    return ["".join("#" if rng.random() < density else "." for _ in range(cols)) for _ in range(rows)]


GRID = [
    ".....",
    ".###.",
    "...#.",
    "#.#..",
    ".....",
]


def test_example() -> None:
    s, t = (2, 0), (2, 4)
    path = hadlock_algorithm(GRID, s, t)
    assert path is not None and is_path(GRID, path, s, t)
    det, _, _ = hadlock_search(GRID, s, t)
    assert det[t] == 2
    assert len(path) - 1 == manhattan(s, t) + 2 * det[t] == 8


def test_edges() -> None:
    assert hadlock_algorithm(["."], (0, 0), (0, 0)) == [(0, 0)]
    assert hadlock_algorithm([".#."], (0, 0), (0, 2)) is None
    assert hadlock_algorithm([".", "#"], (0, 0), (1, 0)) is None
    assert hadlock_algorithm(["...", "...", "..."], (0, 0), (2, 2)) is not None


def test_against_bfs(seed: int = 11) -> None:
    rng = random.Random(seed)
    for _ in range(400):
        rows, cols = rng.randint(1, 9), rng.randint(1, 9)
        grid = random_grid(rng, rows, cols, rng.choice([0.1, 0.25, 0.4]))
        s = (rng.randrange(rows), rng.randrange(cols))
        t = (rng.randrange(rows), rng.randrange(cols))
        path = hadlock_algorithm(grid, s, t)
        if grid[s[0]][s[1]] == "#" or grid[t[0]][t[1]] == "#":
            assert path is None
            continue
        dist = bfs_dist(grid, s)
        if t not in dist:
            assert path is None
        else:
            assert path is not None and is_path(grid, path, s, t)
            assert len(path) - 1 == dist[t]
            det, _, _ = hadlock_search(grid, s, t)
            assert dist[t] == manhattan(s, t) + 2 * det[t]
