# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frontier-based-exploration/. The authors are listed in prov/KCQHFD.jsonl.

"""Frontier-based exploration (Yamauchi 1997) on a grid.

The true world is a list of strings: '#' is an obstacle, anything else is free. The robot
knows nothing at the start. Its map has three states per cell: UNKNOWN, FREE and OCC.
The sensor casts Bresenham rays from the robot cell to every cell on the square of
Chebyshev radius r; along each ray it marks cells FREE until it meets an obstacle, which
it marks OCC. The robot moves one cell at a time between 4-neighbors, only on cells its
map marks FREE.

A frontier cell is a FREE cell with an UNKNOWN 4-neighbor. The method groups frontier
cells into 8-connected regions, keeps the regions with at least min_size cells, and drives
to the nearest cell of a kept region (by breadth-first search over FREE cells), sensing
at each cell of the path. It stops when no kept region is reachable.
"""

from collections import deque

UNKNOWN, FREE, OCC = -1, 0, 1
STEPS4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
STEPS8 = STEPS4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def bresenham(x0, y0, x1, y1):
    """The cells of the digital line from (x0, y0) to (x1, y1), both ends included."""
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x1 > x0 else -1), (1 if y1 > y0 else -1)
    err = dx + dy
    out = []
    while True:
        out.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return out
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def sense(world, known, x, y, r):
    """Cast rays to the square of radius r around (x, y). Returns the number of new cells."""
    rows, cols = len(world), len(world[0])
    new = 0
    ring = [(x + i, y - r) for i in range(-r, r + 1)] + [(x + i, y + r) for i in range(-r, r + 1)]
    ring += [(x - r, y + j) for j in range(-r + 1, r)] + [(x + r, y + j) for j in range(-r + 1, r)]
    for tx, ty in ring:
        for cx, cy in bresenham(x, y, tx, ty)[1:]:
            if not (0 <= cx < cols and 0 <= cy < rows):
                break
            hit = world[cy][cx] == "#"
            if known[cy][cx] == UNKNOWN:
                known[cy][cx] = OCC if hit else FREE
                new += 1
            if hit:
                break
    return new


def frontier_cells(known):
    """FREE cells with at least one UNKNOWN 4-neighbor."""
    rows, cols = len(known), len(known[0])
    out = set()
    for y in range(rows):
        for x in range(cols):
            if known[y][x] != FREE:
                continue
            for dx, dy in STEPS4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and known[ny][nx] == UNKNOWN:
                    out.add((x, y))
                    break
    return out


def frontier_regions(cells):
    """The 8-connected components of a set of cells, as a dict from cell to region id."""
    region = {}
    rid = 0
    for c in sorted(cells):
        if c in region:
            continue
        region[c] = rid
        stack = [c]
        while stack:
            x, y = stack.pop()
            for dx, dy in STEPS8:
                d = (x + dx, y + dy)
                if d in cells and d not in region:
                    region[d] = rid
                    stack.append(d)
        rid += 1
    return region


def nearest_frontier(known, start, targets):
    """Breadth-first search over FREE cells; returns the path to the nearest target, or None."""
    rows, cols = len(known), len(known[0])
    parent = {start: None}
    queue = deque([start])
    while queue:
        c = queue.popleft()
        if c in targets:
            path = []
            while c is not None:
                path.append(c)
                c = parent[c]
            return path[::-1]
        x, y = c
        for dx, dy in STEPS4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and known[ny][nx] == FREE and (nx, ny) not in parent:
                parent[(nx, ny)] = c
                queue.append((nx, ny))
    return None


def explore(world, start, r=3, min_size=1, max_moves=100000):
    """Explore from start. Returns (known map, list of visited cells, number of plans)."""
    rows, cols = len(world), len(world[0])
    known = [[UNKNOWN] * cols for _ in range(rows)]  # @line L1
    x, y = start
    known[y][x] = FREE
    sense(world, known, x, y, r)  # @line L1
    trail, plans = [start], 0
    while len(trail) <= max_moves:
        cells = frontier_cells(known)  # @line L2
        region = frontier_regions(cells)  # @line L3
        size = {}
        for rid in region.values():
            size[rid] = size.get(rid, 0) + 1
        targets = {c for c in cells if size[region[c]] >= min_size}  # @line L3
        path = nearest_frontier(known, (x, y), targets)  # @line L4
        if path is None:  # @line L5
            return known, trail, plans
        plans += 1
        for cx, cy in path[1:]:  # @line L6
            x, y = cx, cy
            trail.append((x, y))
            sense(world, known, x, y, r)  # @line L7
    raise RuntimeError("move limit reached")
