# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/source-stepping/. The authors are listed in prov/QF22WC.jsonl.
"""Source stepping for the DC operating point of a circuit with diodes.

A netlist is a list of elements. Node 0 is ground.

- ("R", p, q, r): a resistor;
- ("V", p, q, s): a voltage source with e_p - e_q = s;
- ("I", p, q, s): a current source; the current s flows from p through the source to q;
- ("D", p, q, i_s, v_t): a diode with anode p and cathode q, whose current from
  p to q is i_s (exp((e_p - e_q) / v_t) - 1).

The unknowns are those of modified nodal analysis: the voltages e_1..e_n and
one current per voltage source, in netlist order. Every independent source is
multiplied by the parameter lam, so lam = 0 gives the circuit with all sources
off and lam = 1 gives the circuit itself.
"""

import math

from densela import SingularMatrixError, lu_factor, lu_solve


class NewtonFailure(ArithmeticError):
    """Newton's method overflowed, met a singular Jacobian or did not converge."""


def _branch_rows(netlist, n):
    rows, size = {}, n
    for k, el in enumerate(netlist):
        if el[0] == "V":
            rows[k] = size
            size += 1
    return rows, size


def _diode(i_s, v_t, v):
    # math.exp raises OverflowError above about 709.78; that is the failure of plain Newton.
    x = math.exp(v / v_t)
    return i_s * (x - 1), i_s * x / v_t


def residual(netlist, n, x, lam):
    """F(x, lam): the KCL sum of the currents leaving each node, then e_p - e_q - lam s per voltage source."""
    rows, size = _branch_rows(netlist, n)
    f = [0 * x[0]] * size
    e = [0 * x[0]] + list(x[:n])

    def leave(p, q, i):
        if p > 0:
            f[p - 1] += i
        if q > 0:
            f[q - 1] -= i

    for k, el in enumerate(netlist):
        kind, p, q = el[0], el[1], el[2]
        if kind == "R":
            leave(p, q, (e[p] - e[q]) / el[3])
        elif kind == "I":
            leave(p, q, lam * el[3])
        elif kind == "D":
            leave(p, q, _diode(el[3], el[4], e[p] - e[q])[0])
        elif kind == "V":
            leave(p, q, x[rows[k]])
            f[rows[k]] = e[p] - e[q] - lam * el[3]
        else:
            raise ValueError(f"unknown element {kind!r}")
    return f


def jacobian(netlist, n, x):
    """The derivative of F with respect to x; it does not depend on lam."""
    rows, size = _branch_rows(netlist, n)
    a = [[0 * x[0]] * size for _ in range(size)]
    e = [0 * x[0]] + list(x[:n])

    def stamp(p, q, g):
        for r, c, s in ((p, p, 1), (q, q, 1), (p, q, -1), (q, p, -1)):
            if r > 0 and c > 0:
                a[r - 1][c - 1] += s * g

    for k, el in enumerate(netlist):
        kind, p, q = el[0], el[1], el[2]
        if kind == "R":
            stamp(p, q, 1 / el[3])
        elif kind == "D":
            stamp(p, q, _diode(el[3], el[4], e[p] - e[q])[1])
        elif kind == "V":
            m = rows[k]
            for node, s in ((p, 1), (q, -1)):
                if node > 0:
                    a[node - 1][m] += s
                    a[m][node - 1] += s
    return a


def newton(netlist, n, x0, lam=1, max_iter=50, reltol=1e-9, abstol=1e-12):
    """Plain Newton on F(x, lam) = 0 from x0. Return (x, iterations) or raise NewtonFailure."""
    x = list(x0)
    for it in range(1, max_iter + 1):
        try:
            f = residual(netlist, n, x, lam)
            a = jacobian(netlist, n, x)
            dx = lu_solve(lu_factor(a), [-v for v in f])
        except (OverflowError, SingularMatrixError) as exc:
            raise NewtonFailure(f"iteration {it}: {exc}") from exc
        x_new = [u + d for u, d in zip(x, dx)]
        if not all(math.isfinite(v) for v in x_new):
            raise NewtonFailure(f"iteration {it}: the iterate is not finite")
        if all(abs(d) <= reltol * abs(u) + abstol for d, u in zip(dx, x_new)):
            return x_new, it
        x = x_new
    raise NewtonFailure(f"no convergence in {max_iter} iterations")


def source_stepping(netlist, n, first_step=0.1, min_step=1e-6, max_iter=20, grow=2):
    """Trace the solution from lam = 0 to lam = 1, with Newton as the corrector.

    Return (x, stats). stats["path"] lists the accepted pairs (lam, x),
    stats["failures"] counts the rejected steps and stats["iterations"] the
    Newton iterations of all corrector runs.
    """
    _, size = _branch_rows(netlist, n)
    zero = 0 * first_step
    lam = zero  # @line L1
    x = [zero] * size  # with every source off, x = 0 solves F, since every element carries no current at zero bias
    step = first_step  # @line L2
    stats = {"path": [(lam, list(x))], "failures": 0, "iterations": 0}
    while lam < 1:  # @line L3
        target = min(lam + step, 1 + zero)  # @line L4
        try:
            x_new, its = newton(netlist, n, x, target, max_iter)  # @line L5
        except NewtonFailure:
            stats["failures"] += 1
            step = step / 2  # @line L7
            if step < min_step:
                raise NewtonFailure(f"the step fell below {min_step} at lam = {lam}") from None
            continue
        stats["iterations"] += its
        lam, x = target, x_new  # @line L6
        step = step * grow
        stats["path"].append((lam, list(x)))
    return x, stats  # @line L8
