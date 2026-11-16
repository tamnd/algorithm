# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/composite-rigid-body-algorithm/. The authors are listed in prov/7BWY71.jsonl.
"""Composite rigid body algorithm (CRBA) for the joint-space inertia matrix.

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

crba(model, q) returns H(q). forward_dynamics solves H qdd = tau - C with
the bias C from one Newton-Euler pass with qdd = 0 and a Cholesky factor.
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


def crba(model, q):
    """Return the joint-space inertia matrix H(q), an n x n list of rows."""
    n = model.n
    if len(q) != n:
        raise ValueError("q needs one entry per joint")
    xs = [joint_transform(model, i, q[i]) for i in range(n)]  # @line L1
    ic = [[list(row) for row in model.inertia[i]] for i in range(n)]
    h = rbm.zeros(n, n)
    for i in range(n - 1, -1, -1):  # @line L2
        p = model.parent[i]
        if p >= 0:  # @line L3
            ic[p] = rbm.add(ic[p], rbm.mul(rbm.transpose(xs[i]), rbm.mul(ic[i], xs[i])))
        f = rbm.matvec(ic[i], model.screw[i])  # @line L4
        h[i][i] = rbm.dot(model.screw[i], f)  # @line L5
        j = i  # @line L6
        while model.parent[j] >= 0:  # @line L7
            f = rbm.matvec(rbm.transpose(xs[j]), f)  # @line L8
            j = model.parent[j]
            h[i][j] = h[j][i] = rbm.dot(f, model.screw[j])  # @line L9
    return h  # @line L10


def bias_forces(model, q, qd, gravity=GRAVITY):
    """Return C(q, qd) qd + g(q) by one Newton-Euler pass with qdd = 0."""
    n = model.n
    a_base = [0.0, 0.0, 0.0] + [-x for x in gravity]
    xs, v, a, f = [None] * n, [None] * n, [None] * n, [None] * n
    for i in range(n):
        p = model.parent[i]
        xs[i] = joint_transform(model, i, q[i])
        vj = rbm.scale(model.screw[i], qd[i])
        v[i] = rbm.add(rbm.matvec(xs[i], [0.0] * 6 if p < 0 else v[p]), vj)
        a[i] = rbm.add(rbm.matvec(xs[i], a_base if p < 0 else a[p]), cross_motion(v[i], vj))
        inertia = model.inertia[i]
        f[i] = rbm.add(rbm.matvec(inertia, a[i]), cross_force(v[i], rbm.matvec(inertia, v[i])))
    out = [0.0] * n
    for i in range(n - 1, -1, -1):
        out[i] = rbm.dot(model.screw[i], f[i])
        if model.parent[i] >= 0:
            f[model.parent[i]] = rbm.add(f[model.parent[i]], rbm.matvec(rbm.transpose(xs[i]), f[i]))
    return out


def cholesky_solve(h, b):
    """Solve h x = b for a symmetric positive definite h with h = L L^T."""
    low = rbm.cholesky(h)
    n = len(b)
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(low[i][k] * y[k] for k in range(i))) / low[i][i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(low[k][i] * x[k] for k in range(i + 1, n))) / low[i][i]
    return x


def forward_dynamics(model, q, qd, tau, gravity=GRAVITY):
    """Return qdd = H^(-1) (tau - C qd - g) with H from crba."""
    rhs = rbm.sub(tau, bias_forces(model, q, qd, gravity))
    return cholesky_solve(crba(model, q), rhs)


def kinetic_energy(model, q, qd):
    """Return (1/2) qd^T H(q) qd."""
    return 0.5 * rbm.dot(qd, rbm.matvec(crba(model, q), qd))
