# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/geometric-jacobian/. The authors are listed in prov/TB3AFJ.jsonl.
"""Geometric Jacobian of a serial arm in the form of Siciliano et al.

The arm is given by standard Denavit-Hartenberg rows (kind, d, theta, a,
alpha), where kind is "R" (revolute: the joint value adds to theta) or
"P" (prismatic: the joint value adds to d). The link transform is
A_i = Rz(theta) Tz(d) Tx(a) Rx(alpha).

geometric_jacobian returns the 6 by n matrix whose top three rows give the
velocity p' of the origin of the end effector frame and whose bottom three
rows give the angular velocity omega, both in base coordinates:

    revolute column i:  (z_{i-1} x (p_e - p_{i-1}), z_{i-1})
    prismatic column i: (z_{i-1}, 0)

(Robotics: Modelling, Planning and Control, Section 3.1.3). to_space_twist
reorders a column into the space twist (omega, v_s) of Lynch and Park, with
v_s = p' - omega x p_e. Matrices are lists of rows.
"""

import math

import rbm


def dh_transform(d, theta, a, alpha):
    """Return Rz(theta) Tz(d) Tx(a) Rx(alpha) as a 4x4 matrix."""
    ct, st = math.cos(theta), math.sin(theta)
    ca, sa = math.cos(alpha), math.sin(alpha)
    return [
        [ct, -st * ca, st * sa, a * ct],
        [st, ct * ca, -ct * sa, a * st],
        [0.0, sa, ca, d],
        [0.0, 0.0, 0.0, 1.0],
    ]


def link_transform(row, x):
    kind, d, theta, a, alpha = row
    if kind == "R":
        return dh_transform(d, theta + x, a, alpha)
    return dh_transform(d + x, theta, a, alpha)


def forward_kinematics(dh, q):
    """Return the pose T_0n(q) of the last frame in the base frame."""
    t = rbm.eye(4)
    for row, x in zip(dh, q):
        t = rbm.mul(t, link_transform(row, x))
    return t


def geometric_jacobian(dh, q):
    """Return the 6 by n geometric Jacobian, linear part first."""
    t = rbm.eye(4)  # @line L1
    frames = [t]
    for row, x in zip(dh, q):  # @line L2
        t = rbm.mul(t, link_transform(row, x))  # @line L3
        frames.append(t)  # @line L4
    pe = [t[0][3], t[1][3], t[2][3]]  # @line L5
    n = len(dh)
    jac = rbm.zeros(6, n)
    for i in range(n):  # @line L6
        f = frames[i]
        z = [f[0][2], f[1][2], f[2][2]]  # @line L7
        p = [f[0][3], f[1][3], f[2][3]]
        if dh[i][0] == "R":  # @line L8
            col = rbm.cross(z, rbm.sub(pe, p)) + z
        else:
            col = z + [0.0, 0.0, 0.0]  # @line L9
        for r in range(6):
            jac[r][i] = col[r]
    return jac  # @line L10


def to_space_twist(jac, pe):
    """Return the space Jacobian (omega first, v_s = p' - omega x p_e)."""
    n = len(jac[0])
    out = rbm.zeros(6, n)
    for c in range(n):
        lin = [jac[r][c] for r in range(3)]
        w = [jac[r + 3][c] for r in range(3)]
        v = rbm.sub(lin, rbm.cross(w, pe))
        for r in range(3):
            out[r][c] = w[r]
            out[r + 3][c] = v[r]
    return out


def to_body_twist(jac, t):
    """Return the body Jacobian: (R^T omega, R^T p') for each column."""
    rt = [[t[j][i] for j in range(3)] for i in range(3)]
    n = len(jac[0])
    out = rbm.zeros(6, n)
    for c in range(n):
        lin = rbm.matvec(rt, [jac[r][c] for r in range(3)])
        w = rbm.matvec(rt, [jac[r + 3][c] for r in range(3)])
        for r in range(3):
            out[r][c] = w[r]
            out[r + 3][c] = lin[r]
    return out
