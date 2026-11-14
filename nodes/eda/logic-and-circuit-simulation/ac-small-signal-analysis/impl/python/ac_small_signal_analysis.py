# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ac-small-signal-analysis/. The authors are listed in prov/ZS7YDS.jsonl.
"""AC small-signal analysis on modified nodal analysis (MNA) equations.

The circuit equations are f(x) + d/dt q(x) = u(t), with x = (e_1..e_n, j_1..j_m):
node voltages first (node 0 is ground), then the currents of voltage sources
and inductors. AC analysis finds the DC operating point x0, linearizes there
(G = df/dx, C = dq/dx) and solves (G + j w C) X = b at each frequency.
"""

import cmath
import math

import sim3dense


class NoConvergence(RuntimeError):
    pass


def mos_current(kind, k, vt, lam, vd, vg, vs):
    """Level-1 (Shichman-Hodges) channel current from d to s and its partials in (vd, vg, vs).

    k, vt and lam are fitted model parameters. For a p device vt is the
    magnitude of the threshold.
    """
    if kind == "p":
        i, gd, gg, gs = mos_current("n", k, vt, lam, -vd, -vg, -vs)
        return -i, gd, gg, gs
    if vd < vs:
        i, gd, gg, gs = mos_current("n", k, vt, lam, vs, vg, vd)
        return -i, -gs, -gg, -gd
    vov, vds = vg - vs - vt, vd - vs
    if vov <= 0:
        return 0.0, 0.0, 0.0, 0.0
    if vds < vov:
        a = vov * vds - vds * vds / 2
        i = k * a * (1 + lam * vds)
        gm = k * vds * (1 + lam * vds)
        gds = k * (vov - vds) * (1 + lam * vds) + k * a * lam
    else:
        i = k / 2 * vov * vov * (1 + lam * vds)
        gm = k * vov * (1 + lam * vds)
        gds = k / 2 * vov * vov * lam
    return i, gds, gm, -gds - gm


class Netlist:
    """Elements between nodes; node 0 is ground. Stamps follow the MNA page."""

    def __init__(self, nodes):
        self.n = nodes  # nodes 1..n are unknown
        self.m = 0  # branch currents
        self.el = []

    def _branch(self):
        self.m += 1
        return self.m - 1

    def resistor(self, p, q, r):
        self.el.append(("R", p, q, 1.0 / r))

    def capacitor(self, p, q, c):
        self.el.append(("C", p, q, c))

    def inductor(self, p, q, l):
        self.el.append(("L", p, q, l, self._branch()))

    def vsource(self, p, q, dc=0.0, ac=0.0):
        """Voltage source e_p - e_q = dc (+ the phasor ac in AC analysis)."""
        self.el.append(("V", p, q, (dc, ac), self._branch()))
        return self.m - 1

    def isource(self, p, q, dc=0.0, ac=0.0):
        """Current source that moves its current out of p and into q."""
        self.el.append(("I", p, q, (dc, ac)))

    def vccs(self, p, q, c, d, g):
        self.el.append(("G", p, q, c, d, g))

    def mosfet(self, kind, d, g, s, k, vt, lam):
        self.el.append(("M", d, g, s, (kind, k, vt, lam)))

    @property
    def size(self):
        return self.n + self.m

    def _row(self, node):
        return node - 1  # ground (0) gives -1 and is dropped

    def evaluate(self, x):
        """Return f(x), G = df/dx, q(x), C = dq/dx."""
        N = self.size
        f, q = [0.0] * N, [0.0] * N
        G = [[0.0] * N for _ in range(N)]
        C = [[0.0] * N for _ in range(N)]

        def e(node):
            return x[node - 1] if node else 0.0

        def add(vec, r, val):
            if r >= 0:
                vec[r] += val

        def addm(mat, r, c, val):
            if r >= 0 and c >= 0:
                mat[r][c] += val

        for el in self.el:
            kind = el[0]
            if kind in "RC":
                _, p, qn, val = el
                rp, rq = self._row(p), self._row(qn)
                vec, mat = (f, G) if kind == "R" else (q, C)
                add(vec, rp, val * (e(p) - e(qn)))
                add(vec, rq, -val * (e(p) - e(qn)))
                for r, s1 in ((rp, 1), (rq, -1)):
                    addm(mat, r, rp, s1 * val)
                    addm(mat, r, rq, -s1 * val)
            elif kind in "LV":
                p, qn, k = el[1], el[2], self.n + el[4]
                rp, rq = self._row(p), self._row(qn)
                add(f, rp, x[k])
                add(f, rq, -x[k])
                addm(G, rp, k, 1.0)
                addm(G, rq, k, -1.0)
                f[k] += e(p) - e(qn)
                addm(G, k, rp, 1.0)
                addm(G, k, rq, -1.0)
                if kind == "L":
                    q[k] -= el[3] * x[k]
                    C[k][k] -= el[3]
            elif kind == "G":
                _, p, qn, c, d, g = el
                cur = g * (e(c) - e(d))
                for r, s1 in ((self._row(p), 1), (self._row(qn), -1)):
                    add(f, r, s1 * cur)
                    addm(G, r, self._row(c), s1 * g)
                    addm(G, r, self._row(d), -s1 * g)
            elif kind == "M":
                _, d, g, s, (mk, k, vt, lam) = el
                i, gd, gg, gs = mos_current(mk, k, vt, lam, e(d), e(g), e(s))
                for r, s1 in ((self._row(d), 1), (self._row(s), -1)):
                    add(f, r, s1 * i)
                    addm(G, r, self._row(d), s1 * gd)
                    addm(G, r, self._row(g), s1 * gg)
                    addm(G, r, self._row(s), s1 * gs)
        return f, G, q, C

    def sources(self, which):
        """The source vector u (which = 0 for DC values, 1 for AC phasors)."""
        u = [0.0] * self.size
        for el in self.el:
            if el[0] == "V":
                u[self.n + el[4]] += el[3][which]
            elif el[0] == "I":
                rp, rq = self._row(el[1]), self._row(el[2])
                if rp >= 0:
                    u[rp] -= el[3][which]
                if rq >= 0:
                    u[rq] += el[3][which]
        return u


def dc_operating_point(net, x0=None, tol=1e-12, max_iter=100):
    """Newton on f(x) = u_DC with a step limit of 0.5 V per iteration."""
    x = list(x0) if x0 else [0.0] * net.size
    u = net.sources(0)
    for _ in range(max_iter):
        f, G, _, _ = net.evaluate(x)
        dx = sim3dense.solve(G, [ui - fi for ui, fi in zip(u, f)])
        big = max(abs(d) for d in dx[: net.n]) if net.n else 0.0
        scale = min(1.0, 0.5 / big) if big > 0 else 1.0
        x = [xi + scale * di for xi, di in zip(x, dx)]
        if max(abs(d) for d in dx) <= tol * (1 + max(abs(v) for v in x)):
            return x
    raise NoConvergence("DC operating point")


def ac_analysis(net, omegas, out):
    """Transfer function out^T X(w) for each angular frequency w.

    out is a vector over the unknowns (for example a unit vector on the
    output node). Returns (x0, list of complex values H(j w)).
    """
    x0 = dc_operating_point(net)  # @line L1
    _, G, _, C = net.evaluate(x0)  # @line L2
    b = net.sources(1)  # @line L3
    result = []
    for w in omegas:  # @line L4
        Y = [[complex(G[i][j], w * C[i][j]) for j in range(net.size)] for i in range(net.size)]  # @line L5
        X = sim3dense.solve(Y, [complex(v) for v in b])  # @line L6
        result.append(sum(o * xi for o, xi in zip(out, X)))  # @line L7
    return x0, result  # @line L8


def decade_sweep(f_start, f_stop, per_decade):
    """Angular frequencies spaced evenly in log scale, per_decade points per decade."""
    n = round(per_decade * math.log10(f_stop / f_start))
    return [2 * math.pi * f_start * 10 ** (k / per_decade) for k in range(n + 1)]


def bode(h):
    """Magnitude in dB and phase in degrees of a complex value."""
    return 20 * math.log10(abs(h)), math.degrees(cmath.phase(h))


def unit(net, node):
    v = [0.0] * net.size
    v[node - 1] = 1.0
    return v
