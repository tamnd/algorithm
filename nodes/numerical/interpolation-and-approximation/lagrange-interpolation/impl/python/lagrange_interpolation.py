# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagrange-interpolation/. The authors are listed in prov/NJK30H.jsonl.

"""Evaluate the interpolating polynomial in Lagrange form."""

from typing import Any, Sequence


def lagrange_basis(xs: Sequence[Any], i: int, t: Any) -> Any:
    """Return l_i(t) = prod over j != i of (t - x_j) / (x_i - x_j).

    Precondition: the nodes xs are distinct. Cost: 4n operations for n + 1 nodes.
    """
    ell = 1
    xi = xs[i]
    for j, xj in enumerate(xs):
        if j != i:
            ell = ell * (t - xj) / (xi - xj)
    return ell


def lagrange_interpolation(xs: Sequence[Any], ys: Sequence[Any], t: Any) -> Any:
    """Return p_n(t), where p_n has degree at most n and p_n(x_i) = y_i.

    The nodes may be in any order but must be distinct; a repeated node raises
    ValueError. Works with float, Fraction or any field type. Cost: (n + 1)(4n + 2)
    arithmetic operations for n + 1 nodes, that is about 4 n^2.
    """
    n1 = len(xs)
    if n1 == 0 or n1 != len(ys):
        raise ValueError("need the same positive number of nodes and values")
    if len(set(xs)) != n1:
        raise ValueError("the nodes must be distinct")
    p = 0 * ys[0]  # @line L1
    for i in range(n1):  # @line L2
        ell = 1  # @line L3
        xi = xs[i]
        for j in range(n1):  # @line L4
            if j != i:  # @line L5
                ell = ell * (t - xs[j]) / (xi - xs[j])
        p = p + ys[i] * ell  # @line L6
    return p  # @line L7
