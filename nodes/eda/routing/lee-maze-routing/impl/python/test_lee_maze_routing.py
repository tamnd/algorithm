# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lee-maze-routing/. The authors are listed in prov/EQ37HH.jsonl.

import random

from lee_maze_routing import lee_maze_routing, lee_wave


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
    for r, c in path:
        if grid[r][c] != ".":
            return False
    return all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(path, path[1:]))


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
    path = lee_maze_routing(GRID, (2, 0), (2, 4))
    assert path is not None and len(path) - 1 == 8
    assert is_path(GRID, path, (2, 0), (2, 4))
    label = lee_wave(GRID, (2, 0), (2, 4))
    assert label[(2, 4)] == 8


def test_edges() -> None:
    assert lee_maze_routing(["."], (0, 0), (0, 0)) == [(0, 0)]
    assert lee_maze_routing([".#."], (0, 0), (0, 2)) is None
    assert lee_maze_routing(["#."], (0, 0), (0, 1)) is None
    assert lee_maze_routing(["..."], (0, 0), (0, 2)) == [(0, 0), (0, 1), (0, 2)]


def test_against_bfs(seed: int = 7) -> None:
    rng = random.Random(seed)
    for _ in range(400):
        rows, cols = rng.randint(1, 9), rng.randint(1, 9)
        grid = random_grid(rng, rows, cols, rng.choice([0.1, 0.25, 0.4]))
        s = (rng.randrange(rows), rng.randrange(cols))
        t = (rng.randrange(rows), rng.randrange(cols))
        path = lee_maze_routing(grid, s, t)
        if grid[s[0]][s[1]] == "#" or grid[t[0]][t[1]] == "#":
            assert path is None
            continue
        dist = bfs_dist(grid, s)
        if t not in dist:
            assert path is None
        else:
            assert path is not None and is_path(grid, path, s, t)
            assert len(path) - 1 == dist[t]
