# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rigid-body-dynamics-derivatives/. The authors are listed in prov/M6C9BY.jsonl.
"""Analytical derivatives of inverse and forward dynamics (Carpentier and Mansard, 2018).

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

The derivatives use two identities. If X_i depends on q_i as above, then
d(X_i m)/dq_i = crm(X_i m) S_i for a motion vector m, and
d(X_i^T f)/dq_i = X_i^T crf(S_i) f for a force vector f.

A derivative of a body quantity is stored as a dict from a joint index k
to the 6-vector of the partial derivative by the k-th coordinate. The
velocity and the acceleration of body i depend only on the joints on the
path from i to the root, so their dicts hold at most depth(i) entries.
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


def _map(xs, d):
    """Return {k: X d[k]} for a dict d of motion vectors."""
    return {k: rbm.matvec(xs, vec) for k, vec in d.items()}


def _add_into(d, k, vec):
    d[k] = rbm.add(d[k], vec) if k in d else vec


def rnea(model, q, qd, qdd, gravity=GRAVITY):
    """Return tau = M(q) qdd + C(q, qd) qd + g(q) by the recursive Newton-Euler algorithm."""
    return rnea_derivatives(model, q, qd, qdd, gravity)[0]


def rnea_derivatives(model, q, qd, qdd, gravity=GRAVITY):
    """Return (tau, dtau/dq, dtau/dqd, dtau/dqdd) at (q, qd, qdd).

    The three Jacobians are n x n lists of rows; dtau/dqdd is the
    joint-space inertia matrix M(q).
    """
    n = model.n
    if not len(q) == len(qd) == len(qdd) == n:
        raise ValueError("q, qd and qdd need one entry per joint")
    zero = [0.0] * 6
    a_base = [0.0, 0.0, 0.0] + [-x for x in gravity]
    xs, v, a, f = [None] * n, [None] * n, [None] * n, [None] * n
    dv_q, da_q, dv_qd, da_qd, da_qdd = ([None] * n for _ in range(5))
    df_q, df_qd, df_qdd = [None] * n, [None] * n, [None] * n
    for i in range(n):  # @line L1
        p = model.parent[i]
        s = model.screw[i]
        inertia = model.inertia[i]
        xs[i] = joint_transform(model, i, q[i])  # @line L2
        vj = rbm.scale(s, qd[i])
        xv = rbm.matvec(xs[i], zero if p < 0 else v[p])
        xa = rbm.matvec(xs[i], a_base if p < 0 else a[p])
        v[i] = rbm.add(xv, vj)
        a[i] = rbm.add(rbm.add(xa, rbm.scale(s, qdd[i])), cross_motion(v[i], vj))
        iv = rbm.matvec(inertia, v[i])
        f[i] = rbm.add(rbm.matvec(inertia, a[i]), cross_force(v[i], iv))
        # Derivatives by the joints above i: carried over from the parent.
        dv_q[i] = {} if p < 0 else _map(xs[i], dv_q[p])  # @line L3
        da_q[i] = {} if p < 0 else _map(xs[i], da_q[p])
        dv_qd[i] = {} if p < 0 else _map(xs[i], dv_qd[p])
        da_qd[i] = {} if p < 0 else _map(xs[i], da_qd[p])
        da_qdd[i] = {} if p < 0 else _map(xs[i], da_qdd[p])
        # The new column i.
        dv_q[i][i] = cross_motion(xv, s)  # @line L4
        da_q[i][i] = cross_motion(xa, s)
        dv_qd[i][i] = list(s)  # @line L5
        da_qd[i][i] = cross_motion(v[i], s)
        da_qdd[i][i] = list(s)
        for k in dv_q[i]:  # @line L6
            da_q[i][k] = rbm.add(da_q[i][k], cross_motion(dv_q[i][k], vj))
            da_qd[i][k] = rbm.add(da_qd[i][k], cross_motion(dv_qd[i][k], vj))
        df_q[i], df_qd[i] = {}, {}
        for dv, da, df in ((dv_q[i], da_q[i], df_q[i]), (dv_qd[i], da_qd[i], df_qd[i])):  # @line L7
            for k in dv:
                df[k] = rbm.add(rbm.add(rbm.matvec(inertia, da[k]), cross_force(dv[k], iv)),
                                cross_force(v[i], rbm.matvec(inertia, dv[k])))
        df_qdd[i] = {k: rbm.matvec(inertia, vec) for k, vec in da_qdd[i].items()}
    tau = [0.0] * n
    d_q, d_qd, d_qdd = rbm.zeros(n, n), rbm.zeros(n, n), rbm.zeros(n, n)
    for i in range(n - 1, -1, -1):  # @line L8
        s = model.screw[i]
        tau[i] = rbm.dot(s, f[i])
        for out, df in ((d_q, df_q[i]), (d_qd, df_qd[i]), (d_qdd, df_qdd[i])):  # @line L9
            for k, vec in df.items():
                out[i][k] = rbm.dot(s, vec)
        p = model.parent[i]
        if p >= 0:  # @line L10
            xt = rbm.transpose(xs[i])
            for src, dst in ((df_q[i], df_q[p]), (df_qd[i], df_qd[p]), (df_qdd[i], df_qdd[p])):  # @line L11
                for k, vec in src.items():
                    _add_into(dst, k, rbm.matvec(xt, vec))
            _add_into(df_q[p], i, rbm.matvec(xt, cross_force(s, f[i])))  # @line L12
            f[p] = rbm.add(f[p], rbm.matvec(xt, f[i]))  # @line L13
    return tau, d_q, d_qd, d_qdd  # @line L14


def forward_dynamics_derivatives(model, q, qd, tau, gravity=GRAVITY):
    """Return (qdd, dqdd/dq, dqdd/dqd, dqdd/dtau) for qdd = FD(q, qd, tau).

    qdd solves M qdd = tau - C qd - g. Then dFD/du = -M^(-1) dID/du at
    (q, qd, qdd) for u = q and u = qd, and dFD/dtau = M^(-1).
    """
    n = model.n
    bias, _, _, m = rnea_derivatives(model, q, qd, [0.0] * n, gravity)
    qdd = rbm.solve(m, rbm.sub(tau, bias))
    _, d_q, d_qd, _ = rnea_derivatives(model, q, qd, qdd, gravity)
    m_inv = rbm.inv(m)
    return qdd, rbm.scale(rbm.mul(m_inv, d_q), -1.0), rbm.scale(rbm.mul(m_inv, d_qd), -1.0), m_inv
