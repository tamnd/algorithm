# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/recursive-newton-euler-algorithm/. The authors are listed in prov/8QXENF.jsonl.
"""Recursive Newton-Euler algorithm (RNEA) for a kinematic tree.

Spatial vectors follow Featherstone, Rigid Body Dynamics Algorithms (2008),
with the angular part first: a motion vector is (omega, v) and a force
vector is (n, f). Every quantity of body i is in the coordinates of the
frame of body i.

The tree has bodies 0 .. n-1. parent[i] < i is the parent body, or -1 for
the fixed base. Joint i has one degree of freedom with the screw axis
S_i (a 6-vector in the coordinates of body i). At joint value q_i the pose
of frame i in the frame of its parent is T_tree[i] exp([S_i] q_i). X_i is
the 6x6 matrix that maps motion vectors from parent coordinates to body i
coordinates, and its transpose maps force vectors from body i to the
parent.
"""

import rbm

# Gravity in the base frame, z up, in m/s^2.
GRAVITY = [0.0, 0.0, -9.81]


def spatial_inertia(mass, com, inertia_com):
    """Return the 6x6 spatial inertia about the frame origin.

    mass in kg, com the center of mass c in the body frame, inertia_com
    the 3x3 rotational inertia about the center of mass. The result is
    [[I_c + m [c][c]^T, m [c]], [m [c]^T, m 1]].
    """
    c = rbm.hat3(com)
    top_left = rbm.add(inertia_com, rbm.scale(rbm.mul(c, rbm.transpose(c)), mass))
    out = rbm.zeros(6, 6)
    for r in range(3):
        for k in range(3):
            out[r][k] = top_left[r][k]
            out[r][k + 3] = mass * c[r][k]
            out[r + 3][k] = mass * c[k][r]
        out[r + 3][r + 3] = mass
    return out


def cross_motion(v, m):
    """Return crm(v) m = (w x m_w, v_lin x m_w + w x m_lin) for motion vectors."""
    w, vl = v[:3], v[3:]
    return rbm.cross(w, m[:3]) + rbm.add(rbm.cross(vl, m[:3]), rbm.cross(w, m[3:]))


def cross_force(v, f):
    """Return crf(v) f = (w x n + v_lin x f_lin, w x f_lin) for a force vector f."""
    w, vl = v[:3], v[3:]
    return rbm.add(rbm.cross(w, f[:3]), rbm.cross(vl, f[3:])) + rbm.cross(w, f[3:])


class Model:
    """A kinematic tree of rigid bodies, each with one joint to its parent."""

    def __init__(self):
        self.parent = []
        self.tree = []
        self.screw = []
        self.inertia = []

    @property
    def n(self):
        return len(self.parent)

    def add_body(self, parent, tree, screw, inertia):
        """Append a body and return its index.

        parent is -1 or an earlier body. tree is the 4x4 pose of the new
        frame in the parent frame at q = 0. screw is (omega, v) with
        |omega| = 1, or omega = 0 and |v| = 1. inertia is 6x6.
        """
        if not -1 <= parent < self.n:
            raise ValueError("the parent must be -1 or an earlier body")
        if len(screw) != 6 or len(inertia) != 6:
            raise ValueError("a screw axis has 6 entries and an inertia is 6x6")
        self.parent.append(parent)
        self.tree.append(tree)
        self.screw.append([float(x) for x in screw])
        self.inertia.append(inertia)
        return self.n - 1


def joint_transform(model, i, qi):
    """Return X_i, the motion transform from the parent of i to body i."""
    pose = rbm.mul(model.tree[i], rbm.se3_exp(rbm.scale(model.screw[i], qi)))
    return rbm.adjoint(rbm.T_inv(pose))


def rnea(model, q, qd, qdd, gravity=GRAVITY, f_ext=None):
    """Return the joint forces tau with tau = M(q) qdd + C(q, qd) qd + g(q) - J^T f_ext.

    gravity is the 3-vector of the acceleration of gravity in base
    coordinates. f_ext, if given, is a list of n external force vectors,
    each in the coordinates of its body (None for no force).
    """
    n = model.n
    if not len(q) == len(qd) == len(qdd) == n:
        raise ValueError("q, qd and qdd need one entry per joint")
    a_base = [0.0, 0.0, 0.0] + [-x for x in gravity]  # @line L1
    zero = [0.0] * 6
    xs, f = [None] * n, [None] * n
    v, a = [None] * n, [None] * n
    for i in range(n):  # @line L2
        p = model.parent[i]
        s = model.screw[i]
        xs[i] = joint_transform(model, i, q[i])  # @line L3
        v_p = zero if p < 0 else v[p]
        a_p = a_base if p < 0 else a[p]
        vj = rbm.scale(s, qd[i])
        v[i] = rbm.add(rbm.matvec(xs[i], v_p), vj)  # @line L4
        a[i] = rbm.add(rbm.add(rbm.matvec(xs[i], a_p), rbm.scale(s, qdd[i])), cross_motion(v[i], vj))  # @line L5
        inertia = model.inertia[i]
        f[i] = rbm.add(rbm.matvec(inertia, a[i]), cross_force(v[i], rbm.matvec(inertia, v[i])))  # @line L6
        if f_ext is not None and f_ext[i] is not None:
            f[i] = rbm.sub(f[i], f_ext[i])
    tau = [0.0] * n
    for i in range(n - 1, -1, -1):  # @line L7
        tau[i] = rbm.dot(model.screw[i], f[i])  # @line L8
        p = model.parent[i]
        if p >= 0:  # @line L9
            f[p] = rbm.add(f[p], rbm.matvec(rbm.transpose(xs[i]), f[i]))
    return tau  # @line L10
