# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lms-algorithm/. The authors are listed in prov/7A11YC.jsonl.

"""The least mean squares (LMS) adaptive filter of Widrow and Hoff.

For each sample, the filter forms the output y = w^T u from the tap vector
u = (x[n], x[n-1], ..., x[n-M+1]), the error e = d[n] - y, and the update
w <- w + mu * e * u. This is a stochastic gradient step on the mean-square
error E[e^2], with the factor 2 of the gradient absorbed into mu. The cost is
O(M) per sample. With int or Fraction inputs and a Fraction step, every value
is exact.
"""

from typing import Sequence


def lms_update(w: Sequence, u: Sequence, d, mu) -> tuple[list, object, object]:
    """One LMS step on regressor u and desired value d. Returns (w_new, y, e)."""
    y = sum((wk * uk for wk, uk in zip(w, u)), 0 * mu)  # @line L4
    e = d - y  # @line L5
    w_new = [wk + mu * e * uk for wk, uk in zip(w, u)]  # @line L6
    return w_new, y, e


def lms(x: Sequence, d: Sequence, m: int, mu, w0: Sequence | None = None) -> tuple[list, list, list]:
    """Run an M-tap LMS filter on input x and desired signal d.

    Samples before x[0] are taken as zero. Returns the final taps, the outputs
    y[n] and the errors e[n].
    """
    if m < 1 or len(x) != len(d):
        raise ValueError("need m >= 1 and len(x) == len(d)")
    w = list(w0) if w0 is not None else [0 * mu] * m  # @line L1
    ys, es = [], []
    for n in range(len(x)):  # @line L2
        u = [x[n - k] if n - k >= 0 else 0 * mu for k in range(m)]  # @line L3
        w, y, e = lms_update(w, u, d[n], mu)
        ys.append(y)
        es.append(e)
    return w, ys, es  # @line L7


def nlms_update(w: Sequence, u: Sequence, d, mu, eps) -> tuple[list, object, object]:
    """Normalized LMS step: the step is mu / (eps + u^T u). Stable for 0 < mu < 2."""
    y = sum((wk * uk for wk, uk in zip(w, u)), 0 * mu)
    e = d - y
    g = mu / (eps + sum(uk * uk for uk in u))
    return [wk + g * e * uk for wk, uk in zip(w, u)], y, e
