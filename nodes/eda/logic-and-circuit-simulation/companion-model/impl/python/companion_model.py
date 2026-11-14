# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/companion-model/. The authors are listed in prov/JH4KPG.jsonl.
"""Companion models of capacitors and inductors, and a fixed-step transient run.

Every companion model is a conductance G in parallel with a current source J,
so that the element current at the new time point is i = G v + J. Currents
are counted from the first node p of the element, through it, to its second
node q, and v = e_p - e_q.

The transient run uses nodal analysis, so a netlist holds only:

- ("R", p, q, r): a resistor;
- ("I", p, q, f): a current source whose current f(t), a function of time,
  flows from p through the source to q;
- ("C", p, q, c): a capacitor;
- ("L", p, q, l): an inductor.

Node 0 is ground. Values are Fraction (exact) or float.
"""

from densela import lu_factor, lu_solve

METHODS = ("be", "tr")


def capacitor_be(c, h, v_old):
    """Backward Euler: i_new = (c/h) (v_new - v_old)."""
    g = c / h
    return g, -g * v_old


def capacitor_tr(c, h, v_old, i_old):
    """Trapezoidal rule: i_new = (2c/h) (v_new - v_old) - i_old."""
    g = 2 * c / h
    return g, -g * v_old - i_old


def inductor_be(l, h, i_old):
    """Backward Euler: i_new = i_old + (h/l) v_new."""
    return h / l, i_old


def inductor_tr(l, h, v_old, i_old):
    """Trapezoidal rule: i_new = i_old + (h/(2l)) (v_new + v_old)."""
    g = h / (2 * l)
    return g, i_old + g * v_old


def _companion(el, method, h, state):
    kind, value = el[0], el[3]
    v_old, i_old = state
    if kind == "C":
        return capacitor_be(value, h, v_old) if method == "be" else capacitor_tr(value, h, v_old, i_old)
    return inductor_be(value, h, i_old) if method == "be" else inductor_tr(value, h, v_old, i_old)


def _stamp_g(a, p, q, g):
    for r, c, s in ((p, p, 1), (q, q, 1), (p, q, -1), (q, p, -1)):
        if r > 0 and c > 0:
            a[r - 1][c - 1] += s * g


def _stamp_j(b, p, q, j):
    # A current j from p to q leaves node p and enters node q.
    if p > 0:
        b[p - 1] -= j
    if q > 0:
        b[q - 1] += j


def transient(netlist, n, e0, h, steps, method="tr", inductor_currents=None, capacitor_currents=None):
    """Integrate from t = 0 with the fixed step h.

    e0 lists the node voltages at t = 0 (e0[0] = 0). inductor_currents and
    capacitor_currents map the netlist index of an element to its current at
    t = 0. Inductor currents default to 0. The trapezoidal rule needs the
    capacitor currents at t = 0; when they are not given, the first step uses
    backward Euler, as SPICE does.

    Return the list of node voltage vectors at t = 0, h, ..., steps h.
    """
    if method not in METHODS:
        raise ValueError(f"method must be one of {METHODS}")
    inductor_currents = dict(inductor_currents or {})
    state = {}
    for k, el in enumerate(netlist):  # @line L1
        if el[0] in ("C", "L"):
            v = e0[el[1]] - e0[el[2]]
            if el[0] == "L":
                state[k] = (v, inductor_currents.get(k, 0 * v))
            else:
                state[k] = (v, capacitor_currents[k] if capacitor_currents else None)
    first = method
    if method == "tr" and any(netlist[k][0] == "C" and s[1] is None for k, s in state.items()):
        first = "be"
    out = [list(e0)]
    factors = {}
    for step in range(1, steps + 1):  # @line L2
        m = first if step == 1 else method
        t = step * h
        comp = {k: _companion(netlist[k], m, h, state[k]) for k in state}  # @line L3
        if m not in factors:
            # The conductances depend only on h and the method, so one LU serves every step.
            a = [[0] * n for _ in range(n)]
            for k, el in enumerate(netlist):
                if el[0] == "R":
                    _stamp_g(a, el[1], el[2], 1 / el[3])
                elif k in comp:
                    _stamp_g(a, el[1], el[2], comp[k][0])
            factors[m] = lu_factor(a)  # @line L4
        b = [0] * n  # @line L5
        for k, el in enumerate(netlist):
            if el[0] == "I":
                _stamp_j(b, el[1], el[2], el[3](t))
            elif k in comp:
                _stamp_j(b, el[1], el[2], comp[k][1])
        x = lu_solve(factors[m], b)  # @line L6
        e = [0 * h] + x
        for k in state:  # @line L7
            el = netlist[k]
            v = e[el[1]] - e[el[2]]
            g, j = comp[k]
            state[k] = (v, g * v + j)
        out.append(e)
    return out  # @line L8
