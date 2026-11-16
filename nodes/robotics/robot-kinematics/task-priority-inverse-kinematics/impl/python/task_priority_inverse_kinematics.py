# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/task-priority-inverse-kinematics/. The authors are listed in prov/791J72.jsonl.
"""Task-priority inverse kinematics.

- pinv(a, tol) is the Moore-Penrose pseudoinverse by a one-sided Jacobi
  singular value decomposition. Singular values below tol times the largest
  one are treated as zero.
- priority_step(tasks) takes a list of (J_i, e_i), highest priority first,
  and returns the joint step of the recursive form of Siciliano and Slotine:
  dq_i = dq_(i-1) + (J_i P_(i-1))^+ (e_i - J_i dq_(i-1)), with
  P_i = P_(i-1) - (J_i P_(i-1))^+ (J_i P_(i-1)) and P_0 = I.
  For two tasks this is the step of Nakamura, Hanafusa and Yoshikawa,
  dq = J1^+ e1 + (J2 P1)^+ (e2 - J2 J1^+ e1).
- ik_task_priority(tasks, q0, ...) iterates the step for position tasks
  given as (fk_i, jac_i, x_d_i). It stops when the step is small, because a
  lower task may not be reachable, and returns (q, steps).

Matrices are lists of rows. The module needs only the standard library.
"""

import math


def transpose(a):
    return [list(col) for col in zip(*a)]


def mul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    return [sum(r * v for r, v in zip(row, x)) for row in a]


def eye(n):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def norm(x):
    return math.sqrt(sum(v * v for v in x))


def svd(a):
    """Return (u_cols, s, v_cols) with a = sum_i s_i u_i v_i^T, by one-sided Jacobi on the columns of a."""
    m, n = len(a), len(a[0])
    w = [[a[i][j] for i in range(m)] for j in range(n)]  # the columns of a
    v = eye(n)  # v[j] is column j of V
    for _ in range(60):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                alpha = sum(x * x for x in w[p])
                beta = sum(x * x for x in w[q])
                gamma = sum(x * y for x, y in zip(w[p], w[q]))
                if abs(gamma) <= 1e-15 * math.sqrt(alpha * beta) or gamma == 0.0:
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = math.copysign(1.0, zeta) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                w[p], w[q] = [c * x - s * y for x, y in zip(w[p], w[q])], [s * x + c * y for x, y in zip(w[p], w[q])]
                v[p], v[q] = [c * x - s * y for x, y in zip(v[p], v[q])], [s * x + c * y for x, y in zip(v[p], v[q])]
        if not rotated:
            break
    s = [norm(col) for col in w]
    u = [[x / sv for x in col] if sv > 0.0 else [0.0] * m for col, sv in zip(w, s)]
    return u, s, v


def pinv(a, tol=1e-10):
    """Return the n by m Moore-Penrose pseudoinverse of the m by n matrix a."""
    m, n = len(a), len(a[0])
    u, s, v = svd(a)
    smax = max(s) if s else 0.0
    out = [[0.0] * m for _ in range(n)]
    for uk, sk, vk in zip(u, s, v):
        if sk > tol * smax and sk > 0.0:
            for i in range(n):
                f = vk[i] / sk
                for j in range(m):
                    out[i][j] += f * uk[j]
    return out


def priority_step(tasks, n=None, tol=1e-10):
    """Return the joint step for a stack of tasks [(J_1, e_1), (J_2, e_2), ...], highest first."""
    if n is None:
        n = len(tasks[0][0][0])
    dq = [0.0] * n  # @line L1
    p = eye(n)  # @line L1
    for j, e in tasks:  # @line L2
        jp = mul(j, p)  # @line L3
        jp_pinv = pinv(jp, tol)  # @line L4
        r = [a - b for a, b in zip(e, matvec(j, dq))]  # @line L5
        dq = [a + b for a, b in zip(dq, matvec(jp_pinv, r))]  # @line L6
        q = mul(jp_pinv, jp)
        p = [[pij - qij for pij, qij in zip(prow, qrow)] for prow, qrow in zip(p, q)]  # @line L7
    return dq  # @line L8


def ik_task_priority(tasks, q0, eps=1e-12, max_iter=500, tol=1e-10):
    """Iterate priority steps for position tasks [(fk_i, jac_i, x_d_i), ...]; return (q, steps)."""
    q = [float(x) for x in q0]
    for k in range(max_iter):
        stack = [(jac(q), [a - b for a, b in zip(x_d, fk(q))]) for fk, jac, x_d in tasks]
        dq = priority_step(stack, len(q), tol)
        q = [a + b for a, b in zip(q, dq)]
        if norm(dq) <= eps:
            return q, k + 1
    return q, max_iter
