# SPDX-License-Identifier: MIT
# Shared helper of the mp3 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small tools for triangle meshes, used by the mp3 pages.

Points are tuples of int, fractions.Fraction or float. The predicates are
exact when the coordinates are int or Fraction. A mesh is a list of faces,
each a tuple of three vertex indices, oriented so that the outward normal
follows the right-hand rule (counterclockwise seen from outside).
"""

from fractions import Fraction


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(s, a):
    return tuple(s * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def orient2d(a, b, c):
    """Twice the signed area of triangle abc: > 0 if counterclockwise."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def orient3d(a, b, c, d):
    """((b - a) x (c - a)) . (d - a): > 0 if d is on the side of the normal of abc."""
    return dot(cross(sub(b, a), sub(c, a)), sub(d, a))


def sign(x):
    return (x > 0) - (x < 0)


def solve(a, b, tol=0.0):
    """Solve a x = b by Gaussian elimination with partial pivoting.

    a is a list of n rows of length n, b is a list of n rows of length m
    (m right-hand sides). Entries are Fraction (exact) or float. Returns the
    n rows of x. Raises ValueError if a pivot has absolute value <= tol, so
    an exact singular matrix always raises when tol is 0.
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
        inv = 1 / pr[col] if isinstance(pr[col], float) else Fraction(1) / pr[col]
        for r in range(col + 1, n):
            f = rows[r][col]
            if f:
                f = f * inv
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
            x[i][k] = s / row[i] if isinstance(s, float) or isinstance(row[i], float) else Fraction(s) / row[i]
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


def neighbours(faces):
    """Map each vertex to the set of its neighbours."""
    nb = {}
    for tri in faces:
        for k in range(3):
            i, j = tri[k], tri[(k + 1) % 3]
            nb.setdefault(i, set()).add(j)
            nb.setdefault(j, set()).add(i)
    return nb


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
    verts = {v for tri in faces for v in tri}
    edges = {frozenset((tri[k], tri[(k + 1) % 3])) for tri in faces for k in range(3)}
    return len(verts) - len(edges) + len(faces)
