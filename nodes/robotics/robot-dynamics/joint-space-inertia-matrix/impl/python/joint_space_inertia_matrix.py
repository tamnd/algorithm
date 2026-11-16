# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/joint-space-inertia-matrix/. The authors are listed in prov/FNGKHS.jsonl.

"""Joint-space inertia matrix of a planar arm with n revolute joints.

The arm moves in a vertical plane with x horizontal and y up. Joint i is at
p_i, link i has length L[i], mass m[i], its center of mass at distance r[i]
from joint i along the link, and rotational inertia I[i] about its center of
mass (about the axis normal to the plane). Angles q[i] are relative, so link
i points at the absolute angle q[0] + ... + q[i].

M(q) = sum_i m_i Jv_i^T Jv_i + I_i Jw_i^T Jw_i, where Jv_i is the 2 x n
Jacobian of the center of mass of link i and Jw_i is the 1 x n Jacobian of
its angle (ones in the first i + 1 columns).
"""

import math


class PlanarArm:
    def __init__(self, L, m, r, I):
        n = len(L)
        if not (len(m) == len(r) == len(I) == n):
            raise ValueError("L, m, r and I must have the same length")
        self.L = list(L)
        self.m = list(m)
        self.r = list(r)
        self.I = list(I)
        self.n = n


def points(arm, q):
    """Return (joints, coms): the joint positions p_i and the centers of mass c_i."""
    x = y = a = 0.0
    joints, coms = [], []
    for i in range(arm.n):
        a += q[i]
        joints.append((x, y))
        coms.append((x + arm.r[i] * math.cos(a), y + arm.r[i] * math.sin(a)))
        x += arm.L[i] * math.cos(a)
        y += arm.L[i] * math.sin(a)
    return joints, coms


def com_jacobians(arm, q):
    """Return lists Jv, Jw. Column j of Jv[i] is z x (c_i - p_j) for j <= i."""
    joints, coms = points(arm, q)
    n = arm.n
    Jv, Jw = [], []
    for i in range(n):
        cx, cy = coms[i]
        rows = [[0.0] * n, [0.0] * n]
        for j in range(i + 1):
            px, py = joints[j]
            rows[0][j] = -(cy - py)
            rows[1][j] = cx - px
        Jv.append(rows)
        Jw.append([1.0 if j <= i else 0.0 for j in range(n)])
    return Jv, Jw


def mass_matrix(arm, q):
    """The joint-space inertia matrix M(q), a symmetric n x n list of rows."""
    n = arm.n
    Jv, Jw = com_jacobians(arm, q)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for a in range(n):
            for b in range(n):
                M[a][b] += arm.m[i] * (Jv[i][0][a] * Jv[i][0][b] + Jv[i][1][a] * Jv[i][1][b])
                M[a][b] += arm.I[i] * Jw[i][a] * Jw[i][b]
    return M


def kinetic_energy(arm, q, qd):
    """K = (1/2) qd^T M(q) qd."""
    M = mass_matrix(arm, q)
    n = arm.n
    return 0.5 * sum(qd[a] * M[a][b] * qd[b] for a in range(n) for b in range(n))


def gravity_torque(arm, q, g=9.81):
    """g(q) = dP/dq with P = sum_i m_i g y_ci; component j is sum_{i >= j} m_i g (x_ci - x_pj)."""
    joints, coms = points(arm, q)
    out = []
    for j in range(arm.n):
        out.append(sum(arm.m[i] * g * (coms[i][0] - joints[j][0]) for i in range(j, arm.n)))
    return out


def mass_matrix_derivatives(arm, q, h=1e-6):
    """dM/dq_k for each k, by central differences."""
    out = []
    for k in range(arm.n):
        qp = list(q)
        qm = list(q)
        qp[k] += h
        qm[k] -= h
        Mp = mass_matrix(arm, qp)
        Mm = mass_matrix(arm, qm)
        out.append([[(Mp[a][b] - Mm[a][b]) / (2 * h) for b in range(arm.n)] for a in range(arm.n)])
    return out


def coriolis_matrix(arm, q, qd, h=1e-6):
    """C(q, qd) from the Christoffel symbols c_ijk = (dM_kj/dq_i + dM_ki/dq_j - dM_ij/dq_k) / 2.

    C[k][j] = sum_i c_ijk qd_i.
    """
    n = arm.n
    dM = mass_matrix_derivatives(arm, q, h)
    C = [[0.0] * n for _ in range(n)]
    for k in range(n):
        for j in range(n):
            s = 0.0
            for i in range(n):
                s += 0.5 * (dM[i][k][j] + dM[j][k][i] - dM[k][i][j]) * qd[i]
            C[k][j] = s
    return C


def inverse_dynamics(arm, q, qd, qdd, g=9.81):
    """tau = M(q) qdd + C(q, qd) qd + g(q)."""
    n = arm.n
    M = mass_matrix(arm, q)
    C = coriolis_matrix(arm, q, qd)
    G = gravity_torque(arm, q, g)
    return [sum(M[k][j] * qdd[j] + C[k][j] * qd[j] for j in range(n)) + G[k] for k in range(n)]


def cholesky(A):
    """Lower triangular L with A = L L^T. Raises ValueError if A is not positive definite."""
    n = len(A)
    Lm = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = A[i][j] - sum(Lm[i][k] * Lm[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("matrix is not positive definite")
                Lm[i][i] = math.sqrt(s)
            else:
                Lm[i][j] = s / Lm[j][j]
    return Lm


def two_link_point_mass():
    """The check arm: L1 = L2 = 1 m, point masses of 1 kg at the link ends."""
    return PlanarArm([1.0, 1.0], [1.0, 1.0], [1.0, 1.0], [0.0, 0.0])
