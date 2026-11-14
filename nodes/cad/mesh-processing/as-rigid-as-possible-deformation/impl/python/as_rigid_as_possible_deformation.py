# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/as-rigid-as-possible-deformation/. The authors are listed in prov/QG8W8W.jsonl.

"""As-rigid-as-possible surface deformation (Sorkine and Alexa, SGP 2007).

The energy of new positions q against the rest positions p, with one
rotation R_i for the cell of each vertex, is

    E(q, R) = sum_i sum_{j in N(i)} w_ij |(q_i - q_j) - R_i (p_i - p_j)|^2.

The handle vertices are fixed at their targets. The method alternates
two steps, and neither increases E.

Local step: for fixed q, R_i maximizes trace(R_i S_i) with
S_i = sum_j w_ij (p_i - p_j)(q_i - q_j)^T, found by a 3 x 3 SVD.

Global step: for fixed R, q minimizes E, which is the linear system
sum_j w_ij (q_i - q_j) = sum_j (w_ij / 2)(R_i + R_j)(p_i - p_j) at each
free vertex. Its matrix depends only on the rest mesh and the handles, so it
is factored once (Cholesky) and each step costs one back substitution.

The weights must be nonnegative, and every connected part of the mesh must
hold a handle. The cotangent weights are nonnegative on meshes without
obtuse triangles, and their signs are decided exactly; weights="uniform"
sets all w_ij = 1.
"""

from mx1mesh import best_rotation, cholesky, cholesky_solve, cot_at, cross, dot, edges, exact, mat_vec, sign, sub


def cotan_sign(points, i, j, opposite):
    """The exact sign of the sum of the cotangents of the angles at the vertices in opposite, against the edge ij.

    cot = d / sqrt(c) with d = (a - o) . (b - o) and c = |(a - o) x (b - o)|^2, both exact
    rationals of the float input. Two terms of opposite signs are compared through d1^2 c2 and d2^2 c1.
    """
    terms = []
    for o in opposite:
        a, b, c = exact(points[i]), exact(points[j]), exact(points[o])
        u, v = sub(a, c), sub(b, c)
        x = cross(u, v)
        terms.append((dot(u, v), dot(x, x)))
    s = [sign(d) for d, _ in terms]
    if len(terms) == 1 or s[0] * s[1] >= 0:
        return sign(sum(s))
    (d1, c1), (d2, c2) = terms
    return s[0] * sign(d1 * d1 * c2 - d2 * d2 * c1)


def weight_lists(n, faces, points, weights="cotan"):
    """For each vertex, the list of (neighbour, w_ij)."""
    if weights == "uniform":
        w = {e: 1.0 for e in edges(faces)}
    else:
        opposite = {}
        for f in faces:
            for k in range(3):
                i, j, o = f[k], f[(k + 1) % 3], f[(k + 2) % 3]
                opposite.setdefault((min(i, j), max(i, j)), []).append(o)
        w = {}
        for (i, j), opp in opposite.items():
            s = cotan_sign(points, i, j, opp)
            if s < 0:
                raise ValueError("a cotangent weight is negative; use weights='uniform' or remesh")
            w[(i, j)] = sum(cot_at(points[o], points[i], points[j]) for o in opp) / 2 if s > 0 else 0.0
    nbw = [[] for _ in range(n)]
    for (i, j), x in w.items():
        nbw[i].append((j, x))
        nbw[j].append((i, x))
    return nbw


def energy(p, q, nbw, R):
    total = 0.0
    for i, row in enumerate(nbw):
        for j, w in row:
            e = mat_vec(R[i], sub(p[i], p[j]))
            d = sub(q[i], q[j])
            total += w * sum((a - b) ** 2 for a, b in zip(d, e))
    return total


def local_step(p, q, nbw):
    """The best rotation of each cell: R_i maximizes trace(R S_i), S_i = sum_j w_ij e_ij e'_ij^T."""
    R = []
    for i, row in enumerate(nbw):
        S = [[0.0] * 3 for _ in range(3)]
        for j, w in row:
            e, f = sub(p[i], p[j]), sub(q[i], q[j])
            for a in range(3):
                for b in range(3):
                    S[a][b] += w * e[a] * f[b]
        R.append(best_rotation(S))  # @line L4
    return R


class GlobalSolver:
    """The system sum_j w_ij (q_i - q_j) = b_i on the free vertices, factored once."""

    def __init__(self, n, nbw, handles):
        self.free = [i for i in range(n) if i not in handles]
        self.index = {v: k for k, v in enumerate(self.free)}
        m = len(self.free)
        A = [[0.0] * m for _ in range(m)]
        for k, i in enumerate(self.free):
            for j, w in nbw[i]:
                A[k][k] += w
                if j in self.index:
                    A[k][self.index[j]] -= w
        self.L = cholesky(A)  # @line L1

    def solve(self, p, nbw, R, handles):
        q = [None] * len(p)
        for i, h in handles.items():
            q[i] = tuple(h)
        rhs = [[0.0] * len(self.free) for _ in range(3)]
        for k, i in enumerate(self.free):
            for j, w in nbw[i]:
                e = sub(p[i], p[j])
                r = mat_vec([[(R[i][a][b] + R[j][a][b]) / 2 for b in range(3)] for a in range(3)], e)
                for c in range(3):
                    rhs[c][k] += w * r[c]  # @line L5
                    if j in handles:
                        rhs[c][k] += w * handles[j][c]
        cols = [cholesky_solve(self.L, rhs[c]) for c in range(3)]  # @line L6
        for k, i in enumerate(self.free):
            q[i] = (cols[0][k], cols[1][k], cols[2][k])
        return q


def arap(points, faces, handles, iterations=10, weights="cotan"):
    """Deform the mesh so that each vertex in handles (a dict index -> target) reaches its target.

    Returns (q, history): the new positions and the energy after the first
    solve and after each local and each global step.
    """
    n = len(points)
    nbw = weight_lists(n, faces, points, weights)
    solver = GlobalSolver(n, nbw, handles)
    identity = [[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]] for _ in range(n)]
    q = solver.solve(points, nbw, identity, handles)  # @line L2
    history = [energy(points, q, nbw, identity)]
    for _ in range(iterations):  # @line L3
        R = local_step(points, q, nbw)
        history.append(energy(points, q, nbw, R))
        q = solver.solve(points, nbw, R, handles)
        history.append(energy(points, q, nbw, R))
    return q, history  # @line L7
