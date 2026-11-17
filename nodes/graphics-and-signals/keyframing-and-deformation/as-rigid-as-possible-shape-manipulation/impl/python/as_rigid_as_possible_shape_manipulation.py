# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/as-rigid-as-possible-shape-manipulation/. The authors are listed in prov/6TBSNN.jsonl.
"""As-rigid-as-possible shape manipulation of Igarashi, Moscovich and Hughes (2005).

The shape is a 2D triangle mesh. The user pins some vertices (the handles)
and moves them. The free vertices follow in two least squares steps.

Step 1 (scale free): each vertex of a triangle has fixed coordinates (x, y)
in the frame of the opposite edge, v2 = v0 + x (v1 - v0) + y R90 (v1 - v0).
E1 sums the squared errors of these relations over all triangles and all
three vertex orders. A minimizer keeps each triangle close to a similar
copy of itself, so it allows rotation and uniform scale.

Step 2 (scale adjustment): fit to each triangle of the step 1 result the
closest triangle similar to the rest triangle, and rescale it to the rest
size about its centroid. Then E2 sums, over all triangle edges, the
squared difference between the new edge vector and the fitted edge vector.

E1 and E2 are quadratic, and the handles enter only on the right-hand
side, so the matrices of both steps are factored once with a Cholesky
factorization. Each handle move costs only triangular solves.
"""

import math


def r90(v):
    return (-v[1], v[0])


def cholesky(a):
    """Return the lower triangular L with a = L L^T. Raise ValueError if a is not positive definite."""
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for j in range(n):
        s = a[j][j] - sum(low[j][k] * low[j][k] for k in range(j))
        if s <= 0:
            raise ValueError("the matrix is not positive definite; pin at least two vertices")
        d = math.sqrt(s)
        low[j][j] = d
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / d
    return low


def cholesky_solve(low, b):
    """Solve L L^T x = b."""
    n = len(low)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def local_frame(p0, p1, p2):
    """Return (x, y) with p2 = p0 + x (p1 - p0) + y R90 (p1 - p0)."""
    ex, ey = p1[0] - p0[0], p1[1] - p0[1]
    dx, dy = p2[0] - p0[0], p2[1] - p0[1]
    ll = ex * ex + ey * ey
    return (dx * ex + dy * ey) / ll, (ex * dy - ey * dx) / ll


def _blocks(x, y):
    """Return the 2 by 2 coefficient blocks of v0, v1, v2 in v2 - v0 - x (v1 - v0) - y R90 (v1 - v0)."""
    b0 = ((x - 1.0, -y), (y, x - 1.0))
    b1 = ((-x, y), (-y, -x))
    b2 = ((1.0, 0.0), (0.0, 1.0))
    return b0, b1, b2


class ArapManipulator:
    """Registration (the factorizations) and compilation (the solves) for one mesh and one set of handles."""

    def __init__(self, rest, triangles, handles):
        self.rest = [tuple(map(float, p)) for p in rest]
        self.tris = [tuple(t) for t in triangles]
        self.handles = list(handles)
        n = len(self.rest)
        hset = set(self.handles)
        self.free = [v for v in range(n) if v not in hset]
        self.pos = {v: k for k, v in enumerate(self.free)}

        # Step 1 matrix over 2n unknowns, with index 2 v + c for coordinate c of vertex v.
        g = [[0.0] * (2 * n) for _ in range(2 * n)]
        self.frames = []
        for t in self.tris:
            fr = []
            for o in range(3):
                i0, i1, i2 = t[o], t[(o + 1) % 3], t[(o + 2) % 3]
                x, y = local_frame(self.rest[i0], self.rest[i1], self.rest[i2])  # @line L1
                fr.append((x, y))
                blocks = list(zip((i0, i1, i2), _blocks(x, y)))
                for r in range(2):
                    for va, ba in blocks:
                        for ca in range(2):
                            for vb, bb in blocks:
                                for cb in range(2):
                                    g[2 * va + ca][2 * vb + cb] += ba[r][ca] * bb[r][cb]
            self.frames.append(fr)
        self.g = g
        fidx = [2 * v + c for v in self.free for c in range(2)]
        self.fidx = fidx
        self.g_low = cholesky([[g[a][b] for b in fidx] for a in fidx])  # @line L2

        # Step 2a: per triangle, the 4 by 4 normal matrix of the similar-copy fit.
        self.fit = []
        for t, fr in zip(self.tris, self.frames):
            x, y = fr[0]
            b0, b1, _ = _blocks(x, y)
            # w2 = -(b0) w0 - (b1) w1, from b0 w0 + b1 w1 + w2 = 0.
            a_rows = [
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
                (-b0[0][0], -b0[0][1], -b1[0][0], -b1[0][1]),
                (-b0[1][0], -b0[1][1], -b1[1][0], -b1[1][1]),
            ]
            f = [[sum(r[i] * r[j] for r in a_rows) for j in range(4)] for i in range(4)]
            self.fit.append((a_rows, cholesky(f)))  # @line L3

        # Step 2b: the edge matrix, the same for x and y.
        h = [[0.0] * n for _ in range(n)]
        for t in self.tris:
            for o in range(3):
                i, j = t[o], t[(o + 1) % 3]
                h[i][i] += 1.0
                h[j][j] += 1.0
                h[i][j] -= 1.0
                h[j][i] -= 1.0
        self.h = h
        self.h_low = cholesky([[h[a][b] for b in self.free] for a in self.free])

    def step1(self, targets):
        """Return the scale-free result for the handle targets (a list, one point per handle)."""
        n = len(self.rest)
        q = [0.0] * (2 * n)
        for v, p in zip(self.handles, targets):
            q[2 * v], q[2 * v + 1] = p
        rhs = [-sum(self.g[a][2 * v + c] * q[2 * v + c] for v in self.handles for c in range(2)) for a in self.fidx]
        u = cholesky_solve(self.g_low, rhs)  # @line L4
        out = [None] * n
        for v, p in zip(self.handles, targets):
            out[v] = tuple(map(float, p))
        for k, v in enumerate(self.free):
            out[v] = (u[2 * k], u[2 * k + 1])
        return out

    def fitted_triangles(self, inter):
        """Return, per triangle, the rest-size copy closest to the step 1 triangle."""
        out = []
        for t, (a_rows, f_low) in zip(self.tris, self.fit):
            b = [inter[t[0]][0], inter[t[0]][1], inter[t[1]][0], inter[t[1]][1], inter[t[2]][0], inter[t[2]][1]]
            rhs = [sum(a_rows[r][i] * b[r] for r in range(6)) for i in range(4)]
            z = cholesky_solve(f_low, rhs)  # @line L5
            w = [sum(a_rows[r][i] * z[i] for i in range(4)) for r in range(6)]
            pts = [(w[0], w[1]), (w[2], w[3]), (w[4], w[5])]
            cx = sum(p[0] for p in pts) / 3
            cy = sum(p[1] for p in pts) / 3
            r0, r1 = self.rest[t[0]], self.rest[t[1]]
            k = math.dist(r0, r1) / math.dist(pts[0], pts[1])
            out.append([(cx + k * (p[0] - cx), cy + k * (p[1] - cy)) for p in pts])
        return out

    def step2(self, targets, fitted):
        """Return the final positions from the fitted triangles."""
        n = len(self.rest)
        out = [None] * n
        for v, p in zip(self.handles, targets):
            out[v] = tuple(map(float, p))
        coords = []
        for c in range(2):
            b = [0.0] * n
            for t, w in zip(self.tris, fitted):
                for o in range(3):
                    i, j = t[o], t[(o + 1) % 3]
                    e = w[o][c] - w[(o + 1) % 3][c]
                    b[i] += e
                    b[j] -= e
            rhs = [b[a] - sum(self.h[a][v] * out[v][c] for v in self.handles) for a in self.free]
            coords.append(cholesky_solve(self.h_low, rhs))  # @line L6
        for k, v in enumerate(self.free):
            out[v] = (coords[0][k], coords[1][k])
        return out

    def solve(self, targets):
        """Return (step 1 result, final result) for the handle targets."""
        inter = self.step1(targets)
        final = self.step2(targets, self.fitted_triangles(inter))
        return inter, final  # @line L7

    def energy1(self, verts):
        total = 0.0
        for t, fr in zip(self.tris, self.frames):
            for o in range(3):
                i0, i1, i2 = t[o], t[(o + 1) % 3], t[(o + 2) % 3]
                x, y = fr[o]
                p0, p1, p2 = verts[i0], verts[i1], verts[i2]
                e = (p1[0] - p0[0], p1[1] - p0[1])
                re = r90(e)
                dx = p2[0] - p0[0] - x * e[0] - y * re[0]
                dy = p2[1] - p0[1] - x * e[1] - y * re[1]
                total += dx * dx + dy * dy
        return total

    def energy2(self, verts, fitted):
        total = 0.0
        for t, w in zip(self.tris, fitted):
            for o in range(3):
                i, j = t[o], t[(o + 1) % 3]
                for c in range(2):
                    d = (verts[i][c] - verts[j][c]) - (w[o][c] - w[(o + 1) % 3][c])
                    total += d * d
        return total


def grid_mesh(nx, ny, size=1.0):
    """Return (vertices, triangles) of an nx by ny grid of squares, each split into two triangles."""
    verts = [(i * size, j * size) for j in range(ny + 1) for i in range(nx + 1)]
    tris = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            b, c, d = a + 1, a + nx + 2, a + nx + 1
            tris.append((a, b, c))
            tris.append((a, c, d))
    return verts, tris
