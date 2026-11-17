# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/green-coordinates/. The authors are listed in prov/2QKV5N.jsonl.
"""2D Green coordinates (Lipman, Levin and Cohen-Or 2008).

The cage is a simple polygon v_0..v_{n-1} in counterclockwise order. Edge j
runs from v_j to v_{j+1} and has the outward unit normal n_j. For a point
eta inside the cage, Green's third identity applied to the coordinate
functions gives

    eta = sum_i phi_i(eta) v_i + sum_j psi_j(eta) n_j,

with G(xi, eta) = (1 / 2 pi) ln |xi - eta| and

    phi_i = integral over the two edges at v_i of Gamma_i(xi) dG/dn(xi, eta),
    psi_j = - integral over edge j of G(xi, eta),

where Gamma_i is the hat function of v_i on the boundary. The integrals
have closed forms, computed below. The deformed point is

    f(eta) = sum_i phi_i v'_i + sum_j psi_j s_j n'_j,   s_j = |e'_j| / |e_j|.
"""

import math

TWO_PI = 2.0 * math.pi


def outward_normal(a, b):
    """Return the outward unit normal of the edge a -> b of a counterclockwise polygon."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy)
    return (dy / ln, -dx / ln)


def edge_integrals(a, b, eta, eps=1e-14):
    """Return (I0, I1, L) for the edge a -> b and the point eta.

    With xi(t) = a + t (b - a) and q(t) = |xi(t) - eta|^2 = Q t^2 + R t + S:
    I0 = int_0^1 dt / q(t), I1 = int_0^1 t dt / q(t), L = int_0^1 ln q(t) dt.
    """
    dx, dy = b[0] - a[0], b[1] - a[1]
    wx, wy = a[0] - eta[0], a[1] - eta[1]
    q = dx * dx + dy * dy
    r = 2.0 * (wx * dx + wy * dy)
    s = wx * wx + wy * wy
    srt = 2.0 * abs(dx * wy - dy * wx)  # sqrt(4 Q S - R^2), computed without cancellation
    l0 = math.log(s)
    l1 = math.log(q + r + s)
    l10 = l1 - l0
    if srt <= eps * q:
        # eta lies on the line of the edge (but not on the edge): h = 0, so
        # I0 and I1 are not needed, and the arctangent term of L vanishes.
        return 0.0, 0.0, l1 + r / (2 * q) * l10 - 2.0
    a10 = (math.atan((2 * q + r) / srt) - math.atan(r / srt)) / srt
    i0 = 2.0 * a10
    i1 = l10 / (2 * q) - (r / q) * a10
    big_l = l1 + r / (2 * q) * l10 - 2.0 + (4 * s - r * r / q) * a10
    return i0, i1, big_l


def green_coordinates(eta, cage):
    """Return (phi, psi): n vertex coordinates and n edge coordinates."""
    n = len(cage)
    phi = [0.0] * n  # @line L1
    psi = [0.0] * n
    for j in range(n):  # @line L2
        a, b = cage[j], cage[(j + 1) % n]
        nx, ny = outward_normal(a, b)  # @line L3
        length = math.hypot(b[0] - a[0], b[1] - a[1])
        h = (a[0] - eta[0]) * nx + (a[1] - eta[1]) * ny  # @line L4
        i0, i1, big_l = edge_integrals(a, b, eta)  # @line L5
        c = h * length / TWO_PI
        phi[j] += c * (i0 - i1)  # @line L6
        phi[(j + 1) % n] += c * i1
        psi[j] = -length / (2 * TWO_PI) * big_l  # @line L7
    return phi, psi  # @line L8


def deform(eta, cage, new_cage):
    """Return f(eta) for the moved cage new_cage."""
    phi, psi = green_coordinates(eta, cage)
    n = len(cage)
    x = sum(p * v[0] for p, v in zip(phi, new_cage))
    y = sum(p * v[1] for p, v in zip(phi, new_cage))
    for j in range(n):
        a, b = cage[j], cage[(j + 1) % n]
        a2, b2 = new_cage[j], new_cage[(j + 1) % n]
        s = math.hypot(b2[0] - a2[0], b2[1] - a2[1]) / math.hypot(b[0] - a[0], b[1] - a[1])
        nx, ny = outward_normal(a2, b2)
        x += psi[j] * s * nx  # @line L9
        y += psi[j] * s * ny
    return (x, y)
