# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-interpolation/. The authors are listed in prov/AEGV52.jsonl.

"""Newton interpolation by divided differences, with Hermite data on repeated nodes.

The functions work with float, Fraction or any field type that supports
+, -, * and /. With Fraction inputs every result is exact.
"""

from math import factorial
from typing import Mapping, Sequence


def newton_coefficients(z: Sequence, y: Sequence, derivs: Mapping | None = None) -> list:
    """Return c with c[k] = f[z_0, ..., z_k], the Newton coefficients.

    z[0..n] are the nodes; equal nodes must be adjacent. y[i] = f(z[i]).
    For a node v that occurs m > 1 times, derivs[v] is a sequence whose
    entry r is f^(r)(v) for 1 <= r < m (entry 0 is not used).
    Cost: 3n(n+1)/2 arithmetic operations, Theta(n) extra space.
    Raises ValueError if a repeated node has no derivative data or if
    equal nodes are not adjacent.
    """
    n = len(z) - 1
    if len(y) != n + 1:
        raise ValueError("z and y must have the same length")
    for i in range(n + 1):
        for j in range(i + 2, n + 1):
            if z[i] == z[j] and z[i + 1] != z[i]:
                raise ValueError("equal nodes must be adjacent")
    c = [y[i] for i in range(n + 1)]  # @line L1
    for k in range(1, n + 1):  # @line L2
        kfact = factorial(k)
        for i in range(n, k - 1, -1):  # @line L3
            if z[i] == z[i - k]:  # @line L4
                if derivs is None or z[i] not in derivs or len(derivs[z[i]]) <= k:
                    raise ValueError("a repeated node needs derivative data")
                c[i] = derivs[z[i]][k] / kfact
            else:
                c[i] = (c[i] - c[i - 1]) / (z[i] - z[i - k])  # @line L5
    return c  # @line L6


def newton_evaluate(z: Sequence, c: Sequence, t):
    """Return sum_k c[k] (t - z[0]) ... (t - z[k-1]) by nested multiplication.

    Cost: 3n arithmetic operations for n + 1 coefficients.
    """
    n = len(c) - 1
    p = c[n]  # @line L7
    for k in range(n - 1, -1, -1):  # @line L8
        p = p * (t - z[k]) + c[k]  # @line L9
    return p  # @line L10


def newton_append(z: Sequence, c: Sequence, last: Sequence, x_new, y_new) -> tuple[list, list, list]:
    """Add a node x_new, distinct from all of z, with value y_new.

    last[k] = f[z_{n-k}, ..., z_n] is the bottom diagonal of the table
    (empty lists for the first node). Returns new (z, c, last); the old
    coefficients are kept. Cost: 3(n + 1) arithmetic operations.
    """
    m = len(z)
    new_last = [y_new]
    for k in range(1, m + 1):
        new_last.append((new_last[k - 1] - last[k - 1]) / (x_new - z[m - k]))
    return list(z) + [x_new], list(c) + [new_last[-1]], new_last
