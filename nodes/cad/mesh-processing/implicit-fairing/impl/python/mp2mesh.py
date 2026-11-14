# SPDX-License-Identifier: MIT
# Shared helper of the mp2 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small tools for triangle meshes, used by the mp2 pages.

A mesh is a list of points (tuples of 3 numbers) and a list of faces
(tuples of 3 vertex indices, oriented by the right-hand rule). The helper has
the adjacency, the cotangent weights and the lumped mass, a sparse conjugate
gradient solver, a dense solver, and the test meshes. It does not hold the
algorithm of any page.
"""

from math import sqrt
from typing import Sequence

Vec = tuple


# ---- vectors ----


def sub(a: Sequence, b: Sequence) -> Vec:
    return tuple(x - y for x, y in zip(a, b))


def add(a: Sequence, b: Sequence) -> Vec:
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a: Sequence) -> Vec:
    return tuple(c * x for x in a)


def dot(a: Sequence, b: Sequence):
    return sum(x * y for x, y in zip(a, b))


def cross(a: Sequence, b: Sequence) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a: Sequence) -> float:
    return sqrt(dot(a, a))


# ---- adjacency ----


def edges(faces: Sequence[Sequence[int]]) -> list[tuple[int, int]]:
    """The undirected edges (i, j) with i < j, sorted."""
    out = set()
    for f in faces:
        for k in range(3):
            i, j = f[k], f[(k + 1) % 3]
            out.add((min(i, j), max(i, j)))
    return sorted(out)


def edge_faces(faces: Sequence[Sequence[int]]) -> dict[tuple[int, int], list[int]]:
    """For each undirected edge, the indices of the faces that contain it."""
    out: dict[tuple[int, int], list[int]] = {}
    for fi, f in enumerate(faces):
        for k in range(3):
            i, j = f[k], f[(k + 1) % 3]
            out.setdefault((min(i, j), max(i, j)), []).append(fi)
    return out


def neighbours(n: int, faces: Sequence[Sequence[int]]) -> list[list[int]]:
    """The sorted neighbours of each of the n vertices."""
    nb: list[set[int]] = [set() for _ in range(n)]
    for i, j in edges(faces):
        nb[i].add(j)
        nb[j].add(i)
    return [sorted(s) for s in nb]


def boundary_vertices(faces: Sequence[Sequence[int]]) -> set[int]:
    """The vertices on an edge that has one face."""
    out: set[int] = set()
    for (i, j), fs in edge_faces(faces).items():
        if len(fs) == 1:
            out.update((i, j))
    return out


def euler_characteristic(n: int, faces: Sequence[Sequence[int]]) -> int:
    used = {v for f in faces for v in f}
    return len(used) - len(edges(faces)) + len(faces)


# ---- geometry ----


def face_area(points: Sequence[Sequence[float]], f: Sequence[int]) -> float:
    a, b, c = (points[v] for v in f)
    return norm(cross(sub(b, a), sub(c, a))) / 2


def cot_at(p: Sequence[float], q: Sequence[float], r: Sequence[float]) -> float:
    """The cotangent of the angle at p of the triangle p, q, r."""
    u, v = sub(q, p), sub(r, p)
    return dot(u, v) / norm(cross(u, v))


def cotan_weights(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]]) -> dict[tuple[int, int], float]:
    """w[(i, j)] = (cot a + cot b) / 2 over the angles opposite the edge (one term on the boundary)."""
    w: dict[tuple[int, int], float] = {}
    for f in faces:
        for k in range(3):
            i, j, o = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
            e = (min(i, j), max(i, j))
            w[e] = w.get(e, 0.0) + cot_at(points[o], points[i], points[j]) / 2
    return w


def stiffness_matrix(points, faces) -> list[dict[int, float]]:
    """C = -L for the cotangent Laplacian L: C[i][j] = -w_ij, C[i][i] = sum of w_ij."""
    n = len(points)
    C: list[dict[int, float]] = [dict() for _ in range(n)]
    for (i, j), wij in cotan_weights(points, faces).items():
        C[i][j] = C[i].get(j, 0.0) - wij
        C[j][i] = C[j].get(i, 0.0) - wij
        C[i][i] = C[i].get(i, 0.0) + wij
        C[j][j] = C[j].get(j, 0.0) + wij
    return C


def lumped_mass(points, faces) -> list[float]:
    """The barycentric vertex areas: one third of the area of each face at the vertex."""
    m = [0.0] * len(points)
    for f in faces:
        a = face_area(points, f) / 3
        for v in f:
            m[v] += a
    return m


def signed_volume(points, faces) -> float:
    """The volume enclosed by a closed oriented mesh (outward normals give a positive value)."""
    return sum(dot(points[a], cross(points[b], points[c])) for a, b, c in faces) / 6


def mean_edge_length(points, faces) -> float:
    es = edges(faces)
    return sum(norm(sub(points[i], points[j])) for i, j in es) / len(es)


# ---- linear algebra ----


def mat_vec(A: Sequence[dict[int, float]], x: Sequence[float]) -> list[float]:
    return [sum(a * x[j] for j, a in row.items()) for row in A]


def conjugate_gradient(A, b, x0=None, tol: float = 1e-12, max_iter: int | None = None) -> list[float]:
    """Solve A x = b for a sparse symmetric positive definite A (a list of dict rows)."""
    n = len(b)
    x = list(x0) if x0 is not None else [0.0] * n
    Ax = mat_vec(A, x)
    r = [bi - ai for bi, ai in zip(b, Ax)]
    p = list(r)
    rr = dot(r, r)
    bb = max(dot(b, b), 1e-300)
    for _ in range(max_iter or 10 * n + 10):
        if rr <= tol * tol * bb:
            break
        Ap = mat_vec(A, p)
        alpha = rr / dot(p, Ap)
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r = [ri - alpha * qi for ri, qi in zip(r, Ap)]
        rr_new = dot(r, r)
        p = [ri + (rr_new / rr) * pi for ri, pi in zip(r, p)]
        rr = rr_new
    return x


def solve_dense(A: Sequence[Sequence], b: Sequence) -> list:
    """Gaussian elimination with partial pivoting. Works with float or Fraction entries."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[p][c] == 0:
            raise ValueError("singular matrix")
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0] * n
    for c in range(n - 1, -1, -1):
        x[c] = (M[c][n] - sum(M[c][k] * x[k] for k in range(c + 1, n))) / M[c][c]
    return x


def dense(A: Sequence[dict[int, float]]) -> list[list[float]]:
    n = len(A)
    return [[A[i].get(j, 0.0) for j in range(n)] for i in range(n)]


# ---- test meshes ----


def grid_mesh(m: int, n: int, h=1.0):
    """The (m+1) x (n+1) grid in the plane z = 0, each square cut by the diagonal from (i, j) to (i+1, j+1)."""
    pts = [(i * h, j * h, 0 * h) for j in range(n + 1) for i in range(m + 1)]

    def v(i, j):
        return j * (m + 1) + i

    faces = []
    for j in range(n):
        for i in range(m):
            faces.append((v(i, j), v(i + 1, j), v(i + 1, j + 1)))
            faces.append((v(i, j), v(i + 1, j + 1), v(i, j + 1)))
    return pts, faces


def octahedron():
    pts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    faces = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    return pts, faces


def icosphere(level: int):
    """The icosahedron, with each triangle cut into 4 `level` times, on the unit sphere."""
    t = (1 + sqrt(5)) / 2
    raw = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
           (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    pts = [scale(1 / norm(p), p) for p in raw]
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
             (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
             (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    for _ in range(level):
        mid: dict[tuple[int, int], int] = {}

        def m(i, j):
            key = (min(i, j), max(i, j))
            if key not in mid:
                p = scale(0.5, add(pts[i], pts[j]))
                pts.append(scale(1 / norm(p), p))
                mid[key] = len(pts) - 1
            return mid[key]

        new = []
        for a, b, c in faces:
            ab, bc, ca = m(a, b), m(b, c), m(c, a)
            new += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
        faces = new
    return pts, faces
