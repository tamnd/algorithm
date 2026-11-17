# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/as-rigid-as-possible-shape-interpolation/. The authors are listed in prov/B6HGFM.jsonl.
"""As-rigid-as-possible shape interpolation of 2D triangulations (Alexa, Cohen-Or and Levin 2000).

The source and the target are two lists of 2D points with the same triangles
(compatible triangulations). For each triangle f, A_f is the linear part of
the affine map that takes the source triangle to the target triangle. Its
polar decomposition A_f = R(gamma_f) S_f, with a rotation R and a symmetric
S, gives the interpolated matrix

    A_f(t) = R(t gamma_f) ((1 - t) I + t S_f).

The angles gamma_f are made consistent first: walking over the triangles
that share an edge, each angle is moved by a multiple of 2 pi to within pi of
its neighbour's angle (Baxter, Barla and Anjyo 2008). The vertices V(t)
minimize sum_f |B_f(V) - A_f(t)|_F^2, where B_f(V) is the linear part of the
affine map that takes the source triangle f to the triangle f of V. Vertex 0
is fixed at (1 - t) p_0 + t q_0. The energy is quadratic, the x and the y
coordinates separate, and both use the same matrix H, which does not depend
on t. H is inverted once.
"""

import math
from collections import deque

from anim import inv, lerp, matvec, mul, polar, rot2


def triangle_edges(points, tri):
    """Return the 2 by 2 matrix whose columns are the edges v_j - v_i and v_k - v_i of tri = (i, j, k)."""
    i, j, k = tri
    return [
        [points[j][0] - points[i][0], points[k][0] - points[i][0]],
        [points[j][1] - points[i][1], points[k][1] - points[i][1]],
    ]


def affine_part(source, target, tri):
    """Return the linear part of the affine map that takes triangle tri of source to that of target."""
    return mul(triangle_edges(target, tri), inv(triangle_edges(source, tri)))


def triangle_neighbours(triangles):
    """Return, for each triangle, the list of triangles that share an edge with it."""
    by_edge = {}
    for f, tri in enumerate(triangles):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            by_edge.setdefault((min(a, b), max(a, b)), []).append(f)
    nb = [[] for _ in triangles]
    for fs in by_edge.values():
        for f in fs:
            nb[f].extend(g for g in fs if g != f)
    return nb


def consistent_angles(angles, triangles):
    """Shift each angle by a multiple of 2 pi so that it is within pi of the neighbour it is reached from."""
    nb = triangle_neighbours(triangles)
    out = list(angles)
    seen = [False] * len(out)
    for start in range(len(out)):
        if seen[start]:
            continue
        seen[start] = True
        queue = deque([start])
        while queue:
            f = queue.popleft()
            for g in nb[f]:
                if not seen[g]:
                    out[g] += 2.0 * math.pi * round((out[f] - out[g]) / (2.0 * math.pi))
                    seen[g] = True
                    queue.append(g)
    return out


class ARAPShapeInterpolation:
    """Interpolate between two compatible 2D triangulations; call the object with t in [0, 1]."""

    def __init__(self, source, target, triangles, consistent=True):
        n = len(source)
        if len(target) != n or n < 3 or not triangles:
            raise ValueError("source and target need the same three or more points and at least one triangle")
        self.source = [tuple(map(float, p)) for p in source]
        self.target = [tuple(map(float, p)) for p in target]
        self.triangles = [tuple(tri) for tri in triangles]
        self.stretch = []
        angles = []
        # Each row is a linear form on one coordinate of the vertices: entry (f, c) of B_f(V).
        self.rows = []
        for f, tri in enumerate(self.triangles):  # @line L1
            a = affine_part(self.source, self.target, tri)  # @line L2
            r, s = polar(a)  # @line L3
            angles.append(math.atan2(r[1][0], r[0][0]))
            self.stretch.append(s)
            m = inv(triangle_edges(self.source, tri))
            i, j, k = tri
            for c in range(2):
                self.rows.append((f, c, ((i, -(m[0][c] + m[1][c])), (j, m[0][c]), (k, m[1][c]))))
        self.angles = consistent_angles(angles, self.triangles) if consistent else angles  # @line L4
        h = [[0.0] * n for _ in range(n)]
        for _, _, coef in self.rows:  # @line L5
            for va, ca in coef:
                for vb, cb in coef:
                    h[va][vb] += ca * cb
        self._h0 = [h[i][0] for i in range(1, n)]
        try:
            self._hinv = inv([row[1:] for row in h[1:]])
        except ValueError:
            raise ValueError("the triangulation must be connected") from None

    def triangle_targets(self, t):
        """Return the matrices A_f(t) = R(t gamma_f) ((1 - t) I + t S_f)."""
        out = []
        for g, s in zip(self.angles, self.stretch):
            blend = [[(1 - t) + t * s[0][0], t * s[0][1]], [t * s[1][0], (1 - t) + t * s[1][1]]]
            out.append(mul(rot2(t * g), blend))  # @line L6
        return out

    def __call__(self, t):
        n = len(self.source)
        a = self.triangle_targets(t)
        v0 = lerp(self.source[0], self.target[0], t)  # @line L7
        coords = []
        for r in range(2):  # @line L8
            b = [0.0] * n
            for f, c, coef in self.rows:
                val = a[f][r][c]
                for v, cv in coef:
                    b[v] += cv * val
            rhs = [b[i] - self._h0[i - 1] * v0[r] for i in range(1, n)]
            coords.append([v0[r]] + list(matvec(self._hinv, rhs)))
        return [(x, y) for x, y in zip(coords[0], coords[1])]  # @line L9

    def energy(self, points, t):
        """Return sum_f |B_f(points) - A_f(t)|_F^2."""
        a = self.triangle_targets(t)
        e = 0.0
        for f, c, coef in self.rows:
            for r in range(2):
                e += (sum(cv * points[v][r] for v, cv in coef) - a[f][r][c]) ** 2
        return e
