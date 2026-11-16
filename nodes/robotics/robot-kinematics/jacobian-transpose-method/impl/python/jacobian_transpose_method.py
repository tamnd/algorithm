# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobian-transpose-method/. The authors are listed in prov/NPCR98.jsonl.
"""Inverse kinematics by Jacobian transpose steps.

- transpose_step(j, e, alpha) returns dq = alpha J^T e. With alpha=None
  the gain is the one of Buss and Kim, alpha = <e, J J^T e> / |J J^T e|^2, the
  gain that makes the linear prediction J dq closest to e.
- ik_transpose(fk, jac, x_d, q0, alpha, ...) is the iteration of the page.
  It returns (q, history, ok): the last joint vector, the error norms before
  each step, and whether the tolerance was met.
- planar_fk and planar_jacobian give a planar arm with n revolute joints,
  used by the tests and the example of the page.

Matrices are lists of rows. The module needs only the standard library.
"""

import math


def matvec(a, x):
    return [sum(r * v for r, v in zip(row, x)) for row in a]


def transpose(a):
    return [list(col) for col in zip(*a)]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm(x):
    return math.sqrt(dot(x, x))


def transpose_step(j, e, alpha=None):
    """Return alpha J^T e, with the gain of Buss and Kim when alpha is None."""
    g = matvec(transpose(j), e)  # @line L6
    if alpha is None:
        jg = matvec(j, g)
        den = dot(jg, jg)
        if den == 0.0:
            return [0.0] * len(g)  # J^T e = 0: a stationary point
        alpha = dot(e, jg) / den  # @line L7
    return [alpha * x for x in g]


def ik_transpose(fk, jac, x_d, q0, alpha=None, eps=1e-10, max_iter=5000):
    """Return (q, history, ok) for the task fk(q) = x_d by Jacobian transpose steps."""
    q = [float(x) for x in q0]  # @line L1
    history = []
    for _ in range(max_iter):  # @line L2
        e = [a - b for a, b in zip(x_d, fk(q))]  # @line L3
        history.append(norm(e))
        if history[-1] <= eps:  # @line L4
            return q, history, True
        j = jac(q)  # @line L5
        dq = transpose_step(j, e, alpha)
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
