# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heterogeneous-multiscale-method/. The authors are listed in prov/HVHGX1.jsonl.
"""The heterogeneous multiscale method (E and Engquist 2003) for a 1D elliptic problem.

Model problem: -(a_eps(x) u')' = f on (0, 1), u(0) = u(1) = 0, where
a_eps(x) varies on a small scale eps. The macroscale solver is the P1
finite element method on M elements. Its coefficient on element K is not
known; it is estimated at the midpoint x_K by a micro problem on the cell
I = [x_K - delta / 2, x_K + delta / 2]:

    -(a_eps v')' = 0 in I,  v(x) = x - x_K at both ends of I,

solved by P1 elements on `cells` micro cells with the midpoint value of
a_eps on each. The estimate is the mean flux (1 / delta) * integral of
a_eps v' over I, the response to a unit macro gradient.

In 1D the flux of the micro problem is constant, and the estimate is the
harmonic mean of a_eps over I. If I holds a whole number of periods of a
periodic a_eps, this is the homogenized coefficient a*.

Cost: M micro problems of `cells` unknowns each, Theta(M cells), and one
tridiagonal macro solve, Theta(M). Nothing depends on eps.
"""

from scisparse import thomas


def micro_coefficient(a_eps, x_k, delta, cells):
    """Estimate the macro coefficient at x_k from the micro problem on a cell of size delta."""
    eta = delta / cells
    left = x_k - delta / 2
    a = [a_eps(left + (j + 0.5) * eta) for j in range(cells)]
    # Unknowns v_1 .. v_(cells-1); v_0 = -delta / 2 and v_cells = delta / 2.
    v0, vn = -delta / 2, delta / 2                                             # @line L2
    if cells == 1:
        v = [v0, vn]
    else:
        sub = [0.0] + [-a[j - 1] / eta for j in range(2, cells)]               # @line L2
        diag = [(a[j - 1] + a[j]) / eta for j in range(1, cells)]              # @line L2
        sup = [-a[j] / eta for j in range(1, cells - 1)] + [0.0]               # @line L2
        rhs = [0.0] * (cells - 1)                                              # @line L2
        rhs[0] += a[0] / eta * v0                                              # @line L2
        rhs[-1] += a[cells - 1] / eta * vn                                     # @line L2
        v = [v0] + thomas(sub, diag, sup, rhs) + [vn]                          # @line L2
    flux = sum(a[j] * (v[j + 1] - v[j]) for j in range(cells))                # @line L3
    return flux / delta                                                        # @line L3


def hmm_1d(a_eps, f, M, delta, cells):
    """Macro P1 solve with coefficients from micro problems at the element midpoints.

    a_eps, f: functions of x. Returns (U, a_K): the M + 1 nodal values and
    the M estimated coefficients.
    """
    H = 1.0 / M
    a_K = []
    diag = [0.0] * (M + 1)
    off = [0.0] * M
    F = [0.0] * (M + 1)
    for e in range(M):                                                         # @line L1
        xl, xr = e * H, (e + 1) * H
        xm = (xl + xr) / 2
        ak = micro_coefficient(a_eps, xm, delta, cells)                        # @line L2
        a_K.append(ak)
        k = ak / H                                                             # @line L4
        diag[e] += k                                                           # @line L4
        diag[e + 1] += k                                                       # @line L4
        off[e] -= k                                                            # @line L4
        # Simpson's rule for the load, exact for f of degree 2
        F[e] += H * (f(xl) + 2 * f(xm)) / 6                                    # @line L4
        F[e + 1] += H * (2 * f(xm) + f(xr)) / 6                                # @line L4
    m = M - 1
    inner = thomas([0.0] + off[1:m], diag[1:M], off[1:m] + [0.0], F[1:M]) if m > 0 else []  # @line L5
    return [0.0] + inner + [0.0], a_K                                          # @line L6
