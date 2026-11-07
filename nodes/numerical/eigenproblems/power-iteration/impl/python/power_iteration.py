# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-iteration/. The authors are listed in prov/F8BB9Q.jsonl.

"""Power iteration for the dominant eigenpair of a square matrix.

power_iteration(a, x0, tol, maxit) multiplies a unit vector by A again and
again. It stops when the residual r = A q - rho q of the Rayleigh quotient
rho = q* A q satisfies ||r|| <= tol ||A q||, so that (rho, q) is an exact
eigenpair of A + E with ||E||_2 = ||r||_2 <= tol ||A||_2. The matrix is a
list of rows of floats or of Python complex numbers. Standard library only.
"""

import math
import random
from typing import NamedTuple


class PowerResult(NamedTuple):
    value: complex | float  # the Rayleigh quotient rho of the returned vector
    vector: list  # the unit vector q
    iterations: int  # the number of products A q
    converged: bool
    residual: float  # ||A q - rho q||_2
    history: list  # rho of each step, for rate measurements


def matvec(a, x):
    return [sum(aij * xj for aij, xj in zip(row, x)) for row in a]


def dot(x, y):
    """x* y, with the conjugate on the first argument."""
    return sum(xi.conjugate() * yi for xi, yi in zip(x, y))


def norm2(x):
    return math.sqrt(sum(abs(t) ** 2 for t in x))


def default_start(n, seed=0):
    rng = random.Random(seed)
    return [rng.uniform(-1.0, 1.0) for _ in range(n)]


def power_iteration(a, x0=None, tol=1e-12, maxit=10000):
    """Return a PowerResult for the eigenvalue of A of largest modulus.

    tol is a relative backward error: on success ||A q - rho q|| <= tol ||A q||.
    The method converges when one eigenvalue is strictly largest in modulus
    and x0 has a component along its eigenvector.
    """
    n = len(a)
    if n == 0:
        raise ValueError("empty matrix")
    x = list(x0) if x0 is not None else default_start(n)
    nx = norm2(x)
    if nx == 0.0:
        raise ValueError("the start vector is zero")
    q = [t / nx for t in x]  # @line L1
    history = []
    for k in range(1, maxit + 1):  # @line L2
        z = matvec(a, q)  # @line L3
        rho = dot(q, z)  # @line L4
        history.append(rho)
        r = [zi - rho * qi for zi, qi in zip(z, q)]  # @line L5
        nr, nz = norm2(r), norm2(z)
        if nr <= tol * nz:  # @line L6
            return PowerResult(rho, q, k, True, nr, history)
        if k == maxit:  # @line L7
            return PowerResult(rho, q, k, False, nr, history)
        q = [t / nz for t in z]  # @line L8
    raise ValueError("maxit must be at least 1")
