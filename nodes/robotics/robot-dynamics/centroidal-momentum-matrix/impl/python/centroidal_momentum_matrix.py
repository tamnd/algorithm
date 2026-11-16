# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/centroidal-momentum-matrix/. The authors are listed in prov/M8T9ZN.jsonl.
"""Centroidal momentum matrix A_G(q) of a kinematic tree, with h_G = A_G qd.

Spatial vectors follow Featherstone, Rigid Body Dynamics Algorithms (2008),
with the angular part first: a motion vector is (omega, v) and a force or
momentum vector is (n, f). h_G = (k_G, l_G) holds the angular momentum
about the center of mass G and the linear momentum, both in the axes of
the base frame {s}. The frame G has its origin at the center of mass and
its axes parallel to {s}.

The tree has bodies 0 .. n-1. parent[i] < i is the parent body, or -1 for
the base. Joint i has one degree of freedom with the screw axis S_i (a
6-vector in the coordinates of body i). At joint value q_i the pose of
frame i in the frame of its parent is T_tree[i] exp([S_i] q_i). A floating
base is modelled as a chain of six joints (three prismatic, three
revolute) whose first five bodies have no mass.

Column j of A_G is Ad(T_jG)^T I^c_j S_j, where I^c_j is the composite
inertia of the subtree of body j and T_jG is the pose of G in frame j.
"""

import rbm


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


def mass_and_com(inertia):
    """Return (m, c) of a 6x6 spatial inertia."""
    m = inertia[5][5]
    if m <= 0.0:
        return 0.0, [0.0, 0.0, 0.0]
    return m, [inertia[2][4] / m, inertia[0][5] / m, inertia[1][3] / m]


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
        """Append a body and return its index (see the module comment)."""
        if not -1 <= parent < self.n:
            raise ValueError("the parent must be -1 or an earlier body")
        if len(screw) != 6 or len(inertia) != 6:
            raise ValueError("a screw axis has 6 entries and an inertia is 6x6")
        self.parent.append(parent)
        self.tree.append(tree)
        self.screw.append([float(x) for x in screw])
        self.inertia.append(inertia)
        return self.n - 1


def body_poses(model, q):
    """Return the pose T_si of every body frame in the base frame."""
    out = []
    for i in range(model.n):
        local = rbm.mul(model.tree[i], rbm.se3_exp(rbm.scale(model.screw[i], q[i])))
        p = model.parent[i]
        out.append(local if p < 0 else rbm.mul(out[p], local))
    return out


def centroidal_momentum_matrix(model, q):
    """Return (A_G, m, c): the 6 x n matrix, the total mass and the center of mass.

    Raise ValueError if the total mass is not positive.
    """
    n = model.n
    if len(q) != n:
        raise ValueError("q needs one entry per joint")
    poses = body_poses(model, q)  # @line C1
    xs = []
    for i in range(n):
        p = model.parent[i]
        rel = poses[i] if p < 0 else rbm.mul(rbm.T_inv(poses[p]), poses[i])
        xs.append(rbm.adjoint(rbm.T_inv(rel)))
    ic = [[list(row) for row in model.inertia[i]] for i in range(n)]  # @line C2
    for i in range(n - 1, -1, -1):  # @line C3
        p = model.parent[i]
        if p >= 0:
            ic[p] = rbm.add(ic[p], rbm.mul(rbm.transpose(xs[i]), rbm.mul(ic[i], xs[i])))
    total, moment = 0.0, [0.0, 0.0, 0.0]  # @line C4
    for i in range(n):
        m_i, c_i = mass_and_com(model.inertia[i])
        total += m_i
        moment = rbm.add(moment, rbm.scale(rbm.T_apply(poses[i], c_i), m_i))
    if not total > 0.0:
        raise ValueError("the total mass must be positive")
    com = rbm.scale(moment, 1.0 / total)
    pose_g = rbm.make_T(rbm.eye(3), com)
    cols = []
    for j in range(n):  # @line C5
        x_jg = rbm.adjoint(rbm.mul(rbm.T_inv(poses[j]), pose_g))
        cols.append(rbm.matvec(rbm.transpose(x_jg), rbm.matvec(ic[j], model.screw[j])))  # @line C6
    return rbm.transpose(cols), total, com  # @line C7


def centroidal_momentum(model, q, qd):
    """Return h_G = A_G(q) qd = (k_G, l_G)."""
    a_g, _, _ = centroidal_momentum_matrix(model, q)
    return rbm.matvec(a_g, qd)
