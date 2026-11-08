# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parareal-algorithm/. The authors are listed in prov/GD4NTE.jsonl.

"""The parareal algorithm for y' = f(t, y), y(t0) = y0.

[t0, T] is cut into N time slices [T_n, T_(n+1)].  G is a cheap coarse
propagator and F an accurate fine propagator; both map (T_n, T_(n+1), y) to
an approximation of the solution at T_(n+1) that starts from y at T_n.
The iteration is

    U_0^(k+1)     = y0
    U_(n+1)^(k+1) = G(U_n^(k+1)) + F(U_n^k) - G(U_n^k).

The N fine solves of one iteration are independent and could run in
parallel; here they run one after the other, and the result counts them.
After k iterations the values at T_0, ..., T_k equal the sequential fine
solution exactly.
"""

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, List

Propagator = Callable[[Any, Any, Any], Any]


@dataclass
class PararealResult:
    """Slice end values, iterations done, propagator calls, convergence flag."""

    times: List[Any]
    values: List[Any]
    iterations: int
    fine_calls: int
    coarse_calls: int
    converged: bool
    history: List[List[Any]] = field(default_factory=list)


def _add(u: Any, v: Any, s: Any = 1) -> Any:
    if isinstance(u, list):
        return [a + s * b for a, b in zip(u, v)]
    return u + s * v


def _dist(u: Any, v: Any) -> float:
    if isinstance(u, list):
        return float(max((abs(a - b) for a, b in zip(u, v)), default=0))
    return float(abs(u - v))


def rk_propagator(f: Callable[[Any, Any], Any], steps: int, method: str = "rk4") -> Propagator:
    """A propagator that takes `steps` equal steps of Euler's method or RK4."""
    if steps < 1:
        raise ValueError("steps must be at least 1")
    if method not in ("euler", "rk4"):
        raise ValueError("method must be 'euler' or 'rk4'")

    def prop(ta: Any, tb: Any, y: Any) -> Any:
        h = (tb - ta) / steps
        t = ta
        for i in range(steps):
            if method == "euler":
                y = _add(y, f(t, y), h)
            else:
                k1 = f(t, y)
                k2 = f(t + h / 2, _add(y, k1, h / 2))
                k3 = f(t + h / 2, _add(y, k2, h / 2))
                k4 = f(t + h, _add(y, k3, h))
                inc = _add(_add(k1, k4), _add(k2, k3), 2)
                y = _add(y, inc, h / 6)
            t = tb if i == steps - 1 else ta + (i + 1) * h
        return y

    return prop


def parareal(coarse: Propagator, fine: Propagator, t0: Any, y0: Any, t_end: Any,
             n_slices: int, max_iter: int = None, tol: float = 0.0,
             keep_history: bool = False) -> PararealResult:
    """Run parareal with n_slices equal slices.

    Stops after max_iter iterations (default n_slices, where the result
    equals the fine solution) or when two iterates differ by at most tol.
    """
    if n_slices < 1:
        raise ValueError("n_slices must be at least 1")
    if t_end < t0:
        raise ValueError("t_end must not be before t0")
    if max_iter is None:
        max_iter = n_slices
    N = n_slices
    T = [t0 + (t_end - t0) * n / N for n in range(N)] + [t_end]
    if t_end == t0:
        return PararealResult([t0], [y0], 0, 0, 0, True)
    U = [y0]                                             # @line L1
    G_old = []
    for n in range(N):
        g = coarse(T[n], T[n + 1], U[n])
        G_old.append(g)
        U.append(g)
    nf, ng = 0, N
    hist = [list(U)] if keep_history else []
    k = 0
    converged = False
    while k < max_iter:                                  # @line L2
        Fv = [fine(T[n], T[n + 1], U[n]) for n in range(N)]  # @line L3
        nf += N
        V = [y0]                                         # @line L4
        G_new = []
        for n in range(N):                               # @line L5
            g = coarse(T[n], T[n + 1], V[n])             # @line L6
            G_new.append(g)
            V.append(_add(_add(g, Fv[n]), G_old[n], -1))  # @line L7
        ng += N
        k += 1
        delta = max(_dist(V[n], U[n]) for n in range(N + 1))  # @line L8
        U, G_old = V, G_new
        if keep_history:
            hist.append(list(U))
        if delta <= tol:                                 # @line L9
            converged = True
            break
    if k >= N:
        converged = True       # equal to the fine solution after N iterations
    return PararealResult(T, U, k, nf, ng, converged, hist)  # @line L10


def sequential_fine(fine: Propagator, t0: Any, y0: Any, t_end: Any, n_slices: int) -> List[Any]:
    """The fine solution at the slice ends, computed sequentially."""
    N = n_slices
    T = [t0 + (t_end - t0) * n / N for n in range(N)] + [t_end]
    U = [y0]
    for n in range(N):
        U.append(fine(T[n], T[n + 1], U[n]))
    return U
