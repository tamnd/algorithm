# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-field-hex-meshing/. The authors are listed in prov/WR7B7E.jsonl.

"""One smoothing sweep of a 3D frame field on a grid of cells.

A frame is a rotation matrix R whose three columns, with their negatives, are
the six directions of a cube. Two rotations R and R g with g in the
octahedral group O (the 24 signed permutation matrices with determinant +1)
describe the same frame. The smoothness energy of an edge between cells i
and j is the least squared distance between the two frames,

    e(i, j) = min over g in O of |R_i - R_j g|^2 = 6 - 2 max over g of tr(R_i^T R_j g),

and the energy of a field is the sum over the face-adjacent pairs of cells.
One sweep visits the free cells in a fixed order. For each it matches every
neighbour frame to the current frame by the best g, and replaces the frame by
the rotation closest to the sum of the matched neighbours, found by Horn's
quaternion method with a cyclic Jacobi eigen solver. This is a simple local
step, not the published methods of Huang and others (2011) or Ray and others
(2016). Floating point arithmetic is used, with tolerances in the tests.
"""

import math
from itertools import permutations, product
from typing import Dict, List, Sequence, Tuple

Matrix = List[List[float]]
Cell = Tuple[int, int, int]


def mat_mul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def transpose(a: Sequence[Sequence[float]]) -> Matrix:
    return [[a[j][i] for j in range(3)] for i in range(3)]


def det(a: Sequence[Sequence[float]]) -> float:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def inner(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> float:
    """tr(a^T b), the sum of the products of matching entries."""
    return sum(a[i][j] * b[i][j] for i in range(3) for j in range(3))


def octahedral_group() -> List[Matrix]:
    """The 24 signed permutation matrices with determinant +1."""
    out = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            g = [[0.0] * 3 for _ in range(3)]
            for i in range(3):
                g[i][perm[i]] = float(signs[i])
            if det(g) > 0:
                out.append(g)
    return out


OCTA = octahedral_group()


def best_match(r_i: Matrix, r_j: Matrix) -> Matrix:
    """R_j g for the g in O that maximizes tr(R_i^T R_j g); the first one on a tie."""
    best, best_val = None, -math.inf
    for g in OCTA:
        m = mat_mul(r_j, g)
        val = inner(r_i, m)
        if val > best_val + 1e-12:
            best, best_val = m, val
    return best


def edge_energy(r_i: Matrix, r_j: Matrix) -> float:
    return 6.0 - 2.0 * inner(r_i, best_match(r_i, r_j))


def quat_to_matrix(q: Sequence[float]) -> Matrix:
    """The rotation of the quaternion (w, x, y, z), scaled by |q|^2 when q is not a unit."""
    w, x, y, z = q
    return [
        [w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z],
    ]


def horn_matrix(m: Matrix) -> Matrix:
    """The symmetric 4 x 4 matrix N with q^T N q = tr(R(q)^T m) for every quaternion q."""

    def f(q):
        return inner(quat_to_matrix(q), m)

    e = [[1.0 if i == k else 0.0 for k in range(4)] for i in range(4)]
    n = [[0.0] * 4 for _ in range(4)]
    for a in range(4):
        n[a][a] = f(e[a])
        for b in range(a + 1, 4):
            s = [e[a][k] + e[b][k] for k in range(4)]
            n[a][b] = n[b][a] = (f(s) - n[a][a] - f(e[b])) / 2.0
    return n


def jacobi_eigen(a: Matrix, sweeps: int = 50, tol: float = 1e-28):
    """Eigenvalues and eigenvectors (columns of v) of a symmetric matrix by cyclic Jacobi.

    Stops when the squared off-diagonal mass is below tol times the squared Frobenius norm.
    """
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == k else 0.0 for k in range(n)] for i in range(n)]
    total = sum(x * x for row in a for x in row)
    for _ in range(sweeps):
        off = sum(a[i][k] ** 2 for i in range(n) for k in range(n) if i != k)
        if off <= tol * total:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, theta) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


def closest_rotation(m: Matrix) -> Matrix:
    """The rotation R that maximizes tr(R^T m), by Horn's quaternion method."""
    vals, vecs = jacobi_eigen(horn_matrix(m))
    k = max(range(4), key=lambda i: vals[i])
    q = [vecs[i][k] for i in range(4)]
    norm = math.sqrt(sum(x * x for x in q))
    return quat_to_matrix([x / norm for x in q])


def neighbours(c: Cell, cells: Dict[Cell, Matrix]) -> List[Cell]:
    out = []
    for t in range(3):
        for step in (-1, 1):
            nb = list(c)
            nb[t] += step
            if tuple(nb) in cells:
                out.append(tuple(nb))
    return out


def field_energy(frames: Dict[Cell, Matrix]) -> float:
    """The sum of the edge energies over the face-adjacent pairs of cells."""
    total = 0.0
    for c in frames:
        for nb in neighbours(c, frames):
            if nb > c:
                total += edge_energy(frames[c], frames[nb])
    return total


def frame_sweep(frames: Dict[Cell, Matrix], free: Sequence[Cell]) -> Dict[Cell, Matrix]:
    """One Gauss-Seidel sweep of the local frame update over the free cells, in place."""
    for c in free:  # @line L1
        m = [[0.0] * 3 for _ in range(3)]  # @line L2
        for nb in neighbours(c, frames):  # @line L3
            matched = best_match(frames[c], frames[nb])  # @line L4
            m = [[m[i][j] + matched[i][j] for j in range(3)] for i in range(3)]  # @line L5
        frames[c] = closest_rotation(m)  # @line L6
    return frames  # @line L7


def axis_rotation(axis: int, angle: float) -> Matrix:
    """The rotation by angle (radians) about the coordinate axis 0, 1 or 2."""
    c, s = math.cos(angle), math.sin(angle)
    i, j = [t for t in range(3) if t != axis]
    r = [[1.0 if a == b else 0.0 for b in range(3)] for a in range(3)]
    r[i][i], r[i][j], r[j][i], r[j][j] = c, -s, s, c
    return r
