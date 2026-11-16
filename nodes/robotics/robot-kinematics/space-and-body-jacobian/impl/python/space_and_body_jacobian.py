# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-and-body-jacobian/. The authors are listed in prov/DQFEN4.jsonl.
"""Space and body Jacobians of an open chain in product of exponentials form.

Lynch and Park, Modern Robotics, Section 5.1:
- T(q) = exp([S1] q1) ... exp([Sn] qn) M with space screw axes S_i, and
  column i of J_s is Ad of exp([S1] q1) ... exp([S_i-1] q_i-1) applied to S_i.
- T(q) = M exp([B1] q1) ... exp([Bn] qn) with body screw axes B_i, and
  column i of J_b is Ad of exp(-[Bn] qn) ... exp(-[B_i+1] q_i+1) applied to B_i.
- B_i = Ad of M^-1 applied to S_i, and J_b = Ad of T^-1 applied to J_s.

A screw axis is (omega, v), angular part first. Matrices are lists of rows.
"""

import rbm


def space_jacobian(slist, q):
    """Return the 6 by n space Jacobian J_s(q)."""
    t = rbm.eye(4)  # @line L1
    cols = []
    for s, x in zip(slist, q):  # @line L2
        cols.append(rbm.matvec(rbm.adjoint(t), s))  # @line L3
        t = rbm.mul(t, rbm.se3_exp([y * x for y in s]))  # @line L4
    return rbm.transpose(cols)  # @line L5


def body_jacobian(blist, q):
    """Return the 6 by n body Jacobian J_b(q)."""
    n = len(blist)
    t = rbm.eye(4)  # @line L6
    cols = [None] * n
    for i in range(n - 1, -1, -1):  # @line L7
        cols[i] = rbm.matvec(rbm.adjoint(t), blist[i])  # @line L8
        t = rbm.mul(t, rbm.se3_exp([-y * q[i] for y in blist[i]]))  # @line L9
    return rbm.transpose(cols)  # @line L10


def fk_space(slist, m, q):
    """Return T(q) = exp([S1] q1) ... exp([Sn] qn) M."""
    t = rbm.eye(4)
    for s, x in zip(slist, q):
        t = rbm.mul(t, rbm.se3_exp([y * x for y in s]))
    return rbm.mul(t, m)


def fk_body(m, blist, q):
    """Return T(q) = M exp([B1] q1) ... exp([Bn] qn)."""
    t = [row[:] for row in m]
    for b, x in zip(blist, q):
        t = rbm.mul(t, rbm.se3_exp([y * x for y in b]))
    return t


def body_screws(slist, m):
    """Return B_i = Ad of M^-1 applied to S_i."""
    ad = rbm.adjoint(rbm.T_inv(m))
    return [rbm.matvec(ad, s) for s in slist]


def space_to_body(js, t):
    """Return J_b = Ad of T^-1 times J_s."""
    return rbm.mul(rbm.adjoint(rbm.T_inv(t)), js)
