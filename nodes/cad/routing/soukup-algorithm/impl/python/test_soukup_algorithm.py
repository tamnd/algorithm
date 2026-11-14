# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soukup-algorithm/. The authors are listed in prov/34KRY7.jsonl.

import random

from soukup_algorithm import manhattan, soukup_algorithm, soukup_search


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
    if len(set(path)) != len(path):
        return False
    return all(manhattan(a, b) == 1 for a, b in zip(path, path[1:]))


def random_grid(rng: random.Random, rows: int, cols: int, density: float) -> list[str]:
    return ["".join("#" if rng.random() < density else "." for _ in range(cols)) for _ in range(rows)]


TRAP = [
    "..",
    "#.",
    "..",
    "..",
    "..",
]


def test_not_shortest() -> None:
    s, t = (4, 1), (0, 0)
    path = soukup_algorithm(TRAP, s, t)
    assert path == [(4, 1), (4, 0), (3, 0), (2, 0), (2, 1), (1, 1), (0, 1), (0, 0)]
    assert is_path(TRAP, path, s, t)
    assert len(path) - 1 == 7 and bfs_dist(TRAP, s)[t] == 5


def test_edges() -> None:
    assert soukup_algorithm(["."], (0, 0), (0, 0)) == [(0, 0)]
    assert soukup_algorithm([".#."], (0, 0), (0, 2)) is None
    assert soukup_algorithm(["..."], (0, 0), (0, 2)) == [(0, 0), (0, 1), (0, 2)]
    parent, order = soukup_search(["....."], (0, 0), (0, 4))
    assert order == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]


def test_against_bfs(seed: int = 13) -> None:
    rng = random.Random(seed)
    longer = 0
    for _ in range(500):
        rows, cols = rng.randint(1, 9), rng.randint(1, 9)
        grid = random_grid(rng, rows, cols, rng.choice([0.1, 0.25, 0.4]))
        s = (rng.randrange(rows), rng.randrange(cols))
        t = (rng.randrange(rows), rng.randrange(cols))
        path = soukup_algorithm(grid, s, t)
        if grid[s[0]][s[1]] == "#" or grid[t[0]][t[1]] == "#":
            assert path is None
            continue
        dist = bfs_dist(grid, s)
        if t not in dist:
            assert path is None
        else:
            assert path is not None and is_path(grid, path, s, t)
            assert len(path) - 1 >= dist[t]
            longer += len(path) - 1 > dist[t]
    assert longer > 0
