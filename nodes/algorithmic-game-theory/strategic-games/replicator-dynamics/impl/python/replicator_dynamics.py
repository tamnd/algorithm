# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/replicator-dynamics/. The authors are listed in prov/DA7ATV.jsonl.

"""Replicator dynamics x_i' = x_i ((A x)_i - x^T A x), solved by RK4 with a fixed step.

A is a square payoff matrix given as a list of rows, and x is a list of shares
that sum to 1. The computation is in float; the tests state their tolerances.
"""


def fitness(A, x):
    """The payoff vector A x."""
    return [sum(a * xj for a, xj in zip(row, x)) for row in A]


def mean_fitness(A, x):
    """The mean payoff x^T A x of the population."""
    return sum(xi * fi for xi, fi in zip(x, fitness(A, x)))


def replicator_field(A, x):
    """The right-hand side F(x) of the replicator equation.

    The mean is divided by sum(x), which is 1 on the simplex. Then the entries of
    F(x) sum to exactly 0 for every x, so rounding errors in sum(x) do not grow.
    """
    f = fitness(A, x)  # @line L8
    phi = sum(xi * fi for xi, fi in zip(x, f)) / sum(x)  # @line L9
    return [xi * (fi - phi) for xi, fi in zip(x, f)]  # @line L10


def _axpy(x, h, k):
    return [xi + h * ki for xi, ki in zip(x, k)]


def rk4_step(A, x, h):
    """One step of the classical Runge-Kutta method of order 4."""
    k1 = replicator_field(A, x)  # @line L2
    k2 = replicator_field(A, _axpy(x, h / 2, k1))  # @line L3
    k3 = replicator_field(A, _axpy(x, h / 2, k2))  # @line L4
    k4 = replicator_field(A, _axpy(x, h, k3))  # @line L5
    return [  # @line L6
        xi + h / 6 * (a + 2 * b + 2 * c + d)
        for xi, a, b, c, d in zip(x, k1, k2, k3, k4)
    ]


def replicator_rk4(A, x0, h, steps, record=False):
    """Run `steps` RK4 steps of size h from x0.

    Returns the final state, or the list of all states (x0 first) if record is true.
    """
    x = list(map(float, x0))
    path = [x] if record else None
    for _ in range(steps):  # @line L1
        x = rk4_step(A, x, h)
        if record:
            path.append(x)
    return path if record else x  # @line L7
