# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/articulated-body-algorithm/. The authors are listed in prov/0W0KC6.jsonl.
"""Articulated-body algorithm (ABA) for the forward dynamics of a kinematic tree.

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


def joint_transform(model, i, qi):
    """Return X_i, the motion transform from the parent of i to body i."""
    pose = rbm.mul(model.tree[i], rbm.se3_exp(rbm.scale(model.screw[i], qi)))
    return rbm.adjoint(rbm.T_inv(pose))


def aba(model, q, qd, tau, gravity=GRAVITY, f_ext=None):
    """Return the joint accelerations qdd = M(q)^(-1) (tau - C(q, qd) qd - g(q) + J^T f_ext).

    gravity is the acceleration of gravity in base coordinates. f_ext, if
    given, is a list of n external force vectors, each in the coordinates
    of its body (None for no force). Raise ValueError if an articulated
    inertia D_i is not positive, which happens only for bodies without
    mass or inertia.
    """
    n = model.n
    if not len(q) == len(qd) == len(tau) == n:
        raise ValueError("q, qd and tau need one entry per joint")
    zero = [0.0] * 6
    xs, v, c = [None] * n, [None] * n, [None] * n
    ia, pa = [None] * n, [None] * n
    for i in range(n):  # @line L1
        p = model.parent[i]
        s = model.screw[i]
        xs[i] = joint_transform(model, i, q[i])  # @line L2
        vj = rbm.scale(s, qd[i])
        v[i] = rbm.add(rbm.matvec(xs[i], zero if p < 0 else v[p]), vj)  # @line L3
        c[i] = cross_motion(v[i], vj)  # @line L4
        ia[i] = [list(row) for row in model.inertia[i]]  # @line L5
        pa[i] = cross_force(v[i], rbm.matvec(model.inertia[i], v[i]))
        if f_ext is not None and f_ext[i] is not None:
            pa[i] = rbm.sub(pa[i], f_ext[i])
    u_vec, d, u = [None] * n, [0.0] * n, [0.0] * n
    for i in range(n - 1, -1, -1):  # @line L6
        s = model.screw[i]
        u_vec[i] = rbm.matvec(ia[i], s)  # @line L7
        d[i] = rbm.dot(s, u_vec[i])
        if not d[i] > 0.0:
            raise ValueError("articulated inertia about joint %d is not positive" % i)
        u[i] = tau[i] - rbm.dot(s, pa[i])
        p = model.parent[i]
        if p >= 0:  # @line L8
            ui = u_vec[i]
            i_art = [[ia[i][r][k] - ui[r] * ui[k] / d[i] for k in range(6)] for r in range(6)]  # @line L9
            p_art = rbm.add(rbm.add(pa[i], rbm.matvec(i_art, c[i])), rbm.scale(ui, u[i] / d[i]))  # @line L10
            xt = rbm.transpose(xs[i])
            ia[p] = rbm.add(ia[p], rbm.mul(xt, rbm.mul(i_art, xs[i])))  # @line L11
            pa[p] = rbm.add(pa[p], rbm.matvec(xt, p_art))
    a_base = [0.0, 0.0, 0.0] + [-x for x in gravity]  # @line L12
    a = [None] * n
    qdd = [0.0] * n
    for i in range(n):  # @line L13
        p = model.parent[i]
        a_prime = rbm.add(rbm.matvec(xs[i], a_base if p < 0 else a[p]), c[i])  # @line L14
        qdd[i] = (u[i] - rbm.dot(u_vec[i], a_prime)) / d[i]  # @line L15
        a[i] = rbm.add(a_prime, rbm.scale(model.screw[i], qdd[i]))  # @line L16
    return qdd  # @line L17
