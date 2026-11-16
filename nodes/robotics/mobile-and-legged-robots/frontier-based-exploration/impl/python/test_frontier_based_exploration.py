# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frontier-based-exploration/. The authors are listed in prov/KCQHFD.jsonl.

import random
from collections import deque

from frontier_based_exploration import (
    FREE,
    UNKNOWN,
    bresenham,
    explore,
    frontier_cells,
    frontier_regions,
    nearest_frontier,
)


def random_world(rng, rows, cols, density):
    return ["".join("#" if rng.random() < density else "." for _ in range(cols)) for _ in range(rows)]


def reachable(world, start):
    rows, cols = len(world), len(world[0])
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and world[ny][nx] != "#" and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return seen


def test_bresenham_lines():
    rng = random.Random(31)
    for _ in range(300):
        x0, y0, x1, y1 = (rng.randint(-9, 9) for _ in range(4))
        line = bresenham(x0, y0, x1, y1)
        assert line[0] == (x0, y0) and line[-1] == (x1, y1)
        assert len(line) == max(abs(x1 - x0), abs(y1 - y0)) + 1
        for (ax, ay), (bx, by) in zip(line, line[1:]):
            assert max(abs(ax - bx), abs(ay - by)) == 1
        # Every cell is within half a cell of the true segment along the minor axis.
        dx, dy = x1 - x0, y1 - y0
        for cx, cy in line:
            if abs(dx) >= abs(dy) and dx != 0:
                assert abs((cy - y0) - dy * (cx - x0) / dx) <= 0.5 + 1e-12
            elif dy != 0:
                assert abs((cx - x0) - dx * (cy - y0) / dy) <= 0.5 + 1e-12


def random_known(rng, rows, cols):
    return [[rng.choice([UNKNOWN, FREE, FREE, 1]) for _ in range(cols)] for _ in range(rows)]


def test_frontier_cells_and_regions_match_definitions():
    rng = random.Random(32)
    for _ in range(40):
        known = random_known(rng, 9, 11)
        # A frontier cell is a FREE 4-neighbor of an UNKNOWN cell.
        expect = set()
        for y in range(9):
            for x in range(11):
                if known[y][x] == UNKNOWN:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 11 and 0 <= ny < 9 and known[ny][nx] == FREE:
                            expect.add((nx, ny))
        cells = frontier_cells(known)
        assert cells == expect
        # Regions: two cells share a region exactly when a chain of 8-neighbors joins them.
        region = frontier_regions(cells)
        label = {c: c for c in cells}

        def find(c):
            while label[c] != c:
                c = label[c]
            return c

        for a in cells:
            for b in cells:
                if max(abs(a[0] - b[0]), abs(a[1] - b[1])) == 1:
                    label[find(a)] = find(b)
        for a in cells:
            for b in cells:
                assert (region[a] == region[b]) == (find(a) == find(b))


def test_nearest_frontier_is_a_shortest_path():
    rng = random.Random(33)
    for _ in range(40):
        known = random_known(rng, 8, 8)
        free = [(x, y) for y in range(8) for x in range(8) if known[y][x] == FREE]
        if len(free) < 3:
            continue
        start = rng.choice(free)
        targets = set(rng.sample(free, 2)) - {start}
        # Distances by repeated relaxation over FREE cells.
        dist = {c: (0 if c == start else 10 ** 9) for c in free}
        for _ in range(len(free)):
            for (x, y) in free:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (x + dx, y + dy)
                    if n in dist:
                        dist[n] = min(dist[n], dist[(x, y)] + 1)
        best = min(dist[t] for t in targets)
        path = nearest_frontier(known, start, targets)
        if best >= 10 ** 9:
            assert path is None
            continue
        assert len(path) - 1 == best and path[-1] in targets and path[0] == start
        for (ax, ay), (bx, by) in zip(path, path[1:]):
            assert abs(ax - bx) + abs(ay - by) == 1 and known[by][bx] == FREE


def test_corridor_by_hand():
    world = ["." * 10]
    known, trail, plans = explore(world, (0, 0), r=1)
    assert plans == 8 and len(trail) == 9 and all(v == FREE for v in known[0])
    known, trail, plans = explore(world, (0, 0), r=3)
    assert plans == 2 and trail[-1] == (6, 0) and all(v == FREE for v in known[0])


def test_explores_every_reachable_cell():
    rng = random.Random(34)
    for trial in range(25):
        rows, cols = rng.randint(6, 16), rng.randint(6, 16)
        world = random_world(rng, rows, cols, 0.3)
        free = [(x, y) for y in range(rows) for x in range(cols) if world[y][x] != "#"]
        if not free:
            continue
        start = rng.choice(free)
        known, trail, plans = explore(world, start, r=rng.randint(1, 4))
        for y in range(rows):
            for x in range(cols):
                if known[y][x] != UNKNOWN:
                    assert (known[y][x] == FREE) == (world[y][x] != "#")
        for x, y in reachable(world, start):
            assert known[y][x] == FREE
        for (ax, ay), (bx, by) in zip(trail, trail[1:]):
            assert abs(ax - bx) + abs(ay - by) == 1 and world[by][bx] != "#"
        assert plans <= rows * cols
        assert not any(known[y][x] == FREE for x, y in frontier_cells(known)
                       if (x, y) in reachable(world, start))


def test_a_large_minimum_size_stops_at_once():
    world = ["." * 12 for _ in range(12)]
    known, trail, plans = explore(world, (5, 5), r=2, min_size=10 ** 6)
    assert plans == 0 and trail == [(5, 5)]
    assert sum(v != UNKNOWN for row in known for v in row) == 25
