# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/implicit-fairing/. The authors are listed in prov/6F02H1.jsonl.

"""Implicit fairing (Desbrun, Meyer, Schroeder and Barr, SIGGRAPH 1999).

Each step is one backward Euler step of the flow M x' = -C x, that is, it
solves (M + dt C) x_new = M x_old on the free vertices, with the fixed
vertices as Dirichlet data. With weights="cotan", C is the cotangent
stiffness matrix and M the lumped (barycentric) mass, both taken at the
current positions, so the flow is the discrete mean curvature flow. With
weights="uniform", C = D - A is the graph Laplacian and M = D the valence
matrix, so the step is (I + dt (I - D^-1 A)) x_new = x_old. The solver is
conjugate gradients, or dense Gaussian elimination, which is exact on
Fraction input with the uniform weights.
"""

from typing import Iterable, Optional, Sequence

from mp2mesh import (boundary_vertices, conjugate_gradient, lumped_mass, neighbours, signed_volume,
                     solve_dense, stiffness_matrix)

Point = tuple


def operators(points, faces, weights: str):
    """The stiffness matrix C (list of dict rows) and the diagonal mass M."""
    n = len(points)
    if weights == "cotan":
        return stiffness_matrix(points, faces), lumped_mass(points, faces)
    if weights == "uniform":
        nb = neighbours(n, faces)
        C = [{i: len(nb[i]), **{j: -1 for j in nb[i]}} if nb[i] else {} for i in range(n)]
        return C, [len(nb[i]) for i in range(n)]
    raise ValueError("weights must be 'cotan' or 'uniform'")


def implicit_fairing(points: Sequence[Sequence], faces: Sequence[Sequence[int]], dt, steps: int = 1,
                     weights: str = "cotan", fixed: Optional[Iterable[int]] = None, keep_volume: bool = False,
                     solver: str = "cg") -> list[Point]:
    """Smooth the mesh by `steps` backward Euler steps of size dt."""
    n = len(points)
    x = [tuple(p) for p in points]
    F = boundary_vertices(faces) if fixed is None else set(fixed)               # @line L1
    used = {v for f in faces for v in f}
    R = [i for i in range(n) if i not in F and i in used]
    pos = {v: r for r, v in enumerate(R)}
    v0 = signed_volume(x, faces) if keep_volume else None
    for _ in range(steps):                                                      # @line L2
        C, M = operators(x, faces, weights)                                     # @line L3
        A = [{pos[j]: dt * c for j, c in C[i].items() if j in pos} for i in R]  # @line L4
        for r, i in enumerate(R):
            A[r][r] = A[r].get(r, 0) + M[i]
        new = [list(p) for p in x]
        for k in range(3):
            b = [M[i] * x[i][k] - sum(dt * c * x[j][k] for j, c in C[i].items() if j not in pos)
                 for i in R]                                                    # @line L5
            if solver == "dense":
                y = solve_dense([[row.get(c, 0) for c in range(len(R))] for row in A], b)
            else:
                y = conjugate_gradient(A, b, x0=[x[i][k] for i in R])
            for r, i in enumerate(R):
                new[i][k] = y[r]                                                # @line L6
        x = [tuple(p) for p in new]
        if keep_volume:                                                         # @line L7
            x = rescale_volume(x, faces, v0)
    return x


def rescale_volume(x, faces, v0):
    """Scale about the vertex centroid so that the enclosed volume is v0 again."""
    v = signed_volume(x, faces)
    s = (v0 / v) ** (1 / 3)
    c = tuple(sum(p[k] for p in x) / len(x) for k in range(3))
    return [tuple(c[k] + s * (p[k] - c[k]) for k in range(3)) for p in x]


def explicit_step(points, faces, dt, weights: str = "uniform"):
    """One forward Euler step x + dt M^-1 (-C x), for comparison. No fixed vertices."""
    C, M = operators(points, faces, weights)
    return [tuple(points[i][k] - dt * sum(c * points[j][k] for j, c in C[i].items()) / M[i] for k in range(3))
            if M[i] else tuple(points[i]) for i in range(len(points))]
