# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-a-star/. The authors are listed in prov/C6X95N.jsonl.

"""Hybrid A* (Dolgov, Thrun, Montemerlo and Diebel, 2008 and 2010).

A* search over the cells of a grid of (x, y, heading). Each cell keeps one continuous pose,
the best one found so far. A node expands by short arcs of a car with curvature -1/rho, 0
or +1/rho, forward and, if allowed, backward. The cost is the arc length, times a factor for
reverse motion, plus a penalty for each change of direction. The heuristic is the Euclidean
distance, and optionally the maximum of it and an 8-connected grid distance that knows the
obstacles. Every few expansions the search tries an analytic shot to the goal. Dolgov et al.
use a Reeds-Shepp path for the shot; this file uses a Dubins path (forward only), which is
shorter to write and is still a feasible path of the car.

The robot is a point. The map is a set of blocked square cells of side res; a motion is
free when its samples, spaced at most res / 4 apart, lie in free cells inside the map.
"""

import heapq
import math

TWO_PI = 2.0 * math.pi
EPS = 1e-10


def wrap(a):
    return (a + math.pi) % TWO_PI - math.pi


# ----- the map -----

class Grid:
    def __init__(self, width, height, res, blocked=()):
        self.nx, self.ny, self.res = width, height, res
        self.blocked = set(blocked)

    def cell(self, x, y):
        return int(math.floor(x / self.res)), int(math.floor(y / self.res))

    def free(self, x, y):
        i, j = self.cell(x, y)
        return 0 <= i < self.nx and 0 <= j < self.ny and (i, j) not in self.blocked


# ----- motion of the car -----

def move(q, kappa, s):
    """Exact pose after signed arc length s with curvature kappa (s < 0 drives backward)."""
    x, y, th = q
    if abs(kappa) < 1e-15:
        return x + s * math.cos(th), y + s * math.sin(th), th
    nth = th + kappa * s
    return x + (math.sin(nth) - math.sin(th)) / kappa, y - (math.cos(nth) - math.cos(th)) / kappa, nth


def motion_free(grid, q, kappa, s):
    n = max(1, int(math.ceil(abs(s) / (grid.res / 4.0))))
    for k in range(1, n + 1):
        p = move(q, kappa, s * k / n)
        if not grid.free(p[0], p[1]):
            return False
    return True


def path_free(grid, q, segments):
    for kappa, s in segments:
        if not motion_free(grid, q, kappa, s):
            return False
        q = move(q, kappa, s)
    return True


def endpoint(q, segments):
    for kappa, s in segments:
        q = move(q, kappa, s)
    return q


# ----- Dubins shot (forward, shortest of the six words) -----

def _mod(a):
    a = a % TWO_PI
    return 0.0 if a > TWO_PI - EPS else a


def _dubins_words(d, a, b):
    sa, sb, ca, cb = math.sin(a), math.sin(b), math.cos(a), math.cos(b)
    cab = math.cos(a - b)
    out = []
    p2 = 2 + d * d - 2 * cab + 2 * d * (sa - sb)  # LSL
    if p2 >= -EPS:
        vx, vy = d + sa - sb, cb - ca
        g = math.atan2(vy, vx) if math.hypot(vx, vy) > EPS else a
        out.append(("LSL", _mod(g - a), math.sqrt(max(p2, 0.0)), _mod(b - g)))
    p2 = 2 + d * d - 2 * cab + 2 * d * (sb - sa)  # RSR
    if p2 >= -EPS:
        vx, vy = d - sa + sb, ca - cb
        g = math.atan2(vy, vx) if math.hypot(vx, vy) > EPS else a
        out.append(("RSR", _mod(a - g), math.sqrt(max(p2, 0.0)), _mod(g - b)))
    p2 = -2 + d * d + 2 * cab + 2 * d * (sa + sb)  # LSR
    if p2 >= -EPS:
        p = math.sqrt(max(p2, 0.0))
        g = math.atan2(-ca - cb, d + sa + sb) - math.atan2(-2.0, p)
        out.append(("LSR", _mod(g - a), p, _mod(g - b)))
    p2 = -2 + d * d + 2 * cab - 2 * d * (sa + sb)  # RSL
    if p2 >= -EPS:
        p = math.sqrt(max(p2, 0.0))
        g = math.atan2(ca + cb, d - sa - sb) - math.atan2(2.0, p)
        out.append(("RSL", _mod(a - g), p, _mod(b - g)))
    c = (6 - d * d + 2 * cab + 2 * d * (sa - sb)) / 8  # RLR
    if abs(c) <= 1:
        p = TWO_PI - math.acos(c)
        t = _mod(a - math.atan2(ca - cb, d - sa + sb) + p / 2)
        out.append(("RLR", t, p, _mod(a - b - t + p)))
    c = (6 - d * d + 2 * cab + 2 * d * (sb - sa)) / 8  # LRL
    if abs(c) <= 1:
        p = TWO_PI - math.acos(c)
        t = _mod(-a - math.atan2(ca - cb, d + sa - sb) + p / 2)
        out.append(("LRL", t, p, _mod(b - a - t + p)))
    return out


def dubins_segments(q0, q1, rho):
    """Shortest Dubins path from q0 to q1 as a list of (curvature, arc length)."""
    dx, dy = q1[0] - q0[0], q1[1] - q0[1]
    d = math.hypot(dx, dy) / rho
    phi = math.atan2(dy, dx)
    best = None
    for word, t, p, q in _dubins_words(d, _mod(q0[2] - phi), _mod(q1[2] - phi)):
        if best is None or t + p + q < best[0]:
            best = (t + p + q, word, (t, p, q))
    _, word, lens = best
    kap = {"L": 1.0 / rho, "R": -1.0 / rho, "S": 0.0}
    return [(kap[w], rho * a) for w, a in zip(word, lens) if a > 0.0]


# ----- heuristics -----

def grid_distance(grid, goal_xy):
    """8-connected Dijkstra over free cells from the goal cell, in meters (Dolgov's second
    heuristic, the holonomic distance with obstacles)."""
    start = grid.cell(*goal_xy)
    dist = {start: 0.0}
    heap = [(0.0, start)]
    diag = math.sqrt(2.0) * grid.res
    while heap:
        d, (i, j) = heapq.heappop(heap)
        if d > dist[(i, j)]:
            continue
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                c = (i + di, j + dj)
                if not (0 <= c[0] < grid.nx and 0 <= c[1] < grid.ny) or c in grid.blocked:
                    continue
                nd = d + (diag if di and dj else grid.res)
                if nd < dist.get(c, math.inf):
                    dist[c] = nd
                    heapq.heappush(heap, (nd, c))
    return dist


# ----- the search -----

def hybrid_a_star(grid, start, goal, rho, step, n_heading=72, reverse=True,
                  reverse_cost=2.0, switch_cost=1.0, pos_tol=0.5, ang_tol=0.1,
                  shot_every=0, use_grid_heuristic=False, bin_res=None, max_expansions=200000):
    """Returns (cost, segments, expansions) or None. segments is a list of
    (curvature, signed arc length) from the start pose."""
    bin_res = grid.res if bin_res is None else bin_res
    dth = TWO_PI / n_heading

    def key(q):  # @line L3
        return (int(math.floor(q[0] / bin_res)), int(math.floor(q[1] / bin_res)),
                int(math.floor((q[2] % TWO_PI) / dth)) % n_heading)

    h2d = grid_distance(grid, goal[:2]) if use_grid_heuristic else None

    def h(q):  # @line L2
        e = max(0.0, math.hypot(q[0] - goal[0], q[1] - goal[1]) - pos_tol)
        if h2d is not None:
            e = max(e, h2d.get(grid.cell(q[0], q[1]), math.inf) - 2.0 * math.sqrt(2.0) * grid.res - pos_tol)
        return e

    def at_goal(q):
        return math.hypot(q[0] - goal[0], q[1] - goal[1]) <= pos_tol and abs(wrap(q[2] - goal[2])) <= ang_tol

    moves = [(k, d) for d in ((1.0, -1.0) if reverse else (1.0,)) for k in (-1.0 / rho, 0.0, 1.0 / rho)]
    k0 = key(start)
    # node: key -> (g, pose, parent key, (kappa, s), direction)
    nodes = {k0: (0.0, tuple(start), None, None, 0.0)}  # @line L1
    heap = [(h(start), 0, k0)]  # @line L1
    closed = set()
    counter = 1
    expansions = 0

    def chain(k):
        segs = []
        while nodes[k][2] is not None:
            segs.append(nodes[k][3])
            k = nodes[k][2]
        return segs[::-1]

    while heap:  # @line L4
        f, _, k = heapq.heappop(heap)  # @line L4
        if k in closed:
            continue
        g, q, _, _, direction = nodes[k]
        if f > g + h(q) + 1e-12:  # an outdated entry
            continue
        closed.add(k)  # @line L5
        expansions += 1
        if at_goal(q):  # @line L6
            return g, chain(k), expansions  # @line L6
        if shot_every and expansions % shot_every == 0:  # @line L7
            shot = dubins_segments(q, goal, rho)  # @line L7
            if path_free(grid, q, shot):  # @line L7
                cost = g + sum(abs(s) for _, s in shot) + (switch_cost if direction < 0 else 0.0)
                return cost, chain(k) + shot, expansions  # @line L7
        if expansions >= max_expansions:
            return None
        for kappa, d in moves:  # @line L8
            if not motion_free(grid, q, kappa, d * step):  # @line L9
                continue
            q2 = move(q, kappa, d * step)  # @line L9
            k2 = key(q2)  # @line L10
            if k2 in closed:  # @line L10
                continue
            g2 = g + step * (reverse_cost if d < 0 else 1.0)  # @line L11
            if direction != 0.0 and d != direction:  # @line L11
                g2 += switch_cost  # @line L11
            if k2 not in nodes or g2 < nodes[k2][0]:  # @line L12
                nodes[k2] = (g2, q2, k, (kappa, d * step), d)  # @line L12
                heapq.heappush(heap, (g2 + h(q2), counter, k2))  # @line L12
                counter += 1
    return None  # @line L13


def path_cost(segments, reverse_cost=2.0, switch_cost=1.0):
    """The cost of a list of (curvature, signed length) as the search counts it."""
    cost, prev = 0.0, 0.0
    for _, s in segments:
        d = 1.0 if s > 0 else -1.0
        cost += abs(s) * (reverse_cost if d < 0 else 1.0)
        if prev != 0.0 and d != prev:
            cost += switch_cost
        prev = d
    return cost
