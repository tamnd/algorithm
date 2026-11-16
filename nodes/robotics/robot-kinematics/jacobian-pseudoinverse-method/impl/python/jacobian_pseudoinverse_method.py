# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobian-pseudoinverse-method/. The authors are listed in prov/MNF4KJ.jsonl.
"""Inverse kinematics by repeated pseudoinverse steps.

- pinv(a, rtol) is the Moore-Penrose pseudoinverse of any matrix, from a
  one-sided Jacobi singular value decomposition. Singular values at most
  rtol times the largest one count as zero.
- ik_pose(m, blist, t_d, q0, ...) is the algorithm of the page: the error
  is the body twist V_b = log(T(q)^-1 T_d), and the step is J_b^+ V_b.
  This is the numerical inverse kinematics algorithm of Lynch and Park,
  Modern Robotics, Section 6.2.2.
- ik_position(fk, jac, x_d, q0, ...) is the same loop for a position task
  x = fk(q) in R^m, with the error x_d - fk(q).

The arm is in the product of exponentials form: T(q) = M exp([B1] q1) ...
exp([Bn] qn) with body screw axes B_i = (omega, v), angular part first.
Matrices are lists of rows. ik_pose and ik_position return None when they
do not reach the tolerance within max_iter steps.
"""

import math

import rbm


def _columns(a):
    return [list(c) for c in zip(*a)]


def svd(a, sweeps=60):
    """Return (u_cols, sigma, v_cols) with a = sum_j sigma_j u_j v_j^T.

    One-sided Jacobi (Hestenes): rotate pairs of columns of a until all
    columns are orthogonal. The rotations are collected in v. u_j is the
    column j divided by its norm sigma_j; for sigma_j = 0, u_j is zero.
    """
    m, n = len(a), len(a[0])
    w = _columns(a)  # n columns of length m
    v = [[1.0 if i == j else 0.0 for i in range(n)] for j in range(n)]  # columns of V
    for _ in range(sweeps):
        rotated = False
        for p in range(n - 1):
            for r in range(p + 1, n):
                alpha = rbm.dot(w[p], w[p])
                beta = rbm.dot(w[r], w[r])
                gamma = rbm.dot(w[p], w[r])
                if gamma == 0.0 or abs(gamma) <= 1e-15 * math.sqrt(alpha * beta):
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                for vec in (w, v):
                    x, y = vec[p], vec[r]
                    vec[p] = [c * xi - s * yi for xi, yi in zip(x, y)]
                    vec[r] = [s * xi + c * yi for xi, yi in zip(x, y)]
        if not rotated:
            break
    sigma = [rbm.norm(col) for col in w]
    u = [[x / s for x in col] if s > 0.0 else [0.0] * m for col, s in zip(w, sigma)]
    return u, sigma, v


def pinv(a, rtol=1e-10):
    """Return the n by m pseudoinverse of the m by n matrix a.

    a^+ = sum over sigma_j > rtol * max(sigma) of v_j u_j^T / sigma_j.
    """
    m, n = len(a), len(a[0])
    u, sigma, v = svd(a)
    smax = max(sigma) if sigma else 0.0
    out = rbm.zeros(n, m)
    for uj, sj, vj in zip(u, sigma, v):
        if sj > rtol * smax and sj > 0.0:
            for i in range(n):
                f = vj[i] / sj
                if f != 0.0:
                    row = out[i]
                    for k in range(m):
                        row[k] += f * uj[k]
    return out


def fk_body(m, blist, q):
    """Return T(q) = M exp([B1] q1) ... exp([Bn] qn)."""
    t = [row[:] for row in m]
    for b, x in zip(blist, q):
        t = rbm.mul(t, rbm.se3_exp([y * x for y in b]))
    return t


def body_jacobian(blist, q):
    """Return the 6 by n body Jacobian; column i is Ad of exp(-[B_n] q_n)...exp(-[B_i+1] q_i+1) applied to B_i."""
    n = len(blist)
    t = rbm.eye(4)
    cols = [None] * n
    for i in range(n - 1, -1, -1):
        cols[i] = rbm.matvec(rbm.adjoint(t), blist[i])
        t = rbm.mul(t, rbm.se3_exp([-y * q[i] for y in blist[i]]))
    return rbm.transpose(cols)


def ik_pose(m, blist, t_d, q0, eps_w=1e-10, eps_v=1e-10, max_iter=100, rtol=1e-10):
    """Return joint values q with T(q) = t_d within (eps_w, eps_v), or None."""
    q = [float(x) for x in q0]  # @line L1
    for _ in range(max_iter):  # @line L2
        vb = rbm.se3_log(rbm.mul(rbm.T_inv(fk_body(m, blist, q)), t_d))  # @line L3
        if rbm.norm(vb[:3]) <= eps_w and rbm.norm(vb[3:]) <= eps_v:  # @line L4
            return q
        jb = body_jacobian(blist, q)  # @line L5
        step = rbm.matvec(pinv(jb, rtol), vb)
        q = [x + d for x, d in zip(q, step)]  # @line L6
    return None  # @line L7


def ik_position(fk, jac, x_d, q0, eps=1e-11, max_iter=100, rtol=1e-10):
    """Return q with |x_d - fk(q)| <= eps, or None, by steps q <- q + J^+ e."""
    q = [float(x) for x in q0]
    for _ in range(max_iter):
        e = rbm.sub(x_d, fk(q))
        if rbm.norm(e) <= eps:
            return q
        step = rbm.matvec(pinv(jac(q), rtol), e)
        q = [x + d for x, d in zip(q, step)]
    return None
