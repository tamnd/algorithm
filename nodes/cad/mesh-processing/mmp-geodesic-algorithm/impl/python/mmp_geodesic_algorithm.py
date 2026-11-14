# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mmp-geodesic-algorithm/. The authors are listed in prov/14F19Q.jsonl.

"""Exact geodesic distances on a triangle mesh by the Mitchell-Mount-Papadimitriou method.

This is the window form of the method described by Surazhsky, Surazhsky,
Kirsanov, Gortler and Hoppe (2005). A window lives on an edge (p, q), p < q,
and looks into one face h of that edge. In the frame of (edge, h) the vertex p
is at (0, 0), q is at (|pq|, 0) and the third vertex of h has y > 0. The window
holds an interval [b0, b1] of the edge, a pseudo-source s = (sx, sy) with
sy < 0 (an unfolded image of the source or of a saddle vertex) and the
distance sigma from the source to that pseudo-source. On the interval, the
distance is sigma + |(x, 0) - s|.

Events are taken from a priority queue in order of distance. A window event
pushes the window across its face onto the two other edges. A vertex event at
a source, a saddle vertex (angle sum above 2 pi), a flat vertex (angle sum
exactly 2 pi) or a border vertex makes that vertex a pseudo-source. New windows are trimmed against the windows already on
the same edge, so that each point of an edge keeps only the windows that give
it the smallest distance.
"""

import heapq
from math import acos, hypot, pi, sqrt
from typing import Optional, Sequence

QUEUED, DONE, DEAD = 0, 1, 2


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _norm(a):
    return sqrt(_dot(a, a))


class Window:
    __slots__ = ("edge", "face", "b0", "b1", "sx", "sy", "sigma", "state", "ver")

    def __init__(self, edge, face, b0, b1, sx, sy, sigma):
        self.edge, self.face, self.b0, self.b1 = edge, face, b0, b1
        self.sx, self.sy, self.sigma = sx, sy, sigma
        self.state, self.ver = QUEUED, 0

    def at(self, x: float) -> float:
        return self.sigma + hypot(x - self.sx, self.sy)

    def key(self) -> float:
        if self.b0 <= self.sx <= self.b1:
            return self.sigma - self.sy
        return min(self.at(self.b0), self.at(self.b1))


def _crossing_roots(w: Window, x: Window, lo: float, hi: float) -> list[float]:
    """The x in (lo, hi) where the distance functions of w and x may be equal."""
    d = x.sigma - w.sigma                         # sqrt(A) - sqrt(B) = d with A, B the squared distances
    hw, hx = w.sy * w.sy, x.sy * x.sy
    p = -2 * (w.sx - x.sx)                        # A - B - d^2 = p t + q
    q = w.sx * w.sx - x.sx * x.sx + hw - hx - d * d
    a2 = p * p - 4 * d * d                        # (p t + q)^2 = 4 d^2 B
    a1 = 2 * p * q + 8 * d * d * x.sx
    a0 = q * q - 4 * d * d * (x.sx * x.sx + hx)
    scale = max(abs(a2), abs(a1), abs(a0), 1e-300)
    roots = []
    if abs(d) <= 1e-13 * (abs(w.sigma) + abs(x.sigma) + 1):
        if p != 0:                                # equal sigma: the equation is linear, p t + q = 0
            roots.append(-(q + d * d) / p)
    elif abs(a2) <= 1e-12 * scale:
        if abs(a1) > 1e-12 * scale:
            roots.append(-a0 / a1)
    else:
        disc = a1 * a1 - 4 * a2 * a0
        if disc >= -1e-12 * a1 * a1:              # a double root can come out slightly negative
            r = sqrt(max(disc, 0.0))
            roots += [(-a1 - r) / (2 * a2), (-a1 + r) / (2 * a2)]
    return sorted(t for t in roots if lo < t < hi)


def _minus(lo: float, hi: float, cuts: list[tuple[float, float]], tol: float) -> list[tuple[float, float]]:
    """[lo, hi] with the intervals in cuts removed, dropping pieces shorter than tol."""
    pieces = [(lo, hi)]
    for c0, c1 in cuts:
        nxt = []
        for a, b in pieces:
            if c1 <= a or c0 >= b:
                nxt.append((a, b))
                continue
            if c0 > a:
                nxt.append((a, c0))
            if c1 < b:
                nxt.append((c1, b))
        pieces = nxt
    return [(a, b) for a, b in pieces if b - a > tol]


def mmp_geodesic(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]], sources: Sequence[int],
                 stats: Optional[dict] = None) -> list[float]:
    """Exact geodesic distance from the nearest source to every vertex of a manifold triangle mesh."""
    P = [tuple(map(float, p)) for p in points]
    n = len(P)
    F = [tuple(f) for f in faces]
    edge_faces: dict[tuple[int, int], list[int]] = {}
    for fid, f in enumerate(F):
        for k in range(3):
            a, b = f[k], f[(k + 1) % 3]
            edge_faces.setdefault((min(a, b), max(a, b)), []).append(fid)
    vfaces = [[] for _ in range(n)]
    angle = [0.0] * n
    for fid, f in enumerate(F):
        for k in range(3):
            v, a, b = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
            vfaces[v].append(fid)
            x, y = _sub(P[a], P[v]), _sub(P[b], P[v])
            angle[v] += acos(max(-1.0, min(1.0, _dot(x, y) / (_norm(x) * _norm(y)))))
    border = [False] * n
    for (a, b), fs in edge_faces.items():
        if len(fs) == 1:
            border[a] = border[b] = True
    # A shortest path can only pass through a border vertex or a vertex with angle sum at least 2 pi. Flat
    # vertices (exactly 2 pi) are included, so that a path straight through one is also carried.
    pseudo = [border[v] or angle[v] > 2 * pi - 1e-9 for v in range(n)]
    is_source = [False] * n
    for s in sources:
        is_source[s] = True

    frames: dict[tuple[int, int, int], tuple[float, float, float]] = {}

    def third(fid, e):
        return next(w for w in F[fid] if w != e[0] and w != e[1])

    def frame(e, fid):
        """(|pq|, x, y) of the third vertex of face fid in the frame of edge e = (p, q)."""
        key = (e[0], e[1], fid)
        if key not in frames:
            p, q, r = P[e[0]], P[e[1]], P[third(fid, e)]
            L = _norm(_sub(q, p))
            u = tuple(c / L for c in _sub(q, p))
            w = _sub(r, p)
            x = _dot(w, u)
            frames[key] = (L, x, sqrt(max(_dot(w, w) - x * x, 0.0)))
        return frames[key]

    def other_face(e, fid):
        return next((g for g in edge_faces[e] if g != fid), None)

    dist = [float("inf")] * n
    spawned = [False] * n
    windows: dict[tuple[int, int], list[Window]] = {e: [] for e in edge_faces}
    heap: list = []
    counter = [0, 0]                                             # heap tie breaker, windows made

    def push(key, item, ver):
        counter[0] += 1
        heapq.heappush(heap, (key, counter[0], item, ver))

    def update(v, d):
        if d < dist[v]:
            dist[v] = d
            push(d, v, -1)

    def insert(e, fid, b0, b1, sx, sy, sigma):
        L = frame(e, fid)[0]
        tol = 1e-10 * L
        b0, b1 = max(b0, 0.0), min(b1, L)
        if b0 <= tol:
            update(e[0], sigma + hypot(sx, sy))
        if b1 >= L - tol:
            update(e[1], sigma + hypot(L - sx, sy))
        if b1 - b0 <= tol:
            return
        w = Window(e, fid, b0, b1, sx, sy, sigma)
        mine = [(b0, b1)]
        for x in list(windows[e]):
            if x.state == DEAD or x.b1 <= b0 or x.b0 >= b1:
                continue
            better = []                                          # where w is strictly better than x
            worse = []                                           # where x is at least as good as w
            for m0, m1 in mine:
                lo, hi = max(m0, x.b0), min(m1, x.b1)
                if hi - lo <= tol:
                    continue
                cuts = [lo] + _crossing_roots(w, x, lo, hi) + [hi]
                for c0, c1 in zip(cuts, cuts[1:]):
                    mid = (c0 + c1) / 2
                    (better if w.at(mid) < x.at(mid) - tol else worse).append((c0, c1))
            if worse:
                mine = [piece for m0, m1 in mine for piece in _minus(m0, m1, worse, tol)]
            if better:
                rest = _minus(x.b0, x.b1, better, tol)
                if not rest:
                    x.state = DEAD
                    windows[e].remove(x)
                else:
                    x.b0, x.b1 = rest[0]
                    x.ver += 1
                    if x.state == QUEUED:
                        push(x.key(), x, x.ver)
                    for a, b in rest[1:]:
                        y = Window(e, x.face, a, b, x.sx, x.sy, x.sigma)
                        y.state = x.state
                        windows[e].append(y)
                        if y.state == QUEUED:
                            push(y.key(), y, y.ver)
            if not mine:
                return
        for a, b in mine:
            y = Window(e, fid, a, b, sx, sy, sigma)
            counter[1] += 1
            windows[e].append(y)
            push(y.key(), y, y.ver)

    def spawn(v):
        """Make v a pseudo-source: one window on the far edge of each face around v."""
        for g in vfaces[v]:
            f = F[g]
            a, b = (w for w in f if w != v)
            e = (min(a, b), max(a, b))
            L, x, y = frame(e, g)                                # v is the third vertex of g
            h = other_face(e, g)
            if h is None:
                update(e[0], dist[v] + hypot(x, y))
                update(e[1], dist[v] + hypot(L - x, y))
            else:
                insert(e, h, 0.0, L, x, -y, dist[v])

    def propagate(w):
        e, h = w.edge, w.face
        L, rx, ry = frame(e, h)
        r = third(h, e)
        sx, sy = w.sx, w.sy

        def g(px, py):                                           # where the ray from s to (px, py) meets y = 0
            return sx + (px - sx) * (-sy) / (py - sy)

        gr = g(rx, ry)
        tol = 1e-10 * L
        if w.b0 - tol <= gr <= w.b1 + tol:
            update(r, w.sigma + hypot(rx - sx, ry - sy))         # the third vertex is lit by the window
        for (i, (ax, ay), ga), (j, (bx, by), gb), (ox, oy) in (
                ((e[0], (0.0, 0.0), 0.0), (r, (rx, ry), gr), (L, 0.0)),
                ((r, (rx, ry), gr), (e[1], (L, 0.0), L), (0.0, 0.0))):
            ne = (min(i, j), max(i, j))
            h2 = other_face(ne, h)
            if h2 is None:
                continue
            lo, hi = max(w.b0, min(ga, gb)), min(w.b1, max(ga, gb))
            if hi - lo <= tol:
                continue
            ex, ey = bx - ax, by - ay

            def at(xv):                                          # the point of segment a-b on the ray through (xv, 0)
                if xv == ga:
                    return 0.0
                if xv == gb:
                    return 1.0
                dx, dy = xv - sx, -sy
                wx, wy = ax - sx, ay - sy
                return (wx * dy - wy * dx) / (dx * ey - dy * ex)

            t0, t1 = at(lo), at(hi)
            if i > j:
                (ax, ay), (bx, by), t0, t1 = (bx, by), (ax, ay), 1 - t0, 1 - t1
            ln = hypot(bx - ax, by - ay)
            ux, uy = (bx - ax) / ln, (by - ay) / ln
            vx, vy = -uy, ux
            if (ox - ax) * vx + (oy - ay) * vy > 0:              # y must point away from face h
                vx, vy = -vx, -vy
            nsx = (sx - ax) * ux + (sy - ay) * uy
            nsy = (sx - ax) * vx + (sy - ay) * vy
            if nsy > -1e-12 * ln:
                continue                                         # the rays only graze this edge
            insert(ne, h2, min(t0, t1) * ln, max(t0, t1) * ln, nsx, nsy, w.sigma)

    for s in sources:                                            # @line L1
        update(s, 0.0)
    while heap:                                                  # @line L2
        key, _, item, ver = heapq.heappop(heap)
        if ver == -1:
            v = item
            if key > dist[v] or spawned[v]:
                continue
            if is_source[v] or pseudo[v]:                        # @line L3
                spawned[v] = True
                spawn(v)
        else:
            if item.state != QUEUED or item.ver != ver:
                continue
            item.state = DONE
            propagate(item)                                      # @line L4 @line L5
    if stats is not None:
        stats["windows"] = counter[1]
        stats["alive"] = sum(len(ws) for ws in windows.values())
    return dist                                                  # @line L6
