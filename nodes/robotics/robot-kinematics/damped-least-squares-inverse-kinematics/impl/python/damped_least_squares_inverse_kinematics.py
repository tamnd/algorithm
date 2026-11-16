# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/damped-least-squares-inverse-kinematics/. The authors are listed in prov/J6EXM0.jsonl.
"""Inverse kinematics by damped least squares steps.

- dls_step(j, e, lam) returns dq = J^T (J J^T + lam^2 I)^-1 e, the step of
  the page. It solves an m by m system, where m is the number of task
  coordinates.
- dls_step_normal(j, e, lam) returns the same step in the form
  (J^T J + lam^2 I)^-1 J^T e, which solves an n by n system.
- ik_dls(fk, jac, x_d, q0, lam, ...) is the iteration of the page. It
  returns (q, history, ok): the last joint vector, the error norms before
  each step, and whether the tolerance was met. When the target is out of
  reach, q is the last iterate, which is the useful answer of the method.
- planar_fk and planar_jacobian give a planar arm with n revolute joints,
  used by the tests and the example of the page.

Matrices are lists of rows, as in the shared helper rbm.
"""

import math

import rbm


def dls_step(j, e, lam):
    """Return J^T (J J^T + lam^2 I)^-1 e."""
    m = len(j)
    jt = rbm.transpose(j)
    a = rbm.add(rbm.mul(j, jt), rbm.scale(rbm.eye(m), lam * lam))  # @line L6
    y = rbm.solve(a, e)  # @line L6
    return rbm.matvec(jt, y)  # @line L7


def dls_step_normal(j, e, lam):
    """Return (J^T J + lam^2 I)^-1 J^T e, the same step as dls_step."""
    jt = rbm.transpose(j)
    n = len(jt)
    a = rbm.add(rbm.mul(jt, j), rbm.scale(rbm.eye(n), lam * lam))
    return rbm.solve(a, rbm.matvec(jt, e))


def ik_dls(fk, jac, x_d, q0, lam, eps=1e-10, max_iter=500):
    """Return (q, history, ok) for the task fk(q) = x_d by damped least squares steps."""
    q = [float(x) for x in q0]  # @line L1
    history = []
    for _ in range(max_iter):  # @line L2
        e = rbm.sub(x_d, fk(q))  # @line L3
        history.append(rbm.norm(e))
        if history[-1] <= eps:  # @line L4
            return q, history, True
        j = jac(q)  # @line L5
        dq = dls_step(j, e, lam)
        q = [x + d for x, d in zip(q, dq)]  # @line L8
    return q, history, False  # @line L9


def planar_fk(lengths, q):
    """Return the hand position of a planar arm with the given link lengths."""
    x = y = a = 0.0
    for length, t in zip(lengths, q):
        a += t
        x += length * math.cos(a)
        y += length * math.sin(a)
    return [x, y]


def planar_jacobian(lengths, q):
    """Return the 2 by n Jacobian of planar_fk."""
    angles = []
    a = 0.0
    for t in q:
        a += t
        angles.append(a)
    n = len(q)
    row_x = [-sum(lengths[k] * math.sin(angles[k]) for k in range(i, n)) for i in range(n)]
    row_y = [sum(lengths[k] * math.cos(angles[k]) for k in range(i, n)) for i in range(n)]
    return [row_x, row_y]
