# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instrumental-variable-identification/. The authors are listed in prov/YQN1Q7.jsonl.

"""Instrumental variable identification of the parameters of an ARX structure.

The model is A(q) y(t) = B(q) u(t) + v(t) with
A = 1 + a_1 q^-1 + ... + a_na q^-na and B = b_1 q^-nk + ... +
b_nb q^-(nk+nb-1). The noise v(t) may be colored. With the regressor
phi(t) = (-y(t-1), ..., -y(t-na), u(t-nk), ..., u(t-nk-nb+1)) and an
instrument vector zeta(t) of the same length d = na + nb, the estimate is

    theta = (sum of zeta(t) phi(t)^T)^-1 (sum of zeta(t) y(t)).

Two instrument choices are given:
- "delayed": zeta(t) = (u(t-nk), u(t-nk-1), ..., u(t-nk-d+1)).
- "model": zeta(t) = (-x(t-1), ..., -x(t-na), u(t-nk), ..., u(t-nk-nb+1))
  with x = (B_aux / A_aux) u, the noise-free output of an auxiliary model
  (by default the least squares ARX fit). This is the two-step IV.

Precondition: na >= 0, nb >= 1, nk >= 0, len(y) == len(u) and the matrix
sum of zeta phi^T is nonsingular. With int or Fraction data and the
"delayed" instruments the result is exact (Fraction).

Cost: O(N d^2) to form the sums and O(d^3) to solve, in the real RAM.
"""

from typing import Callable, Optional, Sequence

from ctlmat import solve


def regressor(y: Sequence, u: Sequence, na: int, nb: int, nk: int, t: int) -> list:
    """Return phi(t) = (-y(t-1), ..., -y(t-na), u(t-nk), ..., u(t-nk-nb+1))."""
    return [-y[t - i] for i in range(1, na + 1)] + [u[t - nk - j] for j in range(nb)]


def iv_solve(y: Sequence, phi: Callable[[int], list], zeta: Callable[[int], list],
             t0: int) -> list:
    """Return theta from sum of zeta phi^T theta = sum of zeta y over t0 <= t < N."""
    d = len(phi(t0))
    r = [[0] * d for _ in range(d)]  # @line L2
    f = [0] * d
    for t in range(t0, len(y)):  # @line L3
        p = phi(t)  # @line L4
        z = zeta(t)
        if len(z) != d:
            raise ValueError("zeta and phi must have the same length")
        for i in range(d):
            zi = z[i]
            if zi == 0:
                continue
            row = r[i]
            for j in range(d):
                row[j] += zi * p[j]  # @line L5
            f[i] += zi * y[t]  # @line L6
    try:
        return solve(r, f)  # @line L8
    except ValueError:
        raise ValueError("sum of zeta phi^T is singular: the instruments are not correlated enough with phi") from None  # @line L7


def _simulate_arx(a: Sequence, b: Sequence, nk: int, u: Sequence) -> list:
    """Return x with A x = B u from rest."""
    x = []
    for t in range(len(u)):
        s = 0
        for j, bj in enumerate(b):
            if t - nk - j >= 0:
                s += bj * u[t - nk - j]
        for i, ai in enumerate(a, start=1):
            if t - i >= 0:
                s -= ai * x[t - i]
        x.append(s)
    return x


def iv_arx(y: Sequence, u: Sequence, na: int, nb: int, nk: int = 1,
           instruments: str = "delayed", aux: Optional[Sequence] = None) -> list:
    """IV estimate (a_1, ..., a_na, b_1, ..., b_nb).

    instruments is "delayed" or "model". For "model", aux is the auxiliary
    parameter vector (a, b); if it is None the least squares ARX estimate is
    used. Raises ValueError for bad orders, short data or a singular matrix.
    """
    if na < 0 or nb < 1 or nk < 0:
        raise ValueError("need na >= 0, nb >= 1 and nk >= 0")
    if len(y) != len(u):
        raise ValueError("y and u must have the same length")
    d = na + nb

    def phi(t):
        return regressor(y, u, na, nb, nk, t)

    if instruments == "delayed":
        t0 = max(na, nk + d - 1)  # @line L1

        def zeta(t):
            return [u[t - nk - j] for j in range(d)]
    elif instruments == "model":
        t0 = max(na, nk + nb - 1)
        if aux is None:
            aux = iv_solve(y, phi, phi, t0)
        x = _simulate_arx(list(aux[:na]), list(aux[na:]), nk, u)

        def zeta(t):
            return regressor(x, u, na, nb, nk, t)
    else:
        raise ValueError("instruments must be 'delayed' or 'model'")
    if len(y) - t0 < d:
        raise ValueError("too few samples for the model orders")
    return iv_solve(y, phi, zeta, t0)  # @line L9
