# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/line-probe-routing/. The authors are listed in prov/CEQKHV.jsonl.

import random

from line_probe_routing import H, V, line_probe_routing, line_probe_search, probe_line


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


def is_simple_path(grid: list[str], path: list[tuple[int, int]], s: tuple[int, int], t: tuple[int, int]) -> bool:
    if path[0] != s or path[-1] != t or len(set(path)) != len(path):
        return False
    if any(grid[r][c] != "." for r, c in path):
        return False
    return all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(path, path[1:]))


def random_grid(rng: random.Random, rows: int, cols: int, density: float) -> list[str]:
    return ["".join("#" if rng.random() < density else "." for _ in range(cols)) for _ in range(rows)]


GRID = [
    "......",
    ".####.",
    "....#.",
    "###.#.",
    "......",
]


def test_probe_line() -> None:
    assert probe_line(GRID, (2, 1), H) == [(2, 0), (2, 1), (2, 2), (2, 3)]
    assert probe_line(GRID, (2, 3), V) == [(2, 3), (3, 3), (4, 3)]


def test_example() -> None:
    s, t = (2, 0), (2, 5)
    path = line_probe_routing(GRID, s, t)
    assert path is not None and is_simple_path(GRID, path, s, t)
    meet, _, levels = line_probe_search(GRID, s, t)
    assert meet is not None and len(levels) == 2


def test_not_shortest() -> None:
    grid = ["...", "...", ".#."]
    path = line_probe_routing(grid, (2, 2), (2, 0))
    assert path == [(2, 2), (1, 2), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0)]
    assert bfs_dist(grid, (2, 2))[(2, 0)] == 4


def test_edges() -> None:
    assert line_probe_routing(["."], (0, 0), (0, 0)) == [(0, 0)]
    assert line_probe_routing([".#."], (0, 0), (0, 2)) is None
    assert line_probe_routing(["..."], (0, 0), (0, 2)) == [(0, 0), (0, 1), (0, 2)]
    assert line_probe_routing(["..", ".."], (0, 0), (1, 1)) is not None


def test_against_bfs(seed: int = 17) -> None:
    rng = random.Random(seed)
    for _ in range(500):
        rows, cols = rng.randint(1, 9), rng.randint(1, 9)
        grid = random_grid(rng, rows, cols, rng.choice([0.1, 0.25, 0.4]))
        s = (rng.randrange(rows), rng.randrange(cols))
        t = (rng.randrange(rows), rng.randrange(cols))
        path = line_probe_routing(grid, s, t)
        if grid[s[0]][s[1]] == "#" or grid[t[0]][t[1]] == "#":
            assert path is None
            continue
        dist = bfs_dist(grid, s)
        if t not in dist:
            assert path is None
        else:
            assert path is not None and is_simple_path(grid, path, s, t)
            assert len(path) - 1 >= dist[t]
