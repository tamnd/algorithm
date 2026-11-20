# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperdynamics/. The authors are listed in prov/W145MS.jsonl.
"""Hyperdynamics (Voter 1997) on overdamped Langevin dynamics.

The dynamics runs on the biased potential V + dV, where the bias dV >= 0
is zero near every dividing surface out of the current basin. Each step
of length h adds h exp(dV(x) / kT) to the hyper time instead of h. When
the system leaves the basin, the hyper time is an estimate of the escape
time of the unbiased dynamics, under the assumptions of transition state
theory (no correlated recrossings, and local equilibrium in the basin).

The dynamics here is dx = -grad(V + dV) dt + sqrt(2 kT) dW, with mobility
1, integrated by the Euler-Maruyama method with time step h. The boost,
hyper time over simulated time, is a measurement of one run.

A simple bias with a flat floor is given: dV = max(0, V_c - V) inside the
basin. It is zero where V >= V_c, which includes the barrier region if V_c
is below the barrier. Such a bias needs the basin to be known; biases for
real systems use local quantities such as the bond lengths.
"""

import math
from typing import Callable, Sequence

Vector = list[float]


def flat_bias(potential: Callable[[Sequence[float]], tuple[float, Vector]], v_c: float,
              in_basin: Callable[[Sequence[float]], bool]):
    """Return f(x) -> (dV, grad dV) for dV = max(0, v_c - V(x)) inside the basin, 0 outside."""
    def bias(x):
        v, g = potential(x)
        if in_basin(x) and v < v_c:
            return v_c - v, [-c for c in g]
        return 0.0, [0.0] * len(x)
    return bias


def hyperdynamics(x0: Sequence[float], potential, bias, kT: float, h: float,
                  escaped: Callable[[Sequence[float]], bool], rng, max_steps: int = 10**6):
    """Run biased overdamped Langevin dynamics until escaped(x) is True.

    potential(x) and bias(x) return (value, gradient). rng needs gauss(0, 1).
    Returns (x, hyper_time, steps, done): the final point, the boosted clock
    sum of h exp(dV / kT), the number of steps and whether the escape
    happened. The boost of the run is hyper_time / (steps * h).
    """
    x = list(x0)
    t_hyper = 0.0                                                       # @line L1
    s = math.sqrt(2.0 * kT * h)
    for step in range(1, max_steps + 1):                                # @line L2
        dv, gb = bias(x)                                                # @line L3
        t_hyper += h * math.exp(dv / kT)                                # @line L4
        g = potential(x)[1]
        x = [xi - h * (gi + bi) + s * rng.gauss(0.0, 1.0)               # @line L5
             for xi, gi, bi in zip(x, g, gb)]
        if escaped(x):                                                  # @line L6
            return x, t_hyper, step, True                               # @line L7
    return x, t_hyper, max_steps, False
