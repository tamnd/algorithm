# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/raghavan-roth-method/. The authors are listed in prov/MTT21K.jsonl.
"""The elimination of Raghavan and Roth, shown on the position problem of a
general 3R arm.

The arm has standard Denavit-Hartenberg parameters (a_i, alpha_i, d_i) for
i = 1, 2, 3, with T_i = Rz(theta_i) Tz(d_i) Tx(a_i) Rx(alpha_i). The task is
to put the origin of frame 3 at a point p. A general 3R arm has at most 4
solutions.

The steps are the same as for the 6R arm, on a smaller system:

- two equations free of theta_1, from |p|^2 and p_z, each linear in
  (cos theta_2, sin theta_2, 1) with coefficients linear in
  (cos theta_3, sin theta_3);
- the half angle substitution x = tan(theta / 2) for theta_2 and theta_3;
- the dialytic step: multiply each equation by x2 to get a 4 by 4 system in
  the power products (x2^3, x2^2, x2, 1), whose determinant is a polynomial
  of degree 8 in x3;
- the removal of an extraneous factor, which leaves a quartic;
- the roots of the quartic, then theta_2 from a null vector and theta_1
  from the first two coordinates of p.

Polynomials are lists of coefficients, the constant first. The module needs
only the standard library.
"""

import cmath
import itertools
import math


# Polynomial arithmetic.

def padd(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0.0) + (b[i] if i < len(b) else 0.0) for i in range(n)]


def pscale(s, a):
    return [s * x for x in a]


def pmul(a, b):
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def peval(a, x):
    out = 0.0
    for c in reversed(a):
        out = out * x + c
    return out


def ptrim(a, rel=1e-12):
    scale = max((abs(c) for c in a), default=0.0)
    a = list(a)
    while len(a) > 1 and abs(a[-1]) <= rel * scale:
        a.pop()
    return a


def exact_divide(a, b):
    """Return (q, residual) where q minimizes |a - b q| in least squares.

    When b divides a, this gives the quotient without the loss of accuracy
    that long division from one end has when that end of b is small.
    """
    n = len(a) - len(b) + 1
    # Column j of the convolution matrix is b shifted by j.
    cols = [[0.0] * j + list(b) + [0.0] * (n - 1 - j) for j in range(n)]
    g = [[sum(x * y for x, y in zip(ci, cj)) for cj in cols] for ci in cols]
    r = [sum(x * y for x, y in zip(ci, a)) for ci in cols]
    for c in range(n):  # Gaussian elimination with partial pivoting
        piv = max(range(c, n), key=lambda i: abs(g[i][c]))
        g[c], g[piv], r[c], r[piv] = g[piv], g[c], r[piv], r[c]
        for i in range(c + 1, n):
            f = g[i][c] / g[c][c]
            g[i] = [x - f * y for x, y in zip(g[i], g[c])]
            r[i] -= f * r[c]
    q = [0.0] * n
    for i in range(n - 1, -1, -1):
        q[i] = (r[i] - sum(g[i][j] * q[j] for j in range(i + 1, n))) / g[i][i]
    res = padd(a, pscale(-1.0, pmul(b, q)))
    return q, math.sqrt(sum(x * x for x in res))


def roots(a, iters=500):
    """All complex roots of the polynomial a, by the Durand-Kerner iteration."""
    a = ptrim(a)
    n = len(a) - 1
    if n < 1:
        return []
    mon = [c / a[-1] for c in a]
    z = [(0.4 + 0.9j) ** k for k in range(n)]
    for _ in range(iters):
        delta = 0.0
        for i in range(n):
            num = peval(mon, z[i])
            den = 1.0
            for j in range(n):
                if j != i:
                    den *= z[i] - z[j]
            step = num / den
            z[i] -= step
            delta = max(delta, abs(step))
        if delta < 1e-15:
            break
    return z


# The arm.

def dh_matrix(theta, d, a, alpha):
    ct, st, ca, sa = math.cos(theta), math.sin(theta), math.cos(alpha), math.sin(alpha)
    return [[ct, -st * ca, st * sa, a * ct],
            [st, ct * ca, -ct * sa, a * st],
            [0.0, sa, ca, d],
            [0.0, 0.0, 0.0, 1.0]]


def mat4(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def fk(dh, q):
    """The position of the origin of frame 3; dh is [(a_i, alpha_i, d_i)] for i = 1, 2, 3."""
    t = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for (a, alpha, d), theta in zip(dh, q):
        t = mat4(t, dh_matrix(theta, d, a, alpha))
    return [t[0][3], t[1][3], t[2][3]]


def lin(u, v, w):
    """(1 + x^2)(u + v cos + w sin) with cos = (1 - x^2)/(1 + x^2) and sin = 2x/(1 + x^2)."""
    return [u + v, 2.0 * w, u - v]


def coefficient_polys(dh, p):
    """Return the polynomials in x3 of P1, Q1, K, P2, Q2, L and of h1, h2,
    each multiplied by (1 + x3^2).

    E1: P1 cos2 + Q1 sin2 + K = 0 comes from |p|^2, and
    E2: P2 cos2 + Q2 sin2 + L = 0 comes from p_z.
    """
    (a1, al1, d1), (a2, al2, d2), (a3, al3, d3) = dh
    ca1, sa1, ca2, sa2 = math.cos(al1), math.sin(al1), math.cos(al2), math.sin(al2)
    pp = sum(x * x for x in p)
    h1 = lin(a2, a3, 0.0)
    h2 = lin(-sa2 * d3, 0.0, ca2 * a3)
    hh0 = a2 * a2 + d2 * d2 + a3 * a3 + d3 * d3 + 2.0 * ca2 * d2 * d3
    k = lin(hh0 + a1 * a1 - d1 * d1 - pp + 2.0 * d1 * p[2], 2.0 * a2 * a3, 2.0 * d2 * sa2 * a3)  # @line L1
    ell = lin(d1 - p[2] + ca1 * (d2 + ca2 * d3), 0.0, ca1 * sa2 * a3)  # @line L1
    p1, q1 = pscale(2.0 * a1, h1), pscale(-2.0 * a1, h2)  # @line L1
    p2, q2 = pscale(sa1, h2), pscale(sa1, h1)  # @line L1
    return p1, q1, k, p2, q2, ell, h1, h2


def dialytic_matrix(dh, p):
    """The 4 by 4 matrix of polynomials in x3 that multiplies (x2^3, x2^2, x2, 1)."""
    p1, q1, k, p2, q2, ell, _, _ = coefficient_polys(dh, p)
    rows = []
    for pj, qj, kj in ((p1, q1, k), (p2, q2, ell)):
        # (1 + x2^2)(P cos2 + Q sin2 + K) = (K - P) x2^2 + 2Q x2 + (K + P)  @line L2
        a, b, c = padd(kj, pscale(-1.0, pj)), pscale(2.0, qj), padd(kj, pj)
        rows.append([a, b, c, [0.0]])  # @line L3
        rows.append([[0.0], a, b, c])  # @line L3
    return [rows[0], rows[1], rows[2], rows[3]]


def poly_det(m):
    """The determinant of a square matrix of polynomials, by the Leibniz formula."""
    n = len(m)
    out = [0.0]
    for perm in itertools.permutations(range(n)):
        inv = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        term = [1.0]
        for i in range(n):
            term = pmul(term, m[i][perm[i]])
        out = padd(out, pscale(-1.0 if inv % 2 else 1.0, term))
    return out


def extraneous_factor(dh, p):
    """(1 + x3^2)^2 (h1^2 + h2^2): a factor of the determinant that gives no solution."""
    h1, h2 = coefficient_polys(dh, p)[6:8]
    return padd(pmul(h1, h1), pmul(h2, h2))


def direct_quartic(dh, p):
    """The quartic 4 a1^2 L^2 + sin^2(alpha1) K^2 - 4 a1^2 sin^2(alpha1)(h1^2 + h2^2), times (1 + x3^2)^2."""
    (a1, al1, _), _, _ = dh
    sa1 = math.sin(al1)
    _, _, k, _, _, ell, h1, h2 = coefficient_polys(dh, p)
    e = padd(pmul(h1, h1), pmul(h2, h2))
    return padd(padd(pscale(4.0 * a1 * a1, pmul(ell, ell)), pscale(sa1 * sa1, pmul(k, k))), pscale(-4.0 * a1 * a1 * sa1 * sa1, e))


def solve_3r(dh, p, tol=1e-7):
    """Return the list of joint vectors (theta1, theta2, theta3) that put the origin of frame 3 at p."""
    (a1, al1, d1), (a2, al2, d2), (a3, al3, d3) = dh
    ca1, sa1, ca2, sa2 = math.cos(al1), math.sin(al1), math.cos(al2), math.sin(al2)
    delta = poly_det(dialytic_matrix(dh, p))  # @line L4
    quartic, _ = exact_divide(delta, pscale(4.0, extraneous_factor(dh, p)))  # @line L5
    quartic = ptrim(quartic)
    candidates = []
    for z in roots(quartic):  # @line L6
        if abs(z.imag) <= 1e-6 * (1.0 + abs(z)):
            candidates.append(2.0 * math.atan(z.real))  # @line L7
    if len(quartic) < 5:
        candidates.append(math.pi)  # the degree dropped: x3 = infinity is a root
    sols = []
    pz = p[2]
    for t3 in candidates:
        c3, s3 = math.cos(t3), math.sin(t3)
        h = [a2 + a3 * c3, ca2 * a3 * s3 - sa2 * d3, d2 + sa2 * a3 * s3 + ca2 * d3]
        hh = sum(x * x for x in h)
        k = hh + a1 * a1 - d1 * d1 - sum(x * x for x in p) + 2.0 * d1 * pz
        ell = d1 + ca1 * h[2] - pz
        r1 = (2.0 * a1 * h[0], -2.0 * a1 * h[1], k)
        r2 = (sa1 * h[1], sa1 * h[0], ell)
        # (cos2, sin2, 1) is a null vector of the 2 by 3 matrix [r1; r2].  @line L7
        n0, n1, n2 = r1[1] * r2[2] - r1[2] * r2[1], r1[2] * r2[0] - r1[0] * r2[2], r1[0] * r2[1] - r1[1] * r2[0]
        if abs(n2) < 1e-12:
            continue
        t2 = math.atan2(n1 / n2, n0 / n2)  # @line L7
        c2, s2 = math.cos(t2), math.sin(t2)
        f = [c2 * h[0] - s2 * h[1], s2 * h[0] + c2 * h[1], h[2]]
        g = [a1 + f[0], ca1 * f[1] - sa1 * f[2], d1 + sa1 * f[1] + ca1 * f[2]]
        t1 = math.atan2(p[1], p[0]) - math.atan2(g[1], g[0])  # @line L8
        q = [math.remainder(t1, 2.0 * math.pi), t2, t3]
        err = math.sqrt(sum((x - y) ** 2 for x, y in zip(fk(dh, q), p)))
        if err <= tol * (1.0 + math.sqrt(sum(x * x for x in p))):  # @line L9
            if all(max(abs(math.remainder(x - y, 2.0 * math.pi)) for x, y in zip(q, s)) > 1e-6 for s in sols):
                sols.append(q)
    return sols  # @line L9
