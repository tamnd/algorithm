# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finite-element-method/. The authors are listed in prov/PAMZX2.jsonl.

"""Linear (P1) finite elements for the Poisson problem -Δu = f in a polygon, u = g on the boundary.

The mesh is a list of nodes (x, y) and triangles (i, j, k). Arithmetic is generic: with
Fraction coordinates and the direct solver the discrete solution is computed exactly.
"""

import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence, Tuple

Point = Tuple[float, float]


@dataclass
class FEMResult:
    u: List                 # nodal values, length = number of nodes
    unknowns: int           # number of free (interior) nodes
    nonzeros: int           # stored entries of the global stiffness matrix
    iterations: int         # CG iterations (0 for the direct solver)


def structured_mesh(nx: int, ny: int, x0=0.0, x1=1.0, y0=0.0, y1=1.0):
    """Rectangle split into nx*ny cells, each cut by its lower-left to upper-right diagonal.

    Returns (nodes, triangles, boundary) with boundary the set of nodes on the rectangle edge.
    """
    if nx < 1 or ny < 1:
        raise ValueError("need at least one cell in each direction")
    nodes = [(x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny)
             for j in range(ny + 1) for i in range(nx + 1)]
    idx = lambda i, j: j * (nx + 1) + i
    tris = []
    for j in range(ny):
        for i in range(nx):
            a, b, c, d = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
            tris.append((a, b, c))
            tris.append((a, c, d))
    boundary = {idx(i, j) for j in range(ny + 1) for i in range(nx + 1)
                if i in (0, nx) or j in (0, ny)}
    return nodes, tris, boundary


def element_stiffness(p1: Point, p2: Point, p3: Point):
    """3x3 matrix K_ij = integral over the triangle of grad(phi_i) . grad(phi_j), and the area."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    det = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)  # twice the signed area
    if det == 0:
        raise ValueError("degenerate triangle")
    b = (y2 - y3, y3 - y1, y1 - y2)
    c = (x3 - x2, x1 - x3, x2 - x1)
    area = abs(det) / 2
    K = [[(b[i] * b[j] + c[i] * c[j]) / (2 * abs(det)) for j in range(3)] for i in range(3)]
    return K, area


def element_load(p1: Point, p2: Point, p3: Point, f: Callable, area):
    """F_i = integral of f phi_i by the edge-midpoint rule (exact when f phi_i is quadratic)."""
    pts = (p1, p2, p3)
    mid = {}
    for i in range(3):
        for j in range(i + 1, 3):
            m = ((pts[i][0] + pts[j][0]) / 2, (pts[i][1] + pts[j][1]) / 2)
            mid[(i, j)] = mid[(j, i)] = f(*m)
    return [area / 6 * (mid[(i, (i + 1) % 3)] + mid[(i, (i + 2) % 3)]) for i in range(3)]


def assemble(nodes, tris, f):
    """Global stiffness matrix as a list of sparse rows {column: value} and load vector."""
    n = len(nodes)
    K: List[Dict[int, object]] = [dict() for _ in range(n)]  # @line L1
    F = [0] * n
    for tri in tris:  # @line L2
        p = [nodes[v] for v in tri]
        Ke, area = element_stiffness(*p)  # @line L3
        Fe = element_load(p[0], p[1], p[2], f, area)
        for a in range(3):  # @line L4
            row = K[tri[a]]
            for b in range(3):
                row[tri[b]] = row.get(tri[b], 0) + Ke[a][b]
            F[tri[a]] += Fe[a]  # @line L5
    return K, F


def _cg(rows, rhs, tol, max_iter):
    n = len(rhs)
    x = [0.0] * n
    r = list(rhs)
    p = list(r)
    rr = sum(v * v for v in r)
    stop = (tol ** 2) * max(rr, 1e-300)
    it = 0
    while rr > stop and it < max_iter:
        Ap = [sum(v * p[j] for j, v in row.items()) for row in rows]
        alpha = rr / sum(p[i] * Ap[i] for i in range(n))
        for i in range(n):
            x[i] += alpha * p[i]
            r[i] -= alpha * Ap[i]
        rr_new = sum(v * v for v in r)
        beta = rr_new / rr
        p = [r[i] + beta * p[i] for i in range(n)]
        rr = rr_new
        it += 1
    return x, it


def _direct(rows, rhs):
    """Gaussian elimination without pivoting (the matrix is symmetric positive definite)."""
    n = len(rhs)
    A = [[row.get(j, 0) for j in range(n)] + [rhs[i]] for i, row in enumerate(rows)]
    for k in range(n):
        for i in range(k + 1, n):
            if A[i][k] != 0:
                m = A[i][k] / A[k][k]
                for j in range(k, n + 1):
                    A[i][j] -= m * A[k][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A[i][n] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


def solve_poisson(nodes, tris, boundary, f: Callable, g: Callable,
                  solver: str = "cg", tol: float = 1e-12, max_iter: int = 100000) -> FEMResult:
    """P1 Galerkin solution of -Δu = f, u = g on the boundary nodes."""
    K, F = assemble(nodes, tris, f)
    u = [0] * len(nodes)
    for v in boundary:  # @line L6
        u[v] = g(*nodes[v])
    free = [v for v in range(len(nodes)) if v not in boundary]
    pos = {v: k for k, v in enumerate(free)}
    rows, rhs = [], []
    for v in free:  # @line L7
        row = {}
        s = F[v]
        for w, val in K[v].items():
            if w in pos:
                row[pos[w]] = val
            else:
                s -= val * u[w]
        rows.append(row)
        rhs.append(s)
    it = 0
    if free:  # @line L8
        if solver == "cg":
            x, it = _cg(rows, rhs, tol, max_iter)
        elif solver == "direct":
            x = _direct(rows, rhs)
        else:
            raise ValueError("solver must be 'cg' or 'direct'")
        for v, val in zip(free, x):
            u[v] = val
    return FEMResult(u, len(free), sum(len(r) for r in K), it)  # @line L9
