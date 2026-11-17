# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-free-form-deformation/. The authors are listed in prov/7CMXN6.jsonl.
"""Extended free-form deformation in the spirit of Coquillart (1990).

The lattice is a list of chunks. Each chunk is a Bezier volume of degree
(l, m, n) whose control points are indices into one global list of points,
so neighbouring chunks that share a face share the same control points and
meet with C0 continuity. The undeformed lattice need not be a box, so the
local coordinates of a point are not given by a formula. They are found by
Newton iteration on B_c(w) = X, chunk by chunk. The deformed point is then
B_c(w) evaluated with the moved control points.
"""

from math import comb

NOT_FOUND = None


def bernstein(deg, x):
    """Return [B_0^deg(x), ..., B_deg^deg(x)]."""
    return [comb(deg, i) * (1 - x) ** (deg - i) * x ** i for i in range(deg + 1)]


def bernstein_derivative(deg, x):
    """Return the derivatives of the Bernstein polynomials of degree deg."""
    if deg == 0:
        return [0.0]
    low = bernstein(deg - 1, x)
    return [deg * ((low[i - 1] if i >= 1 else 0) - (low[i] if i < deg else 0)) for i in range(deg + 1)]


class Chunk:
    """One Bezier volume. idx[i][j][k] is an index into the global point list."""

    def __init__(self, deg, idx):
        self.deg = tuple(deg)
        l, m, n = self.deg
        if len(idx) != l + 1 or any(len(p) != m + 1 for p in idx) or any(len(r) != n + 1 for p in idx for r in p):
            raise ValueError("the index grid does not match the degree")
        self.idx = idx

    def evaluate(self, points, w):
        """Return B_c(w) for the given global point list."""
        l, m, n = self.deg
        bs, bt, bu = bernstein(l, w[0]), bernstein(m, w[1]), bernstein(n, w[2])
        out = [0.0, 0.0, 0.0]
        for i in range(l + 1):
            for j in range(m + 1):
                for k in range(n + 1):
                    c = bs[i] * bt[j] * bu[k]
                    p = points[self.idx[i][j][k]]
                    for d in range(3):
                        out[d] += c * p[d]
        return tuple(out)

    def jacobian(self, points, w):
        """Return the 3 by 3 matrix dB_c/dw; column a is the derivative by w[a]."""
        l, m, n = self.deg
        b = (bernstein(l, w[0]), bernstein(m, w[1]), bernstein(n, w[2]))
        db = (bernstein_derivative(l, w[0]), bernstein_derivative(m, w[1]), bernstein_derivative(n, w[2]))
        jac = [[0.0] * 3 for _ in range(3)]
        for i in range(l + 1):
            for j in range(m + 1):
                for k in range(n + 1):
                    p = points[self.idx[i][j][k]]
                    ws = (db[0][i] * b[1][j] * b[2][k], b[0][i] * db[1][j] * b[2][k], b[0][i] * b[1][j] * db[2][k])
                    for a in range(3):
                        for d in range(3):
                            jac[d][a] += ws[a] * p[d]
        return jac


def solve3(a, r):
    """Solve a x = r for a 3 by 3 matrix by Cramer's rule. Return None if singular."""

    def det(m):
        return (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )

    d = det(a)
    scale = max(abs(v) for row in a for v in row) or 1.0
    if abs(d) <= 1e-14 * scale ** 3:
        return None
    out = []
    for c in range(3):
        m = [[r[i] if k == c else a[i][k] for k in range(3)] for i in range(3)]
        out.append(det(m) / d)
    return out


def embed(chunks, points, x, iters=30, tol=1e-12, slack=1e-9):
    """Return (chunk index, w) with B_c(w) = x and w in [0, 1]^3, or NOT_FOUND."""
    for c, chunk in enumerate(chunks):  # @line L1
        w = [0.5, 0.5, 0.5]  # @line L2
        ok = False
        for _ in range(iters):  # @line L3
            b = chunk.evaluate(points, w)
            r = [b[d] - x[d] for d in range(3)]  # @line L4
            if max(abs(v) for v in r) < tol:  # @line L5
                ok = True
                break
            step = solve3(chunk.jacobian(points, w), r)
            if step is None:
                break
            w = [w[d] - step[d] for d in range(3)]  # @line L6
            if max(abs(v) for v in w) > 1e6:
                break
        if ok and all(-slack <= v <= 1 + slack for v in w):  # @line L7
            return c, tuple(min(1.0, max(0.0, v)) for v in w)
    return NOT_FOUND  # @line L9


def deform(chunks, rest, moved, x, **kw):
    """Return the deformed position of x, or NOT_FOUND if x is outside the lattice."""
    hit = embed(chunks, rest, x, **kw)
    if hit is NOT_FOUND:
        return NOT_FOUND
    c, w = hit
    return chunks[c].evaluate(moved, w)  # @line L8


def quarter_ring_lattice(r_in=1.0, r_out=2.0, height=1.0):
    """Build the two-chunk example lattice: two quarter rings around the z axis.

    Each chunk has degree (2, 1, 1). The index s runs along a quadratic arc
    with the control points (r, 0), (r, r), (0, r) for the first quarter and
    (0, r), (-r, r), (-r, 0) for the second. The index t runs from r_in to
    r_out and the index u from z = 0 to z = height. The two chunks share the
    face at 90 degrees through shared indices.
    """
    points = []
    index = {}

    def pid(key, p):
        if key not in index:
            index[key] = len(points)
            points.append(p)
        return index[key]

    arcs = [((1, 0), (1, 1), (0, 1)), ((0, 1), (-1, 1), (-1, 0))]
    chunks = []
    for q, arc in enumerate(arcs):
        idx = []
        for i, (ax, ay) in enumerate(arc):
            plane = []
            for j, r in enumerate((r_in, r_out)):
                row = []
                for k, z in enumerate((0.0, height)):
                    row.append(pid((2 * q + i, j, k), (r * ax, r * ay, z)))
                plane.append(row)
            idx.append(plane)
        chunks.append(Chunk((2, 1, 1), idx))
    return chunks, points, index
