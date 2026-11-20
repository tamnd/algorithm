# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bennett-acceptance-ratio/. The authors are listed in prov/Y2JYEC.jsonl.
"""Bennett acceptance ratio (Bennett 1976).

Input: the reduced energy differences w_F = beta (U_1 - U_0) at n_0 samples of
state 0, and w_R = beta (U_0 - U_1) at n_1 samples of state 1. With the Fermi
function f(t) = 1 / (1 + e^t) and the shift C, the estimate solves

    sum_j f(w_R[j] + C) = sum_i f(w_F[i] - C),

a single equation with exactly one root, because the left side decreases and
the right side increases in C. Then beta (A_1 - A_0) = C - ln(n_1 / n_0).
The root is found by bisection on a bracket, so the method always converges.

Cost: Theta(n_0 + n_1) per evaluation of the equation, and about 60 bisection
steps for full double precision on the bracket.
"""

import math
from typing import Sequence


def fermi(t: float) -> float:
    """f(t) = 1 / (1 + e^t), computed without overflow."""
    if t > 0:
        e = math.exp(-t)
        return e / (1.0 + e)
    return 1.0 / (1.0 + math.exp(t))


def bar_residual(wf: Sequence[float], wr: Sequence[float], c: float) -> float:
    """sum_j f(w_R[j] + C) - sum_i f(w_F[i] - C); it decreases strictly in C."""
    return sum(fermi(w + c) for w in wr) - sum(fermi(w - c) for w in wf)


def bar(wf: Sequence[float], wr: Sequence[float], beta: float = 1.0,
        tol: float = 1e-12) -> float:
    """Estimate A_1 - A_0 from reduced forward and reverse energy differences."""
    n0, n1 = len(wf), len(wr)
    if n0 == 0 or n1 == 0:
        raise ValueError("BAR needs samples of both states")
    m = math.log(n1 / n0)                                # @line L1
    # The root lies between min(w_F) - 40 and max(-w_R) + 40 (see the proof).
    lo = min(min(wf), min(-w for w in wr)) - 40.0        # @line L2
    hi = max(max(wf), max(-w for w in wr)) + 40.0        # @line L2
    while hi - lo > tol * max(1.0, abs(lo), abs(hi)):    # @line L3
        mid = 0.5 * (lo + hi)                            # @line L4
        if bar_residual(wf, wr, mid) > 0:                # @line L5
            lo = mid                                     # @line L5
        else:
            hi = mid                                     # @line L6
    c = 0.5 * (lo + hi)
    return (c - m) / beta                                # @line L7


def bar_error(wf: Sequence[float], wr: Sequence[float], beta: float, da: float) -> float:
    """Large-sample standard error of the BAR estimate da, for independent samples.

    For any fixed C, beta dA = C + ln E_1[f(w_R + C)] - ln E_0[f(w_F - C)]; at the
    root C the error adds the relative variances of the two independent means.
    """
    n0, n1 = len(wf), len(wr)
    c = beta * da + math.log(n1 / n0)
    a = [fermi(w - c) for w in wf]
    b = [fermi(w + c) for w in wr]
    var = 0.0
    for v in (a, b):
        n = len(v)
        mean = sum(v) / n
        var += sum((x - mean) ** 2 for x in v) / (n - 1) / (n * mean * mean)
    return math.sqrt(var) / beta


def fep_forward(wf: Sequence[float], beta: float = 1.0) -> float:
    """Exponential averaging from state 0 only, for comparison."""
    m = min(wf)
    s = sum(math.exp(-(w - m)) for w in wf)
    return (m - math.log(s / len(wf))) / beta


def fep_reverse(wr: Sequence[float], beta: float = 1.0) -> float:
    """Exponential averaging from state 1 only, for comparison."""
    return -fep_forward(wr, beta)
