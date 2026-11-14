# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjoint-sensitivity-analysis/. The authors are listed in prov/XP8WTV.jsonl.
"""Adjoint sensitivity analysis of a linear resistive circuit at DC.

Nodes are the integers 0 to n, and node 0 is ground. A netlist is a list of
tuples, one for each element, as on the modified nodal analysis page:

- ("R", p, q, r): a resistor of resistance r between p and q;
- ("G", p, q, g): a conductance g between p and q;
- ("I", p, q, s): a current source; the current s flows from p through the
  source to q;
- ("V", p, q, s): a voltage source with e_p - e_q = s, whose current from p
  through the source to q is an extra unknown;
- ("VCCS", p, q, c, d, g): the current g (e_c - e_d) flows from p through the
  element to q.

The parameter of each element is its last value (r, g, s or g). An output is
a linear function phi = c . x of the MNA unknowns x = (e_1..e_n, j_1..j_m).
Values are Fraction (exact) or float.
"""

from densela import SingularMatrixError, lu_factor, lu_solve, lu_solve_transpose

__all__ = ["SingularMatrixError", "stamp", "node_output", "source_current_output", "sensitivities"]


def _add(a, i, j, v):
    if i > 0 and j > 0:
        a[i - 1][j - 1] += v


def stamp(netlist, n):
    """Return (M, z, rows): the MNA system M x = z and the row of each voltage source."""
    rows, size = {}, n
    for k, el in enumerate(netlist):
        if el[0] == "V":
            rows[k] = size
            size += 1
    a = [[0] * size for _ in range(size)]
    z = [0] * size
    for k, el in enumerate(netlist):
        kind = el[0]
        if kind in ("R", "G"):
            _, p, q, value = el
            g = 1 / value if kind == "R" else value
            for r, c, s in ((p, p, 1), (q, q, 1), (p, q, -1), (q, p, -1)):
                _add(a, r, c, s * g)
        elif kind == "I":
            _, p, q, s = el
            if p > 0:
                z[p - 1] -= s
            if q > 0:
                z[q - 1] += s
        elif kind == "V":
            _, p, q, s = el
            m = rows[k]
            for node, sign in ((p, 1), (q, -1)):
                if node > 0:
                    a[node - 1][m] += sign
                    a[m][node - 1] += sign
            z[m] += s
        elif kind == "VCCS":
            _, p, q, c, d, g = el
            for r, col, s in ((p, c, 1), (p, d, -1), (q, c, -1), (q, d, 1)):
                _add(a, r, col, s * g)
        else:
            raise ValueError(f"unknown element {kind!r}")
    return a, z, rows


def node_output(netlist, n, node):
    """The vector c with c . x = e_node."""
    _, _, rows = stamp(netlist, n)
    c = [0] * (n + len(rows))
    c[node - 1] = 1
    return c


def source_current_output(netlist, n, k):
    """The vector c with c . x = the current of the voltage source netlist[k]."""
    _, _, rows = stamp(netlist, n)
    c = [0] * (n + len(rows))
    c[rows[k]] = 1
    return c


def _diff(vec, p, q):
    # vec_p - vec_q, with the ground entry 0.
    return (vec[p - 1] if p > 0 else 0) - (vec[q - 1] if q > 0 else 0)


def sensitivities(netlist, n, outputs, stats=None):
    """Return [(phi, grad)] for each output vector c in outputs.

    grad[k] is d phi / d (parameter of netlist[k]). The work is one LU
    factorization of M, one solve for x, and one transposed solve for the
    adjoint vector of each output, whatever the number of parameters.
    Raise SingularMatrixError when M is singular. If stats is a dict, it
    receives the counts of these operations.
    """
    a, z, rows = stamp(netlist, n)  # @line L1
    factors = lu_factor(a)  # @line L2
    x = lu_solve(factors, z)  # @line L3
    if stats is not None:
        stats.update(factorizations=1, solves=1, transposed_solves=0)
    result = []
    for c in outputs:
        lam = lu_solve_transpose(factors, c)  # @line L4
        if stats is not None:
            stats["transposed_solves"] += 1
        phi = sum(ci * xi for ci, xi in zip(c, x))  # @line L5
        grad = []
        for k, el in enumerate(netlist):  # @line L6
            kind, p, q = el[0], el[1], el[2]
            # @line L7: grad = lam . (dz/dp - (dM/dp) x), which touches at most four entries
            if kind == "G":
                grad.append(-_diff(lam, p, q) * _diff(x, p, q))
            elif kind == "R":
                grad.append(_diff(lam, p, q) * _diff(x, p, q) / (el[3] * el[3]))
            elif kind == "I":
                grad.append(-_diff(lam, p, q))
            elif kind == "V":
                grad.append(lam[rows[k]])
            else:
                c_node, d_node = el[3], el[4]
                grad.append(-_diff(lam, p, q) * _diff(x, c_node, d_node))
        result.append((phi, grad))
    return result  # @line L8
