# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shooting-newton-steady-state/. The authors are listed in prov/FS9DNT.jsonl.
"""Shooting Newton for the periodic steady state of a circuit.

The circuit equations are f(x) + d/dt q(x) = u(t), with x = (e_1..e_n, j_1..j_m):
node voltages first (node 0 is ground), then the currents of voltage sources
and inductors. The sources have period T. One period of transient analysis
with S fixed steps is a map x0 -> x_S; shooting finds a fixed point of that
map with Newton's method, using the sensitivity (monodromy) matrix dx_S/dx0
that the transient steps give at little extra cost.
"""

import math

import sim3dense

VT_300 = 1.380649e-23 * 300.0 / 1.602176634e-19  # kT/q at 300 K, in volts
THETA = {"trap": 0.5, "be": 1.0}  # trapezoidal rule and backward Euler


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

    @property
    def size(self):
        return self.n + self.m

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


def step(net, x, t, h, method, ev=None, tol=1e-13, max_iter=50):
    """One step from (t, x) to t + h; returns (x_new, ev_new, A, B).

    The step solves q(y) - q(x) + h [theta (f(y) - u(t+h)) + (1 - theta)(f(x) - u(t))] = 0
    by Newton. A = C(y) + theta h G(y) and B = C(x) - (1 - theta) h G(x) are the
    matrices of the sensitivity recurrence A dy/dx0 = B dx/dx0.
    """
    th = THETA[method]
    N = net.size
    f, G, q, C = ev if ev else net.evaluate(x)
    u, un = net.sources(t), net.sources(t + h)
    y = list(x)
    for _ in range(max_iter):
        fn, Gn, qn, Cn = net.evaluate(y)
        r = [qn[a] - q[a] + h * (th * (fn[a] - un[a]) + (1 - th) * (f[a] - u[a])) for a in range(N)]
        A = [[Cn[a][b] + th * h * Gn[a][b] for b in range(N)] for a in range(N)]
        dy = sim3dense.solve(A, [-v for v in r])
        y = [y[a] + dy[a] for a in range(N)]
        if max(abs(v) for v in dy) <= tol * (1 + max(abs(v) for v in y)):
            break
    else:
        raise NoConvergence("transient step")
    evn = net.evaluate(y)
    fn, Gn, qn, Cn = evn
    A = [[Cn[a][b] + th * h * Gn[a][b] for b in range(N)] for a in range(N)]
    B = [[C[a][b] - (1 - th) * h * G[a][b] for b in range(N)] for a in range(N)]
    return y, evn, A, B


def period_map(net, x0, T, S, method="trap", sensitivity=True):
    """One period of S fixed steps from x0; returns (x_S, Phi, states).

    Phi = d x_S / d x0 is the monodromy matrix of the discrete map (None when
    sensitivity is False), and states are x_0, ..., x_S.
    """
    h = T / S
    N = net.size
    x, ev = list(x0), None
    Phi = sim3dense.identity(N, 1.0) if sensitivity else None
    states = [list(x)]
    for k in range(S):  # @line L3
        x, ev, A, B = step(net, x, k * h, h, method, ev)
        if sensitivity:
            Phi = sim3dense.solve(A, sim3dense.matmul(B, Phi))  # @line L4
        states.append(list(x))
    return x, Phi, states


def shooting(net, T, S, x0=None, method="trap", tol=1e-11, max_iter=50, step_limit=1.0):
    """Initial state of the periodic steady state of the S-step discrete map.

    Returns (x0, iterations, residual history, states of one period). Newton
    steps are scaled so that no node voltage moves more than step_limit volts.
    """
    N = net.size
    x = list(x0) if x0 else [0.0] * N  # @line L1
    history = []
    for it in range(1, max_iter + 1):  # @line L2
        xT, Phi, states = period_map(net, x, T, S, method)
        r = [xT[a] - x[a] for a in range(N)]  # @line L5
        history.append(max(abs(v) for v in r))
        J = [[Phi[a][b] - (1.0 if a == b else 0.0) for b in range(N)] for a in range(N)]
        dx = sim3dense.solve(J, [-v for v in r])  # @line L6
        big = max((abs(v) for v in dx[: net.n]), default=0.0)
        lam = min(1.0, step_limit / big) if big > 0 else 1.0
        x = [x[a] + lam * dx[a] for a in range(N)]
        if lam == 1.0 and max(abs(v) for v in dx) <= tol * (1 + max(abs(v) for v in x)):  # @line L7
            _, _, states = period_map(net, x, T, S, method, sensitivity=False)
            return x, it, history, states  # @line L8
    raise NoConvergence("shooting")


def transient_until_periodic(net, T, S, x0=None, method="trap", tol=1e-9, max_periods=100000):
    """Plain transient, period after period, until x(kT) changes by at most tol.

    Returns (x at the last period start, number of periods). This is what
    shooting replaces.
    """
    x = list(x0) if x0 else [0.0] * net.size
    for p in range(1, max_periods + 1):
        xT, _, _ = period_map(net, x, T, S, method, sensitivity=False)
        if max(abs(a - b) for a, b in zip(xT, x)) <= tol:
            return xT, p
        x = xT
    raise NoConvergence("transient did not settle")
