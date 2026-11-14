# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heat-method/. The authors are listed in prov/MWDDTN.jsonl.

"""The heat method for geodesic distance (Crane, Weischedel and Wardetzky, 2013).

1. Heat: solve (M + t C) u = delta, one backward Euler step of the heat
   equation from the sources, with t = h^2 for the mean edge length h.
2. Normalize: on each face, X = -grad u / |grad u|.
3. Poisson: solve C phi = -div X, with the integrated divergence of X at
   each vertex, and shift phi so that the smallest value at a source is 0.

C is the cotangent stiffness matrix (C = -L) and M the lumped mass.
"""

from typing import Iterable, Optional, Sequence

from mp2mesh import (conjugate_gradient, cot_at, cross, dense, dot, lumped_mass, mean_edge_length, norm, scale,
                     solve_dense, stiffness_matrix, sub)

Vec = tuple


def face_gradients(points, faces, u) -> list[Vec]:
    """The gradient of the linear interpolant of u on each face: (1 / 2A) sum of u_i (N x e_i)."""
    out = []
    for f in faces:
        p = [points[v] for v in f]
        n = cross(sub(p[1], p[0]), sub(p[2], p[0]))
        a2 = norm(n)                                       # twice the area
        nn = scale(1 / a2, n)
        g = (0.0, 0.0, 0.0)
        for k in range(3):
            e = sub(p[(k + 2) % 3], p[(k + 1) % 3])         # the edge opposite vertex k, in face order
            g = tuple(gi + u[f[k]] * ci / a2 for gi, ci in zip(g, cross(nn, e)))
        out.append(g)
    return out


def divergence(points, faces, X) -> list[float]:
    """The integrated divergence at each vertex: 1/2 sum over faces of cot(t1) (e1 . X) + cot(t2) (e2 . X)."""
    div = [0.0] * len(points)
    for f, x in zip(faces, X):
        for k in range(3):
            i, j, l = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
            pi, pj, pl = points[i], points[j], points[l]
            e1, e2 = sub(pj, pi), sub(pl, pi)
            div[i] += 0.5 * (cot_at(pl, pi, pj) * dot(e1, x) + cot_at(pj, pl, pi) * dot(e2, x))
    return div


def solve_pinned(C, b, pin: int, solver: str) -> list[float]:
    """Solve C phi = b with phi[pin] = 0. C is singular with the constants in its kernel."""
    n = len(b)
    keep = [i for i in range(n) if i != pin]
    pos = {v: r for r, v in enumerate(keep)}
    A = [{pos[j]: c for j, c in C[i].items() if j in pos} for i in keep]
    rhs = [b[i] for i in keep]
    y = solve_dense(dense(A), rhs) if solver == "dense" else conjugate_gradient(A, rhs)
    phi = [0.0] * n
    for r, i in enumerate(keep):
        phi[i] = y[r]
    return phi


def heat_method(points: Sequence[Sequence[float]], faces: Sequence[Sequence[int]], sources: Iterable[int],
                t: Optional[float] = None, solver: str = "cg") -> list[float]:
    """Approximate geodesic distance from the source vertices to every vertex of a connected mesh."""
    src = sorted(set(sources))
    n = len(points)
    if t is None:
        t = mean_edge_length(points, faces) ** 2                       # @line L1
    C = stiffness_matrix(points, faces)                                 # @line L2
    M = lumped_mass(points, faces)
    A = [{j: t * c for j, c in C[i].items()} for i in range(n)]
    for i in range(n):
        A[i][i] = A[i].get(i, 0.0) + M[i]
    delta = [1.0 if i in src else 0.0 for i in range(n)]
    u = solve_dense(dense(A), delta) if solver == "dense" else conjugate_gradient(A, delta)  # @line L3
    X = []
    for g in face_gradients(points, faces, u):                          # @line L4
        m = norm(g)
        X.append(scale(-1 / m, g) if m > 0 else (0.0, 0.0, 0.0))
    div = divergence(points, faces, X)                                  # @line L5
    phi = solve_pinned(C, [-d for d in div], src[0], solver)            # @line L6
    low = min(phi[s] for s in src)
    return [p - low for p in phi]                                       # @line L7
