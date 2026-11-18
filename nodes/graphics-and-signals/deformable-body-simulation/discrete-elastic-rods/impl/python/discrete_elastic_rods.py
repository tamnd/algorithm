# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-elastic-rods/. The authors are listed in prov/56ZBR0.jsonl.
"""Discrete elastic rods (Bergou et al. 2008), isotropic and straight at rest.

The rod is a polyline x_0, ..., x_n in 3D with edges e^j = x_(j+1) - x_j.
At an interior vertex i the curvature binormal is

    kb_i = 2 e^(i-1) x e^i / (|e^(i-1)| |e^i| + e^(i-1) . e^i),

with |kb_i| = 2 tan(phi_i / 2) for the turning angle phi_i. The energy is

    E = sum_j (k_s / 2) |e_bar^j| (|e^j| / |e_bar^j| - 1)^2       stretching (a penalty)
      + sum_i alpha |kb_i|^2 / l_bar_i                             bending
      + beta (delta_theta)^2 / L_bar                              twisting

with l_bar_i = |e_bar^(i-1)| + |e_bar^i|, L_bar = sum_i l_bar_i, and e_bar the
rest edges. The twist term is the quasistatic twist of Bergou et al.: the
material frame of the interior edges is at its energy minimum, so the twist
spreads in proportion to l_bar_i. delta_theta is the angle about the last
tangent from the Bishop frame (the frame of edge 0 carried along the curve by
parallel transport) to the clamped material director d_end. It changes when
the centerline moves because of the holonomy of parallel transport.

With this l_bar the bending stiffness alpha equals EI of a beam, and beta is
the twisting stiffness GJ. Units: SI; alpha and beta in N m^2, k_s in N.
"""

import math

from anim import add, cross, dot, norm, scale, sub


def curvature_binormal(a, b):
    """kb = 2 a x b / (|a| |b| + a . b) for consecutive edges a and b."""
    den = norm(a) * norm(b) + dot(a, b)
    if den <= 0.0:
        raise ValueError("the rod folds back on itself")
    return scale(cross(a, b), 2.0 / den)


def _skew(v):
    return [[0.0, -v[2], v[1]], [v[2], 0.0, -v[0]], [-v[1], v[0], 0.0]]


def grad_kb(a, b):
    """Return (Ga, Gb), the 3 by 3 Jacobians of kb with respect to a and b."""
    na, nb = norm(a), norm(b)
    den = na * nb + dot(a, b)
    kb = scale(cross(a, b), 2.0 / den)
    da = add(scale(a, nb / na), b)
    db = add(scale(b, na / nb), a)
    sa, sb = _skew(a), _skew(b)
    ga = [[(-2.0 * sb[r][c] - kb[r] * da[c]) / den for c in range(3)] for r in range(3)]
    gb = [[(2.0 * sa[r][c] - kb[r] * db[c]) / den for c in range(3)] for r in range(3)]
    return ga, gb


def parallel_transport(t1, t2, v):
    """Rotate v by the smallest rotation that takes the unit vector t1 to t2."""
    c = dot(t1, t2)
    if c <= -1.0 + 1e-12:
        raise ValueError("parallel transport is undefined between opposite tangents")
    b = cross(t1, t2)
    return add(add(scale(v, c), cross(b, v)), scale(b, dot(b, v) / (1.0 + c)))


def _unit(v):
    n = norm(v)
    return (v[0] / n, v[1] / n, v[2] / n)


def bishop_frames(x, u0):
    """The first director u^j of each edge, by parallel transport of u0 from edge 0."""
    t = [_unit(sub(x[j + 1], x[j])) for j in range(len(x) - 1)]
    u = [tuple(u0)]
    for j in range(1, len(t)):
        u.append(parallel_transport(t[j - 1], t[j], u[-1]))
    return u, t


def twist_angle(x, u0, d_end, near=0.0):
    """delta_theta: the angle about the last tangent from u^(n-1) to d_end.

    The angle is defined modulo 2 pi; the value nearest to near is returned,
    so a caller that follows the motion in small steps can count full turns.
    """
    u, t = bishop_frames(x, u0)  # @line L3
    un, tn = u[-1], t[-1]
    ang = math.atan2(dot(cross(un, d_end), tn), dot(un, d_end))  # @line L4
    return ang + 2.0 * math.pi * round((near - ang) / (2.0 * math.pi))


class Rod:
    """Rest data of a rod that is straight at rest."""

    def __init__(self, rest, alpha, beta, ks, density=1.0):
        self.rest = [tuple(map(float, p)) for p in rest]
        n = len(rest) - 1
        if n < 2:
            raise ValueError("a rod needs at least two edges")
        self.rest_len = [norm(sub(rest[j + 1], rest[j])) for j in range(n)]
        for i in range(1, n):
            if norm(curvature_binormal(sub(rest[i], rest[i - 1]), sub(rest[i + 1], rest[i]))) > 1e-9:
                raise ValueError("this implementation supports rods that are straight at rest")
        self.lbar = [0.0] + [self.rest_len[i - 1] + self.rest_len[i] for i in range(1, n)]
        self.Lbar = sum(self.lbar)
        self.alpha, self.beta, self.ks = alpha, beta, ks
        self.mass = [0.0] * (n + 1)
        for j in range(n):
            self.mass[j] += 0.5 * density * self.rest_len[j]
            self.mass[j + 1] += 0.5 * density * self.rest_len[j]


def energy(rod, x, u0=None, d_end=None, near=0.0):
    """Total elastic energy; the twist term is used only when u0 and d_end are given."""
    n = len(x) - 1
    e = [sub(x[j + 1], x[j]) for j in range(n)]
    tot = 0.0
    for j in range(n):
        s = norm(e[j]) / rod.rest_len[j] - 1.0
        tot += 0.5 * rod.ks * rod.rest_len[j] * s * s
    for i in range(1, n):
        kb = curvature_binormal(e[i - 1], e[i])
        tot += rod.alpha * dot(kb, kb) / rod.lbar[i]
    if d_end is not None:
        th = twist_angle(x, u0, d_end, near)
        tot += rod.beta * th * th / rod.Lbar
    return tot


def forces(rod, x, twist=0.0):
    """Return -dE/dx for the rod, with delta_theta = twist held by clamped ends.

    The twist term uses the holonomy gradient, which needs the first and the
    last edge to be fixed; pass twist = 0.0 for a rod with a free end.
    Cost Theta(n).
    """
    n = len(x) - 1
    f = [[0.0, 0.0, 0.0] for _ in x]
    e = [sub(x[j + 1], x[j]) for j in range(n)]  # @line L1
    for j in range(n):  # @line L5
        le = norm(e[j])
        g = scale(e[j], rod.ks * (le / rod.rest_len[j] - 1.0) / le)
        for k in range(3):
            f[j][k] += g[k]
            f[j + 1][k] -= g[k]
    c_twist = 2.0 * rod.beta * twist / rod.Lbar
    for i in range(1, n):
        kb = curvature_binormal(e[i - 1], e[i])  # @line L2
        ga, gb = grad_kb(e[i - 1], e[i])
        c = 2.0 * rod.alpha / rod.lbar[i]
        # dkb/dx_(i-1) = -Ga, dkb/dx_i = Ga - Gb, dkb/dx_(i+1) = Gb
        wa = [c * sum(ga[r][k] * kb[r] for r in range(3)) for k in range(3)]  # @line L6
        wb = [c * sum(gb[r][k] * kb[r] for r in range(3)) for k in range(3)]
        h_prev = scale(kb, 1.0 / (2.0 * norm(e[i - 1])))  # @line L7
        h_next = scale(kb, -1.0 / (2.0 * norm(e[i])))
        for k in range(3):
            f[i - 1][k] += wa[k]
            f[i][k] -= wa[k] - wb[k]
            f[i + 1][k] -= wb[k]
            # d(delta_theta)/dx = -d(holonomy)/dx, so the force is +c_twist d(holonomy)/dx
            f[i - 1][k] += c_twist * h_prev[k]
            f[i + 1][k] += c_twist * h_next[k]
            f[i][k] -= c_twist * (h_prev[k] + h_next[k])
    return [tuple(p) for p in f]


def step(rod, x, v, dt, fixed=(), gravity=(0.0, 0.0, 0.0), damping=0.0, u0=None, d_end=None, twist=0.0):
    """One symplectic Euler step; return (x, v, twist).

    If u0 and d_end are given, the first and last edges must be in fixed.
    The twist of the current centerline is measured first, unwrapped near the
    value passed in, and returned for the next call. The velocity damping
    v <- (1 - damping dt) v is a tuning value, not part of the method.
    """
    if d_end is not None:
        twist = twist_angle(x, u0, d_end, near=twist)
    f = forces(rod, x, twist if d_end is not None else 0.0)
    fixed = set(fixed)
    xn, vn = [], []
    for i in range(len(x)):  # @line L8
        if i in fixed:
            xn.append(x[i])
            vn.append((0.0, 0.0, 0.0))
            continue
        w = tuple((1.0 - damping * dt) * (v[i][k] + dt * (f[i][k] / rod.mass[i] + gravity[k])) for k in range(3))
        vn.append(w)
        xn.append(add(x[i], scale(w, dt)))
    return xn, vn, twist
