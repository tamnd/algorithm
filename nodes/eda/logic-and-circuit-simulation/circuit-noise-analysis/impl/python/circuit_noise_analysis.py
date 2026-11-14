# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/circuit-noise-analysis/. The authors are listed in prov/P2C0RA.jsonl.
"""Small-signal noise analysis with one adjoint solve per frequency.

The circuit is in MNA form f(x) + d/dt q(x) = u(t), x = (e_1..e_n, j_1..j_m),
node 0 is ground. Each noise source is a current between two nodes with a
one-sided power spectral density S(f) in A^2/Hz, computed at the DC operating
point. The output noise density at a frequency is sum_k |H_k|^2 S_k(f), where
H_k is the transfer from source k to the output; all H_k come from one solve
with the transposed matrix.
"""

import math

import sim3dense

BOLTZMANN = 1.380649e-23  # J/K, exact in the SI
CHARGE = 1.602176634e-19  # C, exact in the SI


class NoConvergence(RuntimeError):
    pass


def _level1(k, vt, lam, vgs, vds):
    """Shichman-Hodges current for vds >= 0 and its partials (i, gds, gm)."""
    vov = vgs - vt
    if vov <= 0:
        return 0.0, 0.0, 0.0
    if vds < vov:
        a = vov * vds - vds * vds / 2
        return k * a * (1 + lam * vds), k * (vov - vds) * (1 + lam * vds) + k * a * lam, k * vds * (1 + lam * vds)
    return k / 2 * vov * vov * (1 + lam * vds), k / 2 * vov * vov * lam, k * vov * (1 + lam * vds)


def mosfet_eval(kind, k, vt, lam, vd, vg, vs):
    """Current d -> s, its partials (gd, gg, gs) in (vd, vg, vs), and gm >= 0."""
    if kind == "p":
        i, gd, gg, gs, gm = mosfet_eval("n", k, vt, lam, -vd, -vg, -vs)
        return -i, gd, gg, gs, gm
    if vd < vs:
        i, gd, gg, gs, gm = mosfet_eval("n", k, vt, lam, vs, vg, vd)
        return -i, -gs, -gg, -gd, gm
    i, gds, gm = _level1(k, vt, lam, vg - vs, vd - vs)
    return i, gds, gm, -gds - gm, gm


class Netlist:
    """MNA netlist; the stamps follow the modified nodal analysis page."""

    def __init__(self, nodes, temperature=300.0):
        self.n, self.m, self.el = nodes, 0, []
        self.kt = BOLTZMANN * temperature

    @property
    def size(self):
        return self.n + self.m

    def resistor(self, p, q, r, noisy=True):
        self.el.append(("R", p, q, 1.0 / r, noisy))

    def capacitor(self, p, q, c):
        self.el.append(("C", p, q, c))

    def inductor(self, p, q, l):
        self.el.append(("L", p, q, l, self.m))
        self.m += 1

    def vsource(self, p, q, dc=0.0, ac=0.0):
        self.el.append(("V", p, q, (dc, ac), self.m))
        self.m += 1

    def isource(self, p, q, dc=0.0, ac=0.0):
        """Moves its current out of p and into q. Noiseless."""
        self.el.append(("I", p, q, (dc, ac)))

    def vccs(self, p, q, c, d, g):
        """Current g (e_c - e_d) out of p and into q. Noiseless."""
        self.el.append(("G", p, q, (c, d, g)))

    def mosfet(self, kind, d, g, s, k, vt, lam, kf=0.0, af=1.0, cox_l2=1.0):
        """Level-1 MOSFET. k, vt, lam, kf and af are fitted; cox_l2 is Cox Leff^2."""
        self.el.append(("M", d, g, s, (kind, k, vt, lam, kf, af, cox_l2)))

    def diode(self, a, c, i_s, n=1.0, kf=0.0, af=1.0):
        """Junction diode from a to c; i_s, n, kf and af are fitted."""
        self.el.append(("D", a, c, (i_s, n, kf, af)))

    def _diode(self, v, i_s, n):
        nvt = n * self.kt / CHARGE
        vmax = 40 * nvt
        if v <= vmax:
            e = math.exp(v / nvt)
            return i_s * (e - 1), i_s * e / nvt
        e = math.exp(40.0)
        return i_s * (e * (1 + (v - vmax) / nvt) - 1), i_s * e / nvt

    def evaluate(self, x):
        """f(x), G = df/dx, q(x), C = dq/dx."""
        N = self.size
        f, q = [0.0] * N, [0.0] * N
        G = [[0.0] * N for _ in range(N)]
        C = [[0.0] * N for _ in range(N)]

        def e(node):
            return x[node - 1] if node else 0.0

        def two(vec, mat, p, qn, cur, partials):
            """Current cur leaving p and entering qn, with partials {node: d cur}."""
            for r, s in ((p, 1), (qn, -1)):
                if r:
                    vec[r - 1] += s * cur
                    for node, d in partials:
                        if node:
                            mat[r - 1][node - 1] += s * d

        for el in self.el:
            kind = el[0]
            if kind in "RC":
                p, qn, val = el[1], el[2], el[3]
                vec, mat = (f, G) if kind == "R" else (q, C)
                two(vec, mat, p, qn, val * (e(p) - e(qn)), ((p, val), (qn, -val)))
            elif kind in "LV":
                p, qn, k = el[1], el[2], self.n + el[4]
                for r, s in ((p, 1), (qn, -1)):
                    if r:
                        f[r - 1] += s * x[k]
                        G[r - 1][k] += s
                        G[k][r - 1] += s
                f[k] += e(p) - e(qn)
                if kind == "L":
                    q[k] -= el[3] * x[k]
                    C[k][k] -= el[3]
            elif kind == "G":
                p, qn, (c, d, g) = el[1], el[2], el[3]
                two(f, G, p, qn, g * (e(c) - e(d)), ((c, g), (d, -g)))
            elif kind == "M":
                d, g, s, (mk, k, vt, lam, *_rest) = el[1], el[2], el[3], el[4]
                i, gd, gg, gs, _ = mosfet_eval(mk, k, vt, lam, e(d), e(g), e(s))
                two(f, G, d, s, i, ((d, gd), (g, gg), (s, gs)))
            elif kind == "D":
                a, c, (i_s, n, _, _) = el[1], el[2], el[3]
                i, gdd = self._diode(e(a) - e(c), i_s, n)
                two(f, G, a, c, i, ((a, gdd), (c, -gdd)))
        return f, G, q, C

    def sources(self, which):
        u = [0.0] * self.size
        for el in self.el:
            if el[0] == "V":
                u[self.n + el[4]] += el[3][which]
            elif el[0] == "I":
                if el[1]:
                    u[el[1] - 1] -= el[3][which]
                if el[2]:
                    u[el[2] - 1] += el[3][which]
        return u

    def noise_sources(self, x0):
        """List of (name, p, q, S) with S a function of f in A^2/Hz (one-sided)."""
        kt, out = self.kt, []

        def e(node):
            return x0[node - 1] if node else 0.0

        for idx, el in enumerate(self.el):
            if el[0] == "R" and el[4]:
                g = el[3]
                out.append((f"R{idx} thermal", el[1], el[2], lambda f, g=g: 4 * kt * g))
            elif el[0] == "M":
                d, g, s, (mk, k, vt, lam, kf, af, cox_l2) = el[1], el[2], el[3], el[4]
                i, _, _, _, gm = mosfet_eval(mk, k, vt, lam, e(d), e(g), e(s))
                out.append((f"M{idx} thermal", d, s, lambda f, gm=gm: 4 * kt * 2 / 3 * abs(gm)))
                if kf:
                    out.append((f"M{idx} flicker", d, s,
                                lambda f, a=kf * abs(i) ** af / cox_l2: a / f))
            elif el[0] == "D":
                a, c, (i_s, n, kf, af) = el[1], el[2], el[3]
                i, _ = self._diode(e(a) - e(c), i_s, n)
                out.append((f"D{idx} shot", a, c, lambda f, i=i: 2 * CHARGE * abs(i)))
                if kf:
                    out.append((f"D{idx} flicker", a, c, lambda f, b=kf * abs(i) ** af: b / f))
        return out


def dc_operating_point(net, tol=1e-12, max_iter=200):
    """Newton on f(x) = u_DC, with node voltage steps limited to 0.1 V."""
    x, u = [0.0] * net.size, net.sources(0)
    for _ in range(max_iter):
        f, G, _, _ = net.evaluate(x)
        dx = sim3dense.solve(G, [a - b for a, b in zip(u, f)])
        big = max([abs(d) for d in dx[: net.n]] + [0.0])
        scale = min(1.0, 0.1 / big) if big > 0 else 1.0
        x = [a + scale * d for a, d in zip(x, dx)]
        if scale == 1.0 and max(abs(d) for d in dx) <= tol * (1 + max(abs(v) for v in x)):
            return x
    raise NoConvergence("DC operating point")


def _injection(net, p, q):
    """KCL right side of a unit current out of p and into q."""
    a = [0.0] * net.size
    if p:
        a[p - 1] -= 1.0
    if q:
        a[q - 1] += 1.0
    return a


def noise_analysis(net, freqs, out):
    """Output noise density (V^2/Hz for a voltage output) at each frequency in Hz.

    Returns (x0, totals, contributions) where contributions[i] maps each
    source name to its share of totals[i].
    """
    x0 = dc_operating_point(net)  # @line L1
    _, G, _, C = net.evaluate(x0)
    srcs = net.noise_sources(x0)  # @line L2
    totals, parts = [], []
    for fr in freqs:  # @line L3
        w = 2 * math.pi * fr
        yt = [[complex(G[j][i], w * C[j][i]) for j in range(net.size)] for i in range(net.size)]  # @line L4
        z = sim3dense.solve(yt, [complex(o) for o in out])  # @line L5
        share = {}
        for name, p, q, s in srcs:  # @line L6
            h = (z[q - 1] if q else 0) - (z[p - 1] if p else 0)
            share[name] = abs(h) ** 2 * s(fr)
        totals.append(sum(share.values()))  # @line L7
        parts.append(share)
    return x0, totals, parts  # @line L8


def noise_direct(net, freqs, out):
    """Reference: one forward solve per noise source and frequency, then the sum."""
    x0 = dc_operating_point(net)
    _, G, _, C = net.evaluate(x0)
    srcs = net.noise_sources(x0)
    totals = []
    for fr in freqs:
        w = 2 * math.pi * fr
        y = [[complex(G[i][j], w * C[i][j]) for j in range(net.size)] for i in range(net.size)]
        tot = 0.0
        for _, p, q, s in srcs:
            xk = sim3dense.solve(y, [complex(v) for v in _injection(net, p, q)])
            tot += abs(sum(o * v for o, v in zip(out, xk))) ** 2 * s(fr)
        totals.append(tot)
    return totals


def transfer(net, freqs, out):
    """AC transfer from the AC sources to the output (for input-referred noise)."""
    x0 = dc_operating_point(net)
    _, G, _, C = net.evaluate(x0)
    b = net.sources(1)
    res = []
    for fr in freqs:
        w = 2 * math.pi * fr
        y = [[complex(G[i][j], w * C[i][j]) for j in range(net.size)] for i in range(net.size)]
        xk = sim3dense.solve(y, [complex(v) for v in b])
        res.append(sum(o * v for o, v in zip(out, xk)))
    return res


def unit(net, node):
    v = [0.0] * net.size
    v[node - 1] = 1.0
    return v
