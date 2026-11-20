# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/free-energy-perturbation/. The authors are listed in prov/1TXW31.jsonl.
"""Free energy perturbation (Zwanzig 1954), also called exponential averaging.

For two states with potential energies U_0 and U_1 on the same configuration
space, at the inverse temperature beta,

    A_1 - A_0 = -(1 / beta) ln < exp(-beta (U_1 - U_0)) >_0,

where <.>_0 is the canonical average in state 0. The estimator replaces the
average by the mean over N samples of state 0. It is computed with a shift by
the smallest energy difference, so that no exponential overflows.

The staged form splits the path from state 0 to state 1 into windows
lambda_0 = 0 < lambda_1 < ... < lambda_K = 1 and adds the estimates of the
windows. The sampler of each state is an input (exact draws, Metropolis Monte
Carlo or molecular dynamics); it is not part of the method.

Cost: Theta(N) energy differences and exponentials per window.
"""

import math
from typing import Callable, Sequence


def fep(du: Sequence[float], beta: float) -> float:
    """Estimate A_1 - A_0 from the differences du_i = U_1(x_i) - U_0(x_i), x_i from state 0."""
    n = len(du)
    if n == 0:
        raise ValueError("need at least one sample")
    m = min(du)                                          # @line L2
    s = 0.0
    for d in du:
        s += math.exp(-beta * (d - m))                   # @line L3
    return m - math.log(s / n) / beta                    # @line L4


def fep_from_samples(xs, u0: Callable, u1: Callable, beta: float) -> float:
    """FEP from configurations xs of state 0 and the two energy functions."""
    du = [u1(x) - u0(x) for x in xs]                     # @line L1
    return fep(du, beta)


def fep_error(du: Sequence[float], beta: float) -> float:
    """Delta-method standard error of fep(du, beta) for independent samples.

    With w_i = exp(-beta du_i), the error is sd(w) / (beta sqrt(N) mean(w)).
    It is a large-N estimate; when the variance of w is infinite it is not valid.
    """
    n = len(du)
    if n < 2:
        raise ValueError("need at least two samples")
    m = min(du)
    w = [math.exp(-beta * (d - m)) for d in du]
    mean = sum(w) / n
    var = sum((x - mean) ** 2 for x in w) / (n - 1)
    return math.sqrt(var / n) / (beta * mean)


def staged_fep(lambdas: Sequence[float], sample: Callable, energy: Callable,
               beta: float, n: int, rng) -> tuple[float, float]:
    """Staged FEP over the windows lambdas[0] < ... < lambdas[K].

    sample(lam, n, rng) returns n configurations of the state lam, and
    energy(lam, x) is U_lam(x). Returns the estimate and its standard error
    (the errors of independent windows added in quadrature).
    """
    total, var = 0.0, 0.0                                # @line L5
    for k in range(len(lambdas) - 1):                    # @line L6
        xs = sample(lambdas[k], n, rng)                  # @line L7
        du = [energy(lambdas[k + 1], x) - energy(lambdas[k], x) for x in xs]
        total += fep(du, beta)                           # @line L8
        var += fep_error(du, beta) ** 2
    return total, math.sqrt(var)                         # @line L9
