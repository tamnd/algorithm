# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-boltzmann-inversion/. The authors are listed in prov/JKHDRS.jsonl.
"""Iterative Boltzmann inversion (Reith, Putz and Muller-Plathe 2003).

IBI fits a pair potential V(r) on a grid r_0, ..., r_(M-1) so that a
simulation with V gives a target radial distribution function g*(r).
It starts from the Boltzmann inversion V_0 = -kT ln g* and repeats

    V_(i+1)(r) = V_i(r) + alpha kT ln(g_i(r) / g*(r)),

where g_i is the g(r) of a simulation with V_i. A point where g* or g_i
is below g_min is not updated, because the logarithm is not defined or
is pure noise there; the start value there is -kT ln g_min.

The simulator is a function V -> g on the same grid. A real one is a
molecular dynamics or Monte Carlo run with a histogram of pair
distances. For tests, this file gives two closed forms:

- dilute_g: the low density limit g(r) = exp(-V(r) / kT).
- virial_g_1d: a one-dimensional fluid of density rho to first order in
  rho, g(r) = exp(-V(r)/kT) (1 + rho (f * f)(r)) with the Mayer function
  f = exp(-V/kT) - 1 and the convolution on the line. This is the
  density expansion of the cavity function y(r) = g(r) exp(V(r)/kT)
  truncated after the first term.
"""

import math
from typing import Callable, Sequence

Simulator = Callable[[Sequence[float]], list[float]]


def dilute_g(kt: float) -> Simulator:
    """The simulator g = exp(-V / kT) of a dilute gas."""
    def simulate(v):
        return [math.exp(-x / kt) for x in v]
    return simulate


def virial_g_1d(kt: float, rho: float, dr: float) -> Simulator:
    """The simulator g = exp(-V/kT) (1 + rho (f * f)) of a 1D fluid, first order in rho.

    The grid is r_k = k dr, k = 0..M-1, and V = 0 beyond the grid.
    """
    def simulate(v):
        m = len(v)
        f = [math.exp(-x / kt) - 1.0 for x in v]
        g = []
        for k in range(m):
            conv = 0.0
            for j in range(k - m + 1, m):  # both |j| and |k - j| stay below m
                conv += f[abs(j)] * f[abs(k - j)]
            g.append(math.exp(-v[k] / kt) * (1.0 + rho * dr * conv))
        return g
    return simulate


def iterative_boltzmann_inversion(g_target: Sequence[float], simulate: Simulator, kt: float,
                                  tol: float = 1e-10, max_iter: int = 100, alpha: float = 1.0,
                                  g_min: float = 1e-8) -> tuple[list[float], list[float]]:
    """Return the potential V on the grid and the list of max |g_i - g*| per iteration."""
    v = [-kt * math.log(max(g, g_min)) for g in g_target]                 # @line L1
    errors = []
    for _ in range(max_iter):                                             # @line L2
        g = simulate(v)                                                   # @line L3
        err = max(abs(a - b) for a, b in zip(g, g_target))
        errors.append(err)
        if err < tol:                                                     # @line L4
            return v, errors
        for k in range(len(v)):                                           # @line L5
            if g[k] > g_min and g_target[k] > g_min:
                v[k] += alpha * kt * math.log(g[k] / g_target[k])         # @line L6
    return v, errors                                                      # @line L7
