# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pht-spline/. The authors are listed in prov/BQ9V8S.jsonl.

"""PHT-splines (Deng, Chen, Li, Hu, Tong, Yang and Feng), in exact arithmetic.

The domain is [0, n]^2. A cell (l, i, j) is the square of side h = 2^-l with
lower left corner (i h, j h). The mesh starts with the n x n cells of level 0,
and step k + 1 splits some leaf cells of level k into four by a cross. This
is a hierarchical T-mesh.

A function of S(3, 3, 1, 1, T), bicubic on each leaf cell and C^1, is stored
by its Hermite data (f, f_x, f_y, f_xy) at the vertices of the mesh. On each
leaf cell it is the bicubic Hermite interpolant of the data at the four
corners. A vertex is a basis vertex if it lies on the boundary or is an
interior crossing; the other interior vertices are T-junctions, which lie
inside a side of a leaf cell.

Each basis vertex v of level l carries four basis functions. Their data at v
are the products of the values and derivatives at v of the two C^1 cubic
B-splines with knots (v - h, v - h, v, v, v + h) and (v - h, v, v, v + h,
v + h), h = 2^-l, in each direction. At a refinement the old functions are
subdivided on the split cells and their data at the new basis vertices are
set to zero, and four new functions are added at each new basis vertex.
"""

from fractions import Fraction

ZERO = (Fraction(0),) * 4


def hermite_1d(a, b, x):
    """Values and derivatives at x of the cubic Hermite shapes on [a, b].

    The shapes are, in order: value at a, slope at a, value at b, slope at b.
    """
    h = b - a
    t = (x - a) / h
    return [
        (2 * t**3 - 3 * t**2 + 1, (6 * t**2 - 6 * t) / h),
        (h * (t**3 - 2 * t**2 + t), 3 * t**2 - 4 * t + 1),
        (-2 * t**3 + 3 * t**2, (-6 * t**2 + 6 * t) / h),
        (h * (t**3 - t**2), 3 * t**2 - 2 * t),
    ]


def cell_box(cell):
    l, i, j = cell
    h = Fraction(1, 2**l)
    return i * h, (i + 1) * h, j * h, (j + 1) * h


def bicubic(corner_data, box, x, y):
    """(f, f_x, f_y, f_xy) at (x, y) of the bicubic Hermite interpolant on the box.

    corner_data[(cx, cy)] is the data at the corner, cx, cy in {0, 1}.
    """
    x0, x1, y0, y1 = box
    X, Y = hermite_1d(x0, x1, x), hermite_1d(y0, y1, y)
    out = [Fraction(0)] * 4
    for cx in (0, 1):
        for cy in (0, 1):
            d = corner_data[(cx, cy)]
            vx, sx = X[2 * cx], X[2 * cx + 1]  # value shape, slope shape: (value, derivative)
            vy, sy = Y[2 * cy], Y[2 * cy + 1]
            for k, (px, py) in enumerate(((vx, vy), (sx, vy), (vx, sy), (sx, sy))):
                out[0] += d[k] * px[0] * py[0]
                out[1] += d[k] * px[1] * py[0]
                out[2] += d[k] * px[0] * py[1]
                out[3] += d[k] * px[1] * py[1]
    return tuple(out)


class PHT:
    def __init__(self, n):
        self.n, self.K = n, 0
        self.leaves = {(0, i, j) for i in range(n) for j in range(n)}
        self.classify()
        self.vlevel = {v: 0 for v in self.basis_vertices}
        self.funcs = {(v, a, b): {v: self.vertex_data(v, a, b)} for v in sorted(self.basis_vertices) for a in (0, 1) for b in (0, 1)}

    # --- the mesh -------------------------------------------------------
    def corners(self, cell):
        x0, x1, y0, y1 = cell_box(cell)
        return {(0, 0): (x0, y0), (1, 0): (x1, y0), (0, 1): (x0, y1), (1, 1): (x1, y1)}

    def classify(self):
        """Split the vertices into boundary, crossing and T-junction vertices."""
        self.vertices = {p for c in self.leaves for p in self.corners(c).values()}
        self.boundary = {v for v in self.vertices if v[0] in (0, self.n) or v[1] in (0, self.n)}
        self.tjunctions = {}
        for v in self.vertices - self.boundary:
            for l in range(self.K + 1):
                s = 2**l
                x, y = v[0] * s, v[1] * s
                if x.denominator == 1 and y.denominator != 1:
                    hosts = [(l, int(x) - 1, y.numerator // y.denominator), (l, int(x), y.numerator // y.denominator)]
                elif y.denominator == 1 and x.denominator != 1:
                    hosts = [(l, x.numerator // x.denominator, int(y) - 1), (l, x.numerator // x.denominator, int(y))]
                else:
                    continue
                host = [c for c in hosts if c in self.leaves]
                if host:
                    self.tjunctions[v] = host[0]
                    break
        self.crossings = self.vertices - self.boundary - set(self.tjunctions)
        self.basis_vertices = self.boundary | self.crossings

    def locate(self, x, y):
        for l in range(self.K + 1):
            s = 2**l
            i = min(int(x * s), self.n * s - 1)
            j = min(int(y * s), self.n * s - 1)
            if (l, i, j) in self.leaves:
                return (l, i, j)
        raise ValueError("point outside the domain")

    # --- functions --------------------------------------------------------
    def vertex_data(self, v, a, b):
        """Data at v of the basis function (a, b) of the basis vertex v."""
        h = Fraction(1, 2 ** self.vlevel[v])

        def one(u, c):
            hm = h if u > 0 else Fraction(0)
            hp = h if u < self.n else Fraction(0)
            return (hp / (hm + hp), -3 / (hm + hp)) if c == 0 else (hm / (hm + hp), 3 / (hm + hp))

        (vx, dx), (vy, dy) = one(v[0], a), one(v[1], b)
        return (vx * vy, dx * vy, vx * dy, dx * dy)

    def cell_values(self, data, cell, x, y):
        cs = self.corners(cell)
        return bicubic({k: data.get(p, ZERO) for k, p in cs.items()}, cell_box(cell), x, y)

    def evaluate(self, data, x, y):
        """(f, f_x, f_y, f_xy) of the function with the given vertex data, at (x, y)."""
        return self.cell_values(data, self.locate(x, y), x, y)

    def refine(self, cells):
        """One refinement step: split leaf cells of the finest level by a cross."""
        cells = set(cells)
        if any(c not in self.leaves or c[0] != self.K for c in cells):
            raise ValueError("only leaf cells of the finest level are split")
        old_vertices = self.vertices
        for l, i, j in cells:  # @line L1
            self.leaves.remove((l, i, j))
            self.leaves |= {(l + 1, 2 * i + a, 2 * j + b) for a in (0, 1) for b in (0, 1)}
        self.K += 1
        self.classify()
        new_basis = sorted(v for v in self.basis_vertices if v not in self.vlevel)  # @line L2
        for v in new_basis:
            self.vlevel[v] = self.K
        for data in self.funcs.values():  # @line L3
            add = {}
            for c in cells:  # @line L4
                cs = self.corners(c)
                if not any(data.get(p, ZERO) != ZERO for p in cs.values()):
                    continue
                x0, x1, y0, y1 = cell_box(c)
                for w in ((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1), (x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2), ((x0 + x1) / 2, (y0 + y1) / 2):
                    if w not in old_vertices:
                        add[w] = self.cell_values(data, c, w[0], w[1])
            data.update({w: d for w, d in add.items() if d != ZERO})
            for v in new_basis:  # @line L5
                data.pop(v, None)
        for v in new_basis:  # @line L6
            for a in (0, 1):
                for b in (0, 1):
                    self.funcs[(v, a, b)] = {v: self.vertex_data(v, a, b)}
        return new_basis

    def coefficients(self, data):
        """Coefficients on the basis of a spline given by its data at the basis vertices.

        For each basis vertex the four coefficients are the B-spline coefficients
        c = f + s f_x + t f_y + s t f_xy, with s in {-h_minus/3, h_plus/3}.
        """
        out = {}
        for v in sorted(self.basis_vertices):
            h = Fraction(1, 2 ** self.vlevel[v])
            f, fx, fy, fxy = data.get(v, ZERO)
            zero = Fraction(0)
            sx = (-(h if v[0] > 0 else zero) / 3, (h if v[0] < self.n else zero) / 3)
            sy = (-(h if v[1] > 0 else zero) / 3, (h if v[1] < self.n else zero) / 3)
            for a in (0, 1):
                for b in (0, 1):
                    out[(v, a, b)] = f + sx[a] * fx + sy[b] * fy + sx[a] * sy[b] * fxy
        return out
