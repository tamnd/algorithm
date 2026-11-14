# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chebyshev-spacing/. The authors are listed in prov/PFRWQN.jsonl.

"""Chebyshev spacing of precision points for four-bar function generation.

chebyshev_points(a, b, n) returns the zeros of the Chebyshev polynomial T_n
mapped from [-1, 1] to [a, b]:

    x_j = (a + b)/2 - ((b - a)/2) cos((2j - 1) pi / (2n)),  j = 1, ..., n.

The rest of the module builds a three-point four-bar function generator from
any three precision points and measures its structural error, so that the
spacing can be compared with others. Four-bar notation (Norton): ground d from
O2 = (0, 0) to O4 = (d, 0), input a, coupler b, output c; phi = theta2 and
psi = theta4, counterclockwise from the ground line. Freudenstein's equation
is K1 cos(psi) - K2 cos(phi) + K3 = cos(phi - psi) with K1 = d/a, K2 = d/c and
K3 = (a^2 - b^2 + c^2 + d^2) / (2ac).
"""

import math


def chebyshev_points(a, b, n):
    """The n Chebyshev points of [a, b], in increasing order."""
    if n < 1 or not a < b:
        raise ValueError("need n >= 1 and a < b")
    mid, half = (a + b) / 2.0, (b - a) / 2.0
    return [mid - half * math.cos((2 * j - 1) * math.pi / (2 * n)) for j in range(1, n + 1)]


def equal_points(a, b, n):
    """n equally spaced interior points a + (b - a) j / (n + 1)."""
    return [a + (b - a) * j / (n + 1) for j in range(1, n + 1)]


def node_polynomial(points, x):
    """w(x) = (x - x_1)(x - x_2)...(x - x_n)."""
    w = 1.0
    for p in points:
        w *= x - p
    return w


def chebyshev_bound(a, b, n):
    """max |w| on [a, b] for the Chebyshev points: (b - a)^n / 2^(2n - 1)."""
    return (b - a) ** n / 2.0 ** (2 * n - 1)


def solve3(m, r):
    """Gaussian elimination with partial pivoting; None if singular."""
    a = [list(row) + [rhs] for row, rhs in zip(m, r)]
    for col in range(3):
        piv = max(range(col, 3), key=lambda i: abs(a[i][col]))
        if abs(a[piv][col]) < 1e-14:
            return None
        a[col], a[piv] = a[piv], a[col]
        for i in range(col + 1, 3):
            f = a[i][col] / a[col][col]
            for k in range(col, 4):
                a[i][k] -= f * a[col][k]
    x = [0.0] * 3
    for i in (2, 1, 0):
        x[i] = (a[i][3] - sum(a[i][k] * x[k] for k in range(i + 1, 3))) / a[i][i]
    return x


def wrap(angle):
    """Reduce an angle to (-pi, pi]."""
    return math.pi - (math.pi - angle) % (2 * math.pi)


def output_angle(k, phi, branch):
    """psi for input phi on branch +1 or -1, from the half-angle quadratic; None if no assembly."""
    k1, k2, k3 = k
    qa = math.cos(phi) - k1 - k2 * math.cos(phi) + k3
    qb = -2.0 * math.sin(phi)
    qc = k1 - (k2 + 1.0) * math.cos(phi) + k3
    disc = qb * qb - 4.0 * qa * qc
    if disc < 0.0:
        return None
    return 2.0 * math.atan2(-qb + branch * math.sqrt(disc), 2.0 * qa)


class Generator:
    """A function generation task: f on [x0, x1] scaled to angle ranges."""

    def __init__(self, f, x0, x1, phi0, dphi, psi0, dpsi):
        self.f, self.x0, self.x1 = f, x0, x1
        self.phi0, self.dphi, self.psi0, self.dpsi = phi0, dphi, psi0, dpsi
        self.y0, self.y1 = f(x0), f(x1)

    def phi(self, x):
        return self.phi0 + (x - self.x0) / (self.x1 - self.x0) * self.dphi

    def psi(self, x):
        return self.psi0 + (self.f(x) - self.y0) / (self.y1 - self.y0) * self.dpsi

    def design(self, xs):
        """Freudenstein constants K for three precision points xs, or None."""
        if len(xs) != 3:
            raise ValueError("three precision points")
        pairs = [(self.phi(x), self.psi(x)) for x in xs]
        m = [[math.cos(ps), -math.cos(ph), 1.0] for ph, ps in pairs]
        r = [math.cos(ph - ps) for ph, ps in pairs]
        return solve3(m, r)

    def branch(self, k, xs):
        """The branch sign that passes every precision point, or None."""
        for s in (1, -1):
            ok = True
            for x in xs:
                v = output_angle(k, self.phi(x), s)
                if v is None or abs(wrap(v - self.psi(x))) > 1e-9:
                    ok = False
                    break
            if ok:
                return s
        return None

    def errors(self, k, branch, samples=1000):
        """Structural error psi(phi(x)) - psi_d(x) at equally spaced x; None if it does not assemble."""
        out = []
        for i in range(samples):
            x = self.x0 + (self.x1 - self.x0) * i / (samples - 1)
            v = output_angle(k, self.phi(x), branch)
            if v is None:
                return None
            out.append((x, wrap(v - self.psi(x))))
        return out

    def max_error(self, xs, samples=1000):
        """Largest |structural error| of the three-point design on xs, or None if it fails."""
        k = self.design(xs)
        if k is None:
            return None
        s = self.branch(k, xs)
        if s is None:
            return None
        e = self.errors(k, s, samples)
        if e is None:
            return None
        return max(abs(v) for _, v in e)


def chebyshev_design(gen, n=3, samples=1000):
    """CHEBYSHEV-DESIGN: (points, K, lengths, max error) for gen, or None if the design fails.

    With Freudenstein's equation the precision point system of line L5 is the
    3 x 3 linear system, so n must be 3 here. Line L6 reports failure; the
    caller changes the ranges and calls again.
    """
    if n != 3:
        raise ValueError("Freudenstein's equation takes three precision points")
    xs, pairs = [], []
    for j in range(1, n + 1):  # @line L1
        t = math.cos((2 * j - 1) * math.pi / (2 * n))  # @line L2
        x = (gen.x0 + gen.x1) / 2.0 - (gen.x1 - gen.x0) / 2.0 * t  # @line L3
        xs.append(x)
        pairs.append((gen.phi(x), gen.psi(x)))  # @line L4
    m = [[math.cos(ps), -math.cos(ph), 1.0] for ph, ps in pairs]
    k = solve3(m, [math.cos(ph - ps) for ph, ps in pairs])  # @line L5
    branch = gen.branch(k, xs) if k is not None else None
    if k is None or branch is None or link_lengths(k) is None:  # @line L6
        return None
    errs = gen.errors(k, branch, samples)
    if errs is None:
        return None
    e = max(abs(v) for _, v in errs)  # @line L7
    return xs, k, link_lengths(k), e  # @line L8


def link_lengths(k, d=1.0):
    """(a, b, c, d) from K; None if a coupler length is not real."""
    k1, k2, k3 = k
    if k1 == 0.0 or k2 == 0.0:
        return None
    a, c = d / k1, d / k2
    b2 = a * a + c * c + d * d - 2.0 * a * c * k3
    if b2 <= 0.0:
        return None
    return a, math.sqrt(b2), c, d
