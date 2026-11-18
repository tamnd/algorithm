# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/invertible-finite-elements/. The authors are listed in prov/8XGGPB.jsonl.
"""Invertible finite elements (Irving, Teran and Fedkiw 2004) on 2D triangles.

For each element, F = D_s D_m^(-1) is written as F = U F_hat V^T with
rotations U and V (det U = det V = +1) and F_hat = diag(s1, s2), where
s1 >= |s2| and s2 < 0 exactly when det F < 0. So an inverted element has one
negative entry, the one of smallest magnitude.

The stress of an isotropic model is diagonal in this frame:
P = U P_hat(F_hat) V^T. The force on the nodes 1 and 2 is G = P B_m with
B_m = -V0 D_m^(-T), and node 0 gets minus the sum.

Two diagonal models are given:
- corotated: P_hat_i = 2 mu (s_i - 1) + lambda sum_j (s_j - 1), the gradient
  of mu sum (s_i - 1)^2 + (lambda / 2) (sum (s_i - 1))^2. It is defined for
  every F, inverted or not.
- neo-Hookean: P_hat_i = mu s_i - mu / s_i + lambda log(s1 s2) / s_i, the
  gradient of (mu / 2)(s1^2 + s2^2 - 2) - mu log J + (lambda / 2) (log J)^2.
  It is undefined for s_i <= 0. Below the threshold c > 0 the stress is
  replaced by its first order Taylor expansion about the clamped point
  max(s_i, c), which is continuous with a continuous first derivative at
  s_i = c. The threshold is a tuning value; the paper gives none.

Units: SI in 2D; mu and lambda in N/m, masses in kg.
"""

import math

from anim import det, inv, mul, rot2, transpose


def signed_svd2(f):
    """Return (U, (s1, s2), V) with F = U diag(s1, s2) V^T and det U = det V = +1.

    s1 >= |s2| >= 0 when det F >= 0, and s2 < 0 when det F < 0. Closed form:
    F = rot(phi) diag(s1, s2) rot(theta), so U = rot(phi) and V = rot(-theta).
    """
    a, b, c, d = f[0][0], f[0][1], f[1][0], f[1][1]
    e, g = 0.5 * (a + d), 0.5 * (a - d)
    h, k = 0.5 * (c + b), 0.5 * (c - b)
    q, r = math.hypot(e, k), math.hypot(g, h)
    a1, a2 = math.atan2(h, g), math.atan2(k, e)
    theta, phi = 0.5 * (a2 - a1), 0.5 * (a2 + a1)
    return rot2(phi), (q + r, q - r), rot2(-theta)


def corotated_diag(s, mu, lam):
    """Diagonal stress and its 2 by 2 Jacobian for the corotated model."""
    t = (s[0] - 1.0) + (s[1] - 1.0)
    p = [2.0 * mu * (s[i] - 1.0) + lam * t for i in range(2)]
    jac = [[2.0 * mu + lam, lam], [lam, 2.0 * mu + lam]]
    return p, jac


def neo_hookean_diag(s, mu, lam):
    """Diagonal stress and its Jacobian for the neo-Hookean model (s1, s2 > 0)."""
    lj = math.log(s[0] * s[1])
    p = [mu * s[i] - mu / s[i] + lam * lj / s[i] for i in range(2)]
    jac = [[0.0, 0.0], [0.0, 0.0]]
    for i in range(2):
        jac[i][i] = mu + (mu + lam * (1.0 - lj)) / (s[i] * s[i])
    jac[0][1] = jac[1][0] = lam / (s[0] * s[1])
    return p, jac


def diag_energy(s, mu, lam, model):
    """The energy density in terms of the signed singular values (no extrapolation)."""
    if model == "corotated":
        t = (s[0] - 1.0) + (s[1] - 1.0)
        return mu * ((s[0] - 1.0) ** 2 + (s[1] - 1.0) ** 2) + 0.5 * lam * t * t
    lj = math.log(s[0] * s[1])
    return 0.5 * mu * (s[0] ** 2 + s[1] ** 2 - 2.0) - mu * lj + 0.5 * lam * lj * lj


def diagonal_stress(s, mu, lam, model, c):
    """P_hat at the signed singular values s, linearized below the threshold c."""
    st = [max(s[0], c), max(s[1], c)]  # @line L5
    if model == "corotated":
        p, jac = corotated_diag(st, mu, lam)
    else:
        p, jac = neo_hookean_diag(st, mu, lam)
    return [p[i] + sum(jac[i][j] * (s[j] - st[j]) for j in range(2)) for i in range(2)]  # @line L6


class Mesh:
    """2D triangle mesh with rest data and lumped masses (density in kg/m^2)."""

    def __init__(self, rest, tris, mu, lam, density=1.0):
        self.rest = [tuple(map(float, p)) for p in rest]
        self.tris = [tuple(t) for t in tris]
        self.mu, self.lam = mu, lam
        self.dm_inv, self.bm, self.v0 = [], [], []
        self.mass = [0.0] * len(rest)
        for t in self.tris:
            dm = edge_matrix(self.rest, t)
            if det(dm) <= 0.0:
                raise ValueError("each triangle needs a positive rest orientation")
            di = inv(dm)
            v0 = 0.5 * det(dm)
            self.dm_inv.append(di)
            self.v0.append(v0)
            self.bm.append([[-v0 * x for x in row] for row in transpose(di)])
            for a in t:
                self.mass[a] += density * v0 / 3.0


def edge_matrix(p, t):
    a, b, c = p[t[0]], p[t[1]], p[t[2]]
    return [[b[0] - a[0], c[0] - a[0]], [b[1] - a[1], c[1] - a[1]]]


def invertible_forces(mesh, x, model="neo-hookean", c=0.3):
    """Return the elastic forces on all nodes, valid for inverted elements too.

    Cost O(m) for m elements: one closed form 2 by 2 SVD per element.
    """
    f = [[0.0, 0.0] for _ in x]  # @line L1
    for e, t in enumerate(mesh.tris):  # @line L2
        fmat = mul(edge_matrix(x, t), mesh.dm_inv[e])  # @line L3
        u, s, v = signed_svd2(fmat)  # @line L4
        ph = diagonal_stress(s, mesh.mu, mesh.lam, model, c)
        p = mul(mul(u, [[ph[0], 0.0], [0.0, ph[1]]]), transpose(v))  # @line L7
        g = mul(p, mesh.bm[e])  # @line L8
        for k in range(2):  # @line L9
            f[t[k + 1]][0] += g[0][k]
            f[t[k + 1]][1] += g[1][k]
            f[t[0]][0] -= g[0][k]
            f[t[0]][1] -= g[1][k]
    return [tuple(q) for q in f]


def total_energy(mesh, x, model):
    """Sum of V0 Psi(F) over the elements, from the signed singular values."""
    tot = 0.0
    for e, t in enumerate(mesh.tris):
        _, s, _ = signed_svd2(mul(edge_matrix(x, t), mesh.dm_inv[e]))
        tot += mesh.v0[e] * diag_energy(s, mesh.mu, mesh.lam, model)
    return tot


def direct_neo_hookean_stress(f, mu, lam):
    """P = mu (F - F^(-T)) + lambda log(J) F^(-T), the usual form for det F > 0."""
    fit = transpose(inv(f))
    lj = math.log(det(f))
    return [[mu * (f[i][j] - fit[i][j]) + lam * lj * fit[i][j] for j in range(2)] for i in range(2)]


def step(mesh, x, v, dt, model="neo-hookean", c=0.3, fixed=(), damping=0.0):
    """One symplectic Euler step with the velocity damping v <- (1 - damping dt) v.

    The damping is a tuning value, not part of the method. Cost O(n + m).
    """
    f = invertible_forces(mesh, x, model, c)
    fixed = set(fixed)
    xn, vn = [], []
    for i in range(len(x)):
        if i in fixed:
            xn.append(x[i])
            vn.append((0.0, 0.0))
            continue
        w = tuple((1.0 - damping * dt) * (v[i][k] + dt * f[i][k] / mesh.mass[i]) for k in range(2))
        vn.append(w)
        xn.append((x[i][0] + dt * w[0], x[i][1] + dt * w[1]))
    return xn, vn


def signed_area(x, t):
    return 0.5 * det(edge_matrix(x, t))
