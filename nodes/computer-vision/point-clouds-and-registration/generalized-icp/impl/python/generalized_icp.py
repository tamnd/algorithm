# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-icp/. The authors are listed in prov/W2QK6S.jsonl.
"""Generalized-ICP (GICP) of Segal, Haehnel and Thrun.

Each source point a_i and target point b_j carries a 3 x 3 covariance
(C_i^A, C_j^B). With the matches fixed, the motion (R, t) minimizes

    sum_i d_i^T (C_j^B + R C_i^A R^T)^-1 d_i,   d_i = b_j - (R a_i + t),

which is the maximum likelihood estimate when both points are Gaussian.
C^A = 0 and C^B = I give point-to-point ICP. The plane-to-plane form takes
each covariance from the k nearest neighbors of the point, with the
eigenvalues replaced by (eps, 1, 1), so a point is sure along its normal
and unsure in its tangent plane.

Each iteration matches by Euclidean closest point (brute force,
Theta(n m)), drops pairs farther than d_max, computes the weights
M_i = (C_j^B + R C_i^A R^T)^-1 from the current R, and then minimizes
sum_i d_i^T M_i d_i over (R, t) with these weights held fixed, by
Gauss-Newton steps on the motion x -> Exp(w) x + u. A step is halved until
the cost goes down. The paper minimizes with conjugate gradients instead.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from cvgeom import axis_angle_to_R
from cvla import add, inv, matvec, mul, skew, solve, sym_eig, transpose

Matrix = List[List[float]]
Vector = List[float]


def transform(R, t, pts) -> List[Vector]:
    """The points R p + t."""
    return [[sum(R[i][k] * p[k] for k in range(3)) + t[i] for i in range(3)] for p in pts]


def closest_points(pts, target) -> Tuple[List[int], List[float]]:
    """Index of the closest target point of each point and the squared
    distance (brute force; ties go to the lowest index)."""
    idx, d2 = [], []
    for x, y, z in pts:
        best, bj = float("inf"), -1
        for j, q in enumerate(target):
            dx, dy, dz = x - q[0], y - q[1], z - q[2]
            d = dx * dx + dy * dy + dz * dz
            if d < best:
                best, bj = d, j
        idx.append(bj)
        d2.append(best)
    return idx, d2


def plane_covariances(pts: Sequence[Sequence[float]], k: int = 10,
                      eps: float = 1e-3) -> List[Matrix]:
    """The plane-to-plane covariance of each point: the empirical covariance
    of its k nearest neighbors (itself included) is written V diag(w) V^T
    with w ascending, and w is replaced by (eps, 1, 1). The first column of
    V, the direction of least spread, is the estimated normal."""
    out = []
    for p in pts:
        d = sorted(range(len(pts)), key=lambda j: sum((pts[j][c] - p[c]) ** 2 for c in range(3)))
        nb = [pts[j] for j in d[:k]]
        mu = [sum(q[c] for q in nb) / len(nb) for c in range(3)]
        cov = [[sum((q[r] - mu[r]) * (q[c] - mu[c]) for q in nb) / len(nb) for c in range(3)] for r in range(3)]
        _, V = sym_eig(cov)
        D = [[eps, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        out.append(mul(mul(V, D), transpose(V)))
    return out


def weights(R, CA, CB, pairs) -> List[Matrix]:
    """M = (C_j^B + R C_i^A R^T)^-1 for each pair (i, j)."""
    Rt = transpose(R)
    return [inv(add(CB[j], mul(mul(R, CA[i]), Rt))) for i, j in pairs]


def weighted_cost(R, t, A, B, pairs, Ms) -> float:
    """sum over the pairs of d^T M d, d = b_j - (R a_i + t)."""
    total = 0.0
    for (i, j), M in zip(pairs, Ms):
        x = [sum(R[r][c] * A[i][c] for c in range(3)) + t[r] for r in range(3)]
        d = [B[j][r] - x[r] for r in range(3)]
        total += sum(d[r] * sum(M[r][c] * d[c] for c in range(3)) for r in range(3))
    return total


def gicp_cost(R, t, A, B, CA, CB, pairs) -> float:
    """The GICP cost, with the weights taken at this R."""
    return weighted_cost(R, t, A, B, pairs, weights(R, CA, CB, pairs))


def minimize_fixed_weights(R, t, A, B, pairs, Ms, steps: int = 30,
                           tol: float = 1e-12) -> Tuple[Matrix, Vector]:
    """Gauss-Newton on (w, u) for fixed pairs and fixed weights, with step
    halving so that the cost never goes up. Stops when a step has norm at
    most tol, or when no halved step lowers the cost."""
    cost = weighted_cost(R, t, A, B, pairs, Ms)
    for _ in range(steps):
        H = [[0.0] * 6 for _ in range(6)]
        g = [0.0] * 6
        for (i, j), M in zip(pairs, Ms):
            x = [sum(R[r][c] * A[i][c] for c in range(3)) + t[r] for r in range(3)]
            d = [B[j][r] - x[r] for r in range(3)]
            S = skew(x)
            J = [S[r] + [-1.0 if c == r else 0.0 for c in range(3)] for r in range(3)]
            MJ = mul(M, J)
            Md = matvec(M, d)
            for a in range(6):
                g[a] += sum(J[r][a] * Md[r] for r in range(3))
                for b in range(6):
                    H[a][b] += sum(J[r][a] * MJ[r][b] for r in range(3))
        step = solve(H, [-v for v in g])  # @line L6
        if sum(v * v for v in step) <= tol * tol:
            break
        lam, moved = 1.0, False
        for _ in range(30):  # @line L7
            dR = axis_angle_to_R([lam * v for v in step[:3]])
            R2 = mul(dR, R)
            t2 = [a + lam * b for a, b in zip(matvec(dR, t), step[3:])]
            c2 = weighted_cost(R2, t2, A, B, pairs, Ms)
            if c2 < cost:
                R, t, cost, moved = R2, t2, c2, True
                break
            lam *= 0.5
        if not moved:
            break
    return R, t


def generalized_icp(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]],
                    CA: Sequence[Matrix], CB: Sequence[Matrix],
                    R0: Optional[Sequence[Sequence[float]]] = None,
                    t0: Optional[Sequence[float]] = None,
                    max_iter: int = 30, d_max: Optional[float] = None,
                    tol: float = 1e-10) -> Tuple[Matrix, Vector, List[float]]:
    """GICP from the start pose (R0, t0) (default identity). Returns
    (R, t, costs), where costs[k] is the GICP cost at the end of iteration k
    (weights at the new R, same pairs). Stops when the motion changes by at
    most tol (sum of the absolute entry changes of R and t) or after
    max_iter iterations."""
    R = [list(r) for r in R0] if R0 is not None else [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]  # @line L1
    t = list(t0) if t0 is not None else [0.0, 0.0, 0.0]  # @line L1
    costs: List[float] = []
    for _ in range(max_iter):  # @line L2
        idx, d2 = closest_points(transform(R, t, A), B)  # @line L3
        pairs = [(i, j) for i, (j, d) in enumerate(zip(idx, d2))  # @line L3
                 if d_max is None or d <= d_max * d_max]
        if len(pairs) < 3:
            raise ValueError("generalized_icp: fewer than 3 pairs within d_max")
        Ms = weights(R, CA, CB, pairs)  # @line L4
        R2, t2 = minimize_fixed_weights(R, t, A, B, pairs, Ms)  # @line L5
        costs.append(gicp_cost(R2, t2, A, B, CA, CB, pairs))
        change = sum(abs(R2[r][c] - R[r][c]) for r in range(3) for c in range(3)) + \
            sum(abs(a - b) for a, b in zip(t2, t))
        R, t = R2, t2
        if change <= tol:  # @line L8
            break  # @line L8
    return R, t, costs  # @line L9
