# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-lattice-planning/. The authors are listed in prov/C6YCHP.jsonl.

"""State lattice planning for a forward-driving car on a lattice of 8 headings.

States are (i, j, k): the position (i r, j r) on a square lattice of spacing r and the
heading k pi / 4. A motion primitive is a short path of the car, made of arcs of radius
R = (1 + sqrt(2)) r and straight segments, that starts at a lattice state and ends exactly
at another one (Pivtoraiko and Kelly 2005, Pivtoraiko, Knepper and Kelly 2009). The
control set here, for heading 0, is:

    straight  (0, 0, 0) -> (1, 0, 0), length r
    left 45   (0, 0, 0) -> (2, 1, 1): arc of R through pi / 4, then straight (sqrt(2) - 1) r
    right 45  (0, 0, 0) -> (2, -1, 7): the mirror image

and for heading 1 (pi / 4):

    straight  (0, 0, 1) -> (1, 1, 1), length sqrt(2) r
    right 45  (0, 0, 1) -> (2, 1, 0): straight (sqrt(2) - 1) r, then arc of R through -pi / 4
    left 45   (0, 0, 1) -> (1, 2, 2): the mirror image across the line y = x

Rotations by multiples of pi / 2 give the primitives of the other six headings. Each
primitive's swept cells are computed once (the precomputed swath of the paper), so a
collision check is a set lookup. The search is A* with the Euclidean heuristic.
"""

import heapq
import math

SQRT2 = math.sqrt(2.0)
R_UNIT = 1.0 + SQRT2  # the turning radius in lattice units
STUB = SQRT2 - 1.0  # the straight part of a 45 degree turn
QUARTER = math.pi / 4.0


def wrap(a):
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def drive(q, segments):
    """Exact pose after segments of (curvature, length) from q, in lattice units."""
    x, y, th = q
    for kappa, s in segments:
        if kappa == 0.0:
            x, y = x + s * math.cos(th), y + s * math.sin(th)
        else:
            nth = th + kappa * s
            x += (math.sin(nth) - math.sin(th)) / kappa
            y -= (math.cos(nth) - math.cos(th)) / kappa
            th = nth
    return x, y, th


def _base_primitives():
    """Primitives for headings 0 and 1 as (di, dj, k_end, segments), in lattice units."""
    left, right = 1.0 / R_UNIT, -1.0 / R_UNIT
    arc = R_UNIT * QUARTER
    return {
        0: [
            (1, 0, 0, [(0.0, 1.0)]),
            (2, 1, 1, [(left, arc), (0.0, STUB)]),
            (2, -1, 7, [(right, arc), (0.0, STUB)]),
        ],
        1: [
            (1, 1, 1, [(0.0, SQRT2)]),
            (2, 1, 0, [(0.0, STUB), (right, arc)]),
            (1, 2, 2, [(0.0, STUB), (left, arc)]),
        ],
    }


def _rotate(di, dj, quarter_turns):
    for _ in range(quarter_turns):
        di, dj = -dj, di
    return di, dj


def build_control_set():
    """Primitives for all 8 headings: k -> list of (di, dj, k_end, length, segments)."""
    base = _base_primitives()
    out = {}
    for k in range(8):
        b, turns = k % 2, k // 2
        prims = []
        for di, dj, ke, segs in base[b]:
            ri, rj = _rotate(di, dj, turns)
            prims.append((ri, rj, (ke + 2 * turns) % 8, sum(s for _, s in segs), segs))
        out[k] = prims
    return out


def swath(k, segments, samples_per_unit=8):
    """Cells (a, b) of unit size touched by the samples of a primitive from (0, 0, k),
    relative to the start lattice point. Cell (a, b) is the square [a, a + 1) x [b, b + 1)."""
    total = sum(s for _, s in segments)
    n = max(2, int(math.ceil(total * samples_per_unit)))
    cells = set()
    for m in range(n + 1):
        target = total * m / n
        part, acc = [], 0.0
        for kappa, s in segments:
            if acc + s >= target:
                part.append((kappa, target - acc))
                break
            part.append((kappa, s))
            acc += s
        x, y, _ = drive((0.0, 0.0, k * QUARTER), part)
        # Nudge points on cell borders to both sides, so a border counts for both cells.
        for ex in (-1e-9, 1e-9):
            for ey in (-1e-9, 1e-9):
                cells.add((int(math.floor(x + ex)), int(math.floor(y + ey))))
    return frozenset(cells)


class Lattice:
    def __init__(self, width, height, blocked=(), resolution=1.0):
        self.nx, self.ny, self.r = width, height, resolution
        self.blocked = set(blocked)
        self.control = build_control_set()
        self.swaths = {k: [swath(k, p[4]) for p in self.control[k]] for k in range(8)}

    def inside(self, i, j):
        return 0 <= i <= self.nx and 0 <= j <= self.ny

    def free_cells(self, i, j, cells):
        for a, b in cells:
            c = (i + a, j + b)
            if not (0 <= c[0] < self.nx and 0 <= c[1] < self.ny) or c in self.blocked:
                return False
        return True

    def successors(self, state):
        i, j, k = state
        for (di, dj, ke, length, segs), cells in zip(self.control[k], self.swaths[k]):  # @line L5
            if self.inside(i + di, j + dj) and self.free_cells(i, j, cells):  # @line L6
                yield (i + di, j + dj, ke), length * self.r, segs


def lattice_search(lattice, start, goal, use_heuristic=True):
    """A* (or Dijkstra with use_heuristic=False) from lattice state start to goal.
    Returns (cost in meters, list of states, expansions) or None."""
    r = lattice.r

    def h(s):  # @line L2
        return r * math.hypot(s[0] - goal[0], s[1] - goal[1]) if use_heuristic else 0.0

    g = {start: 0.0}  # @line L1
    parent = {start: None}
    heap = [(h(start), 0, start)]  # @line L1
    closed = set()
    counter = 1
    while heap:  # @line L3
        f, _, s = heapq.heappop(heap)  # @line L3
        if s in closed:
            continue
        closed.add(s)
        if s == goal:  # @line L4
            path = []
            while s is not None:
                path.append(s)
                s = parent[s]
            return g[goal], path[::-1], len(closed)
        for t, cost, _ in lattice.successors(s):  # @line L5
            if t in closed:
                continue
            nd = g[s] + cost  # @line L7
            if nd < g.get(t, math.inf):  # @line L7
                g[t] = nd  # @line L7
                parent[t] = s
                heapq.heappush(heap, (nd + h(t), counter, t))  # @line L7
                counter += 1
    return None  # @line L8


def primitive_between(lattice, a, b):
    """The primitive that joins lattice state a to lattice state b."""
    for di, dj, ke, length, segs in lattice.control[a[2]]:
        if (a[0] + di, a[1] + dj, ke) == b:
            return segs
    raise ValueError("no primitive joins these states")
