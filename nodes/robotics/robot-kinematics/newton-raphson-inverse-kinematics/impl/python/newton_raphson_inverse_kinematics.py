# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-raphson-inverse-kinematics/. The authors are listed in prov/85CD1Z.jsonl.
"""Inverse kinematics by Newton-Raphson steps.

- ik_newton(m, blist, t_d, q0, ...) is the algorithm of the page for an arm
  with as many joints as the task has dimensions (six for a full pose).
  The error is the body twist V_b = log(T(q)^-1 T_d) and the step solves
  J_b(q) dq = V_b. This is the Newton-Raphson method of Lynch and Park,
  Modern Robotics, Section 6.2, for a square Jacobian.
- newton_position(fk, jac, x_d, q0, ...) is the same loop for a position
  task x = fk(q) with as many joints as coordinates.

The arm is in the product of exponentials form T(q) = M exp([B1] q1) ...
exp([Bn] qn) with body screw axes B_i = (omega, v), angular part first.
Both functions return (q, history), where history lists the error norm
before each step, and q is None when the loop fails: the tolerance is not
met within max_iter steps, or the Jacobian is singular to working
precision.
"""

import rbm


def fk_body(m, blist, q):
    """Return T(q) = M exp([B1] q1) ... exp([Bn] qn)."""
    t = [row[:] for row in m]
    for b, x in zip(blist, q):
        t = rbm.mul(t, rbm.se3_exp([y * x for y in b]))
    return t


def body_jacobian(blist, q):
    """Return the 6 by n body Jacobian.

    Column i is Ad of exp(-[B_n] q_n) ... exp(-[B_i+1] q_i+1) applied to B_i.
    """
    n = len(blist)
    t = rbm.eye(4)
    cols = [None] * n
    for i in range(n - 1, -1, -1):
        cols[i] = rbm.matvec(rbm.adjoint(t), blist[i])
        t = rbm.mul(t, rbm.se3_exp([-y * q[i] for y in blist[i]]))
    return rbm.transpose(cols)


def ik_newton(m, blist, t_d, q0, eps_w=1e-10, eps_v=1e-10, max_iter=50):
    """Return (q, history) with T(q) = t_d within (eps_w, eps_v), or (None, history)."""
    q = [float(x) for x in q0]  # @line L1
    history = []
    for _ in range(max_iter):  # @line L2
        vb = rbm.se3_log(rbm.mul(rbm.T_inv(fk_body(m, blist, q)), t_d))  # @line L3
        history.append(rbm.norm(vb))
        if rbm.norm(vb[:3]) <= eps_w and rbm.norm(vb[3:]) <= eps_v:  # @line L4
            return q, history
        jb = body_jacobian(blist, q)  # @line L5
        try:
            step = rbm.solve(jb, vb)  # @line L6
        except ValueError:
            return None, history  # @line L7
        q = [x + d for x, d in zip(q, step)]  # @line L8
    return None, history  # @line L9


def newton_position(fk, jac, x_d, q0, eps=1e-12, max_iter=50):
    """Return (q, history) with |x_d - fk(q)| <= eps by steps J(q) dq = x_d - fk(q)."""
    q = [float(x) for x in q0]
    history = []
    for _ in range(max_iter):
        e = rbm.sub(x_d, fk(q))
        history.append(rbm.norm(e))
        if rbm.norm(e) <= eps:
            return q, history
        try:
            step = rbm.solve(jac(q), e)
        except ValueError:
            return None, history
        q = [x + d for x, d in zip(q, step)]
    return None, history
