# SPDX-License-Identifier: MIT
# Shared helper of the mx2 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small tools for triangle meshes, used by the mx2 pages.

Points are tuples of int, fractions.Fraction or float. ORIENT2D is exact
when the coordinates are int or Fraction. A mesh is a list of faces, each a
tuple of three vertex indices, oriented so that the outward normal follows
the right-hand rule (counterclockwise seen from outside).
"""

import math
from fractions import Fraction


def orient2d(a, b, c):
    """Twice the signed area of triangle abc: > 0 if counterclockwise."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def exact_orient2d(a, b, c):
    """ORIENT2D with the float coordinates converted to rationals first, so the sign is exact."""
    return orient2d(*[tuple(Fraction(x) for x in p) for p in (a, b, c)])


def solve(a, b, tol=0.0):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    a is a list of n rows of length n, b is a list of n rows of length m
    (m right-hand sides). Entries are Fraction (exact), float or complex.
    Raises ValueError if a pivot has absolute value <= tol.
    """
    n = len(a)
    m = len(b[0]) if n else 0
    rows = [list(a[i]) + list(b[i]) for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(rows[r][col]))
        if abs(rows[piv][col]) <= tol:
            raise ValueError("singular matrix")
        rows[col], rows[piv] = rows[piv], rows[col]
        pr = rows[col]
        for r in range(col + 1, n):
            f = rows[r][col]
            if f:
                f = Fraction(f) / pr[col] if isinstance(f, int) and isinstance(pr[col], int) else f / pr[col]
                row = rows[r]
                for k in range(col, n + m):
                    if pr[k]:
                        row[k] -= f * pr[k]
    x = [[0] * m for _ in range(n)]
    for i in range(n - 1, -1, -1):
        row = rows[i]
        for k in range(m):
            s = row[n + k]
            for j in range(i + 1, n):
                if row[j]:
                    s -= row[j] * x[j][k]
            x[i][k] = Fraction(s) / row[i] if isinstance(s, int) and isinstance(row[i], int) else s / row[i]
    return x


def cholesky(a):
    """The lower triangular factor l with a = l l^T of a symmetric positive definite float matrix."""
    n = len(a)
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if s <= 0:
                    raise ValueError("matrix is not positive definite")
                l[i][i] = math.sqrt(s)
            else:
                l[i][j] = s / l[j][j]
    return l


def cholesky_solve(l, b):
    """Solve l l^T x = b for one right-hand side b, a list of floats."""
    n = len(l)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(l[i][k] * y[k] for k in range(i))) / l[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(l[k][i] * x[k] for k in range(i + 1, n))) / l[i][i]
    return x


def directed_edges(faces):
    """Map each directed edge (i, j) to (face index, corner of i). Raises on a repeated directed edge."""
    out = {}
    for f, tri in enumerate(faces):
        for k in range(3):
            e = (tri[k], tri[(k + 1) % 3])
            if e in out:
                raise ValueError("directed edge %r used twice: not an oriented manifold" % (e,))
            out[e] = (f, k)
    return out


def undirected_edges(faces):
    """The sorted list of edges, each a sorted pair of vertex indices."""
    return sorted({tuple(sorted((tri[k], tri[(k + 1) % 3]))) for tri in faces for k in range(3)})


def boundary_loop(faces):
    """The boundary of an oriented disk as one vertex loop, in the order of the face orientation."""
    de = directed_edges(faces)
    nxt = {}
    for i, j in de:
        if (j, i) not in de:
            if i in nxt:
                raise ValueError("boundary vertex %r is not manifold" % (i,))
            nxt[i] = j
    if not nxt:
        raise ValueError("the mesh has no boundary")
    start = min(nxt)
    loop = [start]
    while True:
        v = nxt[loop[-1]]
        if v == start:
            break
        loop.append(v)
    if len(loop) != len(nxt):
        raise ValueError("the boundary has more than one loop")
    return loop


def euler_characteristic(faces):
    """V - E + F of the mesh, counting only the vertices used by faces."""
    verts = {v for tri in faces for v in tri}
    return len(verts) - len(undirected_edges(faces)) + len(faces)


def length(p, q):
    return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(p, q)))


def corner_angle(a, b, c):
    """The angle opposite the side of length a in a triangle with sides a, b, c (law of cosines)."""
    x = (b * b + c * c - a * a) / (2 * b * c)
    return math.acos(max(-1.0, min(1.0, x)))


def triangle_frame(p0, p1, p2):
    """Corners of a congruent counterclockwise 2D triangle: p0 at 0, p1 on the positive x-axis."""
    l01, l12, l20 = length(p0, p1), length(p1, p2), length(p2, p0)
    a0 = corner_angle(l12, l01, l20)
    return (0.0, 0.0), (l01, 0.0), (l20 * math.cos(a0), l20 * math.sin(a0))
