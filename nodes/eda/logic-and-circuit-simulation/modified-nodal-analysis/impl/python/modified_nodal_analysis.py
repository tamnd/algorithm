# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-nodal-analysis/. The authors are listed in prov/CCJ8NY.jsonl.
"""Modified nodal analysis of a linear resistive circuit at DC.

Nodes are the integers 0 to n, and node 0 is ground. A netlist is a list of
tuples, one for each element:

- ("R", p, q, r): a resistor of resistance r between p and q.
- ("G", p, q, g): a conductance g between p and q.
- ("I", p, q, s): a current source; the current s flows from p through the
  source to q.
- ("V", p, q, s): a voltage source with e_p - e_q = s. Its current, from p
  through the source to q, is an extra unknown.
- ("VCCS", p, q, c, d, g): the current g (e_c - e_d) flows from p through the
  element to q.

Values are Fraction (exact) or float. The unknowns are e_1, ..., e_n and then
one current for each voltage source, in netlist order. Row k of the system,
for k <= n, is Kirchhoff's current law at node k: the currents that leave node
k through the elements sum to zero, with the known source currents moved to the
right-hand side.
"""

from densela import SingularMatrixError, lu_factor, lu_solve

__all__ = ["SingularMatrixError", "stamp_mna", "solve_mna"]


def _add(a, i, j, v):
    # Row or column 0 is ground: its equation and its voltage are dropped.
    if i > 0 and j > 0:
        a[i - 1][j - 1] += v


def stamp_mna(netlist, n):
    """Return (A, b, names) of the MNA system A x = b."""
    nv = sum(1 for el in netlist if el[0] == "V")  # @line L1
    size = n + nv
    a = [[0] * size for _ in range(size)]  # @line L2
    b = [0] * size
    names = [f"e{k}" for k in range(1, n + 1)]
    m = n  # @line L3: index of the next source-current unknown, 0-based
    for el in netlist:  # @line L4
        kind = el[0]
        nodes = el[1:-1]
        for node in nodes:
            if not 0 <= node <= n:
                raise ValueError(f"node {node} is out of range in {el}")
        if kind in ("R", "G"):  # @line L6: the stamps follow, one branch for each kind
            _, p, q, value = el
            g = 1 / value if kind == "R" else value
            _add(a, p, p, g)
            _add(a, q, q, g)
            _add(a, p, q, -g)
            _add(a, q, p, -g)
        elif kind == "I":
            _, p, q, s = el
            if p > 0:
                b[p - 1] -= s
            if q > 0:
                b[q - 1] += s
        elif kind == "V":
            _, p, q, s = el
            row = m  # @line L5
            names.append(f"j{len(names) - n}")
            if p > 0:
                a[p - 1][row] += 1
                a[row][p - 1] += 1
            if q > 0:
                a[q - 1][row] -= 1
                a[row][q - 1] -= 1
            b[row] += s
            m += 1
        elif kind == "VCCS":
            _, p, q, c, d, g = el
            _add(a, p, c, g)
            _add(a, p, d, -g)
            _add(a, q, c, -g)
            _add(a, q, d, g)
        else:
            raise ValueError(f"unknown element {kind!r}")
    return a, b, names


def solve_mna(netlist, n, tol=0):
    """Solve the circuit.

    Return (e, j): e[k] is the voltage of node k with e[0] = 0, and j[i] is the
    current of the i-th voltage source. Raise SingularMatrixError when the MNA
    matrix is singular, for example with a loop of voltage sources or a cut set
    of current sources.
    """
    a, b, _ = stamp_mna(netlist, n)
    if not a:
        return [0], []
    x = lu_solve(lu_factor(a, tol), b)  # @line L7
    return [0] + x[:n], x[n:]  # @line L8
