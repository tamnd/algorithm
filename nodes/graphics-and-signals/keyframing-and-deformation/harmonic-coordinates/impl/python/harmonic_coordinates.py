# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harmonic-coordinates/. The authors are listed in prov/XS2ZCM.jsonl.
"""Harmonic coordinates of a 2D cage (Joshi, Meyer, DeRose, Green and Sanocki 2007).

The coordinate h_i of cage vertex i is the solution of the Laplace equation
inside the cage, with the boundary value equal to the piecewise linear hat
function of vertex i on the cage boundary. This module solves the equation
on a uniform grid with the Shortley-Weller five-point stencil: an arm of
the stencil that leaves the cage is cut at the first boundary crossing, and
the stencil weights use the shorter arm length. The stencil is exact on
quadratic functions, so the discrete coordinates reproduce linear
functions exactly at the grid nodes. The matrix is an M-matrix, so the
coordinates are nonnegative and the LU factorization needs no pivoting.

The cage is a simple polygon with the vertices in counterclockwise order.
"""

import math


def _cross(ax, ay, bx, by):
    return ax * by - ay * bx


def point_in_polygon(p, poly):
    """Even-odd rule. The result on the boundary is not defined; callers test that first."""
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def nearest_on_boundary(p, poly):
    """Return (distance, edge index, s) of the boundary point closest to p."""
    best = (math.inf, 0, 0.0)
    n = len(poly)
    for k in range(n):
        (ax, ay), (bx, by) = poly[k], poly[(k + 1) % n]
        dx, dy = bx - ax, by - ay
        dd = dx * dx + dy * dy
        s = min(1.0, max(0.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / dd))
        d = math.hypot(p[0] - ax - s * dx, p[1] - ay - s * dy)
        if d < best[0]:
            best = (d, k, s)
    return best


def hat_values(poly, k, s):
    """Return the boundary data of all n coordinates at the point with parameter s on edge k."""
    n = len(poly)
    out = [0.0] * n
    out[k] += 1.0 - s
    out[(k + 1) % n] += s
    return out


def first_crossing(p, q, poly, eps=1e-12):
    """Return (t, edge index, s) of the first crossing of the segment p + t (q - p), t in (0, 1].

    Edges parallel to the segment are skipped; their end points are found
    through the neighbouring edges. Return None if there is no crossing.
    """
    best = None
    n = len(poly)
    rx, ry = q[0] - p[0], q[1] - p[1]
    for k in range(n):
        (ax, ay), (bx, by) = poly[k], poly[(k + 1) % n]
        ex, ey = bx - ax, by - ay
        den = _cross(rx, ry, ex, ey)
        if abs(den) < eps * (abs(rx) + abs(ry)) * (abs(ex) + abs(ey)):
            continue
        wx, wy = ax - p[0], ay - p[1]
        t = _cross(wx, wy, ex, ey) / den
        s = _cross(wx, wy, rx, ry) / den
        if -eps <= s <= 1 + eps and eps < t <= 1 + eps:
            if best is None or t < best[0]:
                best = (min(t, 1.0), k, min(1.0, max(0.0, s)))
    return best


class BandLU:
    """LU factorization without pivoting of a band matrix, for M-matrices.

    The matrix is given as rows of {column: value}. Fill-in stays inside
    the band, so the cost is O(N p q) for the factorization and O(N (p + q))
    for each solve.
    """

    def __init__(self, rows):
        self.n = n = len(rows)
        p = q = 0
        for i, row in enumerate(rows):
            for j in row:
                p = max(p, i - j)
                q = max(q, j - i)
        self.p, self.q = p, q
        width = p + q + 1
        band = [[0.0] * width for _ in range(n)]
        for i, row in enumerate(rows):
            for j, v in row.items():
                band[i][j - i + p] += v
        for k in range(n):
            piv = band[k][p]
            if piv <= 0:
                raise ValueError("a pivot is not positive; the matrix is not an M-matrix")
            for i in range(k + 1, min(n, k + p + 1)):
                lik = band[i][k - i + p]
                if lik == 0:
                    continue
                lik /= piv
                band[i][k - i + p] = lik
                ri, rk = band[i], band[k]
                for j in range(k + 1, min(n, k + q + 1)):
                    ukj = rk[j - k + p]
                    if ukj != 0:
                        ri[j - i + p] -= lik * ukj
        self.band = band

    def solve(self, b):
        n, p, q, band = self.n, self.p, self.q, self.band
        y = list(b)
        for i in range(n):
            s = y[i]
            for k in range(max(0, i - p), i):
                s -= band[i][k - i + p] * y[k]
            y[i] = s
        for i in range(n - 1, -1, -1):
            s = y[i]
            for j in range(i + 1, min(n, i + q + 1)):
                s -= band[i][j - i + p] * y[j]
            y[i] = s / band[i][p]
        return y


class HarmonicCoordinates:
    """Discrete harmonic coordinates of a 2D cage on a grid with n_cells cells across."""

    def __init__(self, cage, n_cells=32, on_boundary=1e-9):
        self.cage = [tuple(map(float, c)) for c in cage]
        n = len(self.cage)
        xs = [c[0] for c in self.cage]
        ys = [c[1] for c in self.cage]
        size = max(max(xs) - min(xs), max(ys) - min(ys))
        self.h = h = size / n_cells
        self.x0, self.y0 = min(xs) - h, min(ys) - h
        self.nx = int(math.ceil((max(xs) - self.x0) / h)) + 2
        self.ny = int(math.ceil((max(ys) - self.y0) / h)) + 2
        tol = on_boundary * size

        # L1: the nodes strictly inside the cage are the unknowns.
        self.index = {}
        for j in range(self.ny):  # @line L1
            for i in range(self.nx):
                p = self.node(i, j)
                if nearest_on_boundary(p, self.cage)[0] > tol and point_in_polygon(p, self.cage):
                    self.index[(i, j)] = len(self.index)

        rows, rhs = [], []
        for (i, j), r in sorted(self.index.items(), key=lambda kv: kv[1]):
            p = self.node(i, j)
            row, b = {}, [0.0] * n
            diag = 0.0
            arms = {}
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                q = self.node(i + di, j + dj)
                hit = first_crossing(p, q, self.cage)  # @line L2
                if hit is not None and (hit[0] < 1.0 or (i + di, j + dj) not in self.index):
                    t, k, s = hit
                    arms[(di, dj)] = (t * h, hat_values(self.cage, k, s))
                elif (i + di, j + dj) in self.index:
                    arms[(di, dj)] = (h, self.index[(i + di, j + dj)])
                else:
                    d, k, s = nearest_on_boundary(q, self.cage)
                    arms[(di, dj)] = (h, hat_values(self.cage, k, s))
            for lo, hi in (((-1, 0), (1, 0)), ((0, -1), (0, 1))):
                hl, hr = arms[lo][0], arms[hi][0]
                for arm, length in ((arms[lo], hl), (arms[hi], hr)):
                    a = 2.0 / (length * (hl + hr))  # @line L3
                    diag += a
                    target = arm[1]
                    if isinstance(target, int):
                        row[target] = row.get(target, 0.0) - a
                    else:
                        for v in range(n):
                            b[v] += a * target[v]  # @line L4
            row[r] = diag
            rows.append(row)
            rhs.append(b)
        self.rows, self.rhs = rows, rhs

        lu = BandLU(rows)  # @line L5
        cols = []
        for v in range(n):
            cols.append(lu.solve([b[v] for b in rhs]))  # @line L6
        self.values = [[cols[v][r] for v in range(n)] for r in range(len(rows))]  # @line L7

    def node(self, i, j):
        return (self.x0 + i * self.h, self.y0 + j * self.h)

    def node_coordinates(self, i, j):
        """Return the n coordinates at grid node (i, j).

        Nodes outside the cage or on its boundary take the boundary data at
        the closest boundary point.
        """
        r = self.index.get((i, j))
        if r is not None:
            return list(self.values[r])
        _, k, s = nearest_on_boundary(self.node(i, j), self.cage)
        return hat_values(self.cage, k, s)

    def coordinates(self, p):
        """Return the n coordinates at the point p by bilinear interpolation of the nodes."""
        fx = (p[0] - self.x0) / self.h
        fy = (p[1] - self.y0) / self.h
        i = min(max(int(math.floor(fx)), 0), self.nx - 2)
        j = min(max(int(math.floor(fy)), 0), self.ny - 2)
        a, b = fx - i, fy - j
        out = [0.0] * len(self.cage)
        for di, dj, w in ((0, 0, (1 - a) * (1 - b)), (1, 0, a * (1 - b)), (0, 1, (1 - a) * b), (1, 1, a * b)):
            if w != 0:
                for v, c in enumerate(self.node_coordinates(i + di, j + dj)):
                    out[v] += w * c
        return out

    def deform(self, p, new_cage):
        """Return sum_i h_i(p) c'_i."""
        w = self.coordinates(p)
        return (sum(wi * c[0] for wi, c in zip(w, new_cage)), sum(wi * c[1] for wi, c in zip(w, new_cage)))  # @line L8


def gauss_seidel(rows, b, iters=5000, tol=1e-13):
    """Solve the same system by Gauss-Seidel iteration. Used by the tests as a second method."""
    n = len(rows)
    x = [0.0] * n
    for _ in range(iters):
        change = 0.0
        for i, row in enumerate(rows):
            s = b[i]
            for j, v in row.items():
                if j != i:
                    s -= v * x[j]
            new = s / row[i]
            change = max(change, abs(new - x[i]))
            x[i] = new
        if change < tol:
            break
    return x
