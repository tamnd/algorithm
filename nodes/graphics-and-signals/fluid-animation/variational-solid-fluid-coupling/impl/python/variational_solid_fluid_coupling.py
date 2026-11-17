# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-solid-fluid-coupling/. The authors are listed in prov/T5ZPKE.jsonl.

"""Variational pressure projection with face weights, and two-way coupling with a rigid body.

This is the method of Batty, Bertails and Bridson (2007) on the 2D MAC grid of
macgrid.py. The pressure p minimizes the kinetic energy

    KE(p) = 1/2 rho dx^2 sum_f w_f u_f^2 + 1/2 V^T M V,
    u = u* - (dt / rho) G p,   V = V* + dt M^-1 J p,

where w_f in [0, 1] is the part of face f that is open to the fluid, G p is
the pressure difference across a face divided by dx, and V = (vx, vy, omega)
is the velocity of one rigid body. The body covers the part b_f of face f. Its
mass matrix M = rho_s dx^2 R^T B R comes from the same face weights, where R
maps V to the normal rigid velocity at each face. The minimum solves

    A p = G^T (W u* + B R V*),
    A = (dt / rho) G^T W G + (dt / rho_s) G^T B R (R^T B R)^-1 R^T B G.

G^T q is minus the divergence of the face field q, so the right side is minus
the divergence of the mixed velocity W u* + B R V*. A is symmetric positive
semidefinite; it is definite when every group of unknown cells touches an AIR
cell. With w_f in {0, 1} and no body, A and the right side are those of
macgrid.pressure_solve.

Walls are the grid border, the SOLID cells of the grid, and an optional
static level set wall_phi(x, y) < 0. A body is given by its own level set.
Only the weights on faces enter: the method uses the face area fractions,
which the paper names as one of its approximations of the mass in the
control volume of a face.
"""

import math

import macgrid
from macgrid import AIR, FLUID


def inside_fraction(a, b):
    """The part of a segment where a linear function with end values a and b is negative."""
    if a < 0.0 and b < 0.0:
        return 1.0
    if a >= 0.0 and b >= 0.0:
        return 0.0
    neg, pos = (a, b) if a < 0.0 else (b, a)
    return -neg / (pos - neg)


def node_values(g, phi):
    """phi(x, y) at the (nx + 1) by (ny + 1) grid nodes (i dx, j dx)."""
    return [[phi(i * g.dx, j * g.dx) for j in range(g.ny + 1)] for i in range(g.nx + 1)]


def face_fractions(g, phi):
    """The part of each u face and each v face where phi < 0, from phi at the two ends of the face."""
    nd = node_values(g, phi)
    fu = [[inside_fraction(nd[i][j], nd[i][j + 1]) for j in range(g.ny)] for i in range(g.nx + 1)]
    fv = [[inside_fraction(nd[i][j], nd[i + 1][j]) for j in range(g.ny + 1)] for i in range(g.nx)]
    return fu, fv


class Body:
    """A rigid body: a level set shape(x, y) < 0 in its own frame, its center, angle, velocity and density.

    V = [vx, vy, omega]. A scripted body has an infinite mass: the fluid does
    not change its velocity.
    """

    def __init__(self, shape, center, rho_s, V=(0.0, 0.0, 0.0), angle=0.0, scripted=False):
        if not scripted and rho_s <= 0.0:
            raise ValueError("need rho_s > 0")
        self.shape = shape
        self.center = [float(center[0]), float(center[1])]
        self.angle = float(angle)
        self.V = [float(t) for t in V]
        self.rho_s = float(rho_s)
        self.scripted = scripted

    def phi(self, x, y):
        """The level set of the body in world coordinates."""
        dx, dy = x - self.center[0], y - self.center[1]
        c, s = math.cos(self.angle), math.sin(self.angle)
        return self.shape(c * dx + s * dy, -s * dx + c * dy)

    def move(self, dt):
        """Move the body with its velocity for time dt (forward Euler)."""
        self.center[0] += dt * self.V[0]
        self.center[1] += dt * self.V[1]
        self.angle += dt * self.V[2]


class Weights:
    """The face weights: s (static wall), b (body) and w = 1 - s - b (fluid) for every u and v face."""

    def __init__(self, g, wall_phi=None, body=None):
        nx, ny = g.nx, g.ny
        su = macgrid.zeros(nx + 1, ny)
        sv = macgrid.zeros(nx, ny + 1)
        if wall_phi is not None:
            su, sv = face_fractions(g, wall_phi)
        if body is not None:
            bu, bv = face_fractions(g, body.phi)
        else:
            bu, bv = macgrid.zeros(nx + 1, ny), macgrid.zeros(nx, ny + 1)
        for i in range(nx + 1):
            for j in range(ny):
                if macgrid.is_solid_u_face(g, i, j):
                    su[i][j], bu[i][j] = 1.0, 0.0
        for i in range(nx):
            for j in range(ny + 1):
                if macgrid.is_solid_v_face(g, i, j):
                    sv[i][j], bv[i][j] = 1.0, 0.0
        self.su, self.sv, self.bu, self.bv = su, sv, bu, bv
        self.wu = [[max(0.0, 1.0 - su[i][j] - bu[i][j]) for j in range(ny)] for i in range(nx + 1)]  # @line L1
        self.wv = [[max(0.0, 1.0 - sv[i][j] - bv[i][j]) for j in range(ny + 1)] for i in range(nx)]


def binary_weights(g):
    """Weights from the cell labels only: w = 0 on a face that touches a SOLID cell, else 1."""
    return Weights(g)


def _unknowns(g, W):
    """The cells that are not SOLID or AIR and have a face with w > 0, and their index map."""
    cells, idx = [], {}
    for i in range(g.nx):
        for j in range(g.ny):
            if g.label[i][j] != FLUID:
                continue
            if W.wu[i][j] > 0.0 or W.wu[i + 1][j] > 0.0 or W.wv[i][j] > 0.0 or W.wv[i][j + 1] > 0.0:  # @line L2
                idx[(i, j)] = len(cells)
                cells.append((i, j))
    return cells, idx


def _faces(g):
    """Every face as (axis, i, j, left cell, right cell, x, y)."""
    dx = g.dx
    out = []
    for i in range(g.nx + 1):
        for j in range(g.ny):
            out.append((0, i, j, (i - 1, j), (i, j), i * dx, (j + 0.5) * dx))
    for i in range(g.nx):
        for j in range(g.ny + 1):
            out.append((1, i, j, (i, j - 1), (i, j), (i + 0.5) * dx, j * dx))
    return out


def _rigid_row(body, axis, x, y):
    """R_f: the normal rigid velocity at a face is R_f . V."""
    if axis == 0:
        return (1.0, 0.0, -(y - body.center[1]))
    return (0.0, 1.0, x - body.center[0])


def _solve3(M, r):
    """Solve the 3 by 3 system M z = r by Gaussian elimination with partial pivoting."""
    a = [list(M[k]) + [r[k]] for k in range(3)]
    for c in range(3):
        piv = max(range(c, 3), key=lambda k: abs(a[k][c]))
        a[c], a[piv] = a[piv], a[c]
        if a[c][c] == 0.0:
            raise ValueError("the body covers too few faces")
        for k in range(c + 1, 3):
            f = a[k][c] / a[c][c]
            for m in range(c, 4):
                a[k][m] -= f * a[c][m]
    z = [0.0, 0.0, 0.0]
    for c in (2, 1, 0):
        z[c] = (a[c][3] - sum(a[c][m] * z[m] for m in range(c + 1, 3))) / a[c][c]
    return z


class System:
    """The pressure system of one projection: unknown cells, faces with weights, and the body terms."""

    def __init__(self, g, W, dt, rho, body=None):
        if dt <= 0.0 or rho <= 0.0:
            raise ValueError("need dt > 0 and rho > 0")
        self.g, self.W, self.dt, self.rho, self.body = g, W, dt, rho, body
        self.cells, self.idx = _unknowns(g, W)
        self.faces = []
        for (axis, i, j, L, Rc, x, y) in _faces(g):
            w = (W.wu if axis == 0 else W.wv)[i][j]
            bb = (W.bu if axis == 0 else W.bv)[i][j] if body is not None else 0.0
            if w == 0.0 and bb == 0.0:
                continue
            kl, kr = self.idx.get(L, -1), self.idx.get(Rc, -1)
            if kl < 0 and kr < 0 and bb == 0.0:
                continue
            rrow = _rigid_row(body, axis, x, y) if bb > 0.0 else None
            self.faces.append((axis, i, j, kl, kr, w, bb, rrow))
        self.coupled = body is not None and not body.scripted
        if body is not None:
            M = [[0.0] * 3 for _ in range(3)]
            for f in self.faces:
                bb, rrow = f[6], f[7]
                if bb > 0.0:
                    for a in range(3):
                        for c in range(3):
                            M[a][c] += bb * rrow[a] * rrow[c]
            self.Mgeo = M  # the mass matrix is rho_s dx^2 Mgeo (per unit depth)

    def grad(self, p, f):
        """(G p)_f: the pressure difference across face f over dx; p is 0 outside the unknowns."""
        kl, kr = f[3], f[4]
        return ((p[kr] if kr >= 0 else 0.0) - (p[kl] if kl >= 0 else 0.0)) / self.g.dx

    def _gt(self, out, f, q):
        """out += G^T q_f for one face."""
        kl, kr = f[3], f[4]
        if kr >= 0:
            out[kr] += q / self.g.dx
        if kl >= 0:
            out[kl] -= q / self.g.dx

    def body_force(self, p):
        """R^T B G p: the pressure force and torque on the body, divided by -dx^2."""
        y = [0.0, 0.0, 0.0]
        for f in self.faces:
            if f[6] > 0.0:
                gp = self.grad(p, f)
                for a in range(3):
                    y[a] += f[6] * gp * f[7][a]
        return y

    def apply(self, p):
        """A p."""
        out = [0.0] * len(self.cells)
        c = self.dt / self.rho
        for f in self.faces:
            if f[5] > 0.0:
                self._gt(out, f, c * f[5] * self.grad(p, f))
        if self.coupled:
            z = _solve3(self.Mgeo, self.body_force(p))
            cs = self.dt / self.body.rho_s
            for f in self.faces:
                if f[6] > 0.0:
                    self._gt(out, f, cs * f[6] * sum(f[7][a] * z[a] for a in range(3)))  # @line L4
        return out

    def rhs(self, u, v):
        """G^T (W u* + B R V*): minus the divergence of the mixed velocity of fluid and body."""
        out = [0.0] * len(self.cells)
        for f in self.faces:
            axis, i, j = f[0], f[1], f[2]
            q = f[5] * (u if axis == 0 else v)[i][j]
            if f[6] > 0.0:
                q += f[6] * sum(f[7][a] * self.body.V[a] for a in range(3))  # @line L3
            self._gt(out, f, q)
        return out

    def has_air(self):
        """True if some face with w > 0 joins an unknown cell to an AIR cell."""
        g = self.g
        for (axis, i, j, kl, kr, w, bb, rrow) in self.faces:
            if w > 0.0 and (kl < 0) != (kr < 0):
                a, c = ((i - 1, j), (i, j)) if axis == 0 else ((i, j - 1), (i, j))
                other = a if kl < 0 else c
                if macgrid.cell_label(g, other[0], other[1]) == AIR:
                    return True
        return False


def conjugate_gradients(apply, b, tol=1e-12, max_iter=None):
    """Solve A x = b for a symmetric positive (semi)definite A given by apply(x). Returns (x, iterations)."""
    n = len(b)
    x = [0.0] * n
    bmax = max((abs(t) for t in b), default=0.0)
    if bmax == 0.0:
        return x, 0
    if max_iter is None:
        max_iter = max(100, 4 * n)
    r = list(b)
    d = list(r)
    rr = sum(t * t for t in r)
    it = 0
    while it < max_iter and max(abs(t) for t in r) > tol * bmax:
        q = apply(d)
        dq = sum(d[k] * q[k] for k in range(n))
        if dq <= 0.0:
            break
        alpha = rr / dq
        for k in range(n):
            x[k] += alpha * d[k]
            r[k] -= alpha * q[k]
        rr_new = sum(t * t for t in r)
        beta = rr_new / rr
        rr = rr_new
        for k in range(n):
            d[k] = r[k] + beta * d[k]
        it += 1
    return x, it


def project(g, dt, rho, W, body=None, tol=1e-12):
    """Minimize the kinetic energy of fluid and body over the pressure, and update u, v, p and body.V.

    g.u and g.v hold u* (after advection and forces); body.V holds V*. On a face
    with w = 0, the velocity is set to the normal velocity of the solid there
    (0 for a wall). Returns the System and the number of CG iterations.
    """
    S = System(g, W, dt, rho, body)
    b = S.rhs(g.u, g.v)
    closed = not S.has_air()
    if closed and b:
        mean = sum(b) / len(b)
        b = [t - mean for t in b]
    p, it = conjugate_gradients(S.apply, b, tol)  # @line L5
    if closed and p:
        mean = sum(p) / len(p)
        p = [t - mean for t in p]
    if S.coupled:
        z = _solve3(S.Mgeo, S.body_force(p))
        cs = dt / body.rho_s
        body.V = [body.V[a] - cs * z[a] for a in range(3)]  # @line L7
    s = dt / rho
    for f in S.faces:
        axis, i, j, w, bb = f[0], f[1], f[2], f[5], f[6]
        arr = g.u if axis == 0 else g.v
        if w > 0.0:
            arr[i][j] -= s * S.grad(p, f)  # @line L6
        elif bb > 0.0:
            arr[i][j] = sum(f[7][a] * body.V[a] for a in range(3))
    for i in range(g.nx + 1):
        for j in range(g.ny):
            if W.wu[i][j] == 0.0 and W.bu[i][j] == 0.0:
                g.u[i][j] = 0.0
    for i in range(g.nx):
        for j in range(g.ny + 1):
            if W.wv[i][j] == 0.0 and W.bv[i][j] == 0.0:
                g.v[i][j] = 0.0
    g.p = macgrid.zeros(g.nx, g.ny)
    for k, (i, j) in enumerate(S.cells):
        g.p[i][j] = p[k]
    S.p = p
    return S, it


def kinetic_energy(S, u, v, V=None):
    """(1/2) rho dx^2 sum w u^2 over the faces of S, plus (1/2) V^T M V for a coupled body."""
    dx2 = S.g.dx * S.g.dx
    ke = 0.0
    for f in S.faces:
        q = (u if f[0] == 0 else v)[f[1]][f[2]]
        ke += f[5] * q * q
    ke *= 0.5 * S.rho * dx2
    if S.coupled and V is not None:
        M = S.Mgeo
        ke += 0.5 * S.body.rho_s * dx2 * sum(V[a] * M[a][c] * V[c] for a in range(3) for c in range(3))
    return ke


def energy_of_pressure(S, u0, v0, V0, p):
    """KE(p): the kinetic energy after the pressure update with p, from u*, v* and V*."""
    u = macgrid.copy_field(u0)
    v = macgrid.copy_field(v0)
    s = S.dt / S.rho
    for f in S.faces:
        if f[5] > 0.0:
            (u if f[0] == 0 else v)[f[1]][f[2]] -= s * S.grad(p, f)
    V = None
    if S.coupled:
        z = _solve3(S.Mgeo, S.body_force(p))
        V = [V0[a] - S.dt / S.body.rho_s * z[a] for a in range(3)]
    return kinetic_energy(S, u, v, V)


def mixed_divergence(S, u, v):
    """The largest |div(W u + B R V)| over the unknown cells, with the current body velocity."""
    r = S.rhs(u, v)
    return max((abs(t) for t in r), default=0.0)


def matrix(S):
    """The dense matrix A, column by column (for tests on small grids)."""
    n = len(S.cells)
    cols = []
    for k in range(n):
        e = [0.0] * n
        e[k] = 1.0
        cols.append(S.apply(e))
    return [[cols[c][r] for c in range(n)] for r in range(n)]


def gravity(g, W, dt, grav, body=None):
    """Add -grav dt to v on faces with w > 0 next to a FLUID cell, and to the body if it is not scripted."""
    for i in range(g.nx):
        for j in range(g.ny + 1):
            if W.wv[i][j] > 0.0 and FLUID in (macgrid.cell_label(g, i, j - 1), macgrid.cell_label(g, i, j)):
                g.v[i][j] -= dt * grav
    if body is not None and not body.scripted:
        body.V[1] -= dt * grav
