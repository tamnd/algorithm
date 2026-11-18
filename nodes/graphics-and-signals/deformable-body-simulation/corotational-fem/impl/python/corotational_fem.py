# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/corotational-fem/. The authors are listed in prov/NYXCZF.jsonl.
"""Corotational linear finite elements on 2D triangles.

Each element has the rest positions X_a of its three nodes, the matrix D_m of
rest edge vectors, the rest area V0 = |det D_m| / 2 and the 6 by 6 stiffness
matrix K_e of linear elasticity,

    Psi_lin(F) = mu |eps|_F^2 + (lambda / 2) tr(eps)^2,  eps = (F + F^T) / 2 - I.

The corotational force rotates the element back to the rest frame, applies
the linear force there and rotates the result forward:

    f_e = -R K_e (R^T x_e - X_e),

with R the rotation factor of the polar decomposition F = R S. This force is
the exact negative gradient of the corotated energy

    Psi_cr(F) = mu |F - R|_F^2 + (lambda / 2) tr(R^T F - I)^2,

whose first Piola-Kirchhoff stress is P = 2 mu (F - R) + lambda tr(R^T F - I) R.
The warped stiffness R K_e R^T leaves out the derivative of R, so it is not
the exact Hessian of Psi_cr away from the rest shape.

Units: SI in 2D (positions in m, mu and lambda in N/m, masses in kg).
The Lame parameters are the 3D (plane strain) values of lame().
"""

import math

from anim import det, inv, mul, polar, solve, transpose


def lame(young, poisson):
    """Return (mu, lambda) from Young's modulus and Poisson's ratio (3D formula)."""
    mu = young / (2.0 * (1.0 + poisson))
    lam = young * poisson / ((1.0 + poisson) * (1.0 - 2.0 * poisson))
    return mu, lam


def edge_matrix(p, tri):
    """Return the 2 by 2 matrix [p1 - p0, p2 - p0] (edge vectors as columns)."""
    a, b, c = (p[i] for i in tri)
    return [[b[0] - a[0], c[0] - a[0]], [b[1] - a[1], c[1] - a[1]]]


def linear_stress(f, mu, lam):
    """First Piola-Kirchhoff stress of linear elasticity at F."""
    e00 = f[0][0] - 1.0
    e11 = f[1][1] - 1.0
    e01 = 0.5 * (f[0][1] + f[1][0])
    tr = e00 + e11
    return [[2.0 * mu * e00 + lam * tr, 2.0 * mu * e01], [2.0 * mu * e01, 2.0 * mu * e11 + lam * tr]]


def element_force_from_stress(p_stress, dm_inv_t, v0):
    """Return the forces on the 3 nodes, -V0 P D_m^(-T) and minus the sum for node 0."""
    h = mul(p_stress, dm_inv_t)
    f1 = (-v0 * h[0][0], -v0 * h[1][0])
    f2 = (-v0 * h[0][1], -v0 * h[1][1])
    f0 = (-f1[0] - f2[0], -f1[1] - f2[1])
    return [f0, f1, f2]


class Mesh:
    """A 2D triangle mesh with its rest data, per element stiffness and lumped masses.

    rest: list of (x, y) rest positions in m; tris: list of index triples with
    positive rest orientation; density in kg/m^2. Cost of the build: O(n + m)
    for n nodes and m elements.
    """

    def __init__(self, rest, tris, mu, lam, density=1.0):
        self.rest = [tuple(map(float, r)) for r in rest]
        self.tris = [tuple(t) for t in tris]
        self.mu = mu
        self.lam = lam
        self.dm_inv = []
        self.dm_inv_t = []
        self.v0 = []
        self.ke = []
        self.mass = [0.0] * len(rest)
        for t in self.tris:
            dm = edge_matrix(self.rest, t)
            if det(dm) <= 0.0:
                raise ValueError("each triangle needs a positive rest orientation")
            di = inv(dm)
            self.dm_inv.append(di)
            self.dm_inv_t.append(transpose(di))
            v0 = 0.5 * abs(det(dm))
            self.v0.append(v0)
            for a in t:
                self.mass[a] += density * v0 / 3.0
            self.ke.append(self._stiffness(len(self.v0) - 1))

    def deformation_gradient(self, x, e):
        """F = D_s D_m^(-1) of element e at the positions x."""
        return mul(edge_matrix(x, self.tris[e]), self.dm_inv[e])

    def linear_element_force(self, x, e):
        """Forces of linear elasticity on the nodes of element e (a linear map of x - X)."""
        f = self.deformation_gradient(x, e)
        return element_force_from_stress(linear_stress(f, self.mu, self.lam), self.dm_inv_t[e], self.v0[e])

    def _stiffness(self, e):
        """The 6 by 6 matrix K_e with f_lin = -K_e (x_e - X_e), one column per unit displacement."""
        t = self.tris[e]
        k = [[0.0] * 6 for _ in range(6)]
        for col in range(6):
            x = list(self.rest)
            a, comp = t[col // 2], col % 2
            moved = list(x[a])
            moved[comp] += 1.0
            x[a] = tuple(moved)
            fe = self.linear_element_force(x, e)
            for row in range(6):
                k[row][col] = -fe[row // 2][row % 2]
        return k


def corotational_forces(mesh, x):
    """Return the corotational elastic forces on all nodes at the positions x.

    Cost O(m) for m elements: one 2 by 2 polar decomposition and one 6 by 6
    product per element.
    """
    n = len(x)
    f = [[0.0, 0.0] for _ in range(n)]  # @line L1
    rots = []
    for e, t in enumerate(mesh.tris):  # @line L2
        ds = edge_matrix(x, t)  # @line L3
        fmat = mul(ds, mesh.dm_inv[e])  # @line L4
        r, _ = polar(fmat)  # @line L5
        rots.append(r)
        y = []
        for k, a in enumerate(t):  # @line L6
            ya = (r[0][0] * x[a][0] + r[1][0] * x[a][1], r[0][1] * x[a][0] + r[1][1] * x[a][1])
            ra = mesh.rest[a]
            y.extend((ya[0] - ra[0], ya[1] - ra[1]))
        ke = mesh.ke[e]
        g = [-sum(ke[i][j] * y[j] for j in range(6)) for i in range(6)]  # @line L7
        for k, a in enumerate(t):  # @line L8
            gx, gy = g[2 * k], g[2 * k + 1]
            f[a][0] += r[0][0] * gx + r[0][1] * gy
            f[a][1] += r[1][0] * gx + r[1][1] * gy
    return [tuple(v) for v in f], rots


def warped_stiffness(mesh, rots):
    """Assemble the 2n by 2n matrix K_w = sum over elements of R K_e R^T. Cost O(m + n^2)."""
    n = len(mesh.rest)
    kw = [[0.0] * (2 * n) for _ in range(2 * n)]
    for e, t in enumerate(mesh.tris):
        r = rots[e]
        ke = mesh.ke[e]
        for i in range(3):
            for j in range(3):
                blk = [[ke[2 * i + p][2 * j + q] for q in range(2)] for p in range(2)]
                w = mul(mul(r, blk), transpose(r))
                for p in range(2):
                    for q in range(2):
                        kw[2 * t[i] + p][2 * t[j] + q] += w[p][q]
    return kw


def step_implicit(mesh, x, v, dt, f_ext=None, fixed=()):
    """One linearized backward Euler step with the warped stiffness.

    Solves (M + dt^2 K_w) v' = M v + dt (f(x) + f_ext), then x' = x + dt v'.
    Nodes in fixed keep v' = 0. Cost: O(m) for the forces plus one dense solve
    of size 2n, O(n^3) here (a sparse solver or CG is used in practice).
    """
    n = len(x)
    f, rots = corotational_forces(mesh, x)
    kw = warped_stiffness(mesh, rots)  # @line L9
    fixed = set(fixed)
    a = [[dt * dt * kw[i][j] for j in range(2 * n)] for i in range(2 * n)]
    b = [0.0] * (2 * n)
    for i in range(n):
        for c in range(2):
            row = 2 * i + c
            a[row][row] += mesh.mass[i]
            fe = f_ext[i][c] if f_ext is not None else 0.0
            b[row] = mesh.mass[i] * v[i][c] + dt * (f[i][c] + fe)
    for i in fixed:
        for c in range(2):
            row = 2 * i + c
            a[row] = [0.0] * (2 * n)
            a[row][row] = 1.0
            b[row] = 0.0
            for k in range(2 * n):
                if k != row:
                    a[k][row] = 0.0
    vn = solve(a, b)  # @line L10
    v_new = [(vn[2 * i], vn[2 * i + 1]) for i in range(n)]
    x_new = [(x[i][0] + dt * v_new[i][0], x[i][1] + dt * v_new[i][1]) for i in range(n)]  # @line L11
    return x_new, v_new


def step_explicit(mesh, x, v, dt, f_ext=None, fixed=()):
    """One symplectic Euler step: v' = v + dt M^(-1) f(x), then x' = x + dt v'.

    Stable for a linear spring only if omega dt < 2. Cost O(n + m).
    """
    f, _ = corotational_forces(mesh, x)
    fixed = set(fixed)
    v_new, x_new = [], []
    for i in range(len(x)):
        if i in fixed:
            v_new.append((0.0, 0.0))
            x_new.append(x[i])
            continue
        fe = f_ext[i] if f_ext is not None else (0.0, 0.0)
        vi = tuple(v[i][c] + dt * (f[i][c] + fe[c]) / mesh.mass[i] for c in range(2))
        v_new.append(vi)
        x_new.append((x[i][0] + dt * vi[0], x[i][1] + dt * vi[1]))
    return x_new, v_new


# ---------------------------------------------------------------- reference quantities


def corotated_energy_density(f, mu, lam):
    """Psi_cr(F) = mu |F - R|_F^2 + (lambda / 2) tr(R^T F - I)^2 with R from polar(F)."""
    r, s = polar(f)
    d = sum((f[i][j] - r[i][j]) ** 2 for i in range(2) for j in range(2))
    tr = s[0][0] + s[1][1] - 2.0
    return mu * d + 0.5 * lam * tr * tr


def corotated_energy(mesh, x):
    """Total corotated energy, the sum of V0 Psi_cr(F) over the elements."""
    return sum(mesh.v0[e] * corotated_energy_density(mesh.deformation_gradient(x, e), mesh.mu, mesh.lam)
               for e in range(len(mesh.tris)))


def linear_forces(mesh, x):
    """Forces of plain linear FEM, -K (x - X), for comparison."""
    f = [[0.0, 0.0] for _ in x]
    for e, t in enumerate(mesh.tris):
        fe = mesh.linear_element_force(x, e)
        for k, a in enumerate(t):
            f[a][0] += fe[k][0]
            f[a][1] += fe[k][1]
    return [tuple(v) for v in f]


def grid_mesh(nx, ny, width, height):
    """A rectangle split into nx by ny squares, each cut into two triangles."""
    rest = [(width * i / nx, height * j / ny) for j in range(ny + 1) for i in range(nx + 1)]
    tris = []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            b, c, d = a + 1, a + nx + 1, a + nx + 2
            tris.append((a, b, d))
            tris.append((a, d, c))
    return rest, tris


def rotate_points(points, theta, center=(0.0, 0.0), shift=(0.0, 0.0)):
    """Rotate points by theta about center, then translate by shift."""
    c, s = math.cos(theta), math.sin(theta)
    out = []
    for p in points:
        dx, dy = p[0] - center[0], p[1] - center[1]
        out.append((center[0] + c * dx - s * dy + shift[0], center[1] + s * dx + c * dy + shift[1]))
    return out
