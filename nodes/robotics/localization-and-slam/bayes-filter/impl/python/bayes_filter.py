# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayes-filter/. The authors are listed in prov/V7B1QT.jsonl.

"""The Bayes filter on a finite state space (Thrun, Burgard and Fox 2005, Table 2.1).

The states are 0, 1, ..., n - 1. A belief is a list of n probabilities.
The caller gives two functions:
  motion(x, u, x_prev)   returns p(x_t = x | u_t = u, x_(t-1) = x_prev),
  measurement(z, x)      returns p(z_t = z | x_t = x).
The arithmetic is generic: with fractions.Fraction inputs the result is exact.
"""


def bayes_filter(bel, u, z, motion, measurement):
    """Return bel(x_t) from bel(x_(t-1)), the control u and the measurement z.

    If u is None the prediction is skipped (the state does not move).
    If z is None the correction is skipped (no measurement at time t).
    """
    n = len(bel)
    if u is None:
        bel_bar = list(bel)
    else:
        bel_bar = []
        for x in range(n):  # @line L1
            bel_bar.append(sum(motion(x, u, xp) * bel[xp] for xp in range(n)))  # @line L2
    if z is None:
        return bel_bar
    unnorm = [measurement(z, x) * bel_bar[x] for x in range(n)]  # @line L3
    total = sum(unnorm)
    if total == 0:
        raise ValueError("the measurement has probability zero under the predicted belief")
    eta = 1 / total  # @line L4
    new_bel = [eta * b for b in unnorm]  # @line L5
    return new_bel  # @line L6


def run_bayes_filter(bel0, controls, measurements, motion, measurement):
    """Apply bayes_filter for t = 1..T and return [bel_1, ..., bel_T]."""
    if len(controls) != len(measurements):
        raise ValueError("one control and one measurement per step")
    out, bel = [], list(bel0)
    for u, z in zip(controls, measurements):
        bel = bayes_filter(bel, u, z, motion, measurement)
        out.append(bel)
    return out
