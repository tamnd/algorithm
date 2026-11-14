# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harmonic-balance-analysis/. The authors are listed in prov/WY97C5.jsonl.
"""Harmonic balance on modified nodal analysis (MNA) equations.

The circuit equations are f(x) + d/dt q(x) = u(t), with x = (e_1..e_n, j_1..j_m):
node voltages first (node 0 is ground), then the currents of voltage sources
and inductors. The sources have period T = 2 pi / w. Harmonic balance writes
each unknown as a truncated Fourier series with harmonics -K..K and solves the
circuit equations for the coefficients with Newton's method.

The transforms are direct sums of cost O(M^2) with M = 2K + 1 samples. A
production code uses the fast Fourier transform for them.
"""

import cmath
import math

import sim3dense

VT_300 = 1.380649e-23 * 300.0 / 1.602176634e-19  # kT/q at 300 K, in volts


class NoConvergence(RuntimeError):
    pass


def _wave(w):
    return w if callable(w) else (lambda t, c=float(w): c)


class Netlist:
    """Elements between nodes; node 0 is ground. Stamps follow the MNA page."""

    def __init__(self, nodes):
        self.n = nodes
        self.m = 0
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

    def vsource(self, p, q, wave):
        """Voltage source e_p - e_q = wave(t); wave is a function of t or a constant."""
        self.el.append(("V", p, q, _wave(wave), self._branch()))

    def isource(self, p, q, wave):
        """Current source that moves wave(t) out of p and into q."""
        self.el.append(("I", p, q, _wave(wave)))

    def diode(self, a, c, i_s, n=1.0, tt=0.0):
        """Junction diode from a to c with diffusion charge tt * i.

        The saturation current i_s, the emission coefficient n and the transit
        time tt are fitted model parameters.
        """
        self.el.append(("D", a, c, (i_s, n, tt)))

    def cubic(self, p, q, g1, g3):
        """Nonlinear conductor with current g1 v + g3 v^3 from p to q."""
        self.el.append(("N", p, q, (g1, g3)))

    @property
    def size(self):
        return self.n + self.m

    @property
    def linear(self):
        return all(el[0] not in "DN" for el in self.el)

    def evaluate(self, x):
        """Return f(x), G = df/dx, q(x), C = dq/dx."""
        N = self.size
        f, q = [0.0] * N, [0.0] * N
        G = [[0.0] * N for _ in range(N)]
        C = [[0.0] * N for _ in range(N)]

        def e(node):
            return x[node - 1] if node else 0.0

        def branch(vec, mat, p, qn, val, dval):
            """Add val leaving p and entering qn; dval = d val / d(e_p - e_q)."""
            rp, rq = p - 1, qn - 1
            for r, s in ((rp, 1.0), (rq, -1.0)):
                if r < 0:
                    continue
                vec[r] += s * val
                if rp >= 0:
                    mat[r][rp] += s * dval
                if rq >= 0:
                    mat[r][rq] -= s * dval

        for el in self.el:
            kind = el[0]
            if kind in "RC":
                _, p, qn, val = el
                v = e(p) - e(qn)
                if kind == "R":
                    branch(f, G, p, qn, val * v, val)
                else:
                    branch(q, C, p, qn, val * v, val)
            elif kind in "LV":
                p, qn, k = el[1], el[2], self.n + el[4]
                for r, s in ((p - 1, 1.0), (qn - 1, -1.0)):
                    if r >= 0:
                        f[r] += s * x[k]
                        G[r][k] += s
                        G[k][r] += s
                f[k] += e(p) - e(qn)
                if kind == "L":
                    q[k] -= el[3] * x[k]
                    C[k][k] -= el[3]
            elif kind == "D":
                _, a, c, (i_s, n, tt) = el
                nvt = n * VT_300
                v, vmax = e(a) - e(c), 40.0 * nvt
                if v <= vmax:
                    ex = math.exp(v / nvt)
                    i, g = i_s * (ex - 1.0), i_s * ex / nvt
                else:
                    ex = math.exp(40.0)
                    i, g = i_s * (ex * (1.0 + (v - vmax) / nvt) - 1.0), i_s * ex / nvt
                branch(f, G, a, c, i, g)
                branch(q, C, a, c, tt * i, tt * g)
            elif kind == "N":
                _, p, qn, (g1, g3) = el
                v = e(p) - e(qn)
                branch(f, G, p, qn, g1 * v + g3 * v ** 3, g1 + 3 * g3 * v * v)
        return f, G, q, C

    def sources(self, t):
        """The source vector u(t)."""
        u = [0.0] * self.size
        for el in self.el:
            if el[0] == "V":
                u[self.n + el[4]] += el[3](t)
            elif el[0] == "I":
                val = el[3](t)
                if el[1]:
                    u[el[1] - 1] -= val
                if el[2]:
                    u[el[2] - 1] += val
        return u


class Spectrum:
    """Direct DFT on M = 2K + 1 points, coefficient index k = -K..K stored at k + K."""

    def __init__(self, K):
        self.K, self.M = K, 2 * K + 1
        M = self.M
        self.root = [cmath.exp(-2j * math.pi * r / M) for r in range(M)]

    def forward(self, samples):
        """X_k = (1/M) sum_i x_i exp(-j k 2 pi i / M) for k = -K..K."""
        M, K, root = self.M, self.K, self.root
        return [sum(samples[i] * root[(k * i) % M] for i in range(M)) / M for k in range(-K, K + 1)]

    def backward(self, coeffs):
        """x_i = sum_k X_k exp(j k 2 pi i / M), the real part (the imaginary part is rounding)."""
        M, K, root = self.M, self.K, self.root
        return [sum(coeffs[k + K] * root[(-k * i) % M] for k in range(-K, K + 1)).real for i in range(M)]

    def aliased(self, samples):
        """D_d = (1/M) sum_i x_i exp(-j d 2 pi i / M) for d = 0..M-1 (index taken mod M)."""
        M, root = self.M, self.root
        return [sum(samples[i] * root[(d * i) % M] for i in range(M)) / M for d in range(M)]


def source_spectrum(net, omega, K):
    """U[a][k + K], the Fourier coefficients of the source samples u(t_i)."""
    sp = Spectrum(K)
    M = sp.M
    ts = [2 * math.pi * i / (M * omega) for i in range(M)]
    us = [net.sources(t) for t in ts]
    return [sp.forward([us[i][a] for i in range(M)]) for a in range(net.size)]


def hb_system(net, X, omega, U):
    """The HB residual R (a flat list) and its Jacobian J at the spectrum X.

    Row a * M + (k + K) is the equation of unknown a at harmonic k, and column
    b * M + (l + K) is the coefficient of unknown b at harmonic l.
    """
    K = (len(X[0]) - 1) // 2
    sp = Spectrum(K)
    M, N = sp.M, net.size
    jw = [1j * k * omega for k in range(-K, K + 1)]
    xs = [sp.backward(X[a]) for a in range(N)]  # @line L4
    ev = [net.evaluate([xs[a][i] for a in range(N)]) for i in range(M)]  # @line L5
    R = []  # @line L6
    for a in range(N):
        F = sp.forward([ev[i][0][a] for i in range(M)])
        Q = sp.forward([ev[i][2][a] for i in range(M)])
        R.extend(F[k] + jw[k] * Q[k] - U[a][k] for k in range(M))
    J = [[0j] * (N * M) for _ in range(N * M)]  # @line L7
    for a in range(N):
        for b in range(N):
            gs = [ev[i][1][a][b] for i in range(M)]
            cs = [ev[i][3][a][b] for i in range(M)]
            if not any(gs) and not any(cs):
                continue
            Gd, Cd = sp.aliased(gs), sp.aliased(cs)
            for k in range(M):
                row = J[a * M + k]
                for l in range(M):
                    d = (k - l) % M  # the samples alias index k - l to (k - l) mod M
                    row[b * M + l] = Gd[d] + jw[k] * Cd[d]
    return R, J


def harmonic_balance(net, omega, K, X0=None, tol=1e-10, max_iter=100, step_limit=0.1):
    """Periodic steady state as Fourier coefficients X[a][k + K] of each unknown a.

    Returns (X, iterations, samples), where samples[i] is x at t_i = 2 pi i / (M omega).
    Newton steps are scaled so that no node voltage sample moves more than
    step_limit volts in one iteration.
    """
    sp = Spectrum(K)  # @line L1
    M, N = sp.M, net.size
    U = source_spectrum(net, omega, K)  # @line L2
    X = [list(row) for row in X0] if X0 else [[0j] * M for _ in range(N)]
    for it in range(1, max_iter + 1):  # @line L3
        R, J = hb_system(net, X, omega, U)
        dX = sim3dense.solve(J, [-r for r in R])  # @line L8
        dxs = [sp.backward(dX[a * M:(a + 1) * M]) for a in range(net.n)]
        big = max((abs(v) for row in dxs for v in row), default=0.0)
        lam = min(1.0, step_limit / big) if big > 0 else 1.0
        for a in range(N):
            for k in range(M):
                X[a][k] += lam * dX[a * M + k]
        size = max(abs(v) for v in dX)
        scale = 1.0 + max(abs(v) for row in X for v in row)
        if lam == 1.0 and size <= tol * scale:  # @line L9
            xs = [sp.backward(X[a]) for a in range(N)]
            return X, it, [[xs[a][i] for a in range(N)] for i in range(M)]  # @line L10
    raise NoConvergence("harmonic balance")


def evaluate_series(X, omega, t):
    """Value of the Fourier series of every unknown at time t."""
    K = (len(X[0]) - 1) // 2
    return [sum(row[k + K] * cmath.exp(1j * k * omega * t) for k in range(-K, K + 1)).real for row in X]


def residual(net, X, omega):
    """The HB residual R at the spectrum X (the function whose root Newton finds)."""
    K = (len(X[0]) - 1) // 2
    return hb_system(net, X, omega, source_spectrum(net, omega, K))[0]


def transient(net, T, steps_per_period, periods, x0=None):
    """Trapezoidal-rule transient with a fixed step; returns the samples of the last period.

    This is the reference for the nonlinear tests: it runs from x0 (zero by
    default) until the start-up transient has died out.
    """
    h = T / steps_per_period
    N = net.size
    x = list(x0) if x0 else [0.0] * N
    f, G, q, C = net.evaluate(x)
    u = net.sources(0.0)
    out = []
    for s in range(1, steps_per_period * periods + 1):
        t = s * h
        un = net.sources(t)
        y = list(x)
        for _ in range(50):
            fn, Gn, qn, Cn = net.evaluate(y)
            r = [qn[a] - q[a] + h / 2 * (fn[a] + f[a] - un[a] - u[a]) for a in range(N)]
            Jt = [[Cn[a][b] + h / 2 * Gn[a][b] for b in range(N)] for a in range(N)]
            dy = sim3dense.solve(Jt, [-v for v in r])
            y = [y[a] + dy[a] for a in range(N)]
            if max(abs(v) for v in dy) <= 1e-13 * (1 + max(abs(v) for v in y)):
                break
        else:
            raise NoConvergence("transient step")
        x, u = y, un
        f, G, q, C = net.evaluate(x)
        if s > steps_per_period * (periods - 1):
            out.append(list(x))
    return out
