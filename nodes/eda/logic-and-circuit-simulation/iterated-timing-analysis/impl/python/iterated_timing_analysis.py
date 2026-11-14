# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-timing-analysis/. The authors are listed in prov/8PGXDW.jsonl.
"""Iterated timing analysis: event-driven Gauss-Seidel-Newton relaxation of the
backward Euler node equations at each time point.

A circuit has nodes 0 .. n-1. Some nodes are fixed (ground, supplies, inputs)
and carry a waveform; the others are unknown. Elements are capacitors,
resistors, voltage-controlled current sources and level-1 MOSFETs. The node
equation of an unknown node i at time t, with step h and previous voltages vn,
is the sum of the currents leaving i:

    F_i(v) = sum_C C ((v_i - vn_i) - (v_j - vn_j)) / h + sum of resistive currents = 0.
"""

from collections import deque

import sim3dense


class NonConvergence(RuntimeError):
    """The relaxation did not settle at a time point within the work limit."""


def _mos_core(k, vt, lam, vgs, vds):
    """Square-law current from drain to source for vds >= 0, with gm and gds."""
    vov = vgs - vt
    if vov <= 0:
        return 0.0, 0.0, 0.0
    if vds < vov:
        a = vov * vds - vds * vds / 2
        return k * a * (1 + lam * vds), k * vds * (1 + lam * vds), k * (vov - vds) * (1 + lam * vds) + k * a * lam
    return k / 2 * vov * vov * (1 + lam * vds), k * vov * (1 + lam * vds), k / 2 * vov * vov * lam


def mos_current(kind, k, vt, lam, vd, vg, vs):
    """Channel current from terminal d to terminal s and its partials (in vd, vg, vs).

    Level-1 (Shichman-Hodges) model. k, vt and lam are fitted model
    parameters. The device is symmetric: if the voltages reverse, d and s
    swap roles. A p device is the n device on negated voltages, with vt the
    magnitude of its threshold.
    """
    if kind == "p":
        i, gd, gg, gs = mos_current("n", k, vt, lam, -vd, -vg, -vs)
        return -i, gd, gg, gs
    if vd >= vs:
        i, gm, gds = _mos_core(k, vt, lam, vg - vs, vd - vs)
        return i, gds, gm, -gds - gm
    i, gm, gds = _mos_core(k, vt, lam, vg - vd, vs - vd)
    return -i, gds + gm, -gm, -gds


class Circuit:
    def __init__(self, n, fixed):
        """n nodes; fixed maps each fixed node to a function of time."""
        self.n, self.fixed = n, dict(fixed)
        self.elements = []

    def cap(self, a, b, c):
        self.elements.append(("C", (a, b), (a, b), c))

    def res(self, a, b, g):
        """A conductance g between a and b."""
        self.elements.append(("G", (a, b), (a, b), g))

    def vccs(self, p, q, c, d, g):
        """A current g (v_c - v_d) that leaves p and enters q."""
        self.elements.append(("V", (p, q), (c, d), g))

    def mos(self, kind, d, g, s, k, vt, lam):
        self.elements.append(("M", (d, s), (d, g, s), (kind, k, vt, lam)))

    def build(self):
        """Index the elements by node and compute the fanout of every node."""
        self.unknown = [i for i in range(self.n) if i not in self.fixed]
        self.at = [[] for _ in range(self.n)]
        self.fanout = [set() for _ in range(self.n)]
        for e in self.elements:
            carry, ctrl = e[1], e[2]
            for i in set(carry):
                self.at[i].append(e)
            for i in set(carry) | set(ctrl):
                for j in carry:
                    if j not in self.fixed:
                        self.fanout[i].add(j)
        return self

    def apply_fixed(self, v, t):
        for i, w in self.fixed.items():
            v[i] = w(t)


def node_row(ckt, i, v, vn, h):
    """Residual F_i of the backward Euler equation of node i and its partials."""
    f, dv = 0.0, {}

    def add(j, x):
        dv[j] = dv.get(j, 0.0) + x

    for kind, carry, ctrl, p in ckt.at[i]:
        if kind in "CGV":
            a, b = carry
            sign = 1 if a == i else -1
            if kind == "C":
                f += sign * p * ((v[a] - vn[a]) - (v[b] - vn[b])) / h
                add(a, sign * p / h)
                add(b, -sign * p / h)
            elif kind == "G":
                f += sign * p * (v[a] - v[b])
                add(a, sign * p)
                add(b, -sign * p)
            else:
                c, d = ctrl
                f += sign * p * (v[c] - v[d])
                add(c, sign * p)
                add(d, -sign * p)
        else:
            d, g, s = ctrl
            ids, gd, gg, gs = mos_current(p[0], p[1], p[2], p[3], v[d], v[g], v[s])
            sign = (d == i) - (s == i)
            f += sign * ids
            add(d, sign * gd)
            add(g, sign * gg)
            add(s, sign * gs)
    return f, dv


def relax_time_point(ckt, v, vn, h, active, tau, max_evals):
    """Event-driven Gauss-Seidel-Newton at one time point. Changes v in place."""
    queue = deque(i for i in ckt.unknown if i in active)  # @line L4
    inq = set(queue)
    evals = 0
    while queue:  # @line L5
        i = queue.popleft()  # @line L6
        inq.discard(i)
        f, dv = node_row(ckt, i, v, vn, h)  # @line L7
        delta = -f / dv[i]  # @line L8
        v[i] += delta
        evals += 1
        if evals > max_evals:
            raise NonConvergence(f"more than {max_evals} node evaluations")
        if abs(delta) > tau:  # @line L9
            for j in ckt.fanout[i]:
                if j not in inq:
                    queue.append(j)
                    inq.add(j)
    return evals


def ita(ckt, v0, h, steps, tau, max_evals=None):
    """Iterated timing analysis with a fixed step h.

    Returns the list of (t, v) and the total number of node evaluations.
    """
    ckt.build()
    if max_evals is None:
        max_evals = 200 * max(1, len(ckt.unknown))
    v = list(v0)  # @line L1
    ckt.apply_fixed(v, 0.0)
    active = set(ckt.unknown)
    out, total = [(0.0, list(v))], 0
    for k in range(1, steps + 1):  # @line L2
        t = k * h
        vn = list(v)
        ckt.apply_fixed(v, t)  # @line L3
        for i in ckt.fixed:
            if v[i] != vn[i]:
                active |= ckt.fanout[i]
        total += relax_time_point(ckt, v, vn, h, active, tau, max_evals)
        moved = [i for i in ckt.unknown if abs(v[i] - vn[i]) > tau]  # @line L10
        active = set().union(*(ckt.fanout[i] for i in moved)) if moved else set()
        out.append((t, list(v)))
    return out, total  # @line L11


def sweep(ckt, v, vn, h, order=None):
    """One Gauss-Seidel-Newton sweep over all unknown nodes; returns the largest step."""
    big = 0.0
    for i in order or ckt.unknown:
        f, dv = node_row(ckt, i, v, vn, h)
        delta = -f / dv[i]
        v[i] += delta
        big = max(big, abs(delta))
    return big


def one_sweep_simulation(ckt, v0, h, steps):
    """The MOTIS scheme: one sweep per time point, with no iteration."""
    ckt.build()
    v = list(v0)
    ckt.apply_fixed(v, 0.0)
    out, evals = [(0.0, list(v))], 0
    for k in range(1, steps + 1):
        vn = list(v)
        ckt.apply_fixed(v, k * h)
        sweep(ckt, v, vn, h)
        evals += len(ckt.unknown)
        out.append((k * h, list(v)))
    return out, evals


def backward_euler_newton(ckt, v0, h, steps, tol=1e-12, max_iter=50):
    """Reference: backward Euler with full Newton on all unknown nodes at once."""
    ckt.build()
    idx = {i: r for r, i in enumerate(ckt.unknown)}
    v = list(v0)
    ckt.apply_fixed(v, 0.0)
    out = [(0.0, list(v))]
    for k in range(1, steps + 1):
        vn = list(v)
        ckt.apply_fixed(v, k * h)
        for _ in range(max_iter):
            m = len(idx)
            jac = [[0.0] * m for _ in range(m)]
            res = [0.0] * m
            for i, r in idx.items():
                f, dv = node_row(ckt, i, v, vn, h)
                res[r] = -f
                for j, x in dv.items():
                    if j in idx:
                        jac[r][idx[j]] += x
            dx = sim3dense.solve(jac, res)
            for i, r in idx.items():
                v[i] += dx[r]
            if max(abs(x) for x in dx) <= tol:
                break
        else:
            raise NonConvergence("full Newton did not converge")
        out.append((k * h, list(v)))
    return out


def jacobian_rho(ckt, v, vn, h):
    """max_i sum_{j != i} |J_ij| / J_ii over unknown nodes: the bound of the proof."""
    ckt.build()
    rho = 0.0
    for i in ckt.unknown:
        _, dv = node_row(ckt, i, v, vn, h)
        off = sum(abs(x) for j, x in dv.items() if j != i and j not in ckt.fixed)
        rho = max(rho, off / dv[i] if dv[i] > 0 else float("inf"))
    return rho
